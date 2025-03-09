import sqlite3

DB_NAME = "expenses.db"

def create_db():
    """Creates the database and tables if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            payment_method TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, category, payment_method):
    """Adds an expense record to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO expenses (amount, category, payment_method) VALUES (?, ?, ?)', 
                   (amount, category, payment_method))
    conn.commit()
    conn.close()

def get_totals():
    """Calculates the total expenses."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM expenses')
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0  # Return 0 if no expenses exist

def reset_expenses():
    """Deletes all expenses from the database and resets the table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses')  # Clear all expenses
    conn.commit()
    conn.close()
