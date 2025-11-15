# Audit Pro Enterprise 🔍

Enterprise Audit Management System with CAR/8D Methodology and Advanced Reporting

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

**Audit Pro Enterprise** is a comprehensive audit management system designed for organizations following quality standards such as ISO 9001, IATF 16949, and VDA 6.3. The system provides end-to-end management of audits, non-conformances, corrective actions using 8D methodology, and powerful analytics dashboards.

### Key Features

- **📋 Audit Management** - Plan, execute, and track audits
- **🔧 CAR & 8D Methodology** - Complete 8D problem-solving workflow with root cause analysis
- **📊 Reports & Analytics** - Executive dashboards, KPIs, trend analysis, and PDF generation
- **📈 Real-time KPIs** - Track completion rates, audit scores, and NC closure rates
- **📄 PDF Report Generation** - Professional audit reports, NC summaries, and management reviews
- **🔍 Advanced Analytics** - Plotly-powered interactive charts and trend analysis
- **📤 Data Export** - Export to Excel, CSV, and PDF formats

## 🏗️ Architecture

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: SQLAlchemy ORM
- **Database**: SQLite (easily configurable for PostgreSQL, MySQL)
- **Visualization**: Plotly, Matplotlib, Seaborn
- **PDF Generation**: ReportLab, WeasyPrint
- **Testing**: pytest

### Project Structure

```
audit-pro-enterprise/
├── app.py                      # Main Streamlit application
├── database.py                 # Database configuration
├── requirements.txt            # Python dependencies
├── models/                     # Data models
│   ├── __init__.py
│   ├── audit.py               # Audit model
│   ├── nc_ofi.py              # Non-Conformance/OFI model
│   ├── car.py                 # CAR with 8D methodology
│   └── reports.py             # Audit Reports model
├── pages/                      # Streamlit pages
│   ├── 05_🔧_Corrective_Actions.py    # CAR & 8D workflow
│   └── 06_📊_Reports_Analytics.py      # Reports & Analytics
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── generate_sample_data.py        # Sample data generator
│   └── pdf_generator.py               # PDF report generator
├── tests/                      # Test suite
│   ├── test_car_8d.py                 # CAR & 8D tests
│   └── test_reports_analytics.py      # Reports tests
└── data/                       # Data directory
    └── sample_pdfs/            # Generated PDF reports
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/ganeshgowri-ASA/audit-pro-enterprise.git
cd audit-pro-enterprise
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Initialize the database**

The database will be automatically initialized on first run, or you can manually initialize it:

```bash
python -c "from database import init_db; init_db()"
```

5. **Generate sample data** (optional but recommended)

```bash
python utils/generate_sample_data.py
```

This will create:
- 24 audits (covering 12 months)
- NC/OFI findings
- 8 CARs using 8D methodology (5 completed, 3 in-progress)
- Sample audit reports

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 User Guide

### 1. Corrective Actions & 8D Methodology

Navigate to **🔧 Corrective Actions** to:

#### View CARs
- Filter by status, method, or search by CAR number
- View 8D progress for each CAR
- Edit or delete existing CARs

#### Create New CAR
1. Select an open NC/OFI
2. Choose CAR method (8D, 5-Why, Fishbone, PDCA)
3. Assign responsible person
4. Set due date
5. Add immediate actions

#### 8D Workflow

Complete each discipline in sequence:

- **D1: Team Formation** - Form cross-functional team
- **D2: Problem Description** - Use 5W2H method (What, When, Where, Who, Why, How, How Many)
- **D3: Containment Actions** - Implement immediate containment
- **D4: Root Cause Analysis** - Use 5-Why or Fishbone diagram
- **D5: Corrective Actions** - Define permanent corrective actions
- **D6: Implementation** - Execute implementation plan
- **D7: Prevention** - Implement systemic prevention measures
- **D8: Team Recognition** - Recognize team and document lessons learned

The system tracks progress through all 8 disciplines with a visual progress indicator.

### 2. Reports & Analytics Dashboard

Navigate to **📊 Reports & Analytics** for:

#### Executive Dashboard
- Total Audits count
- Completion Rate percentage
- Average Audit Score
- Open NC count with alerts
- NC Closure Rate
- Monthly audit trends
- NC status distribution charts
- Severity analysis
- Audit score trends

#### PDF Report Generation

Generate professional PDF reports:

1. **Audit Report** - Comprehensive audit report with findings
2. **NC/OFI Summary** - Summary of all non-conformances
3. **CAR Status Report** - Status of all corrective actions
4. **Management Review** - Executive summary for management

#### Analytics

Advanced analytics features:
- **Audit Score Trends** - Track audit performance over time
- **NC by Category** - Distribution analysis with pie/bar charts
- **Repeat Findings Analysis** - Identify systemic issues
- **Auditor Performance** - Compare auditor effectiveness
- **Entity-wise Heatmap** - Performance across entities

#### Data Export

Export data in multiple formats:
- **Excel** - Full data export for analysis
- **CSV** - Compatible with all spreadsheet tools
- **PDF** - Professional formatted reports

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_car_8d.py -v

# Run tests for reports
pytest tests/test_reports_analytics.py -v
```

