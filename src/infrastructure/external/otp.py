"""OTP generation and verification service."""

import pyotp
from datetime import datetime, timedelta
from src.config import settings

OTP_SECRET_LENGTH = settings.OTP_SECRET_LENGTH
OTP_VALIDITY_SECONDS = settings.OTP_VALIDITY_PERIOD * 60
OTP_DIGITS = settings.OTP_DIGITS


def generate_otp():
    """Generate a new OTP and its expiration time."""
    otp = pyotp.random_base32()[:6]
    expires_at = datetime.utcnow() + timedelta(seconds=OTP_VALIDITY_SECONDS)
    return otp, expires_at


def verify_otp(user_otp: str, stored_otp: str, expires_at):
    """Verify an OTP against stored value and expiration."""
    if not stored_otp or not expires_at:
        return False

    if datetime.utcnow() > expires_at:
        return False

    return user_otp == stored_otp
