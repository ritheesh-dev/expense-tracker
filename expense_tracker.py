 # expense_tracker_mysql.py

import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------- Database Setup ---------------- #
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # 🔹 change to your MySQL username
        password="root",  # 🔹 change to your MySQL password
        database="expense_tracker"
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DOUBLE NOT NULL,
            category VARCHAR(50) NOT NULL,
            description VARCHAR(255),
            date DATETIME NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# ---------------- CRUD Operations ---------------- #
def add_expense(amount, category, description=""):
    conn = get_connection()
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s)",
                   (amount, category, description, date))
    conn.commit()
    conn.close()
    print("✅ Expense added successfully!")


def view_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("⚠️ No expenses recorded yet.")
        return

    print("\n📒 Expense List:")
    print("-" * 60)
    for row in rows:
        print(f"ID: {row[0]} | Amount: ₹{row[1]} | Category: {row[2]} | Note: {row[3]} | Date: {row[4]}")
    print("-" * 60)


def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    conn.close()
    print("🗑️ Expense deleted successfully!")


# ---------------- Visualization ---------------- #
def visualize_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("⚠️ No data to visualize.")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(7, 7))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("💰 Expense Breakdown by Category")
    plt.show() 


# ---------------- Menu ---------------- #
def menu():
    init_db()
    while True:
        print("\n===== Expense Tracker (MySQL) =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Visualize Expenses")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount: ₹"))
                category = input("Enter category (Food, Travel, Shopping, etc.): ")
                description = input("Enter description (optional): ")
                add_expense(amount, category, description)
            except ValueError:
                print("⚠️ Invalid input. Please enter a number for amount.")

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                delete_expense(expense_id)
            except ValueError:
                print("⚠️ Invalid ID. Please enter a number.")

        elif choice == "4":
            visualize_expenses()

        elif choice == "5":
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("⚠️ Invalid choice, please try again.")


if __name__ == "__main__":
    menu()

