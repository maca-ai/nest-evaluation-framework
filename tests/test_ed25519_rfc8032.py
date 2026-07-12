from __future__ import annotations

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

SEED = bytes.fromhex("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
PUBLIC = bytes.fromhex("d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a")
SIGNATURE = bytes.fromhex(
    "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
    "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
)


def test_rfc8032_test_vector_one() -> None:
    private = Ed25519PrivateKey.from_private_bytes(SEED)
    public = private.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    assert public == PUBLIC
    assert private.sign(b"") == SIGNATURE
    Ed25519PublicKey.from_public_bytes(PUBLIC).verify(SIGNATURE, b"")


@pytest.mark.parametrize("message", [b"x", b"\x00"])
def test_rfc8032_signature_refuses_message_tampering(message: bytes) -> None:
    with pytest.raises(InvalidSignature):
        Ed25519PublicKey.from_public_bytes(PUBLIC).verify(SIGNATURE, message)


def test_rfc8032_signature_refuses_signature_tampering() -> None:
    tampered = bytes([SIGNATURE[0] ^ 1]) + SIGNATURE[1:]
    with pytest.raises(InvalidSignature):
        Ed25519PublicKey.from_public_bytes(PUBLIC).verify(tampered, b"")


def test_rfc8032_signature_refuses_wrong_public_key() -> None:
    wrong_public = Ed25519PrivateKey.generate().public_key()
    with pytest.raises(InvalidSignature):
        wrong_public.verify(SIGNATURE, b"")
