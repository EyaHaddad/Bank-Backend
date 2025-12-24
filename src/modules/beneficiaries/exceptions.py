"""Exceptions for beneficiaries module."""

from fastapi import HTTPException


class BeneficiaryError(HTTPException):
    """Base exception for beneficiary-related errors."""
    pass


class BeneficiaryNotFoundError(BeneficiaryError):
    """Exception raised when a beneficiary is not found."""

    def __init__(self, beneficiary_id=None):
        message = "Beneficiary not found" if beneficiary_id is None else f"Beneficiary with id {beneficiary_id} not found"
        super().__init__(status_code=404, detail=message)


class BeneficiaryNotVerifiedError(BeneficiaryError):
    """Exception raised when trying to use an unverified beneficiary."""

    def __init__(self, beneficiary_id=None):
        message = "Beneficiary is not verified" if beneficiary_id is None else f"Beneficiary {beneficiary_id} is not verified"
        super().__init__(status_code=400, detail=message)


class BeneficiaryAccessDeniedError(BeneficiaryError):
    """Exception raised when user tries to access a beneficiary they don't own."""

    def __init__(self):
        super().__init__(status_code=403, detail="Access denied to this beneficiary")


class DuplicateBeneficiaryError(BeneficiaryError):
    """Exception raised when trying to create a duplicate beneficiary."""

    def __init__(self, iban: str = None):
        message = "Beneficiary with this IBAN already exists" if iban else "Beneficiary already exists"
        super().__init__(status_code=409, detail=message)
