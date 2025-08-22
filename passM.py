import sqlite3
from cryptography.fernet import Fernet
import getpass
# ------------------------------
# DATABASE FUNCTIONS
# ------------------------------

def create_database():
    """Create the passwords table if it doesn't exist"""
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            service_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database and table ready.")


# ------------------------------
# ENCRYPTION FUNCTIONS
# ------------------------------

def generate_key():
    """Generate a new encryption key and save it"""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("🔑 Encryption key generated and saved.")


def load_key():
    """Load the encryption key from file"""
    return open("key.key", "rb").read()


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


# ------------------------------
# PASSWORD STORAGE FUNCTIONS
# ------------------------------

def save_password(service, username, password, key):
    """Encrypt and store a password in the database"""
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    encrypted_pw = encrypt_password(password, key)
    cursor.execute(
        "INSERT INTO passwords (service_name, username, password) VALUES (?, ?, ?)",
        (service, username, encrypted_pw)
    )
    conn.commit()
    conn.close()
    print(f"💾 Password for {service} saved successfully.")


def view_passwords(key):
    """Retrieve and decrypt all passwords from the database"""
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute("SELECT service_name, username, password FROM passwords")
    rows = cursor.fetchall()
    conn.close()

    print("📂 Stored passwords:")
    for service, username, encrypted_pw in rows:
        #decrypted_pw = decrypt_password(encrypted_pw, key)
        print(f"Service: {service} | Username: {username} | Password (encrypted): {encrypted_pw}")



# ------------------------------
# CLI INTERFACE
# ------------------------------

def main():
    print("=== Personal Password Manager ===")
    create_database()

    # Check if key exists, otherwise generate
    try:
        key = load_key()
        print("🔑 Encryption key loaded.")
    except FileNotFoundError:
        print("No key found. Generating a new one...")
        generate_key()
        key = load_key()

    while True:
        print("\nChoose an option:")
        print("1. Save a new password")
        print("2. View all passwords")
        print("3. Master Password (For viewing passwords)")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            save_password(service, username, password, key)

        elif choice == "2":
            view_passwords(key)

        elif choice == "3":
            print("👋 Exiting Password Manager. Bye!")
            break

        else:
            print("❌ Invalid choice. Try again.")


# ------------------------------
# RUN THE CLI
# ------------------------------

if __name__ == "__main__":
    main()
