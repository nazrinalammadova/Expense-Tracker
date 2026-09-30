import unittest

from database import ExpenseDatabase


class TestExpenseDatabase(unittest.TestCase):
    def setUp(self):
        self.db = ExpenseDatabase(":memory:")
        self.db.add_expense(10.5, "Food", "Lunch", "2026-09-01")
        self.db.add_expense(4.0, "Transport", "Metro card", "2026-09-02")
        self.db.add_expense(20.0, "Food", "Groceries", "2026-09-10")
        self.db.add_expense(15.0, "Education", "Book", "2026-08-25")

    def tearDown(self):
        self.db.close()

    def test_get_all_expenses(self):
        self.assertEqual(len(self.db.get_expenses()), 4)

    def test_filter_by_month(self):
        september = self.db.get_expenses("2026-09")
        self.assertEqual(len(september), 3)

    def test_summary_by_category(self):
        summary = self.db.summary_by_category("2026-09")
        self.assertEqual(summary[0], ("Food", 30.5))
        self.assertEqual(len(summary), 2)

    def test_total(self):
        self.assertAlmostEqual(self.db.get_total(), 49.5)
        self.assertAlmostEqual(self.db.get_total("2026-08"), 15.0)

    def test_delete_expense(self):
        expense_id = self.db.add_expense(3.0, "Other", "Test")
        self.assertTrue(self.db.delete_expense(expense_id))
        self.assertFalse(self.db.delete_expense(expense_id))

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.db.add_expense(-5, "Food")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            self.db.add_expense(5, "Unknown")


if __name__ == "__main__":
    unittest.main()
