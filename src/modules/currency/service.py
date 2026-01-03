"""Currency exchange service - handles API calls and business logic."""

import logging
import httpx
from typing import Optional
from datetime import datetime
from .schemas import (
    CurrencyRate, 
    ExchangeRatesResponse, 
    ConversionRequest, 
    ConversionResponse,
    BankContactInfo
)

logger = logging.getLogger(__name__)

# External API configuration
CURRENCY_API_BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1"

# Supported currencies for display (with TND as base)
SUPPORTED_CURRENCIES = {
    "eur": {"name": "Euro", "flag": "🇪🇺"},
    "usd": {"name": "US Dollar", "flag": "🇺🇸"},
    "gbp": {"name": "British Pound", "flag": "🇬🇧"},
    "mad": {"name": "Moroccan Dirham", "flag": "🇲🇦"},
    "sar": {"name": "Saudi Riyal", "flag": "🇸🇦"},
}

# Bank contact information (can be moved to config/database later)
BANK_CONTACT_INFO = BankContactInfo(
    bank_name="BankFlow Tunisia",
    address="Avenue Habib Bourguiba, Immeuble BankFlow",
    city="Tunis",
    country="Tunisie",
    postal_code="1000",
    phone="+216 71 123 456",
    fax="+216 71 123 457",
    email="contact@bankflow.tn",
    website="https://www.bankflow.tn",
    working_hours="Lundi - Vendredi: 08:00 - 17:00, Samedi: 08:00 - 12:00",
    swift_code="BKFLTNTT"
)


async def fetch_exchange_rates() -> Optional[ExchangeRatesResponse]:
    """
    Fetch exchange rates from external API with TND as base currency.
    Returns rates for EUR, USD, GBP, MAD, SAR only.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Fetch TND rates from the external API
            response = await client.get(f"{CURRENCY_API_BASE_URL}/currencies/tnd.json")
            response.raise_for_status()
            
            data = response.json()
            tnd_rates = data.get("tnd", {})
            
            # Build response with only supported currencies
            rates = []
            for currency_code, info in SUPPORTED_CURRENCIES.items():
                if currency_code in tnd_rates:
                    rate = tnd_rates[currency_code]
                    rates.append(CurrencyRate(
                        code=currency_code.upper(),
                        name=info["name"],
                        rate=round(rate, 6),
                        flag=info["flag"]
                    ))
            
            return ExchangeRatesResponse(
                base_currency="TND",
                base_currency_name="Tunisian Dinar",
                last_updated=datetime.now().isoformat(),
                rates=rates
            )
            
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching exchange rates: {e.response.status_code}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Request error fetching exchange rates: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching exchange rates: {str(e)}")
        return None


async def convert_currency(request: ConversionRequest) -> Optional[ConversionResponse]:
    """
    Convert an amount from TND to a target currency.
    """
    target_code = request.target_currency.lower()
    
    if target_code not in SUPPORTED_CURRENCIES:
        logger.warning(f"Unsupported currency requested: {target_code}")
        return None
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Fetch TND rates
            response = await client.get(f"{CURRENCY_API_BASE_URL}/currencies/tnd.json")
            response.raise_for_status()
            
            data = response.json()
            tnd_rates = data.get("tnd", {})
            
            if target_code not in tnd_rates:
                logger.error(f"Rate not found for currency: {target_code}")
                return None
            
            rate = tnd_rates[target_code]
            converted_amount = request.amount * rate
            
            return ConversionResponse(
                original_amount=request.amount,
                converted_amount=round(converted_amount, 2),
                target_currency=request.target_currency.upper(),
                rate=round(rate, 6),
                base_currency="TND"
            )
            
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during conversion: {e.response.status_code}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Request error during conversion: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during conversion: {str(e)}")
        return None


def get_bank_contact_info() -> BankContactInfo:
    """
    Get bank contact information.
    """
    return BANK_CONTACT_INFO
