-- ==============================================================================
-- Phase 5: SQL Validation Queries for Task Manager Database
-- ==============================================================================

-- 1. Confirm a specific user exists by email
-- What it checks: Verifies that a user account was properly inserted and can be retrieved by their unique email.
-- Expected result: 1 row returned with the user's id, email, and hashed_password.
SELECT id, email, hashed_password 
FROM users 
WHERE email = 'testuser@example.com';


-- 2. Check no duplicate emails in users table
-- What it checks: Groups all users by their email and returns any email that appears more than once.
-- Expected result: 0 rows returned (the unique constraint on the email column should prevent duplicates).
SELECT email, COUNT(*) as email_count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;


-- 3. Confirm a task exists by ID
-- What it checks: Retrieves a specific task using its primary key.
-- Expected result: 1 row returned with the task details (title, description, status, etc.) if the task exists.
SELECT id, title, description, status, due_date, owner_id 
FROM tasks 
WHERE id = 1;


-- 4. Confirm a task belongs to correct owner_id
-- What it checks: Uses an INNER JOIN to fetch a task alongside its owner's email to verify the foreign key relationship.
-- Expected result: 1 row returned showing the task details properly linked to the expected user's email.
SELECT t.id as task_id, t.title, t.owner_id, u.email as owner_email
FROM tasks t
JOIN users u ON t.owner_id = u.id
WHERE t.id = 1;


-- 5. Find orphaned tasks (owner_id with no matching user)
-- What it checks: Uses a LEFT JOIN to find any tasks that point to a non-existent user ID.
-- Expected result: 0 rows returned. (This proves the foreign key constraint `owner_id -> users.id` is strictly enforced).
SELECT t.id, t.title, t.owner_id
FROM tasks t
LEFT JOIN users u ON t.owner_id = u.id
WHERE u.id IS NULL;


-- 6. Confirm deleted task no longer exists
-- What it checks: Attempts to retrieve a task that has been deleted from the database.
-- Expected result: 0 rows returned.
SELECT id, title, status
FROM tasks 
WHERE id = 999; -- Assuming 999 is the ID of a recently deleted task


-- 7. Check no tasks with empty or NULL title exist
-- What it checks: Scans the tasks table for any records where the required `title` field was left blank or NULL.
-- Expected result: 0 rows returned. (This proves the NOT NULL constraint and API-level Pydantic length validations are working).
SELECT id, owner_id, title 
FROM tasks 
WHERE title IS NULL OR title = '';
