"""
PDF Generator
AuditPro Enterprise - Generate PDF reports
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
from config.settings import BASE_DIR


def generate_audit_report(audit_data: dict, filename: str = None) -> str:
    """
    Generate audit report PDF

    Args:
        audit_data: Dictionary containing audit information
        filename: Output filename (optional)

    Returns:
        str: Path to generated PDF file
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audit_report_{audit_data.get('audit_number', 'unknown')}_{timestamp}.pdf"

    output_path = BASE_DIR / "data" / "reports" / filename
    os.makedirs(output_path.parent, exist_ok=True)

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    # Container for elements
    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        spaceBefore=12
    )

    # Title
    elements.append(Paragraph("AUDIT REPORT", title_style))
    elements.append(Spacer(1, 12))

    # Audit Information
    elements.append(Paragraph("Audit Information", heading_style))

    audit_info = [
        ['Audit Number:', audit_data.get('audit_number', 'N/A')],
        ['Title:', audit_data.get('title', 'N/A')],
        ['Date:', str(audit_data.get('audit_date', 'N/A'))],
        ['Entity:', audit_data.get('entity_name', 'N/A')],
        ['Auditor:', audit_data.get('auditor_name', 'N/A')],
        ['Standard:', audit_data.get('standard', 'N/A')],
        ['Status:', audit_data.get('status', 'N/A')]
    ]

    info_table = Table(audit_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Executive Summary
    if audit_data.get('executive_summary'):
        elements.append(Paragraph("Executive Summary", heading_style))
        elements.append(Paragraph(audit_data['executive_summary'], styles['Normal']))
        elements.append(Spacer(1, 12))

    # Findings Summary
    elements.append(Paragraph("Findings Summary", heading_style))

    findings_data = [
        ['Finding Type', 'Count'],
        ['Non-Conformances', str(audit_data.get('nc_count', 0))],
        ['Opportunities for Improvement', str(audit_data.get('ofi_count', 0))],
        ['Overall Score', f"{audit_data.get('overall_score', 0):.1f}%"]
    ]

    findings_table = Table(findings_data, colWidths=[3*inch, 2*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(findings_table)
    elements.append(Spacer(1, 20))

    # Strengths
    if audit_data.get('strengths'):
        elements.append(Paragraph("Strengths", heading_style))
        elements.append(Paragraph(audit_data['strengths'], styles['Normal']))
        elements.append(Spacer(1, 12))

    # Areas for Improvement
    if audit_data.get('areas_for_improvement'):
        elements.append(Paragraph("Areas for Improvement", heading_style))
        elements.append(Paragraph(audit_data['areas_for_improvement'], styles['Normal']))
        elements.append(Spacer(1, 12))

    # Footer
    elements.append(Spacer(1, 30))
    footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | AuditPro Enterprise"
    elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER)))

    # Build PDF
    doc.build(elements)

    return str(output_path)


def generate_nc_report(nc_data: dict, filename: str = None) -> str:
    """
    Generate NC/OFI report PDF

    Args:
        nc_data: Dictionary containing NC/OFI information
        filename: Output filename (optional)

    Returns:
        str: Path to generated PDF file
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nc_report_{nc_data.get('nc_number', 'unknown')}_{timestamp}.pdf"

    output_path = BASE_DIR / "data" / "reports" / filename
    os.makedirs(output_path.parent, exist_ok=True)

    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph(f"<b>{nc_data.get('finding_type', 'NC')} Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    # NC Information
    nc_info = [
        ['NC Number:', nc_data.get('nc_number', 'N/A')],
        ['Type:', nc_data.get('finding_type', 'N/A')],
        ['Severity:', nc_data.get('severity', 'N/A')],
        ['Status:', nc_data.get('status', 'N/A')],
        ['Raised Date:', str(nc_data.get('raised_date', 'N/A'))],
        ['Target Closure:', str(nc_data.get('target_closure_date', 'N/A'))]
    ]

    table = Table(nc_info, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Description
    elements.append(Paragraph("<b>Description:</b>", styles['Heading3']))
    elements.append(Paragraph(nc_data.get('description', 'N/A'), styles['Normal']))
    elements.append(Spacer(1, 12))

    # Root Cause
    if nc_data.get('root_cause'):
        elements.append(Paragraph("<b>Root Cause:</b>", styles['Heading3']))
        elements.append(Paragraph(nc_data['root_cause'], styles['Normal']))
        elements.append(Spacer(1, 12))

    # Corrective Action
    if nc_data.get('corrective_action_plan'):
        elements.append(Paragraph("<b>Corrective Action Plan:</b>", styles['Heading3']))
        elements.append(Paragraph(nc_data['corrective_action_plan'], styles['Normal']))

    doc.build(elements)
    return str(output_path)


def generate_car_report(car_data: dict, filename: str = None) -> str:
    """
    Generate 8D CAR report PDF

    Args:
        car_data: Dictionary containing CAR information
        filename: Output filename (optional)

    Returns:
        str: Path to generated PDF file
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"car_report_{car_data.get('car_number', 'unknown')}_{timestamp}.pdf"

    output_path = BASE_DIR / "data" / "reports" / filename
    os.makedirs(output_path.parent, exist_ok=True)

    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title = Paragraph("<b>8D Corrective Action Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    # CAR Information
    elements.append(Paragraph(f"<b>CAR Number:</b> {car_data.get('car_number', 'N/A')}", styles['Heading2']))
    elements.append(Paragraph(f"<b>Title:</b> {car_data.get('title', 'N/A')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # 8D Steps
    d_steps = [
        ('D1', 'Team Formation', car_data.get('d1_team_description')),
        ('D2', 'Problem Description', car_data.get('d2_problem_description')),
        ('D3', 'Interim Containment', car_data.get('d3_containment_action')),
        ('D4', 'Root Cause Analysis', car_data.get('d4_root_cause')),
        ('D5', 'Corrective Actions', car_data.get('d5_corrective_actions')),
        ('D6', 'Implementation', car_data.get('d6_validation_results')),
        ('D7', 'Preventive Actions', car_data.get('d7_preventive_actions')),
        ('D8', 'Lessons Learned', car_data.get('d8_lessons_learned'))
    ]

    for step_num, step_name, step_content in d_steps:
        elements.append(Paragraph(f"<b>{step_num}: {step_name}</b>", styles['Heading3']))
        elements.append(Paragraph(step_content or 'Not completed', styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    return str(output_path)
