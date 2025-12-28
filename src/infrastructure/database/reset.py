"""Database reset utility."""

from src.infrastructure.database import Base, get_engine

# IMPORTANT: Import all models so Base.metadata knows about all tables
from src.models import (
    User, Account, Transaction, Beneficiary, 
    OTP, Notification, Transfer
)

engine = get_engine()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

#print("Database removed successfully.")
print("Database reset done.")
#print(engine.url)
