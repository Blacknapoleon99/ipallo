from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
import os
from .models import Base

# Database configuration
DATABASE_URL = "sqlite:///./blackz_allocator.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL debugging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session() -> Session:
    """
    Get a database session for non-FastAPI usage
    """
    return SessionLocal()

def init_database():
    """
    Initialize the database with tables and sample data
    """
    # Create tables
    create_tables()
    
    # Add sample data if database is empty
    db = SessionLocal()
    try:
        from .models import IPPool, NetworkInterface
        
        # Check if pools exist
        pool_count = db.query(IPPool).count()
        if pool_count == 0:
            # Create sample pools
            sample_pools = [
                IPPool(
                    name="Default_LAN",
                    cidr="192.168.1.0/24",
                    description="Default LAN pool for testing",
                    gateway="192.168.1.1",
                    dns_servers='["8.8.8.8", "8.8.4.4"]',
                    reserved_ranges='[{"start": "192.168.1.1", "end": "192.168.1.10"}, {"start": "192.168.1.250", "end": "192.168.1.255"}]'
                ),
                IPPool(
                    name="Guest_Network",
                    cidr="192.168.100.0/24",
                    description="Guest network isolation",
                    gateway="192.168.100.1",
                    dns_servers='["1.1.1.1", "1.0.0.1"]',
                    reserved_ranges='[{"start": "192.168.100.1", "end": "192.168.100.5"}]'
                ),
                IPPool(
                    name="DMZ_Network",
                    cidr="10.0.1.0/24",
                    description="DMZ for servers",
                    gateway="10.0.1.1",
                    dns_servers='["8.8.8.8", "8.8.4.4"]',
                    reserved_ranges='[{"start": "10.0.1.1", "end": "10.0.1.10"}]'
                )
            ]
            
            for pool in sample_pools:
                db.add(pool)
            
            db.commit()
            print("Sample IP pools created successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

# Initialize database on import
if not os.path.exists("blackz_allocator.db"):
    print("Creating new database...")
    init_database()
else:
    # Ensure tables exist
    create_tables() 