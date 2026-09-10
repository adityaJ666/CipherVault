from core.encryption import encrypt_text, decrypt_text


message = "Hello, this is my secret message!"
password = "Cyber123"


print("Original message:")
print(message)

encrypted = encrypt_text(message, password)

print("\nEncrypted message:")
print(encrypted)

decrypted = decrypt_text(encrypted, password)

print("\nDecrypted message:")
print(decrypted)

if message == decrypted:
    print("\n✓ Encryption test successful!")
else:
    print("\n✗ Encryption test failed!")