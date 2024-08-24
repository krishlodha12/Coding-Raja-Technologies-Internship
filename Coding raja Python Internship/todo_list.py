import sqlite3

# Define priorities and their rank for sorting
PRIORITY_RANK = {"low": 3, "medium": 2, "high": 1}

# Create the database and tasks table
def create_database():
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks
                     (id INTEGER PRIMARY KEY, 
                     task TEXT NOT NULL, 
                     priority TEXT NOT NULL, 
                     due_date TEXT, 
                     completed INTEGER)''')

# Add task to the database
def add_task(task, priority="low", due_date=None):
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task, priority, due_date, completed) VALUES (?, ?, ?, ?)",
                  (task, priority, due_date, 0))
        print("\nTask added successfully!")

# Remove task from the database
def remove_task(task_id):
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        print("\nTask removed successfully!")

# Mark task as completed in the database
def complete_task(task_id):
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        print("\nTask marked as completed!")

# Display tasks with sorting from the database
def display_tasks(sort_by="priority"):
    with sqlite3.connect("tasks.db") as conn:
        c = conn.cursor()
        if sort_by == "priority":
            c.execute("SELECT * FROM tasks ORDER BY completed, CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END")
        elif sort_by == "due_date":
            c.execute("SELECT * FROM tasks ORDER BY completed, due_date")
        
        rows = c.fetchall()
        
        if not rows:
            print("\nNo tasks to show!")
            return
        
        print("\nYour tasks:")
        for row in rows:
            status = "Completed" if row[4] else "Pending"
            print(f"{row[0]}. {row[1]} (Priority: {row[2].capitalize()}, Due: {row[3]}, Status: {status})")

# Command-line loop with SQLite
def main():
    create_database()
    
    while True:
        print("\nOptions: (1) Add task (2) Remove task (3) Mark as completed (4) Show tasks (5) Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter task description: ").strip()
            priority = input("Enter priority (low, medium, high): ").lower().strip()
            if priority not in PRIORITY_RANK:
                print("Invalid priority! Please enter 'low', 'medium', or 'high'.")
                continue
            due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
            add_task(task, priority, due_date)

        elif choice == "2":
            display_tasks()
            try:
                task_id = int(input("Enter task ID to remove: ").strip())
                remove_task(task_id)
            except ValueError:
                print("Invalid input! Please enter a valid task ID.")

        elif choice == "3":
            display_tasks()
            try:
                task_id = int(input("Enter task ID to mark as completed: ").strip())
                complete_task(task_id)
            except ValueError:
                print("Invalid input! Please enter a valid task ID.")

        elif choice == "4":
            sort_by = input("Sort tasks by 'priority' or 'due_date'? (default: priority): ").lower().strip()
            if sort_by not in ["priority", "due_date"]:
                sort_by = "priority"
            display_tasks(sort_by)

        elif choice == "5":
            print("Exiting the to-do list application. Goodbye!")
            break

        else:
            print("Invalid option! Please choose a valid number.")

if __name__ == "__main__":
    main()
