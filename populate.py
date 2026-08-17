import sqlite3
import os

DB_PATH = "qa_tasks.db"

def populate():
    # Make sure we have the schema created
    # Normally SQLAlchemy would do this, but just in case
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, hashed_password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, description TEXT, status TEXT, due_date TEXT, owner_id INTEGER)''')
    
    # Check if empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (email, hashed_password) VALUES ('test@example.com', 'hashed')")
        
    c.execute("SELECT COUNT(*) FROM tasks")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO tasks (title, description, status, owner_id) VALUES ('Initial Task', 'Desc', 'open', 1)")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate()
