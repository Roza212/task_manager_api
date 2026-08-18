[![CI/CD Pipeline](https://github.com/Roza212/task_manager_api/actions/workflows/tests.yml/badge.svg)](https://github.com/Roza212/task_manager_api/actions/workflows/tests.yml)

# QA Task Manager API

A secure, fully-tested REST API built with FastAPI, SQLAlchemy, and SQLite. Features full JWT authentication, cross-user data isolation, and comprehensive CI/CD testing.

## Features
- **User Authentication:** Secure JWT-based signup and login (using `passlib` and `bcrypt`).
- **Task Management:** Complete CRUD functionality for user tasks.
- **Data Isolation:** Users can only access and modify their own tasks.
- **Automated Testing:** 31 comprehensive pytest tests with an HTML reporting dashboard.
- **CI/CD Pipeline:** Fully integrated GitHub Actions workflow for automated cloud testing.

## Running Locally

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Visit `http://localhost:8000/docs` to use the interactive Swagger UI.
4. Visit `http://localhost:8000/qa/dashboard` to view the QA Test Report dashboard.

## Running Tests
To execute the automated test suite locally and generate a new HTML report:
```bash
pytest tests/ -v --html=docs/test_report.html --self-contained-html
```
