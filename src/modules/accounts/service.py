"""Account services module for account-related operations."""

from uuid import UUID
import logging

from sqlalchemy.orm import Session

from . import schemas
from .exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    AccountAccessDeniedError,
)
from src.models.account import Account

logger = logging.getLogger(__name__)


class AccountService:
    """Service class for account-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    def list_accounts(self, user_id: UUID) -> list[Account]:
        """Retrieve all accounts for a specific user."""
        logger.debug(f"Fetching all accounts for user ID: {user_id}")
        accounts = self._db.query(Account).filter(Account.user_id == user_id).all()
        logger.info(f"Retrieved {len(accounts)} accounts for user {user_id}")
        return accounts

    def get_account(self, account_id: UUID) -> Account | None:
        """Retrieve an account by its ID."""
        logger.debug(f"Fetching account with ID: {account_id}")
        return self._db.query(Account).filter(Account.id == account_id).first()

    def get_account_by_id(self, account_id: UUID) -> Account:
        """Retrieve an account by ID, raising an exception if not found."""
        account = self.get_account(account_id)
        if not account:
            logger.warning(f"Account not found with ID: {account_id}")
            raise AccountNotFoundError(account_id)
        logger.debug(f"Successfully retrieved account with ID: {account_id}")
        return account

    def get_user_account(self, account_id: UUID, user_id: UUID) -> Account:
        """Retrieve an account ensuring it belongs to the specified user."""
        account = self.get_account_by_id(account_id)
        if account.user_id != user_id:
            logger.warning(f"User {user_id} attempted to access account {account_id}")
            raise AccountAccessDeniedError()
        return account

    def create_account(self, user_id: UUID, account_data: schemas.AccountCreate) -> Account:
        """Create a new account for a user."""
        logger.info(f"Creating new account for user: {user_id}")
        new_account = Account(
            user_id=user_id,
            currency=account_data.currency,
            balance=account_data.initial_balance,
        )
        self._db.add(new_account)
        self._db.commit()
        self._db.refresh(new_account)
        logger.info(f"Successfully created account with ID: {new_account.id}")
        return new_account

    def update_account(self, account_id: UUID, user_id: UUID, account_data: schemas.AccountUpdate) -> Account:
        """Update an account."""
        account = self.get_user_account(account_id, user_id)
        if account_data.currency:
            account.currency = account_data.currency
        self._db.commit()
        self._db.refresh(account)
        logger.info(f"Successfully updated account with ID: {account_id}")
        return account

    def delete_account(self, account_id: UUID, user_id: UUID) -> bool:
        """Delete an account."""
        account = self.get_user_account(account_id, user_id)
        self._db.delete(account)
        self._db.commit()
        logger.info(f"Successfully deleted account with ID: {account_id}")
        return True

    def deposit(self, account_id: UUID, user_id: UUID, amount: float) -> Account:
        """Deposit money into an account."""
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        
        account = self.get_user_account(account_id, user_id)
        account.balance += amount
        self._db.commit()
        self._db.refresh(account)
        logger.info(f"Deposited {amount} to account {account_id}")
        return account

    def withdraw(self, account_id: UUID, user_id: UUID, amount: float) -> Account:
        """Withdraw money from an account."""
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        
        account = self.get_user_account(account_id, user_id)
        if account.balance < amount:
            raise InsufficientFundsError(account_id)
        
        account.balance -= amount
        self._db.commit()
        self._db.refresh(account)
        logger.info(f"Withdrew {amount} from account {account_id}")
        return account

    def transfer(self, source_account_id: UUID, user_id: UUID, target_account_id: UUID, amount: float) -> Account:
        """Transfer money between accounts."""
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be positive")
        
        source_account = self.get_user_account(source_account_id, user_id)
        target_account = self.get_account_by_id(target_account_id)
        
        if source_account.balance < amount:
            raise InsufficientFundsError(source_account_id)
        
        source_account.balance -= amount
        target_account.balance += amount
        self._db.commit()
        self._db.refresh(source_account)
        logger.info(f"Transferred {amount} from account {source_account_id} to {target_account_id}")
        return source_account

    def get_balance(self, account_id: UUID, user_id: UUID) -> schemas.BalanceResponse:
        """Get the balance of an account."""
        account = self.get_user_account(account_id, user_id)
        return schemas.BalanceResponse(
            account_id=account.id,
            balance=account.balance,
            currency=account.currency
        )
