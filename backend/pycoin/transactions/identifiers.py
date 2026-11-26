"""Transaction identifier generation for PyCoin."""

from pycoin.crypto.hashing import sha256_hex
from pycoin.transactions.serialization import serialize_unsigned_transaction
from pycoin.transactions.transactions import Transaction


def calculate_transaction_id(transaction: Transaction) -> str:
    """Calculate a transaction ID from its unsigned serialized representation.

    Unlocking data is intentionally excluded from the transaction ID.
    This keeps the identifier stable when transaction inputs are signed.
    """
    if not isinstance(transaction, Transaction):
        raise TypeError("transaction must be a Transaction instance")

    unsigned_transaction = serialize_unsigned_transaction(transaction)
    return sha256_hex(unsigned_transaction)
