# Audit Pro Enterprise

Enterprise Audit Management System - ISO 9001, IATF 16949, VDA 6.3 compliant.

A comprehensive audit management platform featuring NC/OFI tracking, CAR/8D, Audit Planning & Reporting built with Streamlit.

## 📋 Features

### ⚠️ NC/OFI Tracking System (Implemented)

Complete Non-Conformity (NC) and Opportunity for Improvement (OFI) tracking system with:

#### Core Features:
- ✅ **Finding Creation Form** - Document NCs and OFIs with complete details
- ✅ **Severity Classification** - Critical, Major, Minor severity levels
- ✅ **Assignment Management** - Assign findings to responsible persons
- ✅ **Due Date Tracking** - Set and monitor due dates
- ✅ **Status Workflow** - Open → InProgress → Verified → Closed
- ✅ **Aging Analysis Dashboard** - Monitor how long findings remain open
- ✅ **Overdue Alerts** - Red highlighting for overdue items
- ✅ **Advanced Filtering** - Filter by status, severity, assignee
- ✅ **Search Functionality** - Search by clause number or description
- ✅ **Excel Export** - Export findings data for reporting
- ✅ **Email Notifications** - Auto-email notifications to assignees
- ✅ **Trend Analysis** - Open vs Closed trends over time
- ✅ **Bulk Assignment** - Assign multiple findings at once
- ✅ **Status Change History** - Complete audit trail of status changes

#### Analytics:
- Real-time KPI dashboard
- Status breakdown charts
- Severity distribution analysis
- Aging analysis by time buckets
- Assignee workload distribution
- 30-day trend analysis

### 🔜 Coming Soon:
- Audit Planning Module
- CAR/8D Management
- Document Control
- User Management & RBAC

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ganeshgowri-ASA/audit-pro-enterprise.git
cd audit-pro-enterprise
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Load sample data:
```bash
python scripts/load_sample_data.py
```

5. Run the application:
```bash
streamlit run Home.py
```

6. Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
audit-pro-enterprise/
├── Home.py                      # Main Streamlit application
├── pages/
│   └── 04_⚠️_NC_OFI_Tracking.py # NC/OFI tracking page
├── models/
│   ├── user.py                  # User model
│   ├── audit.py                 # Audit model
│   ├── nc_ofi.py               # NC/OFI finding model
│   └── nc_ofi_history.py       # Status change history model
├── database/
│   └── __init__.py             # Database configuration
├── utils/
│   ├── email_utils.py          # Email notification utilities
│   ├── export_utils.py         # Excel export utilities
│   └── analytics_utils.py      # Analytics and statistics utilities
├── scripts/
│   └── load_sample_data.py     # Sample data loader
├── tests/
│   ├── conftest.py             # Pytest fixtures
│   └── test_nc_ofi.py          # NC/OFI tests
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🗄️ Database Schema

### NCOFI Model
- `id` - Primary key
- `audit_id` - Foreign key to Audit
- `type` - NC or OFI
- `category` - Major, Minor, Observation
- `clause_no` - ISO clause reference
- `description` - Detailed description
- `severity` - Critical, Major, Minor
- `status` - Open, InProgress, Verified, Closed
- `assignee_id` - Foreign key to User
- `due_date` - Target completion date
- `closure_date` - Actual closure date
- `evidence_path` - Path to evidence files
- `created_at` - Creation timestamp

### Computed Properties:
- `days_open` - Days since creation (or until closure)
- `is_overdue` - Boolean indicating overdue status
- `days_until_due` - Days until/past due date

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=models --cov=utils

# Run specific test
pytest tests/test_nc_ofi.py::TestNCCreation::test_nc_creation
```

### Test Coverage:
- ✅ `test_nc_creation()` - NC/OFI creation tests
- ✅ `test_status_workflow()` - Status workflow transitions
- ✅ `test_aging_calculation()` - Aging and overdue logic

## 📊 Sample Data

The system includes comprehensive sample data:
- **10 Users** - Across Quality, Production, Engineering, Operations
- **5 Audits** - Internal, External, Supplier audits
- **15 NCs** - 5 Critical, 5 Major, 5 Minor
- **10 OFIs** - Various improvement opportunities
- **Complete status history** - Realistic status transitions

Load sample data:
```bash
python scripts/load_sample_data.py
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Database
DATABASE_URL=sqlite:///./audit_pro.db

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=audit-system@example.com

# Application
APP_NAME=Audit Pro Enterprise
APP_ENV=development
```

### Application Settings (config.py)

Customize:
- NC/OFI types
- Severity levels
- Status workflow
- Overdue threshold

## 📧 Email Notifications

The system sends automatic email notifications for:
- New finding assignments
- Overdue finding alerts

Configure SMTP settings in `.env` to enable email functionality.

## 📈 Usage Guide

### Creating a Finding

1. Navigate to **NC/OFI Tracking** page
2. Click **Create Finding** tab
3. Fill in the form:
   - Select audit
   - Choose type (NC/OFI)
   - Set severity and category
   - Enter clause number and description
   - Assign to responsible person
   - Set due date
4. Click **Create Finding**
5. Assignee receives email notification

### Managing Findings

1. Use **Findings List** tab
2. Apply filters in sidebar:
   - Status
   - Severity
   - Type
   - Assignee
3. Search by clause or description
4. Expand finding to update status
5. Add comments to status changes

### Exporting Data

1. Apply desired filters
2. Click **Export to Excel**
3. Download generated Excel file

## 🎯 Compliance Standards

The system is designed to support:

- **ISO 9001:2015** - Quality Management Systems
- **IATF 16949:2016** - Automotive Quality Management
- **VDA 6.3** - Process Audit

## 🤝 Contributing

This is a private enterprise system. For feature requests or bug reports, contact the development team.

## 📄 License

Proprietary - All rights reserved

## 🔧 Development

### Adding New Features

1. Create feature branch
2. Implement models in `models/`
3. Add utilities in `utils/`
4. Create Streamlit page in `pages/`
5. Write tests in `tests/`
6. Update documentation

### Database Migrations

When modifying models:
1. Update model classes
2. Delete `audit_pro.db`
3. Restart application (auto-creates tables)
4. Reload sample data

## 📞 Support

For technical support or questions:
- Check the in-app documentation
- Contact your system administrator
- Review test cases for usage examples

## 🏆 Credits

Developed for enterprise audit management and compliance tracking.

**Version:** 1.0.0
**Last Updated:** 2024
**Session:** APE-006
