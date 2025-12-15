"""Database setup: engine, session factory, and FastAPI dependency.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Annotated
from ..core.config import settings
from fastapi import Depends

# Create the SQLAlchemy engine
# pool_pre_ping=True checks if the connection is alive before using it
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
# Factory that creates new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base class for all ORM models
Base = declarative_base()

# Dependency that provides a database session per request
def get_db():
    """
    Creates a database session and ensures it is closed
    after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db # The session is injected into the request
    finally:
        db.close() # Always close the session (important for security)

# Type alias for cleaner dependency injection
# FastAPI will use get_db to provide a Session where DbSession is used
DbSession = Annotated[Session, Depends(get_db)]
