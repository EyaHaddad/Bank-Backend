"""OTP router module for OTP-related endpoints."""

from uuid import UUID
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.database.session import DbSession
from src.modules.auth.service import get_current_user
from src.models.user import User
from src.models.otp import OTPPurpose
from . import schemas
from .service import OTPService, OTPMessages

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/otp",
    tags=["OTP"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/generate",
    response_model=schemas.OTPGenerateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a new OTP",
    description="Generate a new OTP for the authenticated user for a specific purpose.",
)
async def generate_otp(
    request: schemas.OTPGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(DbSession),
):
    """Generate a new OTP for the authenticated user."""
    logger.info(f"OTP generation requested by user {current_user.id} for purpose {request.purpose}")
    
    otp_service = OTPService(db)
    return otp_service.generate_otp_response(current_user.id, request.purpose)


@router.post(
    "/verify",
    response_model=schemas.OTPVerifyResponse,
    summary="Verify an OTP",
    description="Verify an OTP code for the authenticated user.",
)
async def verify_otp(
    request: schemas.OTPVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(DbSession),
):
    """Verify an OTP code for the authenticated user."""
    logger.info(f"OTP verification requested by user {current_user.id} for purpose {request.purpose}")
    
    otp_service = OTPService(db)
    result = otp_service.verify_user_otp_response(current_user.id, request.code, request.purpose)
    
    if not result.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.message,
        )
    
    return result


@router.get(
    "/history",
    response_model=list[schemas.OTPResponse],
    summary="Get OTP history",
    description="Retrieve recent OTPs for the authenticated user.",
)
async def get_otp_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(DbSession),
):
    """Retrieve recent OTPs for the authenticated user."""
    logger.info(f"OTP history requested by user {current_user.id}")
    
    otp_service = OTPService(db)
    otps = otp_service.get_user_otps(current_user.id, limit)
    
    return otps


@router.get(
    "/active/{purpose}",
    response_model=schemas.OTPResponse | None,
    summary="Get active OTP",
    description="Get the current active OTP for a specific purpose.",
)
async def get_active_otp(
    purpose: OTPPurpose,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(DbSession),
):
    """Get the current active OTP for a specific purpose."""
    logger.info(f"Active OTP requested by user {current_user.id} for purpose {purpose}")
    
    otp_service = OTPService(db)
    otp = otp_service.get_active_otp(current_user.id, purpose)
    
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active OTP found for this purpose",
        )
    
    return otp
