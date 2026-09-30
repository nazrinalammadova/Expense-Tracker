import sqlite3
from datetime import date

CATEGORIES = ["Food", "Transport", "Education", "Entertainment", "Bills", "Shopping", "Other"]


class ExpenseDatabase:
    def __init__(self, db_path="expenses.db"):
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                amount      REAL    NOT NULL CHECK (amount > 0),
                category    TEXT    NOT NULL,
                description TEXT,
                date        TEXT    NOT NULL
            )
            """
        )
        self.connection.commit()

    def add_expense(self, amount, category, description="", expense_date=None):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        if category not in CATEGORIES:
            raise ValueError(f"Unknown category: {category}")
        if expense_date is None:
            expense_date = date.today().isoformat()

        cursor = self.connection.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (amount, category, description, expense_date),
        )
        self.connection.commit()
        return cursor.lastrowid

    def delete_expense(self, expense_id):
        cursor = self.connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.connection.commit()
        return cursor.rowcount > 0

    def get_expenses(self, month=None):
        if month:
            rows = self.connection.execute(
                "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC", (month + "-%",)
            )
        else:
            rows = self.connection.execute("SELECT * FROM expenses ORDER BY date DESC")
        return [dict(row) for row in rows]

    def summary_by_category(self, month=None):
        query = "SELECT category, SUM(amount) AS total FROM expenses"
        params = ()
        if month:
            query += " WHERE date LIKE ?"
            params = (month + "-%",)
        query += " GROUP BY category ORDER BY total DESC"
        return [(row["category"], row["total"]) for row in self.connection.execute(query, params)]

    def get_total(self, month=None):
        return sum(total for _, total in self.summary_by_category(month))

    def close(self):
        self.connection.close()
