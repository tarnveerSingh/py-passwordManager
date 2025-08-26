import sqlite3

class Database:
    def __init__(self, db_name="passwords.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the passwords table if it doesn't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                service_name TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        print("✅ Database and table ready.")

    def close(self):
        self.conn.close()

# Mock user database for authentication
users_db = {
    "admin": {
        "password": "pass123",
        "notes": []
    },
    "john": {
        "password": "john123",
        "notes": []
    }
}
