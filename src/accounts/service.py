"""Account services module for account-related operations.

This module contains all the business logic related to bank accounts: CRUD operations,
deposits, withdrawals, transfers, and balance management.
"""
from uuid import UUID
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import model
from .exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    InvalidAmountError,
    AccountAccessDeniedError,
)
from src.entities.account import Account

# Configure module-level logger
logger = logging.getLogger(__name__)


class AccountService:
    """Service class for account-related operations.
    
    This service handles all account CRUD operations and financial transactions,
    with proper exception handling and logging.
    """
    
    def __init__(self, session: Session):
        """Initialize the service with a database session.
        
        Args:
            session: SQLAlchemy database session for database operations.
        """
        self._db = session

    def list_accounts(self, user_id: UUID) -> list[Account]:
        """Retrieve all accounts for a specific user.
        
        Args:
            user_id: The UUID of the user whose accounts to retrieve.
            
        Returns:
            List of Account entities belonging to the user.
        """
        logger.debug(f"Fetching all accounts for user ID: {user_id}")
        accounts = self._db.query(Account).filter(Account.user_id == user_id).all()
        logger.info(f"Retrieved {len(accounts)} accounts for user {user_id}")
        return accounts

    def get_account(self, account_id: UUID) -> Account | None:
        """Retrieve an account by its ID.
        
        Args:
            account_id: The UUID of the account to retrieve.
            
        Returns:
            The Account entity if found, None otherwise.
        """
        logger.debug(f"Fetching account with ID: {account_id}")
        return self._db.query(Account).filter(Account.id == account_id).first()

    def get_account_by_id(self, account_id: UUID) -> Account:
        """Retrieve an account by ID, raising an exception if not found.
        
        Args:
            account_id: The UUID of the account to retrieve.
            
        Returns:
            The Account entity.
            
        Raises:
            AccountNotFoundError: If the account does not exist.
        """
        account = self.get_account(account_id)
        if not account:
            logger.warning(f"Account not found with ID: {account_id}")
            raise AccountNotFoundError(account_id)
        logger.debug(f"Successfully retrieved account with ID: {account_id}")
        return account

    def get_user_account(self, account_id: UUID, user_id: UUID) -> Account:
        """Retrieve an account ensuring it belongs to the specified user.
        
        Args:
            account_id: The UUID of the account to retrieve.
            user_id: The UUID of the user who should own the account.
            
        Returns:
            The Account entity.
            
        Raises:
            AccountNotFoundError: If the account does not exist.
            AccountAccessDeniedError: If the account doesn't belong to the user.
        """
        account = self.get_account_by_id(account_id)
        if account.user_id != user_id:
            logger.warning(f"User {user_id} attempted to access account {account_id} without permission")
            raise AccountAccessDeniedError()
        return account

    def create_account(self, user_id: UUID, account_data: model.AccountCreate) -> Account:
        """Create a new account for a user.
        
        Args:
            user_id: The UUID of the user creating the account.
            account_data: AccountCreate model containing account data.
            
        Returns:
            The created Account entity.
        """
        logger.info(f"Creating new account for user ID: {user_id}")
        
        try:
            new_account = Account(
                user_id=user_id,
                balance=account_data.initial_balance,
                currency=account_data.currency,
            )
            self._db.add(new_account)
            self._db.commit()
            self._db.refresh(new_account)
            logger.info(f"Successfully created account with ID: {new_account.id}")
            return new_account
        except IntegrityError as e:
            self._db.rollback()
            logger.error(f"Database integrity error while creating account: {e}")
            raise

    def update_account(self, account_id: UUID, user_id: UUID, account_data: model.AccountUpdate) -> Account:
        """Update an existing account's information.
        
        Args:
            account_id: The UUID of the account to update.
            user_id: The UUID of the user who owns the account.
            account_data: AccountUpdate model containing fields to update.
            
        Returns:
            The updated Account entity.
            
        Raises:
            AccountNotFoundError: If the account does not exist.
            AccountAccessDeniedError: If the user doesn't own the account.
        """
        logger.info(f"Attempting to update account with ID: {account_id}")
        
        account = self.get_user_account(account_id, user_id)

        if account_data.currency is not None:
            account.currency = account_data.currency
            logger.debug(f"Updated currency for account {account_id}")

        self._db.commit()
        self._db.refresh(account)
        logger.info(f"Successfully updated account with ID: {account_id}")
        return account

    def delete_account(self, account_id: UUID, user_id: UUID) -> None:
        """Delete an account from the database.
        
        Args:
            account_id: The UUID of the account to delete.
            user_id: The UUID of the user who owns the account.
            
        Raises:
            AccountNotFoundError: If the account does not exist.
            AccountAccessDeniedError: If the user doesn't own the account.
        """
        logger.info(f"Attempting to delete account with ID: {account_id}")
        
        account = self.get_user_account(account_id, user_id)
        
        self._db.delete(account)
        self._db.commit()
        logger.info(f"Successfully deleted account with ID: {account_id}")

    def deposit(self, account_id: UUID, user_id: UUID, amount: float) -> Account:
        """Deposit funds into an account.
        
        Args:
            account_id: The UUID of the account to deposit into.
            user_id: The UUID of the user who owns the account.
            amount: The amount to deposit.
            
        Returns:
            The updated Account entity.
            
        Raises:
            AccountNotFoundError: If the account does not exist.
            AccountAccessDeniedError: If the user doesn't own the account.
            InvalidAmountError: If the amount is not positive.
        """
        logger.info(f"Processing deposit of {amount} to account {account_id}")
        
        if amount <= 0:
            logger.warning(f"Invalid deposit amount: {amount}")
            raise InvalidAmountError("Deposit amount must be positive")
        
        account = self.get_user_account(account_id, user_id)
        account.balance += amount
        
        self._db.commit()
        self._db.refresh(account)
        logger.info(f"Successfully deposited {amount} to account {account_id}. New balance: {account.balance}")
        return account

    def withdraw(self, account_id: UUID, user_id: UUID, amount: float) -> Account:
        """Withdraw funds from an account.
        
        Args:
            account_id: The UUID of the account to withdraw from.
            user_id: The UUID of the user who owns the account.
            amount: The amount to withdraw.
            
        Returns:
            The updated Account entity.
            
        Raises:
            AccountNotFoundError: If the account does not exist.
            AccountAccessDeniedError: If the user doesn't own the account.
            InvalidAmountError: If the amount is not positive.
            InsufficientFundsError: If the account has insufficient funds.
        """
        logger.info(f"Processing withdrawal of {amount} from account {account_id}")
        
        if amount <= 0:
            logger.warning(f"Invalid withdrawal amount: {amount}")
            raise InvalidAmountError("Withdrawal amount must be positive")
        
        account = self.get_user_account(account_id, user_id)
        
        if account.balance < amount:
            logger.warning(f"Insufficient funds in account {account_id}. Balance: {account.balance}, Requested: {amount}")
            raise InsufficientFundsError(account_id)
        
        account.balance -= amount
        
        self._db.commit()
        self._db.refresh(account)
        logger.info(f"Successfully withdrew {amount} from account {account_id}. New balance: {account.balance}")
        return account

    def transfer(self, source_account_id: UUID, user_id: UUID, target_account_id: UUID, amount: float) -> tuple[Account, Account]:
        """Transfer funds between accounts.
        
        Args:
            source_account_id: The UUID of the source account.
            user_id: The UUID of the user who owns the source account.
            target_account_id: The UUID of the target account.
            amount: The amount to transfer.
            
        Returns:
            Tuple of (source_account, target_account) after transfer.
            
        Raises:
            AccountNotFoundError: If either account does not exist.
            AccountAccessDeniedError: If the user doesn't own the source account.
            InvalidAmountError: If the amount is not positive.
            InsufficientFundsError: If the source account has insufficient funds.
        """
        logger.info(f"Processing transfer of {amount} from account {source_account_id} to {target_account_id}")
        
        if amount <= 0:
            logger.warning(f"Invalid transfer amount: {amount}")
            raise InvalidAmountError("Transfer amount must be positive")
        
        # Get source account (verify ownership)
        source_account = self.get_user_account(source_account_id, user_id)
        
        # Get target account (no ownership check needed)
        target_account = self.get_account_by_id(target_account_id)
        
        if source_account.balance < amount:
            logger.warning(f"Insufficient funds in account {source_account_id}. Balance: {source_account.balance}, Requested: {amount}")
            raise InsufficientFundsError(source_account_id)
        
        # Perform transfer
        source_account.balance -= amount
        target_account.balance += amount
        
        self._db.commit()
        self._db.refresh(source_account)
        self._db.refresh(target_account)
        
        logger.info(f"Successfully transferred {amount} from {source_account_id} to {target_account_id}")
        return source_account, target_account

    def get_balance(self, account_id: UUID, user_id: UUID) -> model.BalanceResponse:
        """Get the balance of an account.
        
        Args:
            account_id: The UUID of the account.
            user_id: The UUID of the user who owns the account.
            
        Returns:
            BalanceResponse with account balance information.
            
        Raises:
            AccountNotFoundError: If the account does not exist.
            AccountAccessDeniedError: If the user doesn't own the account.
        """
        logger.debug(f"Fetching balance for account {account_id}")
        
        account = self.get_user_account(account_id, user_id)
        
        return model.BalanceResponse(
            account_id=account.id,
            balance=account.balance,
            currency=account.currency
        )
