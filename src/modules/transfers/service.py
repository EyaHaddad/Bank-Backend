"""Transfer services module for transfer-related operations."""

import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from . import schemas
from .exceptions import (
    TransferNotFoundError,
    BeneficiaryNotFoundError,
    BeneficiaryNotVerifiedError,
    InsufficientFundsError,
    InvalidTransferAmountError,
    TransferAccessDeniedError,
    AccountNotActiveError,
    BeneficiaryAccessDeniedError,
    TransferFailedError,
)
from src.models.transfer import Transfer
from src.models.transaction import TransactionType, TransactionStatus
from src.models.account import Account, AccountStatus
from src.models.beneficiary import Beneficiary

logger = logging.getLogger(__name__)


class TransferService:
    """Service class for transfer-related operations."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self._db = session

    def _generate_reference(self) -> str:
        """Generate a unique reference for a transfer."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        count = self._db.query(Transfer).count() + 1
        return f"TRF_{timestamp}_{count}"

    def _get_account(self, account_id: UUID) -> Account:
        """Retrieve an account by its ID."""
        account = self._db.query(Account).filter(Account.id == account_id).first()
        if not account:
            from src.modules.accounts.exceptions import AccountNotFoundError
            raise AccountNotFoundError(account_id)
        return account

    def _get_beneficiary(self, beneficiary_id: UUID) -> Beneficiary:
        """Retrieve a beneficiary by its ID."""
        beneficiary = self._db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
        if not beneficiary:
            raise BeneficiaryNotFoundError(beneficiary_id)
        return beneficiary

    def _validate_account_active(self, account: Account) -> None:
        """Validate that an account is active."""
        if account.status != AccountStatus.ACTIVE:
            raise AccountNotActiveError(account.id)

    def _validate_account_ownership(self, account: Account, user_id: UUID) -> None:
        """Validate that the user owns the account."""
        if account.user_id != user_id:
            raise TransferAccessDeniedError()

    def _validate_beneficiary_ownership(self, beneficiary: Beneficiary, user_id: UUID) -> None:
        """Validate that the user owns the beneficiary."""
        if beneficiary.user_id != user_id:
            raise BeneficiaryAccessDeniedError()

    def _validate_beneficiary_verified(self, beneficiary: Beneficiary) -> None:
        """Validate that the beneficiary is verified."""
        if not beneficiary.is_verified:
            raise BeneficiaryNotVerifiedError(beneficiary.id)

    def _validate_sufficient_funds(self, account: Account, amount: float) -> None:
        """Validate that the account has sufficient funds."""
        if account.balance < amount:
            raise InsufficientFundsError(account.id)

    def _transfer_to_response(self, transfer: Transfer) -> schemas.TransferResponse:
        """Convert a Transfer model to TransferResponse schema."""
        beneficiary = self._get_beneficiary(transfer.beneficiary_id)
        return schemas.TransferResponse(
            id=transfer.id,
            sender_account_id=transfer.sender_account_id,
            beneficiary_id=transfer.beneficiary_id,
            amount=transfer.amount,
            status=schemas.TransferStatusEnum(transfer.status.value),
            reference=transfer.reference,
            type="TRANSFER",
            created_at=transfer.created_at,
            updated_at=transfer.updated_at,
            beneficiary_name=beneficiary.name,
            beneficiary_iban=beneficiary.iban,
            beneficiary_bank=beneficiary.bank_name,
        )

    def create_transfer(self, user_id: UUID, request: schemas.TransferRequest) -> schemas.TransferResponse:
        """
        Create a new transfer from source account to beneficiary.
        
        This deducts the amount from the source account and creates a transfer record.
        """
        logger.info(f"Processing transfer of {request.amount} from account {request.sender_account_id} to beneficiary {request.beneficiary_id}")

        if request.amount <= 0:
            raise InvalidTransferAmountError("Transfer amount must be positive")

        # Get and validate source account
        source_account = self._get_account(request.sender_account_id)
        self._validate_account_ownership(source_account, user_id)
        self._validate_account_active(source_account)
        self._validate_sufficient_funds(source_account, request.amount)

        # Get and validate beneficiary
        beneficiary = self._get_beneficiary(request.beneficiary_id)
        self._validate_beneficiary_ownership(beneficiary, user_id)
        self._validate_beneficiary_verified(beneficiary)

        try:
            # Create the transfer record
            transfer = Transfer(
                sender_account_id=request.sender_account_id,
                beneficiary_id=request.beneficiary_id,
                type=TransactionType.TRANSFER,
                amount=request.amount,
                reference=request.reference or self._generate_reference(),
                status=TransactionStatus.PENDING,
            )
            self._db.add(transfer)

            # Deduct from source account
            source_account.balance -= request.amount

            # Mark transfer as completed
            transfer.status = TransactionStatus.COMPLETED

            self._db.commit()
            self._db.refresh(transfer)

            logger.info(f"Transfer {transfer.id} completed successfully")
            return self._transfer_to_response(transfer)

        except (InsufficientFundsError, InvalidTransferAmountError):
            raise
        except Exception as e:
            self._db.rollback()
            logger.error(f"Transfer failed: {str(e)}")
            raise TransferFailedError(f"Transfer failed: {str(e)}")

    def get_transfer(self, transfer_id: UUID) -> Transfer:
        """Retrieve a transfer by its ID."""
        transfer = self._db.query(Transfer).filter(Transfer.id == transfer_id).first()
        if not transfer:
            raise TransferNotFoundError(transfer_id)
        return transfer

    def get_user_transfer(self, transfer_id: UUID, user_id: UUID) -> schemas.TransferResponse:
        """Retrieve a transfer ensuring the user owns the source account."""
        transfer = self.get_transfer(transfer_id)
        account = self._get_account(transfer.sender_account_id)
        self._validate_account_ownership(account, user_id)
        return self._transfer_to_response(transfer)

    def list_transfers_by_account(
        self,
        account_id: UUID,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[TransactionStatus] = None,
    ) -> schemas.TransferListResponse:
        """List all transfers for a specific account with pagination."""
        # Validate account ownership
        account = self._get_account(account_id)
        self._validate_account_ownership(account, user_id)

        # Build query
        query = self._db.query(Transfer).filter(Transfer.sender_account_id == account_id)

        if status:
            query = query.filter(Transfer.status == status)

        # Get total count
        total = query.count()

        # Apply pagination
        transfers = (
            query.order_by(Transfer.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return schemas.TransferListResponse(
            transfers=[self._transfer_to_response(t) for t in transfers],
            total=total,
            page=page,
            page_size=page_size,
        )

    def list_user_transfers(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[TransactionStatus] = None,
    ) -> schemas.TransferListResponse:
        """List all transfers for all accounts of a user with pagination."""
        # Get all user accounts
        user_accounts = self._db.query(Account).filter(Account.user_id == user_id).all()
        account_ids = [acc.id for acc in user_accounts]

        if not account_ids:
            return schemas.TransferListResponse(
                transfers=[],
                total=0,
                page=page,
                page_size=page_size,
            )

        # Build query
        query = self._db.query(Transfer).filter(Transfer.sender_account_id.in_(account_ids))

        if status:
            query = query.filter(Transfer.status == status)

        # Get total count
        total = query.count()

        # Apply pagination
        transfers = (
            query.order_by(Transfer.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return schemas.TransferListResponse(
            transfers=[self._transfer_to_response(t) for t in transfers],
            total=total,
            page=page,
            page_size=page_size,
        )

    def get_transfer_summary(
        self,
        account_id: UUID,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> schemas.TransferSummary:
        """Get transfer summary/statistics for an account."""
        # Validate account ownership
        account = self._get_account(account_id)
        self._validate_account_ownership(account, user_id)

        # Build query
        query = self._db.query(Transfer).filter(
            Transfer.sender_account_id == account_id,
            Transfer.status == TransactionStatus.COMPLETED,
        )

        if start_date:
            query = query.filter(Transfer.created_at >= start_date)
        if end_date:
            query = query.filter(Transfer.created_at <= end_date)

        transfers = query.all()
        total_sent = sum(t.amount for t in transfers)
        transfer_count = len(transfers)
        average_transfer = total_sent / transfer_count if transfer_count > 0 else 0.0

        return schemas.TransferSummary(
            account_id=account_id,
            total_sent=total_sent,
            transfer_count=transfer_count,
            average_transfer=average_transfer,
            period_start=start_date,
            period_end=end_date,
        )

    # ==================== Beneficiary Management ====================

    def create_beneficiary(self, user_id: UUID, request: schemas.BeneficiaryCreate) -> schemas.BeneficiaryResponse:
        """Create a new beneficiary for a user."""
        logger.info(f"Creating beneficiary for user {user_id}")

        beneficiary = Beneficiary(
            user_id=user_id,
            name=request.name,
            bank_name=request.bank_name,
            iban=request.iban,
            email=request.email,
            is_verified=False,  # Beneficiaries need to be verified before use
        )
        self._db.add(beneficiary)
        self._db.commit()
        self._db.refresh(beneficiary)

        logger.info(f"Beneficiary {beneficiary.id} created successfully")
        return schemas.BeneficiaryResponse.model_validate(beneficiary)

    def get_beneficiary_for_user(self, beneficiary_id: UUID, user_id: UUID) -> schemas.BeneficiaryResponse:
        """Get a beneficiary ensuring it belongs to the user."""
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_beneficiary_ownership(beneficiary, user_id)
        return schemas.BeneficiaryResponse.model_validate(beneficiary)

    def list_beneficiaries(self, user_id: UUID) -> schemas.BeneficiaryListResponse:
        """List all beneficiaries for a user."""
        beneficiaries = self._db.query(Beneficiary).filter(Beneficiary.user_id == user_id).all()
        return schemas.BeneficiaryListResponse(
            beneficiaries=[schemas.BeneficiaryResponse.model_validate(b) for b in beneficiaries],
            total=len(beneficiaries),
        )

    def update_beneficiary(
        self, beneficiary_id: UUID, user_id: UUID, request: schemas.BeneficiaryUpdate
    ) -> schemas.BeneficiaryResponse:
        """Update a beneficiary."""
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_beneficiary_ownership(beneficiary, user_id)

        if request.name is not None:
            beneficiary.name = request.name
        if request.bank_name is not None:
            beneficiary.bank_name = request.bank_name
        if request.email is not None:
            beneficiary.email = request.email

        self._db.commit()
        self._db.refresh(beneficiary)

        logger.info(f"Beneficiary {beneficiary_id} updated successfully")
        return schemas.BeneficiaryResponse.model_validate(beneficiary)

    def delete_beneficiary(self, beneficiary_id: UUID, user_id: UUID) -> bool:
        """Delete a beneficiary."""
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_beneficiary_ownership(beneficiary, user_id)

        # Check if there are any transfers to this beneficiary
        transfer_count = self._db.query(Transfer).filter(Transfer.beneficiary_id == beneficiary_id).count()
        if transfer_count > 0:
            logger.warning(f"Cannot delete beneficiary {beneficiary_id} - has {transfer_count} transfers")
            # We still allow deletion but log the warning
            # In a real app, you might want to soft-delete instead

        self._db.delete(beneficiary)
        self._db.commit()

        logger.info(f"Beneficiary {beneficiary_id} deleted successfully")
        return True

    def verify_beneficiary(self, beneficiary_id: UUID, user_id: UUID) -> schemas.BeneficiaryResponse:
        """
        Verify a beneficiary (mark as verified).
        
        In a real application, this would involve additional verification steps
        like confirming bank details, sending a test transaction, etc.
        """
        beneficiary = self._get_beneficiary(beneficiary_id)
        self._validate_beneficiary_ownership(beneficiary, user_id)

        beneficiary.is_verified = True
        self._db.commit()
        self._db.refresh(beneficiary)

        logger.info(f"Beneficiary {beneficiary_id} verified successfully")
        return schemas.BeneficiaryResponse.model_validate(beneficiary)
