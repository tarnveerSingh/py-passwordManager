import sqlite3

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
