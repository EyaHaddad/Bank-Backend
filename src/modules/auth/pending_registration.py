"""Pending registration store - holds registration data until OTP verification."""

import secrets
import hashlib
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional
import threading

from src.models.user import Role

@dataclass
class PendingRegistration:
    """Data for a pending registration."""
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    password_hash: str
    otp_code: str
    otp_expires_at: datetime
    role: Role = Role.USER
    attempts: int = 0
    max_attempts: int = 3
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
    
    def is_otp_expired(self) -> bool:
        """Check if OTP has expired."""
        return datetime.utcnow() > self.otp_expires_at
    
    def is_registration_expired(self) -> bool:
        """Check if the entire registration has expired (30 minutes)."""
        return datetime.utcnow() > self.created_at + timedelta(minutes=30)
    
    def verify_otp(self, code: str) -> bool:
        """Verify OTP code."""
        if self.is_otp_expired():
            return False
        if self.attempts >= self.max_attempts:
            return False
        self.attempts += 1
        return secrets.compare_digest(self.otp_code, code)
    
    def can_resend_otp(self) -> bool:
        """Check if enough time has passed to resend OTP (60 seconds)."""
        time_since_created = datetime.utcnow() - self.created_at
        return time_since_created > timedelta(seconds=60)


class PendingRegistrationStore:
    """Thread-safe in-memory store for pending registrations."""
    
    def __init__(self):
        self._store: dict[str, PendingRegistration] = {}
        self._lock = threading.Lock()
    
    def _generate_otp(self) -> str:
        """Generate a 6-digit OTP code."""
        return ''.join([str(secrets.randbelow(10)) for _ in range(6)])
    
    def _hash_email(self, email: str) -> str:
        """Create a hash key from email."""
        return hashlib.sha256(email.lower().encode()).hexdigest()
    
    def add(self, first_name: str, last_name: str, email: str, phone: Optional[str], password_hash: str, role: Role = Role.USER) -> str:
        """Add a pending registration and return the OTP code."""
        otp_code = self._generate_otp()
        key = self._hash_email(email)
        
        pending = PendingRegistration(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password_hash=password_hash,
            otp_code=otp_code,
            otp_expires_at=datetime.utcnow() + timedelta(minutes=10),
            role=role,
        )
        
        with self._lock:
            self._store[key] = pending
        
        return otp_code
    
    def get(self, email: str) -> Optional[PendingRegistration]:
        """Get pending registration by email."""
        key = self._hash_email(email)
        with self._lock:
            pending = self._store.get(key)
            if pending and pending.is_registration_expired():
                del self._store[key]
                return None
            return pending
    
    def remove(self, email: str) -> Optional[PendingRegistration]:
        """Remove and return pending registration."""
        key = self._hash_email(email)
        with self._lock:
            return self._store.pop(key, None)
    
    def regenerate_otp(self, email: str) -> Optional[str]:
        """Regenerate OTP for existing pending registration."""
        key = self._hash_email(email)
        with self._lock:
            pending = self._store.get(key)
            if pending and not pending.is_registration_expired():
                pending.otp_code = self._generate_otp()
                pending.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
                pending.attempts = 0
                pending.created_at = datetime.utcnow()
                return pending.otp_code
            return None
    
    def cleanup_expired(self):
        """Remove all expired registrations."""
        with self._lock:
            expired_keys = [
                key for key, pending in self._store.items()
                if pending.is_registration_expired()
            ]
            for key in expired_keys:
                del self._store[key]


# Global instance
pending_registrations = PendingRegistrationStore()
