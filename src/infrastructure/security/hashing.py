"""Password hashing utilities."""

from passlib.context import CryptContext
from src.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

MAX_BCRYPT_BYTES = settings.MAX_BCRYPT_BYTES


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    # bcrypt requires <= 72 bytes
    password_bytes = password.encode("utf-8")
    safe_password = password_bytes[:MAX_BCRYPT_BYTES]
    return pwd_context.hash(safe_password.decode("utf-8", errors="ignore"))


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a hashed password."""
    plain_bytes = plain.encode("utf-8")[:MAX_BCRYPT_BYTES]
    return pwd_context.verify(
        plain_bytes.decode("utf-8", errors="ignore"),
        hashed
    )
