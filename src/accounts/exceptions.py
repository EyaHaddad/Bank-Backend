"""Exceptions for accounts module."""

from fastapi import HTTPException


class AccountError(HTTPException):
    """Base exception for account-related errors."""
    pass


class AccountNotFoundError(AccountError):
    """Exception raised when an account is not found."""

    def __init__(self, account_id=None):
        message = "Account not found" if account_id is None else f"Account with id {account_id} not found"
        super().__init__(status_code=404, detail=message)


class InsufficientFundsError(AccountError):
    """Exception raised when there are insufficient funds for a transaction."""

    def __init__(self, account_id=None):
        message = "Insufficient funds" if account_id is None else f"Insufficient funds in account {account_id}"
        super().__init__(status_code=400, detail=message)


class InvalidAmountError(AccountError):
    """Exception raised when an invalid amount is provided."""

    def __init__(self, message: str = "Amount must be positive"):
        super().__init__(status_code=400, detail=message)


class AccountAccessDeniedError(AccountError):
    """Exception raised when user tries to access an account they don't own."""

    def __init__(self):
        super().__init__(status_code=403, detail="Access denied to this account")


class DuplicateAccountError(AccountError):
    """Exception raised when trying to create a duplicate account."""

    def __init__(self, message: str = "Account already exists"):
        super().__init__(status_code=409, detail=message)
