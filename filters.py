def get_expenses_by_period(start_date, end_date):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
    return cursor.fetchall()
