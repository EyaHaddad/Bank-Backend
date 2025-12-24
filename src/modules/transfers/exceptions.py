"""Exceptions for transfers module."""

from fastapi import HTTPException


class TransferError(HTTPException):
    """Base exception for transfer-related errors."""
    pass


class TransferNotFoundError(TransferError):
    """Exception raised when a transfer is not found."""

    def __init__(self, transfer_id=None):
        message = "Transfer not found" if transfer_id is None else f"Transfer with id {transfer_id} not found"
        super().__init__(status_code=404, detail=message)


class BeneficiaryNotFoundError(TransferError):
    """Exception raised when a beneficiary is not found."""

    def __init__(self, beneficiary_id=None):
        message = "Beneficiary not found" if beneficiary_id is None else f"Beneficiary with id {beneficiary_id} not found"
        super().__init__(status_code=404, detail=message)


class BeneficiaryNotVerifiedError(TransferError):
    """Exception raised when trying to transfer to an unverified beneficiary."""

    def __init__(self, beneficiary_id=None):
        message = "Beneficiary is not verified" if beneficiary_id is None else f"Beneficiary {beneficiary_id} is not verified"
        super().__init__(status_code=400, detail=message)


class InsufficientFundsError(TransferError):
    """Exception raised when there are insufficient funds for a transfer."""

    def __init__(self, account_id=None):
        message = "Insufficient funds" if account_id is None else f"Insufficient funds in account {account_id}"
        super().__init__(status_code=400, detail=message)


class InvalidTransferAmountError(TransferError):
    """Exception raised when an invalid amount is provided."""

    def __init__(self, message: str = "Transfer amount must be positive"):
        super().__init__(status_code=400, detail=message)


class TransferAccessDeniedError(TransferError):
    """Exception raised when user tries to access a transfer they don't own."""

    def __init__(self):
        super().__init__(status_code=403, detail="Access denied to this transfer")


class AccountNotActiveError(TransferError):
    """Exception raised when trying to perform a transfer from a non-active account."""

    def __init__(self, account_id=None):
        message = "Account is not active" if account_id is None else f"Account {account_id} is not active"
        super().__init__(status_code=400, detail=message)


class BeneficiaryAccessDeniedError(TransferError):
    """Exception raised when user tries to use a beneficiary they don't own."""

    def __init__(self):
        super().__init__(status_code=403, detail="Access denied to this beneficiary")


class TransferFailedError(TransferError):
    """Exception raised when a transfer fails to process."""

    def __init__(self, message: str = "Transfer failed to process"):
        super().__init__(status_code=500, detail=message)


class SameAccountTransferError(TransferError):
    """Exception raised when trying to transfer to the same account."""

    def __init__(self):
        super().__init__(status_code=400, detail="Cannot transfer to the same account")
