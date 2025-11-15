"""
Initialize sample user data for testing and demonstration.
Creates default users for each role type.
"""
from models import init_database, get_session, User
from components.auth import hash_password
from datetime import datetime


def create_sample_users():
    """Create sample users for each role."""
    session = get_session()

    try:
        # Check if users already exist
        existing_users = session.query(User).count()
        if existing_users > 0:
            print(f"Database already contains {existing_users} users. Skipping sample data creation.")
            print("To recreate sample data, delete the database file and run this script again.")
            return

        print("Creating sample users...")

        # Sample users data
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@auditpro.com',
                'password': 'admin123',
                'role': 'admin',
                'full_name': 'System Administrator',
                'department': 'IT & Quality',
                'is_active': True
            },
            {
                'username': 'auditor1',
                'email': 'auditor1@auditpro.com',
                'password': 'audit123',
                'role': 'auditor',
                'full_name': 'John Smith',
                'department': 'Quality Assurance',
                'is_active': True
            },
            {
                'username': 'auditor2',
                'email': 'auditor2@auditpro.com',
                'password': 'audit123',
                'role': 'auditor',
                'full_name': 'Sarah Johnson',
                'department': 'Quality Assurance',
                'is_active': True
            },
            {
                'username': 'auditee1',
                'email': 'auditee1@auditpro.com',
                'password': 'auditee123',
                'role': 'auditee',
                'full_name': 'Michael Brown',
                'department': 'Production',
                'is_active': True
            },
            {
                'username': 'auditee2',
                'email': 'auditee2@auditpro.com',
                'password': 'auditee123',
                'role': 'auditee',
                'full_name': 'Emily Davis',
                'department': 'Engineering',
                'is_active': True
            },
            {
                'username': 'viewer1',
                'email': 'viewer1@auditpro.com',
                'password': 'view123',
                'role': 'viewer',
                'full_name': 'David Wilson',
                'department': 'Management',
                'is_active': True
            },
            {
                'username': 'viewer2',
                'email': 'viewer2@auditpro.com',
                'password': 'view123',
                'role': 'viewer',
                'full_name': 'Lisa Anderson',
                'department': 'Finance',
                'is_active': True
            }
        ]

        # Create users
        created_count = 0
        for user_data in users_data:
            # Hash password
            password = user_data.pop('password')
            password_hash = hash_password(password)

            # Create user
            user = User(
                password_hash=password_hash,
                created_at=datetime.utcnow(),
                **user_data
            )

            session.add(user)
            created_count += 1
            print(f"  ✓ Created user: {user_data['username']} ({user_data['role']})")

        # Commit all users
        session.commit()
        print(f"\n✓ Successfully created {created_count} sample users!")

        # Display credentials
        print("\n" + "="*60)
        print("SAMPLE USER CREDENTIALS")
        print("="*60)
        print("\nAdministrator:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nAuditor:")
        print("  Username: auditor1")
        print("  Password: audit123")
        print("\nAuditee:")
        print("  Username: auditee1")
        print("  Password: auditee123")
        print("\nViewer:")
        print("  Username: viewer1")
        print("  Password: view123")
        print("\n" + "="*60)

    except Exception as e:
        print(f"Error creating sample users: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def main():
    """Main function to initialize database and create sample data."""
    print("Initializing Audit Pro Enterprise Database...")
    print("-" * 60)

    # Initialize database (create tables)
    init_database()
    print("✓ Database tables created")

    # Create sample users
    create_sample_users()

    print("\n✓ Database initialization complete!")
    print("\nYou can now run the application with: streamlit run app.py")


if __name__ == "__main__":
    main()
