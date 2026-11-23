# Phase 1 — Cryptographic Foundation

## Objective

Implement the foundational cryptographic components required by PyCoin.

## Implemented components

### SHA-256

- Deterministic 256-bit hashing.
- Binary and hexadecimal digest functions.
- Known-vector tests.

### Ed25519

- Secure keypair generation through PyNaCl.
- 32-byte private seed.
- 32-byte public verification key.
- 64-byte digital signatures.
- Signature verification and invalid-signature handling.

### PYC addresses

- Versioned `PYC1` address format.
- Domain-separated SHA-256 derivation.
- 20-byte address payload.
- 4-byte checksum.
- Base32 encoding without padding.
- Address format and checksum validation.

## Security considerations

- Never log private keys or signatures containing secret material.
- Never commit private keys or wallet files.
- Use cryptographically secure random key generation.
- Do not use the address checksum as an authentication mechanism.
- Address validation does not prove ownership of the associated private key.
- Do not use this educational implementation to store real funds.

## Testing

Run:

```bash
python -m pytest backend/tests/crypto -v
python -m pytest -v
python -m ruff check backend
python -m ruff format --check backend
```

## Completion criteria

- SHA-256 known vectors pass.
- Ed25519 signing and verification pass.
- Invalid signatures are rejected.
- Address generation is deterministic.
- Invalid addresses and checksums are rejected.
- All backend tests pass.
- Ruff lint and formatting pass.
- Changes are committed and pushed to GitHub.

## Next phase

Phase 2 — Blockchain Data Structures.
