"""Beneficiary router - API endpoints for beneficiary operations."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.modules.auth.service import CurrentUser
from src.infrastructure.database import DbSession

from . import schemas
from .service import BeneficiaryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/beneficiaries", tags=["Beneficiaries"])


def get_beneficiary_service(db: DbSession) -> BeneficiaryService:
    """Provide a beneficiary service bound to the current request DB session."""
    return BeneficiaryService(db)


@router.post("/", response_model=schemas.BeneficiaryResponse, status_code=status.HTTP_201_CREATED)
def create_beneficiary(
    request: schemas.BeneficiaryCreate,
    current_user: CurrentUser,
    service: BeneficiaryService = Depends(get_beneficiary_service),
) -> schemas.BeneficiaryResponse:
    """
    Create a new beneficiary.
    
    The beneficiary will need to be verified before transfers can be made to it.
    """
    logger.info(f"User {current_user.user_id} creating new beneficiary")
    return service.create_beneficiary(current_user.get_uuid(), request)


@router.get("/", response_model=schemas.BeneficiaryListResponse)
def list_beneficiaries(
    current_user: CurrentUser,
    verified_only: bool = Query(False, description="Only return verified beneficiaries"),
    service: BeneficiaryService = Depends(get_beneficiary_service),
) -> schemas.BeneficiaryListResponse:
    """
    List all beneficiaries for the current user.
    
    Optionally filter to show only verified beneficiaries.
    """
    logger.debug(f"User {current_user.user_id} listing beneficiaries")
    return service.list_beneficiaries(current_user.get_uuid(), verified_only)


@router.get("/{beneficiary_id}", response_model=schemas.BeneficiaryResponse)
def get_beneficiary(
    beneficiary_id: UUID,
    current_user: CurrentUser,
    service: BeneficiaryService = Depends(get_beneficiary_service),
) -> schemas.BeneficiaryResponse:
    """
    Get a specific beneficiary by ID.
    """
    logger.debug(f"User {current_user.user_id} fetching beneficiary {beneficiary_id}")
    return service.get_beneficiary(beneficiary_id, current_user.get_uuid())


@router.put("/{beneficiary_id}", response_model=schemas.BeneficiaryResponse)
def update_beneficiary(
    beneficiary_id: UUID,
    request: schemas.BeneficiaryUpdate,
    current_user: CurrentUser,
    service: BeneficiaryService = Depends(get_beneficiary_service),
) -> schemas.BeneficiaryResponse:
    """
    Update a beneficiary.
    
    Note: Updating critical fields may require re-verification in a production environment.
    """
    logger.info(f"User {current_user.user_id} updating beneficiary {beneficiary_id}")
    return service.update_beneficiary(beneficiary_id, current_user.get_uuid(), request)


@router.delete("/{beneficiary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_beneficiary(
    beneficiary_id: UUID,
    current_user: CurrentUser,
    service: BeneficiaryService = Depends(get_beneficiary_service),
):
    """
    Delete a beneficiary.
    
    Note: This will not delete associated transfer history.
    """
    logger.info(f"User {current_user.user_id} deleting beneficiary {beneficiary_id}")
    service.delete_beneficiary(beneficiary_id, current_user.get_uuid())


@router.post("/{beneficiary_id}/verify", response_model=schemas.BeneficiaryResponse)
def verify_beneficiary(
    beneficiary_id: UUID,
    current_user: CurrentUser,
    service: BeneficiaryService = Depends(get_beneficiary_service),
) -> schemas.BeneficiaryResponse:
    """
    Verify a beneficiary.
    
    In a production environment, this would involve additional verification steps
    such as confirming bank details or sending a test micro-transaction.
    """
    logger.info(f"User {current_user.user_id} verifying beneficiary {beneficiary_id}")
    return service.verify_beneficiary(beneficiary_id, current_user.get_uuid())


@router.post("/{beneficiary_id}/unverify", response_model=schemas.BeneficiaryResponse)
def unverify_beneficiary(
    beneficiary_id: UUID,
    current_user: CurrentUser,
    service: BeneficiaryService = Depends(get_beneficiary_service),
) -> schemas.BeneficiaryResponse:
    """
    Unverify a beneficiary.
    
    This removes the verified status, requiring re-verification before transfers.
    """
    logger.info(f"User {current_user.user_id} unverifying beneficiary {beneficiary_id}")
    return service.unverify_beneficiary(beneficiary_id, current_user.get_uuid())
