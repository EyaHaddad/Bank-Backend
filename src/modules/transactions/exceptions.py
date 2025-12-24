"""Exceptions for transactions module."""

from fastapi import HTTPException


class TransactionError(HTTPException):
    """Base exception for transaction-related errors."""
    pass


class TransactionNotFoundError(TransactionError):
    """Exception raised when a transaction is not found."""

    def __init__(self, transaction_id=None):
        message = "Transaction not found" if transaction_id is None else f"Transaction with id {transaction_id} not found"
        super().__init__(status_code=404, detail=message)


class InsufficientFundsError(TransactionError):
    """Exception raised when there are insufficient funds for a transaction."""

    def __init__(self, account_id=None):
        message = "Insufficient funds" if account_id is None else f"Insufficient funds in account {account_id}"
        super().__init__(status_code=400, detail=message)


class InvalidTransactionAmountError(TransactionError):
    """Exception raised when an invalid amount is provided."""

    def __init__(self, message: str = "Transaction amount must be positive"):
        super().__init__(status_code=400, detail=message)


class TransactionAccessDeniedError(TransactionError):
    """Exception raised when user tries to access a transaction they don't own."""

    def __init__(self):
        super().__init__(status_code=403, detail="Access denied to this transaction")


class AccountNotActiveError(TransactionError):
    """Exception raised when trying to perform a transaction on a non-active account."""

    def __init__(self, account_id=None):
        message = "Account is not active" if account_id is None else f"Account {account_id} is not active"
        super().__init__(status_code=400, detail=message)


class TransactionFailedError(TransactionError):
    """Exception raised when a transaction fails to process."""

    def __init__(self, message: str = "Transaction failed to process"):
        super().__init__(status_code=500, detail=message)
