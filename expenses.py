import sqlite3
from datetime import datetime

def add_expense(amount, category, payment_method):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, payment_method, date) VALUES (?, ?, ?, ?)", 
                   (amount, category, payment_method, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()
