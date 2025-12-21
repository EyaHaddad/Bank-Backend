"""Transaction services module for transaction-related operations."""

from sqlalchemy.orm import Session

from src.models.user import User


class TransactionService:
    """Service class for transaction-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    def list_transactions(self, user_id: int) -> list:
        """Retrieve all transactions for a user."""
        return self._db.query(User).filter(User.id == user_id).first()
