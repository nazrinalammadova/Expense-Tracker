# Expense Tracker (Python + SQLite)

A console application to track personal expenses. Users can add expenses by category, see monthly reports and export data to a CSV file (for Excel).

I built this project to practice **Python, SQL databases and unit testing**.

## Features

- Add expenses with amount, category, description and date
- View all expenses or only one month
- Monthly summary by category with percentages and a simple text chart
- Delete expenses
- Export all data to `expenses.csv`
- Input validation (wrong amounts, dates or categories are not accepted)
- Unit tests for the database logic

## Technologies

- Python 3 (standard library only, no installation needed)
- SQLite (`sqlite3` module)
- `csv`, `datetime`, `unittest`

## Project structure

```
database.py        # ExpenseDatabase class (all SQL queries)
main.py            # Console menu and user input
test_database.py   # Unit tests
```

## How to run

```bash
python main.py
```

Run the tests:

```bash
python -m unittest -v
```

## Example

```
Summary for 2026-09
Food                30.50 AZN   69.3%  #############
Transport            9.50 AZN   21.6%  ####
Education            4.00 AZN    9.1%  #
Total               44.00 AZN
```

## What I learned

- How to create tables and write SQL queries (`INSERT`, `SELECT`, `GROUP BY`, `SUM`)
- How to use parameterized queries to protect against SQL injection
- How to separate database logic from the user interface
- How to write unit tests with a temporary in-memory database

## Possible improvements

- Monthly budget limits with warnings
- Charts with `matplotlib`
- A web version with Flask
