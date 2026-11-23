
# Phase 2 — Blockchain Data Structures

## Objective

Implement PyCoin's foundational blockchain data structures using
deterministic serialization and SHA-256 hashing.

## Implemented components

- `BlockHeader`: immutable block metadata.
- `Block`: immutable transaction container with Merkle-root verification.
- `Merkle Tree`: domain-separated transaction and node hashing.
- `Genesis Block`: deterministic first block.
- `Blockchain`: in-memory block chain with structural validation.
- `Canonical Serialization`: deterministic JSON encoding.
- `Block Serialization`: deterministic block representation.

## Block header fields

| Field | Description |
|---|---|
| version | Block format version |
| timestamp | Unix timestamp in seconds |
| previous_hash | SHA-256 hash of the previous block |
| merkle_root | Merkle root of transaction payloads |
| nonce | Reserved for the future Proof of Work phase |

## Hashing

Block identifiers use SHA-256 over a domain-separated canonical
JSON representation of the block header.

Transaction leaves and internal Merkle nodes use separate domain
prefixes to avoid ambiguous hashing.

For an odd number of nodes, the final node is duplicated.
An empty transaction list has a deterministic empty root.

## Genesis block

The genesis block uses:

- Version: 1
- Timestamp: 0
- Previous hash: 64 zero characters
- Nonce: 0
- Transactions: empty

This makes the genesis block reproducible.

## Validation

The blockchain validates:

1. Genesis block identity.
2. Block type and structure.
3. Previous-block hash references.
4. Non-decreasing timestamps.
5. Transaction Merkle roots.

## Security and scope limitations

This phase is an educational implementation.

- Proof of Work is not implemented yet.
- Difficulty adjustment is not implemented.
- Transactions are opaque byte payloads until Phase 3.
- The chain is in memory and is not persisted.
- Consensus and peer-to-peer networking are not implemented.
- This is not suitable for real funds or production deployment.

## Tests

Run:

```bash
python -m pytest backend/tests/core -v
python -m pytest -v
python -m ruff check backend
python -m ruff format --check backend
```
