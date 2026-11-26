
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

At the Phase 3.1 foundation stage, the following were deferred:

- Transaction serialization
- Transaction IDs
- Digital signing
- UTXO database or state
- Cross-transaction double-spend detection
- Mempool
- Mining or consensus

Serialization and transaction ID generation are implemented in Phase 3.2.
Digital signing and UTXO state remain deferred.


### Validation

Run:

```bash
python -m pytest backend/tests/transactions -v
python -m pytest -v
python -m ruff check backend
python -m ruff format --check backend
python -m pip check
```

## Phase 3.2: Deterministic Serialization and Transaction IDs

### Deterministic serialization

Transactions use a versioned canonical JSON representation.

- Transaction format: `PyCoin:Transaction`
- Format version: `1`
- Binary fields are represented using lowercase hexadecimal.
- Canonical JSON serialization ensures deterministic byte output.
- Full serialization includes input unlocking data.
- Unsigned serialization excludes input unlocking data.

Public serialization APIs:

- `transaction_to_dict(transaction, include_unlocking_data=True)`
- `transaction_from_dict(data)`
- `serialize_transaction(transaction)`
- `serialize_unsigned_transaction(transaction)`
- `deserialize_transaction(serialized)`

### Transaction ID generation

The transaction ID (TXID) is calculated from the unsigned
canonical transaction representation.

Formula:

`TXID = SHA256(serialize_unsigned_transaction(transaction))`

Implementation:

- `calculate_transaction_id(transaction)` returns a 64-character lowercase hexadecimal string.
- Existing SHA-256 utilities are reused.
- Unlocking data and signatures do not affect the transaction ID.
- Changes to transaction version, lock time, inputs, or outputs
  change the unsigned serialization and therefore the transaction ID.

### Security considerations

- TXIDs are calculated from deterministic unsigned transaction bytes.
- Signing an input does not change its transaction ID.
- The transaction format marker and format version are included
  in the hashed representation.
- SHA-256 collision resistance is relied upon for identifier uniqueness;
  absolute mathematical uniqueness is not guaranteed.

### Current implementation status

Implemented:

- Immutable transaction models
- Deterministic full and unsigned serialization
- Strict transaction deserialization
- Duplicate JSON key rejection
- Deterministic transaction ID generation

Deferred:

- Digital transaction signing and signature verification
- UTXO existence and state validation
- Cross-transaction double-spend detection
- Mempool
- Mining and consensus
