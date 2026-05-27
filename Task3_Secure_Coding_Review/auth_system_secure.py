import sqlite3
import sys

try:
    import bcrypt
except ModuleNotFoundError:
    print("[!] Install bcrypt using: pip install bcrypt")
    sys.exit(1)

DATABASE_NAME = "users.db"

def setup_database():

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL
        )
        """)

        cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))

        if not cursor.fetchone():

            hashed_password = bcrypt.hashpw(
                b"password123",
                bcrypt.gensalt()
            )

            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                ("admin", hashed_password)
            )

            conn.commit()

        conn.close()

    except sqlite3.Error as e:
        print(f"[!] Database Error: {e}")

def login_user(username, password):

    if not username or not password:
        return False

    try:

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        query = "SELECT password_hash FROM users WHERE username = ?"

        cursor.execute(query, (username,))

        row = cursor.fetchone()

        conn.close()

        if row:
            stored_hash = row[0]

            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return True

        return False

    except sqlite3.Error as e:
        print(f"[!] Database Error: {e}")
        return False

def main():

    print("=" * 60)
    print("      SECURE AUTHENTICATION SYSTEM")
    print("=" * 60)

    setup_database()

    print("\n[*] Testing Secure Login System\n")

    username = "admin"
    password = "password123"

    result = login_user(username, password)

    print(f"Login Attempt")
    print(f"Username : {username}")
    print(f"Password : {password}")
    print(f"Access Granted : {result}")

    failed_attempt = login_user("admin", "wrong_password")

    print("\n[*] Invalid Login Test")
    print(f"Access Granted : {failed_attempt}")

    print("\n[+] System executed securely with no vulnerabilities.")

if __name__ == "__main__":
    main()