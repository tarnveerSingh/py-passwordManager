from cryptography.fernet import Fernet
from dotenv import set_key
import os
from dotenv import load_dotenv
from database import users_db

def generate_key():
    """Generate a new encryption key and save it in .env"""
    key = Fernet.generate_key().decode()  # decode bytes → str

    env_file = ".env"

    # create .env if not exists
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("")  

    set_key(env_file, "SECRET_KEY", key)
    print("🔑 Encryption key generated and saved in .env")



def load_key():
    """Load the encryption key from .env"""
    load_dotenv()  # load variables from .env
    key = os.getenv("SECRET_KEY")
    if not key:
        raise ValueError("❌ SECRET_KEY not found in .env. Generate it first.")
    return key.encode()  # Fernet expects bytes

def encrypt_password(password, key):
    """Encrypt a password string"""
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    print(f"🔒 Password encrypted: {encrypted}")
    return encrypted

def decrypt_password(encrypted_password, key):
    """Decrypt an encrypted password"""
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_password).decode()
    print(f"🔓 Password decrypted: {decrypted}")
    return decrypted