### Test Coverage

- **CAR & 8D Workflow**:
  - CAR creation and lifecycle
  - 8D discipline completion (D1-D8)
  - Root cause analysis (5-Why, Fishbone)
  - Effectiveness verification
  - Status transitions

- **Reports & Analytics**:
  - PDF generation (audit, NC, CAR reports)
  - KPI calculations
  - Trend analysis
  - Data export functionality

## 🔧 Configuration

### Database Configuration

By default, the system uses SQLite. To use a different database:

1. Set the `DATABASE_URL` environment variable:

```bash
# PostgreSQL
export DATABASE_URL="postgresql://user:password@localhost/audit_pro"

# MySQL
export DATABASE_URL="mysql://user:password@localhost/audit_pro"
```

2. Install the appropriate database driver:

```bash
# For PostgreSQL
pip install psycopg2-binary

# For MySQL
pip install pymysql
```

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./audit_pro.db
DEBUG=False
```

## 📊 Data Models

### Audit
- Audit planning and execution
- Scoring and compliance tracking
- Findings summary

### NC/OFI (Non-Conformance / Observation for Improvement)
- Finding classification (Major NC, Minor NC, OFI)
- Severity and priority tracking
- Status management
- Repeat finding detection

### Corrective Action (CAR)
- 8D methodology support
- Root cause analysis
- Action tracking
- Effectiveness verification

### Audit Report
- Report generation metadata
- PDF storage paths
- KPI summaries

## 🎨 Features in Detail

### 8D Problem Solving Methodology

The system implements the complete 8D (Eight Disciplines) methodology:

1. **D1: Establish a Team** - Cross-functional team with process knowledge
2. **D2: Describe the Problem** - Use 5W2H for comprehensive problem description
3. **D3: Develop Interim Containment** - Protect customers until permanent fix
4. **D4: Determine Root Causes** - Use analytical tools (5-Why, Fishbone)
5. **D5: Choose Permanent Corrective Actions** - Select and verify solutions
6. **D6: Implement Permanent Corrective Actions** - Execute and track
7. **D7: Prevent Recurrence** - Modify systems and processes
8. **D8: Recognize Team Contributions** - Celebrate success and share learnings

### KPI Tracking

The system calculates and displays:
- Total Audits
- Audit Completion Rate (target: ≥80%)
- Average Audit Score (target: ≥80)
- Open NC Count (alert if >10)
- NC Closure Rate (target: ≥80%)
- CAR Effectiveness Rate

### Supported Standards

- **ISO 9001:2015** - Quality Management Systems
- **IATF 16949:2016** - Automotive Quality Management
- **VDA 6.3** - Process Audit

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

For issues, questions, or suggestions:
- Create an issue in the GitHub repository
- Contact: support@auditpro.example.com

## 🗺️ Roadmap

Future enhancements planned:
- [ ] Email notifications for due dates
- [ ] Advanced RBAC (Role-Based Access Control)
- [ ] Mobile-responsive design
- [ ] API endpoints for integration
- [ ] Custom report templates
- [ ] Multi-language support
- [ ] Advanced scheduling with calendar integration
- [ ] Real-time collaboration features

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Charts powered by [Plotly](https://plotly.com/)
- PDF generation using [ReportLab](https://www.reportlab.com/)
- Testing with [pytest](https://pytest.org/)

---

**Audit Pro Enterprise** - Making audit management efficient and effective.

Version 1.0.0 | © 2024
