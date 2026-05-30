import base64
from cryptography.fernet import Fernet

def load_encrypted_message(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ File '{file_path}' not found.")
        return None

def decrypt_message(encrypted_message: str, user_key: str) -> str:
    try:
        # Prepare Fernet-compatible key
        padded_key = user_key.encode().ljust(32, b'0')[:32]
        fernet_key = base64.urlsafe_b64encode(padded_key)
        f = Fernet(fernet_key)

        decrypted = f.decrypt(encrypted_message.encode())
        return decrypted.decode()

    except Exception as e:
        return f"❌ Error decrypting message: {e}"

if __name__ == '__main__':
    print("🔓 Encrypted Message Decryption")
    print("-------------------------------")

    file_path = "msg.txt"
    encrypted = load_encrypted_message(file_path)

    if encrypted:
        key = input("Enter the encryption key: ").strip()
        result = decrypt_message(encrypted, key)

        print("\n📨 Decrypted Message:\n")
        print(result)
