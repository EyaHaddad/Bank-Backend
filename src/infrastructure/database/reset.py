"""Database reset utility."""

from src.infrastructure.database import engine, Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database reset done.")
