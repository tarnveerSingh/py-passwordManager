import getpass
import sqlite3
from database import create_database
from encryption import generate_key, load_key, encrypt_password, decrypt_password

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
        print(f"Service: {service} | Username: {username} | Password (encrypted): {encrypted_pw}")

def delete_password(service, username):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE service_name = ? AND username = ?', (service, username))
    conn.commit()
    conn.close()

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
        print("3. Delete a password") 
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            save_password(service, username, password, key)

        elif choice == "2":
            view_passwords(key)
        
        # elif choice == "3":
        #     
            
        elif choice == "4":
            print("👋 Exiting Password Manager. Bye!")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
