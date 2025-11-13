"""
Setup script to initialize the database and create tables.
Run this script before starting the application.
"""
from config.db import Base, engine
from domain.user import User  # Import all your models here


def setup_database():
    """
    Creates all database tables based on the defined models.
    """
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

    # List all created tables
    print("\nCreated tables:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")


if __name__ == '__main__':
    setup_database()
