import getpass
from database import Database, users_db
from encryption import generate_key, load_key, encrypt_password, decrypt_password


# ------------------------------
# AUTHENTICATION FUNCTION
# ------------------------------
def authenticate_user():
    """Authenticate user by checking username and password against users_db"""
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    
    if username in users_db and users_db[username]["password"] == password:
        print(f"✅ Welcome, {username}!")
        return True
    else:
        print("❌ Invalid username or password.")
        return False


# ------------------------------
# PASSWORD STORAGE FUNCTIONS
# ------------------------------
def save_password(db, service, username, password, key):
    encrypted_pw = encrypt_password(password, key)
    db.cursor.execute(
        "INSERT INTO passwords (service_name, username, password) VALUES (?, ?, ?)",
        (service, username, encrypted_pw)
    )
    db.conn.commit()
    print(f"💾 Password for {service} saved successfully.")


def view_passwords(db):
    db.cursor.execute("SELECT service_name, username, password FROM passwords")
    rows = db.cursor.fetchall()

    print("📂 Stored passwords:")
    for service, username, encrypted_pw in rows:
        print(f"Service: {service} | Username: {username} | Password (encrypted): {encrypted_pw}")


def view_decrypted_passwords(db, key):
    if not authenticate_user():
        print("❌ Access denied. Only authenticated users can view decrypted passwords.")
        return

    db.cursor.execute("SELECT service_name, username, password FROM passwords")
    rows = db.cursor.fetchall()

    print("📂 Decrypted passwords:")
    for service, username, encrypted_pw in rows:
        try:
            decrypted_pw = decrypt_password(encrypted_pw, key)
            print(f"Service: {service} | Username: {username} | Password: {decrypted_pw}")
        except Exception as e:
            print(f"❌ Error decrypting password for {service}: {e}")


def delete_password(db, service_name, username):
    db.cursor.execute(
        "SELECT id FROM passwords WHERE service_name = ? AND username = ?",
        (service_name, username)
    )
    result = db.cursor.fetchone()

    if result:
        db.cursor.execute(
            "DELETE FROM passwords WHERE service_name = ? AND username = ?",
            (service_name, username)
        )
        db.conn.commit()
        print(f"🗑️ Password for service '{service_name}' and username '{username}' deleted successfully.")
    else:
        print(f"❌ No password found for service '{service_name}' with username '{username}'.")
    

# ------------------------------
# CLI INTERFACE
# ------------------------------
def main():
    print("=== Personal Password Manager ===")
    db = Database()   # ✅ Open DB once here

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
        print("4. View all passwords (decrypted)")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter service name: ")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            save_password(db, service, username, password, key)

        elif choice == "2":
            view_passwords(db)
        
        elif choice == "3":
            service = input("Enter service name to delete: ")
            username = input("Enter username to delete: ")
            delete_password(db, service, username)
     
        elif choice == "4":
            view_decrypted_passwords(db, key)

        elif choice == "5":
            print("👋 Exiting Password Manager. Bye!")
            db.close()   # ✅ Close connection when exiting
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
