"""Notification entity module."""

from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import BaseEntity


class NotificationType(str, PyEnum):
    """Enum for notification types."""
    EMAIL = "EMAIL"
    SMS = "SMS"

class Notification(BaseEntity):
    """Notification entity representing a notification sent to a user."""

    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    type = Column(Enum(NotificationType), default=NotificationType.EMAIL, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationship to User
    user = relationship("User", back_populates="notifications")

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, type={self.type}, title={self.title}, user_id={self.user_id})>"
