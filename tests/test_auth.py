"""
Unit tests for authentication and authorization.
Tests password hashing, login, permissions, and role-based access control.
"""
import unittest
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.auth import (
    hash_password,
    verify_password,
    check_permission,
    check_role,
    get_user_permissions,
    ROLE_PERMISSIONS
)
from models import init_database, get_session, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestPasswordHashing(unittest.TestCase):
    """Test password hashing and verification."""

    def test_hash_password(self):
        """Test that password hashing works correctly."""
        password = "test_password_123"
        hashed = hash_password(password)

        # Check that hash is generated
        self.assertIsNotNone(hashed)
        self.assertIsInstance(hashed, str)
        self.assertGreater(len(hashed), 0)

        # Check that hash is different from password
        self.assertNotEqual(password, hashed)

    def test_hash_password_consistency(self):
        """Test that same password produces different hashes (salt)."""
        password = "test_password_123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Hashes should be different due to different salts
        self.assertNotEqual(hash1, hash2)

    def test_verify_password_success(self):
        """Test successful password verification."""
        password = "test_password_123"
        hashed = hash_password(password)

        # Verify correct password
        result = verify_password(password, hashed)
        self.assertTrue(result)

    def test_verify_password_failure(self):
        """Test failed password verification with wrong password."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)

        # Verify incorrect password
        result = verify_password(wrong_password, hashed)
        self.assertFalse(result)

    def test_verify_password_edge_cases(self):
        """Test password verification with edge cases."""
        # Empty password
        hashed = hash_password("test")
        self.assertFalse(verify_password("", hashed))

        # Special characters
        special_password = "p@ssw0rd!#$%^&*()"
        special_hash = hash_password(special_password)
        self.assertTrue(verify_password(special_password, special_hash))

        # Unicode characters
        unicode_password = "пароль密码🔐"
        unicode_hash = hash_password(unicode_password)
        self.assertTrue(verify_password(unicode_password, unicode_hash))


class TestDatabaseUser(unittest.TestCase):
    """Test User model and database operations."""

    @classmethod
    def setUpClass(cls):
        """Set up test database."""
        # Use in-memory SQLite database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.engine)

        # Create tables
        from models.user import Base
        Base.metadata.create_all(cls.engine)

    def setUp(self):
        """Set up test session."""
        self.session = self.Session()

    def tearDown(self):
        """Clean up test session."""
        self.session.rollback()
        self.session.close()

    def test_create_user(self):
        """Test creating a user."""
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('password123'),
            role='auditor',
            full_name='Test User',
            department='QA',
            is_active=True,
            created_at=datetime.utcnow()
        )

        self.session.add(user)
        self.session.commit()

        # Retrieve user
        retrieved_user = self.session.query(User).filter(User.username == 'testuser').first()

        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertEqual(retrieved_user.role, 'auditor')
        self.assertEqual(retrieved_user.full_name, 'Test User')
        self.assertEqual(retrieved_user.department, 'QA')
        self.assertTrue(retrieved_user.is_active)

    def test_user_unique_username(self):
        """Test that username must be unique."""
        user1 = User(
            username='duplicate',
            email='user1@example.com',
            password_hash=hash_password('password123'),
            role='auditor',
            is_active=True
        )
        self.session.add(user1)
        self.session.commit()

        # Try to create another user with same username
        user2 = User(
            username='duplicate',
            email='user2@example.com',
            password_hash=hash_password('password123'),
            role='viewer',
            is_active=True
        )
        self.session.add(user2)

        with self.assertRaises(Exception):
            self.session.commit()

    def test_user_to_dict(self):
        """Test user to_dict method."""
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('password123'),
            role='auditor',
            full_name='Test User',
            department='QA',
            is_active=True,
            created_at=datetime.utcnow()
        )

        user_dict = user.to_dict()

        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['username'], 'testuser')
        self.assertEqual(user_dict['email'], 'test@example.com')
        self.assertEqual(user_dict['role'], 'auditor')
        self.assertNotIn('password_hash', user_dict)  # Password should not be in dict


class TestRolePermissions(unittest.TestCase):
    """Test role-based permissions."""

    def test_role_permissions_defined(self):
        """Test that all roles have permissions defined."""
        expected_roles = ['admin', 'auditor', 'auditee', 'viewer']

        for role in expected_roles:
            self.assertIn(role, ROLE_PERMISSIONS)
            self.assertIsInstance(ROLE_PERMISSIONS[role], list)
            self.assertGreater(len(ROLE_PERMISSIONS[role]), 0)

    def test_admin_permissions(self):
        """Test admin has full permissions."""
        admin_perms = ROLE_PERMISSIONS['admin']

        # Admin should have all critical permissions
        self.assertIn('create', admin_perms)
        self.assertIn('read', admin_perms)
        self.assertIn('update', admin_perms)
        self.assertIn('delete', admin_perms)
        self.assertIn('manage_users', admin_perms)
        self.assertIn('manage_audits', admin_perms)

    def test_auditor_permissions(self):
        """Test auditor has appropriate permissions."""
        auditor_perms = ROLE_PERMISSIONS['auditor']

        # Auditor should have audit management permissions
        self.assertIn('create', auditor_perms)
        self.assertIn('read', auditor_perms)
        self.assertIn('update', auditor_perms)
        self.assertIn('manage_audits', auditor_perms)

        # Auditor should NOT have user management
        self.assertNotIn('manage_users', auditor_perms)
        self.assertNotIn('delete', auditor_perms)

    def test_auditee_permissions(self):
        """Test auditee has limited permissions."""
        auditee_perms = ROLE_PERMISSIONS['auditee']

        # Auditee should have read access
        self.assertIn('read', auditee_perms)
        self.assertIn('respond_findings', auditee_perms)

        # Auditee should NOT have create/update/delete
        self.assertNotIn('create', auditee_perms)
        self.assertNotIn('update', auditee_perms)
        self.assertNotIn('delete', auditee_perms)
        self.assertNotIn('manage_users', auditee_perms)

    def test_viewer_permissions(self):
        """Test viewer has read-only permissions."""
        viewer_perms = ROLE_PERMISSIONS['viewer']

        # Viewer should have read access
        self.assertIn('read', viewer_perms)
        self.assertIn('view_reports', viewer_perms)

        # Viewer should NOT have write permissions
        self.assertNotIn('create', viewer_perms)
        self.assertNotIn('update', viewer_perms)
        self.assertNotIn('delete', viewer_perms)
        self.assertNotIn('manage_users', viewer_perms)

    def test_check_permission(self):
        """Test check_permission function."""
        # Admin user
        admin_user = {'username': 'admin', 'role': 'admin'}
        self.assertTrue(check_permission('manage_users', admin_user))
        self.assertTrue(check_permission('delete', admin_user))

        # Auditor user
        auditor_user = {'username': 'auditor', 'role': 'auditor'}
        self.assertTrue(check_permission('manage_audits', auditor_user))
        self.assertFalse(check_permission('manage_users', auditor_user))

        # Viewer user
        viewer_user = {'username': 'viewer', 'role': 'viewer'}
        self.assertTrue(check_permission('read', viewer_user))
        self.assertFalse(check_permission('create', viewer_user))

    def test_check_role(self):
        """Test check_role function."""
        admin_user = {'username': 'admin', 'role': 'admin'}
        auditor_user = {'username': 'auditor', 'role': 'auditor'}

        self.assertTrue(check_role('admin', admin_user))
        self.assertFalse(check_role('admin', auditor_user))
        self.assertTrue(check_role('auditor', auditor_user))

    def test_get_user_permissions(self):
        """Test get_user_permissions function."""
        admin_user = {'username': 'admin', 'role': 'admin'}
        perms = get_user_permissions(admin_user)

        self.assertIsInstance(perms, list)
        self.assertGreater(len(perms), 0)
        self.assertEqual(perms, ROLE_PERMISSIONS['admin'])


class TestLoginLogic(unittest.TestCase):
    """Test login and session management logic (without Streamlit)."""

    @classmethod
    def setUpClass(cls):
        """Set up test database."""
        cls.engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.engine)

        from models.user import Base
        Base.metadata.create_all(cls.engine)

    def setUp(self):
        """Set up test session and create test user."""
        self.session = self.Session()

        # Create test user
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=hash_password('password123'),
            role='auditor',
            full_name='Test User',
            department='QA',
            is_active=True,
            created_at=datetime.utcnow()
        )
        self.session.add(self.test_user)
        self.session.commit()

    def tearDown(self):
        """Clean up test session."""
        self.session.query(User).delete()
        self.session.commit()
        self.session.close()

    def test_login_success_logic(self):
        """Test login logic with correct credentials."""
        # Retrieve user
        user = self.session.query(User).filter(User.username == 'testuser').first()
        self.assertIsNotNone(user)

        # Verify password
        is_valid = verify_password('password123', user.password_hash)
        self.assertTrue(is_valid)

        # Check user is active
        self.assertTrue(user.is_active)

    def test_login_failure_wrong_password(self):
        """Test login failure with wrong password."""
        user = self.session.query(User).filter(User.username == 'testuser').first()
        is_valid = verify_password('wrong_password', user.password_hash)
        self.assertFalse(is_valid)

    def test_login_failure_inactive_user(self):
        """Test login failure for inactive user."""
        # Create inactive user
        inactive_user = User(
            username='inactive',
            email='inactive@example.com',
            password_hash=hash_password('password123'),
            role='viewer',
            is_active=False,
            created_at=datetime.utcnow()
        )
        self.session.add(inactive_user)
        self.session.commit()

        # Retrieve user
        user = self.session.query(User).filter(User.username == 'inactive').first()
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active)

    def test_login_failure_user_not_found(self):
        """Test login failure when user doesn't exist."""
        user = self.session.query(User).filter(User.username == 'nonexistent').first()
        self.assertIsNone(user)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPasswordHashing))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseUser))
    suite.addTests(loader.loadTestsFromTestCase(TestRolePermissions))
    suite.addTests(loader.loadTestsFromTestCase(TestLoginLogic))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
