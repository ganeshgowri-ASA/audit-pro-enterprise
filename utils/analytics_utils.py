"""
Analytics and statistics utilities for NC/OFI tracking
"""
from sqlalchemy import func
from datetime import datetime, timedelta
import pandas as pd

def get_nc_ofi_statistics(db, nc_ofi_model):
    """
    Get overall NC/OFI statistics

    Args:
        db: Database session
        nc_ofi_model: NCOFI model class

    Returns:
        dict: Statistics dictionary
    """
    total_findings = db.query(nc_ofi_model).count()
    total_nc = db.query(nc_ofi_model).filter(nc_ofi_model.type == "NC").count()
    total_ofi = db.query(nc_ofi_model).filter(nc_ofi_model.type == "OFI").count()

    # Status breakdown
    status_counts = {}
    for status in ["Open", "InProgress", "Verified", "Closed"]:
        count = db.query(nc_ofi_model).filter(nc_ofi_model.status == status).count()
        status_counts[status] = count

    # Severity breakdown
    severity_counts = {}
    for severity in ["Critical", "Major", "Minor"]:
        count = db.query(nc_ofi_model).filter(nc_ofi_model.severity == severity).count()
        severity_counts[severity] = count

    # Overdue findings
    findings = db.query(nc_ofi_model).filter(
        nc_ofi_model.status.in_(["Open", "InProgress"])
    ).all()
    overdue_count = sum(1 for f in findings if f.is_overdue)

    # Average days to close
    closed_findings = db.query(nc_ofi_model).filter(
        nc_ofi_model.status == "Closed",
        nc_ofi_model.closure_date.isnot(None)
    ).all()

    if closed_findings:
        avg_days_to_close = sum(f.days_open for f in closed_findings) / len(closed_findings)
    else:
        avg_days_to_close = 0

    return {
        'total_findings': total_findings,
        'total_nc': total_nc,
        'total_ofi': total_ofi,
        'status_counts': status_counts,
        'severity_counts': severity_counts,
        'overdue_count': overdue_count,
        'avg_days_to_close': round(avg_days_to_close, 1)
    }


def get_aging_analysis(db, nc_ofi_model):
    """
    Get aging analysis for open findings

    Args:
        db: Database session
        nc_ofi_model: NCOFI model class

    Returns:
        dict: Aging analysis by age buckets
    """
    open_findings = db.query(nc_ofi_model).filter(
        nc_ofi_model.status.in_(["Open", "InProgress"])
    ).all()

    aging_buckets = {
        '0-7 days': 0,
        '8-14 days': 0,
        '15-30 days': 0,
        '31-60 days': 0,
        '60+ days': 0
    }

    for finding in open_findings:
        days_open = finding.days_open
        if days_open <= 7:
            aging_buckets['0-7 days'] += 1
        elif days_open <= 14:
            aging_buckets['8-14 days'] += 1
        elif days_open <= 30:
            aging_buckets['15-30 days'] += 1
        elif days_open <= 60:
            aging_buckets['31-60 days'] += 1
        else:
            aging_buckets['60+ days'] += 1

    return aging_buckets


def get_trend_data(db, nc_ofi_model, days=30):
    """
    Get trend data for open vs closed findings over time

    Args:
        db: Database session
        nc_ofi_model: NCOFI model class
        days: Number of days to look back

    Returns:
        DataFrame: Trend data
    """
    start_date = datetime.utcnow() - timedelta(days=days)

    all_findings = db.query(nc_ofi_model).filter(
        nc_ofi_model.created_at >= start_date
    ).all()

    # Group by date
    trend_data = {}
    current_date = start_date.date()
    end_date = datetime.utcnow().date()

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')

        # Count findings created up to this date
        created = sum(1 for f in all_findings if f.created_at.date() <= current_date)

        # Count findings closed by this date
        closed = sum(1 for f in all_findings
                    if f.closure_date and f.closure_date <= current_date)

        trend_data[date_str] = {
            'date': date_str,
            'created': created,
            'closed': closed,
            'open': created - closed
        }

        current_date += timedelta(days=1)

    return pd.DataFrame(list(trend_data.values()))


def get_assignee_workload(db, nc_ofi_model):
    """
    Get workload distribution by assignee

    Args:
        db: Database session
        nc_ofi_model: NCOFI model class

    Returns:
        list: Workload data by assignee
    """
    from models.user import User

    workload = db.query(
        User.full_name,
        func.count(nc_ofi_model.id).label('total'),
        func.sum(func.case((nc_ofi_model.status == 'Open', 1), else_=0)).label('open'),
        func.sum(func.case((nc_ofi_model.status == 'InProgress', 1), else_=0)).label('in_progress'),
        func.sum(func.case((nc_ofi_model.status == 'Closed', 1), else_=0)).label('closed')
    ).join(
        nc_ofi_model, User.id == nc_ofi_model.assignee_id
    ).group_by(
        User.full_name
    ).all()

    return [{
        'assignee': w[0],
        'total': w[1],
        'open': w[2],
        'in_progress': w[3],
        'closed': w[4]
    } for w in workload]
