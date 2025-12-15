"Unit test module for the database connection and basic operations."

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import BaseEntity

# Setup the in-memory SQLite database for testing
# This is a test database, it doesn't use the production database
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseEntity.metadata.create_all(bind=engine)