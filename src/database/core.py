"""Database setup: engine, session factory, and FastAPI dependency.

Creates a single SQLAlchemy engine (with pool pre-ping), a session factory,
and a FastAPI dependency that yields a scoped session per request and closes it
afterwards. Use `DbSession` as the typed dependency in route signatures to get
an open session. The database URL comes from application settings.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Annotated
from src.core.config import settings
from fastapi import Depends


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]
