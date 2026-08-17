import sqlite3
import os
import sys

DB_PATH = "qa_tasks.db"

def run_validations():
    if not os.path.exists(DB_PATH):
        print(f"FAIL: Database file {DB_PATH} not found.")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    passed = 0
    total = 7

    print(f"--- Running Database Validations on {DB_PATH} ---")

    # 1. At least one user exists in the DB
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count >= 1:
        print("PASS: 1. At least one user exists in the DB.")
        passed += 1
    else:
        print("FAIL: 1. No users found in the DB.")

    # 2. No duplicate email rows exist
    cursor.execute("SELECT email FROM users GROUP BY email HAVING COUNT(*) > 1")
    dups = cursor.fetchall()
    if len(dups) == 0:
        print("PASS: 2. No duplicate email rows exist.")
        passed += 1
    else:
        print(f"FAIL: 2. Duplicate emails found: {dups}")

    # 3. All tasks have a non-null, non-empty title
    cursor.execute("SELECT id FROM tasks WHERE title IS NULL OR title = ''")
    bad_titles = cursor.fetchall()
    if len(bad_titles) == 0:
        print("PASS: 3. All tasks have a non-null, non-empty title.")
        passed += 1
    else:
        print(f"FAIL: 3. Tasks with empty/null titles found: {bad_titles}")

    # 4. All tasks have a valid owner_id (no orphaned tasks)
    cursor.execute("""
        SELECT t.id 
        FROM tasks t 
        LEFT JOIN users u ON t.owner_id = u.id 
        WHERE u.id IS NULL
    """)
    orphans = cursor.fetchall()
    if len(orphans) == 0:
        print("PASS: 4. All tasks have a valid owner_id (no orphaned tasks).")
        passed += 1
    else:
        print(f"FAIL: 4. Orphaned tasks found: {orphans}")

    # 5. No task has owner_id = NULL
    cursor.execute("SELECT id FROM tasks WHERE owner_id IS NULL")
    null_owners = cursor.fetchall()
    if len(null_owners) == 0:
        print("PASS: 5. No task has owner_id = NULL.")
        passed += 1
    else:
        print(f"FAIL: 5. Tasks with NULL owner_id found: {null_owners}")

    # 6. At least one task exists
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    if count >= 1:
        print("PASS: 6. At least one task exists in the DB.")
        passed += 1
    else:
        print("FAIL: 6. No tasks found in the DB.")

    # 7. All task statuses are either 'open' or 'complete'
    cursor.execute("SELECT id, status FROM tasks WHERE status NOT IN ('open', 'complete')")
    bad_statuses = cursor.fetchall()
    if len(bad_statuses) == 0:
        print("PASS: 7. All task statuses are either 'open' or 'complete'.")
        passed += 1
    else:
        print(f"FAIL: 7. Tasks with invalid statuses found: {bad_statuses}")

    print("-" * 50)
    print(f"Summary: {passed}/{total} checks passed.")

    conn.close()

if __name__ == "__main__":
    run_validations()
