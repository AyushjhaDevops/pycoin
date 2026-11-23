import pytest
from pycoin.crypto.hashing import sha256, sha256_hex


def test_sha256_empty_input():
    assert sha256_hex(b"") == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_sha256_known_input():
    assert sha256_hex(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_sha256_returns_bytes():
    assert isinstance(sha256(b"PyCoin"), bytes)
    assert len(sha256(b"PyCoin")) == 32


def test_sha256_rejects_non_bytes():
    with pytest.raises(TypeError):
        sha256("PyCoin")  # type: ignore[arg-type]
