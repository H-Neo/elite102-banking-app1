import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connection to SQLite DB successful: {db_file}")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE,
                balance REAL DEFAULT 0.0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def initialize_database(db_file):
    conn = create_connection(db_file)
    if conn:
        create_table(conn)
        return conn

def insert_user(conn, name, age, email, initial_balance=0.0):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age, email, balance) VALUES (?, ?, ?, ?)", (name, age, email, initial_balance))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")

def get_all_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        return []

def get_user_by_id(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error fetching user: {e}")
        return None

def update_balance(conn, user_id, new_balance):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating balance: {e}")

def log_transaction(conn, user_id, amount, transaction_type, description="", timestamp=None):
    try:
        if timestamp is None:
            import datetime
            timestamp = datetime.datetime.now().isoformat()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount, description, timestamp) VALUES (?, ?, ?, ?, ?)", (user_id, transaction_type, amount, description, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error logging transaction: {e}")

def get_transactions(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching transactions: {e}")
        return []

def close_connection(conn):
    try:
        if conn:
            conn.close()
    except sqlite3.Error as e:
        print(f"Error closing connection: {e}")