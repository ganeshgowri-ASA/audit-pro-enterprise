# Authentication & User Management Module

## Overview

Complete authentication system with role-based access control (RBAC) for the Audit Pro Enterprise application. This module provides secure user authentication, session management, and permission-based access control.

## Features

✓ **Secure Authentication**
- Bcrypt password hashing with salt
- Session-based authentication
- Remember me functionality
- Last login tracking

✓ **Role-Based Access Control (RBAC)**
- Four role types: Admin, Auditor, Auditee, Viewer
- Granular permission system
- Permission decorators for easy access control

✓ **Database Models**
- SQLAlchemy ORM with SQLite
- User model with complete profile support
- Automatic timestamp tracking

✓ **Streamlit Integration**
- Beautiful login page
- Session state management
- User profile display
- Logout functionality

✓ **Testing**
- Comprehensive unit tests
- Password hashing tests
- Permission testing
- Database model tests

## Architecture

```
audit-pro-enterprise/
├── models/
│   ├── __init__.py          # Database initialization
│   └── user.py              # User model
├── components/
│   ├── __init__.py
│   └── auth.py              # Authentication logic
├── pages/
│   ├── __init__.py
│   └── login.py             # Login page
├── tests/
│   ├── __init__.py
│   └── test_auth.py         # Unit tests
├── app.py                   # Main Streamlit app
├── init_sample_data.py      # Sample data creation
└── requirements.txt         # Python dependencies
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_sample_data.py
```

This creates the database and adds sample users for each role.

### 3. Run Application

```bash
streamlit run app.py
```

### 4. Login

Use one of the sample credentials:

**Administrator:**
- Username: `admin`
- Password: `admin123`

**Auditor:**
- Username: `auditor1`
- Password: `audit123`

**Auditee:**
- Username: `auditee1`
- Password: `auditee123`

**Viewer:**
- Username: `viewer1`
- Password: `view123`

## User Roles & Permissions

### Admin
**Full system access**
- Create, Read, Update, Delete
- Manage users
- Manage audits
- Manage findings
- View all reports

### Auditor
**Audit management**
- Create, Read, Update
- Manage audits
- Manage findings
- View reports

### Auditee
**Limited access for audit participants**
- Read assigned audits
- Respond to findings
- View assigned audit data

### Viewer
**Read-only access**
- Read audits
- View reports
- Export data

## Database Schema

### User Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String(50) | Unique username |
| email | String(120) | Unique email |
| password_hash | String(255) | Bcrypt hashed password |
| role | String(20) | User role (admin/auditor/auditee/viewer) |
| full_name | String(100) | User's full name |
| department | String(100) | Department name |
| is_active | Boolean | Account active status |
| created_at | DateTime | Account creation timestamp |
| last_login | DateTime | Last login timestamp |

## API Reference

### Authentication Functions

#### `login(username, password, remember_me=False)`
Authenticate a user with credentials.

```python
from components.auth import login

user = login('admin', 'admin123', remember_me=True)
if user:
    print(f"Logged in as {user['username']}")
```

#### `logout()`
Log out the current user.

```python
from components.auth import logout

logout()
```

#### `check_authentication()`
Check if user is authenticated.

```python
from components.auth import check_authentication

if check_authentication():
    print("User is logged in")
```

#### `get_current_user()`
Get the currently logged-in user.

```python
from components.auth import get_current_user

user = get_current_user()
if user:
    print(f"Current user: {user['username']}")
```

### Permission Functions

#### `check_permission(permission, user=None)`
Check if user has specific permission.

```python
from components.auth import check_permission

if check_permission('manage_users'):
    print("User can manage users")
```

#### `check_role(role, user=None)`
Check if user has specific role.

```python
from components.auth import check_role

if check_role('admin'):
    print("User is an admin")
```

#### `get_user_permissions(user=None)`
Get list of user's permissions.

```python
from components.auth import get_user_permissions

permissions = get_user_permissions()
print(f"User has {len(permissions)} permissions")
```

### Password Functions

#### `hash_password(password)`
Hash a password using bcrypt.

```python
from components.auth import hash_password

hashed = hash_password('my_secure_password')
```

#### `verify_password(password, password_hash)`
Verify password against hash.

```python
from components.auth import verify_password

is_valid = verify_password('my_secure_password', hashed)
```

