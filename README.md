# AuditPro Enterprise

Enterprise Audit Management System - ISO 9001, IATF 16949, VDA 6.3 compliant. NC/OFI tracking, CAR/8D, Audit Planning & Reporting with Streamlit

## Overview

AuditPro Enterprise is a comprehensive web-based audit management system designed for organizations requiring robust quality management system (QMS) audit capabilities. Built with Python and Streamlit, it provides end-to-end audit lifecycle management from planning through corrective actions.

## Features

### Core Capabilities

- **User Authentication & Authorization**: Role-based access control with session management
- **Entity Management**: Hierarchical organization structure (Company → Plant → Department → Process)
- **Audit Planning**: Annual audit programs, scheduling, and resource allocation
- **Audit Execution**: Digital checklists, real-time scoring, evidence capture
- **NC/OFI Tracking**: Non-conformance and opportunity tracking with aging analysis
- **Corrective Actions**: 8D methodology implementation for problem-solving
- **Reports & Analytics**: PDF generation, Excel exports, KPI dashboards

### Supported Standards

- ISO 9001:2015 (Quality Management)
- IATF 16949 (Automotive Quality)
- VDA 6.3 (Process Audits)
- AS9100 (Aerospace)
- ISO 14001 (Environmental)
- ISO 45001 (Occupational Health & Safety)

## Project Structure

```
audit-pro-enterprise/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── seed_data.py             # Database seeding script
├── README.md                # This file
├── config/                  # Configuration files
│   ├── __init__.py
│   ├── database.py          # Database engine and session
│   └── settings.py          # Application settings
├── models/                  # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py              # Base model class
│   ├── user.py              # User model
│   ├── entity.py            # Entity hierarchy
│   ├── audit.py             # Audit models
│   ├── checklist.py         # Checklist models
│   ├── nc_ofi.py            # NC/OFI models
│   └── car.py               # Corrective action models
├── components/              # Reusable UI components
│   ├── __init__.py
│   ├── auth.py              # Authentication functions
│   ├── forms.py             # Form components
│   ├── charts.py            # Chart visualizations
│   └── tables.py            # Table displays
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── validators.py        # Input validation
│   ├── pdf_generator.py     # PDF report generation
│   └── excel_export.py      # Excel exports
├── data/                    # Data storage
│   ├── auditpro.db          # SQLite database (created on first run)
│   ├── uploads/             # File uploads
│   ├── reports/             # Generated PDF reports
│   └── exports/             # Excel exports
└── tests/                   # Unit tests
    ├── __init__.py
    ├── test_models.py
    └── test_database.py
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ganeshgowri-ASA/audit-pro-enterprise.git
   cd audit-pro-enterprise
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv

   # Activate on Windows
   venv\Scripts\activate

   # Activate on Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database and seed data**
   ```bash
   python seed_data.py
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   - Open browser and navigate to: `http://localhost:8501`
   - Login with default credentials:
     - Username: `admin`
     - Password: `admin123`

## Database Schema

### Core Tables

1. **users** - User accounts and authentication
2. **entities** - Organizational hierarchy
3. **audit_programs** - Annual audit plans
4. **audit_types** - Audit classifications
5. **audit_schedules** - Planned audits
6. **audits** - Audit execution records
7. **checklists** - Reusable audit checklists
8. **checklist_items** - Individual checklist questions
9. **audit_responses** - Audit findings per checklist item
10. **nc_ofi** - Non-conformances and opportunities
11. **corrective_actions** - 8D problem-solving records
12. **audit_reports** - Generated report metadata

### Key Relationships

- Users conduct Audits
- Audits belong to Entities
- Audits use Checklists
- Audits generate NC/OFI
- NC/OFI trigger Corrective Actions
- All models inherit from BaseModel (id, created_at, updated_at)

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///data/auditpro.db
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-password
```

### Application Settings

Edit `config/settings.py` to customize:
- Session expiry time
- File upload limits
- Allowed file extensions
- Chart colors
- Pagination settings

## Usage

### First-Time Setup

1. **Create Organizational Structure**
   - Navigate to Entity Management
   - Create Company → Plant → Department hierarchy

2. **Set Up Users**
   - Create user accounts
   - Assign roles (Admin, Auditor, Quality Manager, etc.)
   - Enable auditor flag for audit team members

3. **Define Audit Types**
   - Create audit type classifications
   - Map to standards (ISO 9001, IATF, etc.)

4. **Create Checklists**
   - Build reusable audit checklists
   - Add checklist items with scoring criteria

### Conducting an Audit

1. Plan audit (schedule, assign auditor, select entity)
2. Execute audit using digital checklist
3. Record findings, evidence, and scores
4. Raise NC/OFI as needed
5. Generate audit report
6. Follow up on corrective actions

### Managing NC/OFI

1. Create finding from audit or standalone
2. Classify severity (Critical, Major, Minor)
3. Assign to responsible person
4. Define containment and closure targets
5. Track status through lifecycle
6. Verify effectiveness

### 8D Problem Solving

1. Initiate CAR from NC/OFI
2. Form team (D1)
3. Describe problem (D2)
4. Implement containment (D3)
5. Analyze root cause (D4)
6. Define corrective actions (D5)
7. Implement and validate (D6)
8. Apply preventive measures (D7)
9. Close and recognize team (D8)

## Development Roadmap

### Phase 1: Base Structure (Current)
- ✅ Database models
- ✅ Authentication system
- ✅ Entity management
- ✅ Reusable components

### Phase 2: Audit Management
- 📋 Audit Planning module
- 📋 Audit Execution module
- 📋 Checklist management

### Phase 3: Findings & Actions
- 📋 NC/OFI Tracking module
- 📋 CAR/8D module
- 📋 Workflow automation

### Phase 4: Analytics & Reporting
- 📋 Dashboard analytics
- 📋 Trend analysis
- 📋 Custom reports
- 📋 Email notifications

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

Run specific test file:
```bash
python -m pytest tests/test_models.py
```

## Security Considerations

- Passwords are hashed using bcrypt
- Session state managed securely
- SQL injection prevented via ORM
- Input validation on all forms
- Role-based access control
- File upload restrictions

## Troubleshooting

### Database Issues
```bash
# Reset database
python -c "from config.database import reset_db; reset_db()"

# Re-seed data
python seed_data.py
```

### Application Won't Start
- Check Python version (3.9+)
- Verify all dependencies installed
- Check for port conflicts (8501)
- Review error logs

### Login Issues
- Use default credentials: admin/admin123
- Check database was seeded
- Verify user.is_active = True

## Support

For issues, questions, or feature requests:
- Create an issue on GitHub
- Documentation: Project Wiki

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- ORM powered by [SQLAlchemy](https://www.sqlalchemy.org/)
- Charts by [Plotly](https://plotly.com/)
- PDF generation via [ReportLab](https://www.reportlab.com/)

---

**Version:** 1.0.0
**Last Updated:** 2025-11-15
**Status:** Base Structure Completed
