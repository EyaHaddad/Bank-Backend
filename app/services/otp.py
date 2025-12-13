import pyotp
from datetime import datetime, timedelta

OTP_VALIDITY_SECONDS = 60  # ✅ 1 minute

def generate_otp():
    otp = pyotp.random_base32()[:6]
    expires_at = datetime.utcnow() + timedelta(seconds=OTP_VALIDITY_SECONDS)
    return otp, expires_at


def verify_otp(user_otp: str, stored_otp: str, expires_at):
    if not stored_otp or not expires_at:
        return False

    if datetime.utcnow() > expires_at:
        return False

    return user_otp == stored_otp
