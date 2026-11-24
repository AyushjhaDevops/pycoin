
# Phase 3 — Transaction Engine

## Phase 3.1: Transaction Foundations

### Overview

This subphase introduces the foundational UTXO transaction data
structures for PyCoin.

### TransactionInput

References an output from a previous transaction.

Fields:

- previous_transaction_id: 64-character lowercase SHA-256 hex string
- previous_output_index: non-negative integer
- unlocking_data: bytes, empty before signing

### TransactionOutput

Creates a new spendable output.

Fields:

- amount: positive integer in smallest PYC units
- recipient_public_key: 32-byte Ed25519 public key

The recipient address is derived using the existing PyCoin PYC1
address implementation.

### Transaction

Contains:

- version
- inputs
- outputs
- lock_time

Input and output collections are normalized into immutable tuples.

Transactions must contain at least one input and one output.
Duplicate references to the same previous output are rejected.

### Monetary representation

PyCoin uses integer monetary units.

Floating-point amounts are prohibited to avoid precision errors.

### Security considerations

- Transaction components use immutable dataclasses.
- Previous transaction IDs must use lowercase SHA-256 hexadecimal.
- Public keys must have the expected Ed25519 byte length and pass libsodium Ed25519 point validation.
- Duplicate input references are rejected within a transaction.
- Actual UTXO existence and cross-transaction double-spend validation
  are deferred until UTXO state is implemented.
- Signature creation and verification are implemented in a later
  Phase 3 subphase.

### Limitations

This subphase does not implement:

- Transaction serialization
- Transaction IDs
- Digital signing
- UTXO database or state
- Cross-transaction double-spend detection
- Mempool
- Mining or consensus

### Validation

Run:

```bash
python -m pytest backend/tests/transactions -v
python -m pytest -v
python -m ruff check backend
python -m ruff format --check backend
python -m pip check
```
