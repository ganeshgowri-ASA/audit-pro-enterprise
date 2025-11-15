"""
Database initialization script with sample data

Creates database tables and populates with sample hierarchical data:
- ABC Corp (Level 0)
  - Plant A (Level 1)
    - Assembly Line 1 (Level 2)
      - Welding Process (Level 3)
  - Plant B (Level 1)
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.base import Base
from database.engine import engine
from database.session import get_db
from models.entity import Entity
from config.settings import ENTITY_TYPES


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")


def create_sample_data():
    """Create sample hierarchical entity data"""
    print("\nCreating sample data...")

    with get_db() as db:
        # Check if data already exists
        existing_count = db.query(Entity).count()
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} entities")
            response = input("Do you want to delete existing data and recreate? (yes/no): ")
            if response.lower() != 'yes':
                print("Skipping sample data creation")
                return
            else:
                # Delete existing data
                db.query(Entity).delete()
                db.commit()
                print("Existing data deleted")

        # Level 0 - Corporate
        abc_corp = Entity(
            name="ABC Corporation",
            type=ENTITY_TYPES[0],
            level=0,
            parent_id=None,
            location="New Delhi, India",
            address="123 Corporate Tower, Connaught Place, New Delhi - 110001",
            contact_person="Rajesh Kumar",
            email="rajesh.kumar@abccorp.com",
            phone="+91-11-12345678",
            is_active=True,
            description="Parent corporation managing multiple manufacturing plants"
        )
        db.add(abc_corp)
        db.flush()  # Get ID without committing

        print(f"✅ Created: {abc_corp.name} (Level {abc_corp.level})")

        # Level 1 - Plant A
        plant_a = Entity(
            name="Plant A - Mumbai",
            type=ENTITY_TYPES[1],
            level=1,
            parent_id=abc_corp.id,
            location="Mumbai, Maharashtra",
            address="Plot 45-48, MIDC Industrial Area, Andheri East, Mumbai - 400093",
            contact_person="Priya Sharma",
            email="priya.sharma@abccorp.com",
            phone="+91-22-98765432",
            is_active=True,
            description="Primary manufacturing facility for automotive components"
        )
        db.add(plant_a)
        db.flush()

        print(f"✅ Created: {plant_a.name} (Level {plant_a.level})")

        # Level 1 - Plant B
        plant_b = Entity(
            name="Plant B - Pune",
            type=ENTITY_TYPES[1],
            level=1,
            parent_id=abc_corp.id,
            location="Pune, Maharashtra",
            address="Survey No. 123, Chakan Industrial Area, Pune - 410501",
            contact_person="Amit Patel",
            email="amit.patel@abccorp.com",
            phone="+91-20-87654321",
            is_active=True,
            description="Secondary manufacturing facility focusing on precision parts"
        )
        db.add(plant_b)
        db.flush()

        print(f"✅ Created: {plant_b.name} (Level {plant_b.level})")

        # Level 2 - Assembly Line 1 (under Plant A)
        line_1 = Entity(
            name="Assembly Line 1",
            type=ENTITY_TYPES[2],
            level=2,
            parent_id=plant_a.id,
            location="Building A, Floor 2",
            address="Plant A - Mumbai, Building A, Second Floor",
            contact_person="Suresh Reddy",
            email="suresh.reddy@abccorp.com",
            phone="+91-22-98765433",
            is_active=True,
            description="Main assembly line for chassis components"
        )
        db.add(line_1)
        db.flush()

        print(f"✅ Created: {line_1.name} (Level {line_1.level})")

        # Level 2 - Assembly Line 2 (under Plant A)
        line_2 = Entity(
            name="Assembly Line 2",
            type=ENTITY_TYPES[2],
            level=2,
            parent_id=plant_a.id,
            location="Building B, Floor 1",
            address="Plant A - Mumbai, Building B, First Floor",
            contact_person="Kavita Singh",
            email="kavita.singh@abccorp.com",
            phone="+91-22-98765434",
            is_active=True,
            description="Secondary assembly line for body panels"
        )
        db.add(line_2)
        db.flush()

        print(f"✅ Created: {line_2.name} (Level {line_2.level})")

        # Level 3 - Welding Process (under Assembly Line 1)
        welding = Entity(
            name="Welding Process",
            type=ENTITY_TYPES[3],
            level=3,
            parent_id=line_1.id,
            location="Station W-101",
            address="Assembly Line 1, Welding Station W-101",
            contact_person="Deepak Joshi",
            email="deepak.joshi@abccorp.com",
            phone="+91-22-98765435",
            is_active=True,
            description="Robotic welding process for chassis assembly"
        )
        db.add(welding)
        db.flush()

        print(f"✅ Created: {welding.name} (Level {welding.level})")

        # Level 3 - Painting Process (under Assembly Line 1)
        painting = Entity(
            name="Painting Process",
            type=ENTITY_TYPES[3],
            level=3,
            parent_id=line_1.id,
            location="Station P-201",
            address="Assembly Line 1, Painting Station P-201",
            contact_person="Meena Rao",
            email="meena.rao@abccorp.com",
            phone="+91-22-98765436",
            is_active=True,
            description="Automated painting and coating process"
        )
        db.add(painting)
        db.flush()

        print(f"✅ Created: {painting.name} (Level {painting.level})")

        # Level 2 - Quality Control Line (under Plant B)
        qc_line = Entity(
            name="Quality Control Line",
            type=ENTITY_TYPES[2],
            level=2,
            parent_id=plant_b.id,
            location="Building C, Floor 1",
            address="Plant B - Pune, Building C, First Floor",
            contact_person="Vikram Desai",
            email="vikram.desai@abccorp.com",
            phone="+91-20-87654322",
            is_active=True,
            description="Dedicated quality inspection and testing line"
        )
        db.add(qc_line)
        db.flush()

        print(f"✅ Created: {qc_line.name} (Level {qc_line.level})")

        # Level 3 - Inspection Process (under QC Line)
        inspection = Entity(
            name="Inspection Process",
            type=ENTITY_TYPES[3],
            level=3,
            parent_id=qc_line.id,
            location="Station I-301",
            address="Quality Control Line, Inspection Station I-301",
            contact_person="Anjali Mehta",
            email="anjali.mehta@abccorp.com",
            phone="+91-20-87654323",
            is_active=True,
            description="Visual and dimensional inspection process"
        )
        db.add(inspection)
        db.flush()

        print(f"✅ Created: {inspection.name} (Level {inspection.level})")

        # Create one inactive entity as example
        inactive_line = Entity(
            name="Assembly Line 3 (Decommissioned)",
            type=ENTITY_TYPES[2],
            level=2,
            parent_id=plant_a.id,
            location="Building A, Floor 3",
            address="Plant A - Mumbai, Building A, Third Floor",
            contact_person="N/A",
            email="",
            phone="",
            is_active=False,
            description="Decommissioned assembly line - kept for historical records"
        )
        db.add(inactive_line)

        print(f"✅ Created: {inactive_line.name} (Level {inactive_line.level}) - INACTIVE")

        db.commit()

    print("\n✅ Sample data created successfully!")
    print("\nHierarchy Summary:")
    print("└── ABC Corporation (Corporate)")
    print("    ├── Plant A - Mumbai (Plant)")
    print("    │   ├── Assembly Line 1 (Line)")
    print("    │   │   ├── Welding Process (Process)")
    print("    │   │   └── Painting Process (Process)")
    print("    │   ├── Assembly Line 2 (Line)")
    print("    │   └── Assembly Line 3 (Decommissioned) [INACTIVE]")
    print("    └── Plant B - Pune (Plant)")
    print("        └── Quality Control Line (Line)")
    print("            └── Inspection Process (Process)")


def main():
    """Main initialization function"""
    print("=" * 60)
    print("Audit Pro Enterprise - Database Initialization")
    print("=" * 60)

    try:
        create_tables()
        create_sample_data()

        print("\n" + "=" * 60)
        print("✅ Database initialization completed successfully!")
        print("=" * 60)
        print("\nYou can now run the application with:")
        print("  streamlit run Home.py")

    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
