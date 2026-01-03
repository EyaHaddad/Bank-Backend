"""Currency exchange schemas."""

from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime


class CurrencyRate(BaseModel):
    """Schema for a single currency rate."""
    code: str = Field(..., description="Currency code (e.g., EUR, USD)")
    name: str = Field(..., description="Currency name")
    rate: float = Field(..., description="Exchange rate from TND")
    flag: str = Field(..., description="Currency flag emoji")


class ExchangeRatesResponse(BaseModel):
    """Schema for exchange rates response."""
    base_currency: str = Field(default="TND", description="Base currency code")
    base_currency_name: str = Field(default="Tunisian Dinar", description="Base currency name")
    last_updated: str = Field(..., description="Last update timestamp")
    rates: list[CurrencyRate] = Field(..., description="List of currency rates")


class ConversionRequest(BaseModel):
    """Schema for currency conversion request."""
    amount: float = Field(..., gt=0, description="Amount to convert")
    target_currency: str = Field(..., description="Target currency code")


class ConversionResponse(BaseModel):
    """Schema for currency conversion response."""
    original_amount: float = Field(..., description="Original amount in TND")
    converted_amount: float = Field(..., description="Converted amount")
    target_currency: str = Field(..., description="Target currency code")
    rate: float = Field(..., description="Exchange rate used")
    base_currency: str = Field(default="TND", description="Base currency")


class BankContactInfo(BaseModel):
    """Schema for bank contact information."""
    bank_name: str = Field(..., description="Name of the bank")
    address: str = Field(..., description="Bank address")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")
    postal_code: str = Field(..., description="Postal code")
    phone: str = Field(..., description="Phone number")
    fax: str = Field(..., description="Fax number")
    email: str = Field(..., description="Email address")
    website: str = Field(..., description="Website URL")
    working_hours: str = Field(..., description="Working hours")
    swift_code: str = Field(..., description="SWIFT/BIC code")
