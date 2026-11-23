"""Ed25519 key generation and digital signature utilities."""

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

PRIVATE_KEY_SIZE = 32
PUBLIC_KEY_SIZE = 32
SIGNATURE_SIZE = 64


def generate_keypair() -> tuple[bytes, bytes]:
    """
    Generate an Ed25519 keypair.

    Returns:
        A tuple containing (private_seed, public_key).
    """
    signing_key = SigningKey.generate()

    private_key = bytes(signing_key)
    public_key = bytes(signing_key.verify_key)

    return private_key, public_key


def sign_message(private_key: bytes, message: bytes) -> bytes:
    """Sign a message using an Ed25519 private key."""
    if not isinstance(private_key, bytes):
        raise TypeError("private_key must be bytes")

    if not isinstance(message, bytes):
        raise TypeError("message must be bytes")

    if len(private_key) != PRIVATE_KEY_SIZE:
        raise ValueError("Ed25519 private key must be 32 bytes")

    signing_key = SigningKey(private_key)
    signed_message = signing_key.sign(message)

    return signed_message.signature


def verify_signature(
    public_key: bytes,
    message: bytes,
    signature: bytes,
) -> bool:
    """Verify an Ed25519 signature.

    Returns False for malformed keys, invalid signatures, or
    messages that do not match the signed message.
    """
    if not all(isinstance(value, bytes) for value in (public_key, message, signature)):
        return False

    if len(public_key) != PUBLIC_KEY_SIZE:
        return False

    if len(signature) != SIGNATURE_SIZE:
        return False

    try:
        verify_key = VerifyKey(public_key)
        verify_key.verify(message, signature)
        return True
    except (BadSignatureError, ValueError):
        return False
