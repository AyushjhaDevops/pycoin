"""Transaction-specific exceptions for PyCoin."""


class TransactionError(Exception):
    """Base exception for transaction-related errors."""


class InvalidTransactionError(TransactionError, ValueError):
    """Raised when a transaction or its components are invalid."""
