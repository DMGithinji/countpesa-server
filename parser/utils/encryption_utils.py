import os
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from binascii import unhexlify

# Fetch and decode the hexadecimal key and IV from environment variables
hex_key = os.environ.get('AES_ENCRYPTION_KEY', '')
hex_iv = os.environ.get('IV_STRING', '')

# Convert hex to bytes
key = unhexlify(hex_key)
iv = unhexlify(hex_iv)

def decrypt(token: str) -> str:
    decoded_data = b64decode(token)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(decoded_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return decrypted_data.decode('utf-8')

def encrypt(data: str) -> str:
    # Setup cipher configuration
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Prepare data for encryption
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Encode the encrypted data to Base64 to ensure safe transport over networks
    encoded_encrypted_data = b64encode(encrypted_data).decode('utf-8')

    return encoded_encrypted_data