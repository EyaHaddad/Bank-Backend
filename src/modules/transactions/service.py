"""Transaction services module for transaction-related operations."""

import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func

from . import schemas
from .exceptions import (
    TransactionNotFoundError,
    InsufficientFundsError,
    InvalidTransactionAmountError,
    TransactionAccessDeniedError,
    AccountNotActiveError,
    TransactionFailedError,
)
from src.models.transaction import Transaction, TransactionType, TransactionStatus
from src.models.account import Account, AccountStatus

logger = logging.getLogger(__name__)


class TransactionService:
    """Service class for transaction-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    def _generate_reference(self, transaction_type: TransactionType) -> str:
        """Generate a unique reference for a transaction."""
        prefix = "TR" if transaction_type == TransactionType.TRANSFER else (
            "CR" if transaction_type == TransactionType.CREDIT else "DB"
        )
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        count = self._db.query(Transaction).count() + 1
        return f"{prefix}_{timestamp}_{count}"

    def _get_account(self, account_id: UUID) -> Account:
        """Retrieve an account by its ID."""
        account = self._db.query(Account).filter(Account.id == account_id).first()
        if not account:
            from src.modules.accounts.exceptions import AccountNotFoundError
            raise AccountNotFoundError(account_id)
        return account

    def _validate_account_active(self, account: Account) -> None:
        """Validate that an account is active."""
        if account.status != AccountStatus.ACTIVE:
            raise AccountNotActiveError(account.id)

    def _validate_ownership(self, account: Account, user_id: UUID) -> None:
        """Validate that the user owns the account."""
        if account.user_id != user_id:
            raise TransactionAccessDeniedError()

    def _validate_sufficient_funds(self, account: Account, amount: float) -> None:
        """Validate that the account has sufficient funds."""
        if account.balance < amount:
            raise InsufficientFundsError(account.id)

    def credit(self, user_id: UUID, request: schemas.CreditRequest) -> Transaction:
        """
        Credit (deposit) money to an account.
        Creates a CREDIT transaction and increases the account balance.
        """
        logger.info(f"Processing credit of {request.amount} to account {request.account_id}")
        
        if request.amount <= 0:
            raise InvalidTransactionAmountError("Credit amount must be positive")

        # Get and validate account
        account = self._get_account(request.account_id)
        self._validate_ownership(account, user_id)
        self._validate_account_active(account)

        try:
            # Create the transaction
            transaction = Transaction(
                sender_account_id=request.account_id,
                type=TransactionType.CREDIT,
                amount=request.amount,
                reference=request.reference or self._generate_reference(TransactionType.CREDIT),
                status=TransactionStatus.PENDING,
            )
            self._db.add(transaction)

            # Update account balance
            account.balance += request.amount

            # Mark transaction as completed
            transaction.status = TransactionStatus.COMPLETED

            self._db.commit()
            self._db.refresh(transaction)

            logger.info(f"Credit transaction {transaction.id} completed successfully")
            return transaction

        except Exception as e:
            self._db.rollback()
            logger.error(f"Credit transaction failed: {str(e)}")
            raise TransactionFailedError(f"Credit transaction failed: {str(e)}")

    def debit(self, user_id: UUID, request: schemas.DebitRequest) -> Transaction:
        """
        Debit (withdraw) money from an account.
        Creates a DEBIT transaction and decreases the account balance.
        """
        logger.info(f"Processing debit of {request.amount} from account {request.account_id}")

        if request.amount <= 0:
            raise InvalidTransactionAmountError("Debit amount must be positive")

        # Get and validate account
        account = self._get_account(request.account_id)
        self._validate_ownership(account, user_id)
        self._validate_account_active(account)
        self._validate_sufficient_funds(account, request.amount)

        try:
            # Create the transaction
            transaction = Transaction(
                sender_account_id=request.account_id,
                type=TransactionType.DEBIT,
                amount=request.amount,
                reference=request.reference or self._generate_reference(TransactionType.DEBIT),
                status=TransactionStatus.PENDING,
            )
            self._db.add(transaction)

            # Update account balance
            account.balance -= request.amount

            # Mark transaction as completed
            transaction.status = TransactionStatus.COMPLETED

            self._db.commit()
            self._db.refresh(transaction)

            logger.info(f"Debit transaction {transaction.id} completed successfully")
            return transaction

        except InsufficientFundsError:
            raise
        except Exception as e:
            self._db.rollback()
            logger.error(f"Debit transaction failed: {str(e)}")
            raise TransactionFailedError(f"Debit transaction failed: {str(e)}")

    def get_transaction(self, transaction_id: UUID) -> Transaction:
        """Retrieve a transaction by its ID."""
        transaction = self._db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise TransactionNotFoundError(transaction_id)
        return transaction

    def get_user_transaction(self, transaction_id: UUID, user_id: UUID) -> Transaction:
        """Retrieve a transaction ensuring the user owns the associated account."""
        transaction = self.get_transaction(transaction_id)
        account = self._get_account(transaction.sender_account_id)
        self._validate_ownership(account, user_id)
        return transaction

    def list_transactions_by_account(
        self,
        account_id: UUID,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        transaction_type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None,
    ) -> schemas.TransactionListResponse:
        """List all transactions for a specific account with pagination and filters."""
        # Validate account ownership
        account = self._get_account(account_id)
        self._validate_ownership(account, user_id)

        # Build query
        query = self._db.query(Transaction).filter(Transaction.sender_account_id == account_id)

        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)
        if status:
            query = query.filter(Transaction.status == status)

        # Get total count
        total = query.count()

        # Apply pagination
        transactions = (
            query.order_by(Transaction.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return schemas.TransactionListResponse(
            transactions=[schemas.TransactionResponse.model_validate(t) for t in transactions],
            total=total,
            page=page,
            page_size=page_size,
        )

    def list_user_transactions(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        transaction_type: Optional[TransactionType] = None,
        status: Optional[TransactionStatus] = None,
    ) -> schemas.TransactionListResponse:
        """List all transactions for all accounts of a user with pagination and filters."""
        # Get all user accounts
        user_accounts = self._db.query(Account).filter(Account.user_id == user_id).all()
        account_ids = [acc.id for acc in user_accounts]

        if not account_ids:
            return schemas.TransactionListResponse(
                transactions=[],
                total=0,
                page=page,
                page_size=page_size,
            )

        # Build query
        query = self._db.query(Transaction).filter(Transaction.sender_account_id.in_(account_ids))

        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)
        if status:
            query = query.filter(Transaction.status == status)

        # Get total count
        total = query.count()

        # Apply pagination
        transactions = (
            query.order_by(Transaction.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return schemas.TransactionListResponse(
            transactions=[schemas.TransactionResponse.model_validate(t) for t in transactions],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_transaction_summary(
        self,
        account_id: UUID,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> schemas.TransactionSummary:
        """Get transaction summary/statistics for an account."""
        # Validate account ownership
        account = self._get_account(account_id)
        self._validate_ownership(account, user_id)

        # Build base query
        query = self._db.query(Transaction).filter(
            Transaction.sender_account_id == account_id,
            Transaction.status == TransactionStatus.COMPLETED,
        )

        if start_date:
            query = query.filter(Transaction.created_at >= start_date)
        if end_date:
            query = query.filter(Transaction.created_at <= end_date)

        # Calculate totals
        transactions = query.all()
        
        total_credits = sum(t.amount for t in transactions if t.type == TransactionType.CREDIT)
        total_debits = sum(t.amount for t in transactions if t.type == TransactionType.DEBIT)
        total_transfers = sum(t.amount for t in transactions if t.type == TransactionType.TRANSFER)

        return schemas.TransactionSummary(
            account_id=account_id,
            total_credits=total_credits,
            total_debits=total_debits,
            total_transfers_sent=total_transfers,
            transaction_count=len(transactions),
            period_start=start_date,
            period_end=end_date,
        )

