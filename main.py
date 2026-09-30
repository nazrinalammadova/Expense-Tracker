import csv
from datetime import datetime

from database import CATEGORIES, ExpenseDatabase

MENU = """
1. Add expense
2. Show all expenses
3. Show expenses for a month
4. Monthly summary by category
5. Delete expense
6. Export to CSV
0. Exit"""


def read_amount():
    while True:
        text = input("Amount (AZN): ").strip().replace(",", ".")
        try:
            amount = float(text)
            if amount > 0:
                return round(amount, 2)
            print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a number, for example 12.50")


def read_category():
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"  {number}. {category}")
    while True:
        text = input("Category number: ").strip()
        if text.isdigit() and 1 <= int(text) <= len(CATEGORIES):
            return CATEGORIES[int(text) - 1]
        print(f"Please choose a number from 1 to {len(CATEGORIES)}.")


def read_date():
    while True:
        text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        if text == "":
            return None
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Wrong format. Example: 2026-09-15")


def read_month():
    while True:
        text = input("Month (YYYY-MM): ").strip()
        try:
            datetime.strptime(text, "%Y-%m")
            return text
        except ValueError:
            print("Wrong format. Example: 2026-09")


def print_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'ID':<5}{'Date':<12}{'Category':<15}{'Amount':>10}  Description")
    print("-" * 60)
    for e in expenses:
        print(f"{e['id']:<5}{e['date']:<12}{e['category']:<15}{e['amount']:>10.2f}  {e['description']}")
    total = sum(e["amount"] for e in expenses)
    print("-" * 60)
    print(f"{'Total:':<32}{total:>10.2f} AZN")


def print_summary(db, month):
    summary = db.summary_by_category(month)
    if not summary:
        print("No expenses for this month.")
        return

    total = db.get_total(month)
    print(f"\nSummary for {month}")
    for category, amount in summary:
        percent = amount / total * 100
        bar = "#" * int(percent / 5)
        print(f"{category:<15}{amount:>10.2f} AZN  {percent:5.1f}%  {bar}")
    print(f"{'Total':<15}{total:>10.2f} AZN")


def export_to_csv(db, file_name="expenses.csv"):
    expenses = db.get_expenses()
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "date", "category", "amount", "description"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"{len(expenses)} expenses exported to {file_name}.")


def main():
    db = ExpenseDatabase()
    print("=== Expense Tracker ===")

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            amount = read_amount()
            category = read_category()
            description = input("Description (optional): ").strip()
            expense_id = db.add_expense(amount, category, description, read_date())
            print(f"Expense added with ID {expense_id}.")
        elif choice == "2":
            print_expenses(db.get_expenses())
        elif choice == "3":
            print_expenses(db.get_expenses(read_month()))
        elif choice == "4":
            print_summary(db, read_month())
        elif choice == "5":
            text = input("Expense ID: ").strip()
            if text.isdigit() and db.delete_expense(int(text)):
                print("Expense deleted.")
            else:
                print("Expense not found.")
        elif choice == "6":
            export_to_csv(db)
        elif choice == "0":
            db.close()
            print("Goodbye!")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
