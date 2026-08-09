# QA Task Manager API - Setup Documentation

## Project Structure

A new FastAPI project has been set up from scratch in the `qa-task-manager-api` directory with the following structure:

```text
qa-task-manager-api/
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


