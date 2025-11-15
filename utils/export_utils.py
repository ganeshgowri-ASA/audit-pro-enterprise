"""
Export utility functions for NC/OFI data
"""
import pandas as pd
from datetime import datetime
import io

def export_nc_ofi_to_excel(findings_data):
    """
    Export NC/OFI findings to Excel format

    Args:
        findings_data: List of dictionaries containing finding data

    Returns:
        BytesIO: Excel file in memory
    """
    # Create DataFrame
    df = pd.DataFrame(findings_data)

    # Reorder columns for better readability
    column_order = [
        'id', 'type', 'severity', 'status', 'category', 'clause_no',
        'description', 'assignee_name', 'due_date', 'closure_date',
        'days_open', 'is_overdue', 'audit_number', 'created_at'
    ]

    # Only include columns that exist in the data
    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns]

    # Rename columns for better presentation
    column_names = {
        'id': 'Finding ID',
        'type': 'Type',
        'severity': 'Severity',
        'status': 'Status',
        'category': 'Category',
        'clause_no': 'Clause',
        'description': 'Description',
        'assignee_name': 'Assignee',
        'due_date': 'Due Date',
        'closure_date': 'Closure Date',
        'days_open': 'Days Open',
        'is_overdue': 'Overdue',
        'audit_number': 'Audit Number',
        'created_at': 'Created At'
    }
    df = df.rename(columns=column_names)

    # Create Excel file in memory
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='NC_OFI_Findings', index=False)

        # Get the worksheet
        worksheet = writer.sheets['NC_OFI_Findings']

        # Auto-adjust column widths
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)

    output.seek(0)
    return output


def prepare_findings_for_export(findings, db):
    """
    Prepare NC/OFI findings data for export

    Args:
        findings: List of NCOFI model instances
        db: Database session

    Returns:
        List of dictionaries ready for export
    """
    findings_data = []

    for finding in findings:
        data = {
            'id': finding.id,
            'type': finding.type,
            'severity': finding.severity,
            'status': finding.status,
            'category': finding.category,
            'clause_no': finding.clause_no,
            'description': finding.description,
            'assignee_name': finding.assignee.full_name if finding.assignee else 'Unassigned',
            'due_date': finding.due_date.strftime('%Y-%m-%d') if finding.due_date else '',
            'closure_date': finding.closure_date.strftime('%Y-%m-%d') if finding.closure_date else '',
            'days_open': finding.days_open,
            'is_overdue': 'Yes' if finding.is_overdue else 'No',
            'audit_number': finding.audit.audit_number if finding.audit else '',
            'created_at': finding.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        findings_data.append(data)

    return findings_data
