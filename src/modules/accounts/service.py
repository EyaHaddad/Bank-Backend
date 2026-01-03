"""Account services module for account-related operations."""

from uuid import UUID
from datetime import datetime
import logging

from sqlalchemy.orm import Session

from . import schemas
from .exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    AccountAccessDeniedError,
    AccountAlreadyActiveError,
    AccountAlreadyBlockedError,
    AccountClosedError,
)
from src.models.account import Account, AccountStatus
from src.models.transaction import Transaction, TransactionType, TransactionStatus

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

    def list_all_accounts(self) -> list[Account]:
        """Retrieve all accounts in the system (admin operation)."""
        logger.debug("Fetching all accounts from database")
        accounts = self._db.query(Account).all()
        logger.info(f"Retrieved {len(accounts)} accounts")
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
        """Create a new account for a user. Currency is always TND."""
        logger.info(f"Creating new account for user: {user_id}")
        new_account = Account(
            user_id=user_id,
            currency="TND",  # Always TND - Tunisian Dinar
            balance=account_data.initial_balance,
        )
        self._db.add(new_account)
        self._db.commit()
        self._db.refresh(new_account)
        logger.info(f"Successfully created account with ID: {new_account.id}")
        return new_account

    def update_account(self, account_id: UUID, user_id: UUID, account_data: schemas.AccountUpdate) -> Account:
        """Update an account. Currently no fields can be updated."""
        account = self.get_user_account(account_id, user_id)
        # Currency cannot be changed - always TND
        self._db.commit()
        self._db.refresh(account)
        logger.info(f"Account {account_id} retrieved (no updates applied)")
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

    def _generate_reference(self, prefix: str = "TR") -> str:
        """Generate a unique reference for a transaction."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        count = self._db.query(Transaction).count() + 1
        return f"{prefix}_{timestamp}_{count}"

    def transfer(self, source_account_id: UUID, user_id: UUID, target_account_id: UUID, amount: float) -> Account:
        """Transfer money between the client's own accounts. Creates a transaction record."""
        if amount <= 0:
            raise InvalidAmountError("Transfer amount must be positive")
        
        source_account = self.get_user_account(source_account_id, user_id)
        target_account = self.get_account_by_id(target_account_id)
        
        # Verify target account belongs to the same user
        if target_account.user_id != user_id:
            raise AccountAccessDeniedError()
        
        if source_account.balance < amount:
            raise InsufficientFundsError(source_account_id)
        
        # Create transaction record for the transfer (from source account)
        transaction = Transaction(
            sender_account_id=source_account_id,
            type=TransactionType.TRANSFER,
            amount=amount,
            reference=self._generate_reference("INT"),  # INT = Internal Transfer
            status=TransactionStatus.COMPLETED,
        )
        self._db.add(transaction)
        
        # Update balances
        source_account.balance -= amount
        target_account.balance += amount
        
        self._db.commit()
        self._db.refresh(source_account)
        logger.info(f"Internal transfer of {amount} from account {source_account_id} to {target_account_id}, transaction: {transaction.id}")
        return source_account

    def get_balance(self, account_id: UUID, user_id: UUID) -> schemas.BalanceResponse:
        """Get the balance of an account."""
        account = self.get_user_account(account_id, user_id)
        return schemas.BalanceResponse(
            account_id=account.id,
            balance=account.balance,
            currency=account.currency
        )

    # ==================== ADMIN OPERATIONS ====================

    def activate_account(self, account_id: UUID) -> Account:
        """Activate a blocked account (admin operation)."""
        account = self.get_account_by_id(account_id)
        
        if account.status == AccountStatus.ACTIVE:
            raise AccountAlreadyActiveError(account_id)
        
        if account.status == AccountStatus.CLOSED:
            raise AccountClosedError("Cannot activate a closed account")
        
        account.status = AccountStatus.ACTIVE
        self._db.commit()
        self._db.refresh(account)
        
        logger.info(f"Account {account_id} activated")
        return account

    def block_account(self, account_id: UUID) -> Account:
        """Block an account (admin operation)."""
        account = self.get_account_by_id(account_id)
        
        if account.status == AccountStatus.BLOCKED:
            raise AccountAlreadyBlockedError(account_id)
        
        if account.status == AccountStatus.CLOSED:
            raise AccountClosedError("Cannot block a closed account")
        
        account.status = AccountStatus.BLOCKED
        self._db.commit()
        self._db.refresh(account)
        
        logger.info(f"Account {account_id} blocked")
        return account

    def close_account(self, account_id: UUID) -> Account:
        """Close an account permanently (admin operation)."""
        account = self.get_account_by_id(account_id)
        
        if account.status == AccountStatus.CLOSED:
            raise AccountClosedError(f"Account {account_id} is already closed")
        
        account.status = AccountStatus.CLOSED
        self._db.commit()
        self._db.refresh(account)
        
        logger.info(f"Account {account_id} closed")
        return account

    def admin_delete_account(self, account_id: UUID) -> bool:
        """Delete an account permanently (admin operation)."""
        account = self.get_account_by_id(account_id)
        self._db.delete(account)
        self._db.commit()
        
        logger.info(f"Account {account_id} deleted by admin")
        return True

    def update_balance(self, account_id: UUID, new_balance: float) -> Account:
        """Update account balance (admin operation - for corrections)."""
        if new_balance < 0:
            raise InvalidAmountError("Balance cannot be negative")
        
        account = self.get_account_by_id(account_id)
        old_balance = account.balance
        account.balance = new_balance
        self._db.commit()
        self._db.refresh(account)
        
        logger.info(f"Account {account_id} balance updated from {old_balance} to {new_balance}")
        return account
