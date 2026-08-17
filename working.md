# QA Task Manager API - Setup Documentation

## Project Structure

A new FastAPI project has been set up from scratch in the repository root directory with the following structure:

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       └── tasks.py
├── docs/
│   └── Test_Plan.md
├── tests/
│   └── __init__.py
├── requirements.txt
├── .gitignore
└── README.md
```

## File Explanations

Here is a breakdown of what each file's job is within the architecture:

- **`app/__init__.py`**: Marks the `app` directory as a Python package. Usually left empty.
- **`app/main.py`**: The main entry point of the FastAPI application. It initializes the FastAPI instance (`app = FastAPI()`) and wires up routers. A basic `GET /` endpoint is included to verify the API is running.
- **`app/database.py`**: Manages the database connection and session creation using SQLAlchemy (e.g., setting up the `engine` and `SessionLocal`).
- **`app/models.py`**: Defines the SQLAlchemy ORM models, representing the database tables and relationships (e.g., `User` and `Task` classes).
- **`app/schemas.py`**: Defines Pydantic models (schemas) used for data validation, serialization, and deserialization of API requests and responses.
- **`app/auth.py`**: Contains authentication and authorization logic, including JWT token generation/validation (using `python-jose`), password hashing (using `passlib`), and current user dependency injection.
- **`app/routers/__init__.py`**: Marks the `routers` directory as a package.
- **`app/routers/users.py`**: Contains the API route definitions related to user operations (e.g., register, login, get profile).
- **`app/routers/tasks.py`**: Contains the API route definitions related to task operations (e.g., create task, get tasks, update task).
- **`docs/Test_Plan.md`**: A documentation file reserved for detailing the testing strategy, scenarios, and QA procedures for the project.
- **`tests/__init__.py`**: Marks the `tests` directory as a package, allowing test runners like pytest to discover the test files.
- **`requirements.txt`**: Lists all the Python dependencies required to run the project. We included `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `python-jose[cryptography]`, `passlib[bcrypt]`, `httpx`, `pytest`, and `pytest-html`.
- **`.gitignore`**: Tells Git which files and directories to ignore in version control (like `__pycache__`, `venv`, environment variables `.env`, and IDE configuration files).
- **`README.md`**: The main documentation file for the repository, explaining what the project is, how to set it up, and how to run it.

## Database & Models Configuration

The SQLAlchemy database and ORM models have been implemented and connected to the main application:

- **`app/models.py`**:
  - `User` model: `id` (PK), `email` (unique, not null), `hashed_password` (not null).
  - `Task` model: `id` (PK), `title` (max 200, not null), `description` (optional), `status` (default 'open'), `due_date` (optional), `owner_id` (FK to `users.id`).
  - Added bidirectional SQLAlchemy relationships (`tasks` and `owner`).

- **`app/database.py`**:
  - Configured to use a SQLite database file named `qa_tasks.db`.
  - Initialized SQLAlchemy `engine` and `SessionLocal`.
  - Added a `get_db()` dependency generator to safely yield and close database sessions.

- **`app/main.py`**:
  - Integrated the database connection by calling `models.Base.metadata.create_all(bind=engine)`, which ensures the tables are created automatically on application startup.

## Pydantic Schemas

Pydantic schemas have been implemented for data validation and serialization using Pydantic v2 syntax:

- **`app/schemas.py`**:
  - **Auth**: `Token` schema for JWT login responses.
  - **Users**: `UserCreate` (with email validation via `EmailStr`) and `UserResponse` (hides password).
  - **Tasks**: `TaskCreate` (requires title with 1-200 chars), `TaskUpdate` (all fields optional), and `TaskResponse`.
  - Added `model_config = ConfigDict(from_attributes=True)` to response schemas for seamless SQLAlchemy integration.

## Authentication & Security

Implemented JWT-based authentication and password hashing in `app/auth.py`.

- **`app/auth.py`**:
  - `hash_password(plain_password)`: Uses `passlib` with `bcrypt` to securely hash user passwords.
  - `verify_password(plain_password, hashed_password)`: Verifies plaintext passwords against their stored hashes.
  - `create_access_token(data)`: Generates a JWT access token using `python-jose` (HS256 algorithm) with a 30-minute expiry.
  - `get_current_user()`: A FastAPI dependency that extracts the `Bearer` token from the `Authorization` header, decodes it, and retrieves the corresponding `User` object from the database, raising 401 Unauthorized for missing, invalid, or expired tokens.

## API Routers

User authentication and Task CRUD endpoints have been implemented and registered.

- **`app/routers/users.py`**:
  - Registered an `APIRouter` with the `/auth` prefix.
  - `POST /auth/signup`: Accepts email and password. Validates that the email is not already in use. Hashes the password and saves the new user to the database. Returns `201 Created` with the `UserResponse` schema.
  - `POST /auth/login`: Accepts email and password. Validates credentials. Returns a JWT bearer token upon success or a `401 Unauthorized` if invalid.

- **`app/routers/tasks.py`**:
  - All endpoints use the `get_current_user` dependency to require a valid JWT token.
  - `POST /tasks`: Creates a new task. The `owner_id` is automatically set to the current user's ID, and `status` to "open". Returns `201 Created`.
  - `GET /tasks`: Retrieves all tasks belonging to the current user. Returns an empty list if no tasks exist.
  - `GET /tasks/{task_id}`: Fetches a specific task, enforcing data isolation (403 Forbidden if not owned by user) and existence (404 Not Found).
  - `PUT /tasks/{task_id}`: Partially updates a task (only provided fields). Retains 404/403 authorization checks.
  - `DELETE /tasks/{task_id}`: Deletes a task. Returns a success message.

