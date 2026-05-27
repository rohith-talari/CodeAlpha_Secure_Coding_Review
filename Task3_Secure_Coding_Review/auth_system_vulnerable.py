import sqlite3
import hashlib

DATABASE_NAME = "vulnerable_users.db"

# ---------------- DATABASE SETUP ---------------- #

def setup_vulnerable_database():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password_hash TEXT
    )
    """)

    cursor.execute("SELECT * FROM users WHERE username = 'admin'")

    if not cursor.fetchone():

        # Weak MD5 Hash
        hashed_password = hashlib.md5(
            "password123".encode()
        ).hexdigest()

        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", hashed_password)
        )

        conn.commit()

    conn.close()

# ---------------- VULNERABLE LOGIN ---------------- #

def login_user(username, password):

    hashed_password = hashlib.md5(
        password.encode()
    ).hexdigest()

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # SQL Injection Vulnerability
    query = f"""
    SELECT * FROM users
    WHERE username = '{username}'
    AND password_hash = '{hashed_password}'
    """

    print("\n[DEBUG] Executing Query:")
    print(query)

    cursor.execute(query)

    user = cursor.fetchone()

    conn.close()

    return user

# ---------------- MAIN PROGRAM ---------------- #

def main():

    print("=" * 60)
    print("      VULNERABLE AUTHENTICATION SYSTEM")
    print("=" * 60)

    setup_vulnerable_database()

    # Normal Login
    print("\n[*] Scenario 1: Normal Login")

    result = login_user(
        "admin",
        "password123"
    )

    print(f"Result: {result}")

    # SQL Injection Attack
    print("\n[*] Scenario 2: SQL Injection Attack")

    sqli_payload = "' OR 1=1 -- "

    attacker_login = login_user(
        sqli_payload,
        "randompassword"
    )

    print(f"\nAttacker Payload: {sqli_payload}")

    if attacker_login:
        print("[!] SQL Injection Successful!")
        print(f"Returned Data: {attacker_login}")
    else:
        print("[-] Attack Failed")

    print("\n[+] Vulnerability Demonstration Completed.")

if __name__ == "__main__":
    main()