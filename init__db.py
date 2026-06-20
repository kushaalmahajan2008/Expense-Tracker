import sqlite3

expense_table="""CREATE TABLE IF NOT EXISTS Expenses
    (expnese_id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_date TEXT NOT NULL,
    expense_amount REAL NOT NULL,
    expense_category TEXT NOT NULL,
    expense_tag TEXT NOT NULL,
    expense_description TEXT )"""

tag_table="""CREATE TABLE IF NOT EXISTS TAGS
    (Tags Text NOT NULL)"""


with sqlite3.Connection("expense.db") as conn:
    conn.execute(expense_table)
    conn.execute(tag_table)
print("Database Initialized")