- **`app/main.py`**:
  - Included the `users.router` and `tasks.router` so the endpoints are active on the application.

## Version Control

- **Git Initialization**: Initialized a local Git repository.
- **Root `.gitignore`**: Added a `.gitignore` at the root directory to safely exclude the `venv/` virtual environment, `.pytest_cache/`, and `__pycache__/` from version control.
- **GitHub Push**: Committed all project foundation files and pushed the `main` branch to the remote repository.

## Application Configuration

- **`app/main.py`**:
  - Implemented `CORSMiddleware` configured to allow all origins (`"*"`) for initial development.
  - Registered `users.router` and `tasks.router`.
  - Upgraded the root `GET /` endpoint to serve as a proper health check.

## Bug Fixes

- **`app/models.py`**: Fixed a syntax error where `primary key=True` was used instead of `primary_key=True` on the `id` columns.
- **Dependencies**: Resolved a `ModuleNotFoundError: No module named 'passlib'` error by fully installing all dependencies from `requirements.txt` (which included `passlib[bcrypt]`, `pytest`, etc. that were missing from the initial fast setup).
- **Passlib/Bcrypt Bug**: Fixed a `ValueError: password cannot be longer than 72 bytes` crash on login/signup by downgrading `bcrypt` to `3.2.2` in `requirements.txt` because `passlib 1.7.4` is incompatible with `bcrypt 4.0.0+`.
- **Swagger UI Authentication**: Refactored the `POST /auth/login` endpoint in `users.py` to use `OAuth2PasswordRequestForm` (form-data) instead of JSON. This natively integrates with FastAPI's OAuth2 scheme, enabling the green "Authorize" button in Swagger UI to handle the entire login flow automatically.

*(These bug fixes have been committed and pushed to the `main` branch of the GitHub repository.)*

## Manual Testing Documentation

- **Smoke Tests**: Created a new folder `qa-task-manager-api/docs/test` and added `smoke_test1.md`. This file documents the manual verification steps for the authentication and task CRUD workflow using the Swagger UI, including exact JSON payloads.
- **Automated Smoke Test**: Created and executed `smoke_test.py` to programmatically verify the end-to-end API workflow (Signup -> Login -> Bearer Token Authentication -> Create Task -> Fetch Task).

## Repository Cleanup

- **GitIgnore & Untracking**: Removed unprofessional local files from version control (`qa_tasks.db`, `smoke_test.py`, and the `docs/test/` manual testing folder) by untracking them and adding them to `.gitignore`.
- **Untracked `fix.md`**: Removed `fix.md` from version control as requested to keep the repository professional.

## Troubleshooting

- **Uvicorn `ModuleNotFoundError: No module named 'app'`**: This error occurs when starting the server from a directory that does not contain the `app` folder. This issue was resolved by moving all backend files to the repository root, so `uvicorn app.main:app --reload` now works immediately.
- **Pydantic `ImportError: email-validator is not installed`**: This happens because `EmailStr` in the Pydantic schemas requires the `email-validator` package, which was missing. Added `email-validator` to `requirements.txt`.
- **Pytest `TypeError: Client.__init__() got an unexpected keyword argument 'app'`**: This happens due to a version incompatibility between older versions of Starlette (used by FastAPI's `TestClient`) and newer versions of `httpx` (>=0.28.0) which removed the `app` keyword argument. This was resolved by explicitly downgrading and pinning `httpx==0.27.2` via `pip install httpx==0.27.2`.

## Pytest Configuration

The new testing setup structure includes the following files:
```text
.
├── tests/
│   ├── __init__.py        ← already exists
│   ├── conftest.py        ← NEW: shared fixtures
│   ├── test_auth.py       ← NEW: signup + login tests
│   └── test_tasks.py      ← NEW: task CRUD + security tests
├── pytest.ini             ← NEW: pytest config
└── requirements.txt       ← add pytest-html if not there
```

- **`pytest.ini`**: Created to configure pytest default options (verbose, standard output enabled, and HTML report generation) and point to the `tests` directory.
- **`tests/conftest.py`**: Configured pytest fixtures for tests. It uses a separate SQLite test database (`test_qa_tasks.db`), wipes and recreates tables per test, mocks the `get_db` FastAPI dependency with `TestClient`, and supplies `auth_headers` and `second_user_headers` for isolated cross-user testing.
- **`tests/test_auth.py`**: Created automated tests for the authentication endpoints. Covers valid signup (returns 201), duplicate email protection (400), and parametrized negative testing for missing or invalid signup payloads (422). Also covers login with valid credentials (returns 200 with access token), wrong password (401), non-existent email (401), and missing form data (422).
- **`tests/test_tasks.py`**: Created 21 automated tests for the task CRUD endpoints, including creating, listing, fetching, updating, and deleting tasks, checking for proper validation (e.g., 422 for too long titles), and ensuring correct cross-user data isolation and authorization (403 Forbidden for operating on someone else's tasks).
- **Test Reporting**: Generated a complete test report successfully by running `pytest tests/ -v --html=docs/test_report.html --self-contained-html`, which created a self-contained HTML report at `docs/test_report.html` with all 31 tests passing beautifully.

## SQL Validation (Phase 5)

- **`sql_validation.sql`**: Created a suite of 7 SQL queries to manually verify database integrity and constraints. The queries check for user existence, duplicate emails, task existence, foreign key mapping (task to owner), orphaned tasks, proper deletion handling, and NOT NULL/empty title constraints.
- **`validate_db.py`**: Created a Python script that connects to `qa_tasks.db` using `sqlite3` to automatically execute the 7 SQL validation checks programmatically and print out PASS/FAIL summaries.
