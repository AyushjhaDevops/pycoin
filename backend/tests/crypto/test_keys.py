import pytest
from pycoin.crypto.keys import (
    generate_keypair,
    sign_message,
    verify_signature,
)


def test_generate_keypair():
    private_key, public_key = generate_keypair()

    assert len(private_key) == 32
    assert len(public_key) == 32
    assert private_key != public_key


def test_sign_and_verify_message():
    private_key, public_key = generate_keypair()
    message = b"PyCoin transaction"

    signature = sign_message(private_key, message)

    assert len(signature) == 64
    assert verify_signature(public_key, message, signature)


def test_modified_message_fails_verification():
    private_key, public_key = generate_keypair()
    signature = sign_message(private_key, b"original message")

    assert not verify_signature(
        public_key,
        b"modified message",
        signature,
    )


def test_wrong_public_key_fails_verification():
    private_key, _ = generate_keypair()
    _, another_public_key = generate_keypair()

    message = b"PyCoin transaction"
    signature = sign_message(private_key, message)

    assert not verify_signature(
        another_public_key,
        message,
        signature,
    )


def test_invalid_private_key_length():
    with pytest.raises(ValueError):
        sign_message(b"short", b"message")


def test_malformed_signature_fails_verification():
    _, public_key = generate_keypair()

    assert not verify_signature(
        public_key,
        b"message",
        b"invalid",
    )
