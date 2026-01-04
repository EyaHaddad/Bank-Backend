"""Transfer router - API endpoints for transfer operations."""

import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status, HTTPException

from src.modules.auth.service import CurrentUser
from src.infrastructure.database import DbSession
from src.models.transaction import TransactionStatus
from src.models.otp import OTPPurpose
from src.modules.notifications.service import send_transaction_notification_helper
from src.modules.otps.service import OTPService

from . import schemas
from .service import TransferService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transfers", tags=["Transfers"])

# In-memory store for pending transfers (in production, use Redis or database)
pending_transfers: dict[str, dict] = {}


def get_transfer_service(db: DbSession) -> TransferService:
    """Provide a transfer service bound to the current request DB session."""
    return TransferService(db)


def cleanup_expired_transfers():
    """Remove expired pending transfers."""
    now = datetime.now(timezone.utc)
    expired = [k for k, v in pending_transfers.items() if v["expires_at"] < now]
    for k in expired:
        del pending_transfers[k]


# ==================== Transfer Endpoints ====================

@router.post("/initiate", response_model=schemas.TransferInitiateResponse, status_code=status.HTTP_200_OK)
def initiate_transfer(
    request: schemas.TransferInitiateRequest,
    current_user: CurrentUser,
    db: DbSession,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferInitiateResponse:
    """
    Initiate a transfer - validates the transfer and sends OTP for confirmation.
    
    This endpoint validates the transfer details and sends an OTP to the user's email.
    The user must then call /transfers/confirm with the OTP to complete the transfer.
    """
    logger.info(f"User {current_user.user_id} initiating transfer from {request.sender_account_id}")
    
    # Cleanup expired transfers
    cleanup_expired_transfers()
    
    # Validate the transfer (but don't execute it)
    user_id = current_user.get_uuid()
    
    # Get and validate source account
    source_account = service._get_account(request.sender_account_id)
    service._validate_account_ownership(source_account, user_id)
    service._validate_account_active(source_account)
    service._validate_sufficient_funds(source_account, request.amount)
    
    # Get and validate beneficiary
    beneficiary = service._get_beneficiary(request.beneficiary_id)
    service._validate_beneficiary_ownership(beneficiary, user_id)
    service._validate_beneficiary_verified(beneficiary)
    
    # Generate OTP for transaction
    otp_service = OTPService(db)
    otp_service.create_otp(
        user_id=user_id,
        purpose=OTPPurpose.TRANSACTION,
        max_attempts=3,
        send_notification=True
    )
    
    # Generate a transfer token and store pending transfer
    transfer_token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    
    pending_transfers[transfer_token] = {
        "user_id": str(user_id),
        "sender_account_id": str(request.sender_account_id),
        "beneficiary_id": str(request.beneficiary_id),
        "amount": request.amount,
        "reference": request.reference,
        "expires_at": expires_at,
        "beneficiary_name": beneficiary.name,
    }
    
    logger.info(f"Transfer initiated for user {user_id}, token: {transfer_token[:8]}...")
    
    return schemas.TransferInitiateResponse(
        message="Transfer initiated. Please verify with the OTP sent to your email.",
        transfer_token=transfer_token,
        expires_at=expires_at,
        amount=request.amount,
        beneficiary_name=beneficiary.name,
    )


@router.post("/confirm", response_model=schemas.TransferResponse, status_code=status.HTTP_201_CREATED)
def confirm_transfer(
    transfer_token: str,
    otp_code: str,
    current_user: CurrentUser,
    db: DbSession,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferResponse:
    """
    Confirm and execute a transfer using OTP verification.
    
    Requires the transfer_token from /transfers/initiate and the OTP code.
    """
    logger.info(f"User {current_user.user_id} confirming transfer")
    
    # Cleanup expired transfers
    cleanup_expired_transfers()
    
    # Get pending transfer
    pending = pending_transfers.get(transfer_token)
    if not pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired transfer token. Please initiate a new transfer."
        )
    
    # Verify ownership
    if pending["user_id"] != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to confirm this transfer."
        )
    
    # Verify OTP
    otp_service = OTPService(db)
    otp_result = otp_service.verify_user_otp_response(
        user_id=current_user.get_uuid(),
        code=otp_code,
        purpose=OTPPurpose.TRANSACTION
    )
    
    if not otp_result.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=otp_result.message
        )
    
    # Execute the transfer
    transfer_request = schemas.TransferRequest(
        sender_account_id=UUID(pending["sender_account_id"]),
        beneficiary_id=UUID(pending["beneficiary_id"]),
        amount=pending["amount"],
        reference=pending["reference"],
    )
    
    transfer = service.create_transfer(current_user.get_uuid(), transfer_request)
    
    # Remove pending transfer
    del pending_transfers[transfer_token]
    
    # Send notification
    try:
        send_transaction_notification_helper(
            db=db,
            user_id=current_user.get_uuid(),
            transaction_type="transfer",
            amount=pending["amount"],
            reference=transfer.reference,
        )
    except Exception as e:
        logger.warning(f"Failed to send transfer notification: {str(e)}")
    
    logger.info(f"Transfer confirmed and executed for user {current_user.user_id}")
    return transfer


