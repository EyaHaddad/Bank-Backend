from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets
import string

from app.db.session import get_db
from app.db.models import User
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.utils.validators import validate_password
from app.core.limiter import limiter

router = APIRouter()

# ------------------ Schemas ------------------

class RegisterRequest(BaseModel):
    email: EmailStr
    phone: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    otp: str


# ------------------ Helpers ------------------

def generate_otp(length: int = 6) -> str:
    return "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))


# ------------------ Routes ------------------

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if not validate_password(data.password):
        raise HTTPException(status_code=400, detail="Weak password")

    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    if db.query(User).filter(User.phone == data.phone).first():
        raise HTTPException(status_code=409, detail="Phone already registered")

    otp = generate_otp()

    user = User(
        email=data.email,
        phone=data.phone,
        hashed_password=hash_password(data.password),
        otp=otp,
        otp_expires_at=datetime.utcnow() + timedelta(minutes=1)  # ⬅️ 1 minute
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "dev_otp": otp  # DEV ONLY
    }


@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.otp or user.otp_expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="OTP expired")

    if user.otp != data.otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    # OTP can be invalidated after use
    user.otp = None
    user.otp_expires_at = None
    db.commit()

    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer"
    }
