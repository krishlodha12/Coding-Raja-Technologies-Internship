import sqlite3
from datetime import datetime

# Create the database and transactions table
def create_database():
    with sqlite3.connect("budget.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY, 
                     type TEXT NOT NULL, 
                     category TEXT NOT NULL, 
                     amount REAL NOT NULL, 
                     date TEXT NOT NULL)''')

# Add a transaction (either income or expense) to the database
def add_transaction(trans_type, category, amount):
    with sqlite3.connect("budget.db") as conn:
        c = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
                  (trans_type, category, amount, date))
        print(f"\n{trans_type.capitalize()} of {amount} added successfully!")

# Display all transactions
def display_transactions():
    with sqlite3.connect("budget.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM transactions ORDER BY date DESC")
        rows = c.fetchall()
        
        if not rows:
            print("\nNo transactions to show!")
            return
        
        print("\nYour Transactions:")
        for row in rows:
            print(f"{row[0]}. {row[1].capitalize()} | Category: {row[2]} | Amount: {row[3]} | Date: {row[4]}")

# Calculate and display the remaining budget
def calculate_budget():
    with sqlite3.connect("budget.db") as conn:
        c = conn.cursor()
        
        # Sum of all incomes
        c.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
        total_income = c.fetchone()[0] or 0
        
        # Sum of all expenses
        c.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
        total_expenses = c.fetchone()[0] or 0
        
        remaining_budget = total_income - total_expenses
        print(f"\nTotal Income: {total_income}")
        print(f"Total Expenses: {total_expenses}")
        print(f"Remaining Budget: {remaining_budget}")

# Analyze expenses by category
def analyze_expenses():
    with sqlite3.connect("budget.db") as conn:
        c = conn.cursor()
        c.execute("SELECT category, SUM(amount) FROM transactions WHERE type = 'expense' GROUP BY category")
        rows = c.fetchall()
        
        if not rows:
            print("\nNo expenses to analyze!")
            return
        
        print("\nExpense Analysis by Category:")
        for row in rows:
            print(f"Category: {row[0]} | Total Spent: {row[1]}")

# Main loop for command-line interaction
def main():
    create_database()
    
    while True:
        print("\nOptions: (1) Add income (2) Add expense (3) Show transactions (4) Show budget (5) Analyze expenses (6) Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter income category: ").strip()
            try:
                amount = float(input("Enter amount: ").strip())
                add_transaction("income", category, amount)
            except ValueError:
                print("Invalid amount! Please enter a valid number.")

        elif choice == "2":
            category = input("Enter expense category: ").strip()
            try:
                amount = float(input("Enter amount: ").strip())
                add_transaction("expense", category, amount)
            except ValueError:
                print("Invalid amount! Please enter a valid number.")

        elif choice == "3":
            display_transactions()

        elif choice == "4":
            calculate_budget()

        elif choice == "5":
            analyze_expenses()

        elif choice == "6":
            print("Exiting the budget tracker. Goodbye!")
            break

        else:
            print("Invalid option! Please choose a valid number.")

if __name__ == "__main__":
    main()
