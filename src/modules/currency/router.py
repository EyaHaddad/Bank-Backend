"""Currency exchange router - API endpoints for currency operations."""

import logging
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE, HTTP_400_BAD_REQUEST

from . import schemas
from . import service
from src.modules.auth.service import get_current_user, TokenData

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/rates", response_model=schemas.ExchangeRatesResponse, status_code=HTTP_200_OK)
async def get_exchange_rates(current_user: TokenData = Depends(get_current_user)):
    """
    Get current exchange rates with TND as base currency.
    Returns rates for EUR, USD, GBP, MAD, SAR.
    Only accessible by authenticated users (clients).
    """
    rates = await service.fetch_exchange_rates()
    
    if rates is None:
        raise HTTPException(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch exchange rates. Please try again later."
        )
    
    return rates


@router.post("/convert", response_model=schemas.ConversionResponse, status_code=HTTP_200_OK)
async def convert_currency(
    request: schemas.ConversionRequest,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Convert an amount from TND to a target currency.
    Supported currencies: EUR, USD, GBP, MAD, SAR.
    """
    # Validate target currency
    supported_currencies = ["EUR", "USD", "GBP", "MAD", "SAR"]
    if request.target_currency.upper() not in supported_currencies:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Unsupported currency. Supported currencies: {', '.join(supported_currencies)}"
        )
    
    result = await service.convert_currency(request)
    
    if result is None:
        raise HTTPException(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to perform conversion. Please try again later."
        )
    
    return result


@router.get("/contact", response_model=schemas.BankContactInfo, status_code=HTTP_200_OK)
async def get_bank_contact(current_user: TokenData = Depends(get_current_user)):
    """
    Get bank contact information.
    Only accessible by authenticated users (clients).
    """
    return service.get_bank_contact_info()
