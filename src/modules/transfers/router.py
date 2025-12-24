"""Transfer router - API endpoints for transfer operations."""

import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.modules.auth.service import CurrentUser
from src.infrastructure.database import DbSession
from src.models.transaction import TransactionStatus
from src.modules.notifications.service import send_transaction_notification_helper

from . import schemas
from .service import TransferService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transfers", tags=["Transfers"])


def get_transfer_service(db: DbSession) -> TransferService:
    """Provide a transfer service bound to the current request DB session."""
    return TransferService(db)


# ==================== Transfer Endpoints ====================

@router.post("/", response_model=schemas.TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer(
    request: schemas.TransferRequest,
    current_user: CurrentUser,
    db: DbSession,
    service: TransferService = Depends(get_transfer_service),
) -> schemas.TransferResponse:
    """
    Create a new transfer to a beneficiary.
    
    This endpoint allows the authenticated user to transfer money from their account
    to a verified beneficiary.
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

