# Audit Pro Enterprise

Enterprise Audit Management System - ISO 9001, IATF 16949, VDA 6.3 compliant. NC/OFI tracking, CAR/8D, Audit Planning & Reporting with Streamlit

## 🏢 Entity Hierarchy Management (SESSION-APE-003)

Comprehensive hierarchical entity/organization structure management system with full CRUD operations, circular reference prevention, and data validation.

### Features

- **5-Level Hierarchical Structure**
  - Level 0: Corporate
  - Level 1: Plant
  - Level 2: Line
  - Level 3: Process
  - Level 4: Sub-Process

- **Advanced Hierarchy Management**
  - Automatic level calculation based on parent
  - Circular reference prevention
  - Cascade display with expandable tree view
  - Parent-child relationship validation
  - Active/Inactive status tracking

- **User Interface**
  - Hierarchical tree view with expandable sections
  - Add/Edit/Deactivate entity operations
  - View detailed entity information
  - Search and filter by name, type, level
  - Excel export functionality

- **Data Integrity**
  - Prevents circular references
  - Validates parent-child relationships
  - Type validation based on hierarchy level
  - Email format validation
  - Database constraints for data integrity

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ganeshgowri-ASA/audit-pro-enterprise.git
cd audit-pro-enterprise

# Install dependencies
pip install -r requirements.txt
```

### Database Initialization

```bash
# Initialize database and create sample data
python scripts/init_db.py
```

This will create:
- Database tables
- Sample organizational hierarchy:
  - ABC Corporation (Corporate)
    - Plant A - Mumbai (Plant)
      - Assembly Line 1 (Line)
        - Welding Process (Process)
        - Painting Process (Process)
      - Assembly Line 2 (Line)
    - Plant B - Pune (Plant)
      - Quality Control Line (Line)
        - Inspection Process (Process)

### Run Application

```bash
# Start Streamlit application
streamlit run Home.py
```

Access the application at: `http://localhost:8501`

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_entity.py -v

# Run with coverage
pytest tests/ --cov=models --cov=utils --cov-report=html
```

### Test Coverage

- `test_entity_crud()` - CRUD operations
- `test_hierarchy_integrity()` - Hierarchy relationships and validation
- `test_circular_reference_prevention()` - Circular reference detection
- Entity validation tests
- Helper function tests

## 📁 Project Structure

```
audit-pro-enterprise/
├── Home.py                      # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── config/
│   ├── __init__.py
│   └── settings.py              # Application configuration
├── database/
│   ├── __init__.py
│   ├── base.py                  # SQLAlchemy Base
│   ├── engine.py                # Database engine
│   └── session.py               # Session management
├── models/
│   ├── __init__.py
│   └── entity.py                # Entity model with hierarchy logic
├── pages/
│   ├── __init__.py
│   └── 01_🏢_Entity_Management.py  # Entity management UI
├── utils/
│   ├── __init__.py
│   └── entity_helpers.py        # Entity utility functions
├── scripts/
│   ├── __init__.py
│   └── init_db.py               # Database initialization
└── tests/
    ├── __init__.py
    ├── conftest.py              # Pytest fixtures
    └── test_entity.py           # Entity tests

```

## 🗃️ Database Schema

### Entity Model

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| name | String(200) | Entity name |
| type | String(50) | Entity type (Corporate/Plant/Line/Process/Sub-Process) |
| parent_id | Integer | Foreign key to parent entity |
| level | Integer | Hierarchy level (0-4) |
| location | String(200) | Physical location |
| address | Text | Full address |
| contact_person | String(100) | Contact person name |
| email | String(100) | Contact email |
| phone | String(20) | Contact phone |
| is_active | Boolean | Active status |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |
| description | Text | Optional description |

### Constraints

- Level must be between 0 and 4
- Root entities (level 0) must have no parent
- Parent entity must be one level above child
- Prevents deletion of entities with children

## 🔧 Usage Examples

### Adding an Entity

```python
from database.session import get_db
from models.entity import Entity

with get_db() as db:
    entity = Entity(
        name="New Plant",
        type="Plant",
        level=1,
        parent_id=corporate_id,
        location="Bangalore",
        is_active=True
    )
    db.add(entity)
    db.commit()
```

### Querying Hierarchy

```python
from models.entity import Entity

# Get full path
entity = db.query(Entity).filter(Entity.id == entity_id).first()
full_path = entity.get_full_path()  # "ABC Corp > Plant A > Line 1"

# Get all children
all_children = entity.get_all_children()

# Get ancestors
ancestors = entity.get_ancestors()
```

### Preventing Circular References

```python
from utils.entity_helpers import validate_circular_reference

is_valid, error_msg = validate_circular_reference(
    session=db,
    entity_id=entity_id,
    parent_id=new_parent_id
)

if not is_valid:
    print(f"Error: {error_msg}")
```

## 📊 Export Features

- Export entities to Excel with full hierarchy information
- Includes all entity details and relationships
- Filtered by active/inactive status
- Timestamped export files

## 🛠️ Technology Stack

- **Backend**: Python 3.8+
- **Web Framework**: Streamlit 1.28+
- **ORM**: SQLAlchemy 2.0+
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Testing**: pytest 7.4+
- **Data Export**: pandas, openpyxl

## 📝 Development Guidelines

### Adding New Entity Types

To add new hierarchy levels, update `config/settings.py`:

```python
ENTITY_TYPES = {
    0: "Corporate",
    1: "Plant",
    2: "Line",
    3: "Process",
    4: "Sub-Process",
    5: "New Level"  # Add new level
}

MAX_HIERARCHY_LEVEL = 5  # Update max level
```

### Extending the Model

The Entity model can be extended with additional fields:

```python
class Entity(Base):
    # Existing fields...

    # Add new fields
    cost_center = Column(String(20), nullable=True)
    budget = Column(Float, nullable=True)
```

## 🔐 Security Considerations

- Email validation for contact fields
- SQL injection prevention via SQLAlchemy ORM
- Input sanitization in Streamlit forms
- Database constraints for data integrity

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/entity-management`)
3. Commit changes (`git commit -m 'Add entity feature'`)
4. Push to branch (`git push origin feature/entity-management`)
5. Open Pull Request

## 📄 License

This project is part of the Audit Pro Enterprise system.

## 🐛 Known Issues

None at this time.

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Session**: APE-003
**Branch**: feature/entity-management
**Status**: ✅ Complete - Isolated, merge-ready, no external dependencies
