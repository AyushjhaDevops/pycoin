from nacl.signing import SigningKey
from pycoin.crypto.addresses import derive_address, is_valid_address


def make_public_key(seed: bytes) -> bytes:
    return bytes(SigningKey(seed).verify_key)


def test_address_generation():
    public_key = make_public_key(bytes(range(32)))

    address = derive_address(public_key)

    assert address.startswith("PYC1")
    assert len(address) == 44
    assert is_valid_address(address)


def test_address_generation_is_deterministic():
    public_key = make_public_key(bytes(range(32)))

    assert derive_address(public_key) == derive_address(public_key)


def test_different_public_keys_produce_different_addresses():
    public_key_a = make_public_key(bytes(range(32)))
    public_key_b = make_public_key(bytes(reversed(range(32))))

    assert derive_address(public_key_a) != derive_address(public_key_b)


def test_modified_address_fails_validation():
    public_key = make_public_key(bytes(range(32)))
    address = derive_address(public_key)

    replacement = "A" if address[-1] != "A" else "B"
    modified_address = address[:-1] + replacement

    assert not is_valid_address(modified_address)


def test_invalid_prefix_fails_validation():
    public_key = make_public_key(bytes(range(32)))
    address = derive_address(public_key)

    assert not is_valid_address("ABC1" + address[4:])


def test_malformed_address_fails_validation():
    assert not is_valid_address("PYC1INVALID")
    assert not is_valid_address("")
    assert not is_valid_address("pyc1invalid")
    assert not is_valid_address(None)  # type: ignore[arg-type]