### Decorators

#### `@require_authentication`
Require user to be logged in.

```python
from components.auth import require_authentication

@require_authentication
def protected_function():
    print("This requires login")
```

#### `@require_permission(permission)`
Require specific permission.

```python
from components.auth import require_permission

@require_permission('manage_users')
def admin_function():
    print("This requires manage_users permission")
```

#### `@require_role(role)`
Require specific role.

```python
from components.auth import require_role

@require_role('admin')
def admin_only_function():
    print("This is admin only")
```

## Testing

### Run All Tests

```bash
python tests/test_auth.py
```

### Run with pytest

```bash
pytest tests/test_auth.py -v
```

### Run with Coverage

```bash
pytest tests/test_auth.py --cov=components --cov=models --cov-report=html
```

### Test Categories

1. **Password Hashing Tests**
   - Hash generation
   - Hash consistency (different salts)
   - Password verification
   - Edge cases (empty, special chars, unicode)

2. **Database Tests**
   - User creation
   - Unique constraints
   - to_dict method

3. **Permission Tests**
   - Role permissions defined
   - Admin full access
   - Auditor permissions
   - Auditee limited access
   - Viewer read-only

4. **Login Logic Tests**
   - Successful login
   - Wrong password
   - Inactive user
   - Non-existent user

## Security Considerations

### Password Security
- Bcrypt hashing with automatic salt generation
- Passwords never stored in plain text
- Password hashes never exposed in API responses

### Session Security
- Session state managed by Streamlit
- Automatic session cleanup on logout
- Remember me functionality for persistent sessions

### Database Security
- Parameterized queries via SQLAlchemy ORM
- Protection against SQL injection
- Unique constraints on username and email

### Access Control
- Role-based permissions
- Permission decorators for easy enforcement
- Graceful handling of unauthorized access

## Integration Guide

### Adding Authentication to New Pages

```python
import streamlit as st
from components.auth import require_authentication, check_permission

@require_authentication
def my_page():
    st.title("My Protected Page")

    if check_permission('create'):
        st.button("Create New Item")

    # Page content...
```

### Creating New Users Programmatically

```python
from models import get_session, User
from components.auth import hash_password
from datetime import datetime

session = get_session()

new_user = User(
    username='newuser',
    email='newuser@example.com',
    password_hash=hash_password('secure_password'),
    role='auditor',
    full_name='New User',
    department='Quality',
    is_active=True,
    created_at=datetime.utcnow()
)

session.add(new_user)
session.commit()
session.close()
```

### Checking Permissions in Code

```python
from components.auth import get_current_user, check_permission

user = get_current_user()

if check_permission('manage_audits', user):
    # Show audit management features
    pass

if check_permission('manage_users', user):
    # Show user management features
    pass
```

## Database Management

### View Database

```bash
sqlite3 audit_pro.db
.tables
SELECT * FROM users;
.quit
```

### Reset Database

```bash
rm audit_pro.db
python init_sample_data.py
```

### Backup Database

```bash
cp audit_pro.db audit_pro.db.backup
```

## Troubleshooting

### Issue: "No module named 'bcrypt'"
```bash
pip install bcrypt
```

### Issue: "Database is locked"
Close all connections and restart the app.

### Issue: "Cannot login with sample credentials"
Reinitialize the database:
```bash
rm audit_pro.db
python init_sample_data.py
```

### Issue: "Permission denied"
Check user role and permissions:
```python
from components.auth import get_current_user, get_user_permissions

user = get_current_user()
print(f"Role: {user['role']}")
print(f"Permissions: {get_user_permissions(user)}")
```

## Future Enhancements

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Two-factor authentication (2FA)
- [ ] OAuth integration (Google, Microsoft)
- [ ] Password strength requirements
- [ ] Account lockout after failed attempts
- [ ] Session timeout
- [ ] Audit logging for authentication events
- [ ] User activity tracking
- [ ] Role hierarchy with inheritance

## License

Part of Audit Pro Enterprise - Enterprise Audit Management System

## Support

For issues or questions:
1. Check this documentation
2. Review test cases for examples
3. Check application logs
4. Contact system administrator

---

**Version:** 1.0.0
**Last Updated:** 2025-11-15
**Module:** Authentication & User Management
