"""Database setup: engine, session factory, and FastAPI dependency."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Annotated
from fastapi import Depends

# Base class for all ORM models (can be imported without side effects)
Base = declarative_base()

# Lazy initialization for engine and session factory
_engine = None
_SessionLocal = None


def get_engine():
    """Lazily create and return the SQLAlchemy engine."""
    global _engine
    if _engine is None:
        from src.config import settings
        _engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    return _engine


def get_session_local():
    """Lazily create and return the session factory."""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


class _LazyEngine:
    """Wrapper to allow lazy engine access via module-level 'engine' variable."""
    def __getattr__(self, name):
        return getattr(get_engine(), name)

    def __call__(self, *args, **kwargs):
        return get_engine()(*args, **kwargs)


class _LazySessionLocal:
    """Wrapper to allow lazy SessionLocal access via module-level variable."""
    def __getattr__(self, name):
        return getattr(get_session_local(), name)

    def __call__(self, *args, **kwargs):
        return get_session_local()(*args, **kwargs)


# Module-level lazy proxies for backward compatibility
engine = _LazyEngine()
SessionLocal = _LazySessionLocal()


def get_db():
    """
    Creates a database session and ensures it is closed
    after the request is finished.
    """
    db = get_session_local()()
    try:
        yield db  # The session is injected into the request
    finally:
        db.close()  # Always close the session (important for security)


# Type alias for cleaner dependency injection
# FastAPI will use get_db to provide a Session where DbSession is used
DbSession = Annotated[Session, Depends(get_db)]
