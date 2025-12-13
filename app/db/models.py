from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    
    hashed_password = Column(String)

    otp = Column(String, nullable=True)
    otp_expires_at = Column(DateTime, nullable=True)

    
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="TND")

    user = relationship("User", back_populates="accounts")


class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    bank = Column(String)
    account_number = Column(String)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    sender_account_id = Column(Integer)
    beneficiary_account = Column(String)
    amount = Column(Float)
    reference = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
