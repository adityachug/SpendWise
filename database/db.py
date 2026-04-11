import sqlite3
from werkzeug.security import generate_password_hash


DATABASE = "spendly.db"


def get_db():
    """
    Opens connection to spendly.db in project root.
    Sets row_factory for dict-like access and enables foreign keys.
    Returns the connection.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Creates users and expenses tables using CREATE TABLE IF NOT EXISTS.
    Safe to call multiple times.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """
    Inserts sample demo data for development.
    Checks if data already exists to prevent duplicates.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count > 0:
        conn.close()
        return  # Data already exists, skip seeding

    # Hash the demo password
    password_hash = generate_password_hash("demo123")

    # Insert demo user
    cursor.execute("""
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    """, ("Demo User", "demo@spendly.com", password_hash))

    # Get the user_id of the demo user
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@spendly.com",))
    user_id = cursor.fetchone()[0]

    # Insert 8 sample expenses across all categories
    # Categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
    sample_expenses = [
        (50.00, "Food", "2026-04-01", "Lunch at restaurant"),
        (25.50, "Transport", "2026-04-02", "Uber ride to airport"),
        (120.00, "Bills", "2026-04-03", "Electricity bill"),
        (45.00, "Health", "2026-04-05", "Pharmacy purchase"),
        (35.00, "Entertainment", "2026-04-07", "Movie tickets"),
        (200.00, "Shopping", "2026-04-10", "New clothes"),
        (15.00, "Other", "2026-04-12", "Miscellaneous item"),
        (65.00, "Food", "2026-04-15", "Grocery shopping"),
    ]

    for amount, category, date, description in sample_expenses:
        cursor.execute("""
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, amount, category, date, description))

    conn.commit()
    conn.close()