@router.post("/", response_model=schemas.TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(
    request: schemas.TransferRequest,
    current_user: CurrentUser,
    db: DbSession,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferResponse:
    """
    Create a new transfer to a beneficiary (without OTP - for backward compatibility).
    
    This endpoint allows the authenticated user to transfer money from their account
    to a verified beneficiary. For enhanced security, use /transfers/initiate instead.
    """
    logger.info(f"User {current_user.user_id} requesting transfer from {request.sender_account_id} to beneficiary {request.beneficiary_id}")
    transfer = service.create_transfer(current_user.get_uuid(), request)
    
    # Send notification
    try:
        send_transaction_notification_helper(
            db=db,
            user_id=current_user.get_uuid(),
            transaction_type="transfer",
            amount=request.amount,
            reference=transfer.reference,
        )
    except Exception as e:
        logger.warning(f"Failed to send transfer notification: {str(e)}")
    
    return transfer


@router.get("/{transfer_id}", response_model=schemas.TransferResponse)
def get_transfer(
    transfer_id: UUID,
    current_user: CurrentUser,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferResponse:
    """
    Get a specific transfer by ID.
    
    The user must own the source account associated with the transfer.
    """
    logger.debug(f"User {current_user.user_id} fetching transfer {transfer_id}")
    return service.get_user_transfer(transfer_id, current_user.get_uuid())


@router.get("/account/{account_id}", response_model=schemas.TransferListResponse)
def list_account_transfers(
    account_id: UUID,
    current_user: CurrentUser,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    transfer_status: Optional[str] = Query(None, description="Filter by status (PENDING, COMPLETED, FAILED)"),
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferListResponse:
    """
    List all transfers for a specific account with pagination.
    
    The user must own the account to view its transfers.
    """
    logger.debug(f"User {current_user.user_id} listing transfers for account {account_id}")
    
    status_filter = TransactionStatus(transfer_status) if transfer_status else None
    
    return service.list_transfers_by_account(
        account_id=account_id,
        user_id=current_user.get_uuid(),
        page=page,
        page_size=page_size,
        status=status_filter,
    )


@router.get("/", response_model=schemas.TransferListResponse)
def list_my_transfers(
    current_user: CurrentUser,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    transfer_status: Optional[str] = Query(None, description="Filter by status (PENDING, COMPLETED, FAILED)"),
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferListResponse:
    """
    List all transfers for the current user across all their accounts.
    
    Supports pagination and optional status filter.
    """
    logger.debug(f"User {current_user.user_id} listing all their transfers")
    
    status_filter = TransactionStatus(transfer_status) if transfer_status else None
    
    return service.list_user_transfers(
        user_id=current_user.get_uuid(),
        page=page,
        page_size=page_size,
        status=status_filter,
    )


@router.get("/account/{account_id}/summary", response_model=schemas.TransferSummary)
def get_transfer_summary(
    account_id: UUID,
    current_user: CurrentUser,
    start_date: Optional[datetime] = Query(None, description="Start date for summary period"),
    end_date: Optional[datetime] = Query(None, description="End date for summary period"),
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferSummary:
    """
    Get transfer summary/statistics for a specific account.
    
    Optionally filter by date range.
    """
    logger.debug(f"User {current_user.user_id} getting transfer summary for account {account_id}")
    return service.get_transfer_summary(
        account_id=account_id,
        user_id=current_user.get_uuid(),
        start_date=start_date,
        end_date=end_date,
    )


# ==================== Beneficiary Endpoints ====================

@router.post("/beneficiaries", response_model=schemas.BeneficiaryResponse, status_code=status.HTTP_201_CREATED)
def create_beneficiary(
    request: schemas.BeneficiaryCreate,
    current_user: CurrentUser,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.BeneficiaryResponse:
    """
    Create a new beneficiary.
    
    The beneficiary will need to be verified before transfers can be made to it.
    """
    logger.info(f"User {current_user.user_id} creating new beneficiary")
    return service.create_beneficiary(current_user.get_uuid(), request)


@router.get("/beneficiaries", response_model=schemas.BeneficiaryListResponse)
def list_beneficiaries(
    current_user: CurrentUser,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.BeneficiaryListResponse:
    """
    List all beneficiaries for the current user.
    """
    logger.debug(f"User {current_user.user_id} listing beneficiaries")
    return service.list_beneficiaries(current_user.get_uuid())


@router.get("/beneficiaries/{beneficiary_id}", response_model=schemas.BeneficiaryResponse)
def get_beneficiary(
    beneficiary_id: UUID,
    current_user: CurrentUser,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.BeneficiaryResponse:
    """
    Get a specific beneficiary by ID.
    """
    logger.debug(f"User {current_user.user_id} fetching beneficiary {beneficiary_id}")
    return service.get_beneficiary_for_user(beneficiary_id, current_user.get_uuid())


@router.put("/beneficiaries/{beneficiary_id}", response_model=schemas.BeneficiaryResponse)
def update_beneficiary(
    beneficiary_id: UUID,
    request: schemas.BeneficiaryUpdate,
    current_user: CurrentUser,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.BeneficiaryResponse:
    """
    Update a beneficiary.
    
    Note: Updating a beneficiary may require re-verification.
    """
    logger.info(f"User {current_user.user_id} updating beneficiary {beneficiary_id}")
    return service.update_beneficiary(beneficiary_id, current_user.get_uuid(), request)


@router.delete("/beneficiaries/{beneficiary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_beneficiary(
    beneficiary_id: UUID,
    current_user: CurrentUser,
    service: TransferService = Depends(get_transfer_service),
):
    """
    Delete a beneficiary.
    
    Note: This will not delete associated transfer history.
    """
    logger.info(f"User {current_user.user_id} deleting beneficiary {beneficiary_id}")
    service.delete_beneficiary(beneficiary_id, current_user.get_uuid())


@router.post("/beneficiaries/{beneficiary_id}/verify", response_model=schemas.BeneficiaryResponse)
def verify_beneficiary(
    beneficiary_id: UUID,
    current_user: CurrentUser,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.BeneficiaryResponse:
    """
    Verify a beneficiary.
    
    In a production environment, this would involve additional verification steps.
    For now, this simply marks the beneficiary as verified.
    """
    logger.info(f"User {current_user.user_id} verifying beneficiary {beneficiary_id}")
    return service.verify_beneficiary(beneficiary_id, current_user.get_uuid())

