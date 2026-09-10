import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def derive_key(password, salt):
    """Convert the user's password into a 256-bit encryption key."""

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )

    return kdf.derive(password.encode("utf-8"))


def encrypt_text(text, password):
    """Encrypt text using AES-256-GCM."""

    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)

    aes = AESGCM(key)
    encrypted = aes.encrypt(
        nonce,
        text.encode("utf-8"),
        None
    )

    package = salt + nonce + encrypted

    return base64.urlsafe_b64encode(package).decode("utf-8")


def decrypt_text(encrypted_text, password):
    """Decrypt text using the same password."""

    package = base64.urlsafe_b64decode(
        encrypted_text.encode("utf-8")
    )

    salt = package[:16]
    nonce = package[16:28]
    encrypted = package[28:]

    key = derive_key(password, salt)

    aes = AESGCM(key)

    decrypted = aes.decrypt(
        nonce,
        encrypted,
        None
    )

    return decrypted.decode("utf-8")
def encrypt_file(input_path, output_path, password):
    """Encrypt a file using AES-256-GCM."""

    with open(input_path, "rb") as file:
        data = file.read()

    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)

    aes = AESGCM(key)

    encrypted = aes.encrypt(
        nonce,
        data,
        None
    )

    package = salt + nonce + encrypted

    with open(output_path, "wb") as file:
        file.write(package)


def decrypt_file(input_path, output_path, password):
    """Decrypt a file using AES-256-GCM."""

    with open(input_path, "rb") as file:
        package = file.read()

    salt = package[:16]
    nonce = package[16:28]
    encrypted = package[28:]

    key = derive_key(password, salt)

    aes = AESGCM(key)

    decrypted = aes.decrypt(
        nonce,
        encrypted,
        None
    )

    with open(output_path, "wb") as file:
        file.write(decrypted)