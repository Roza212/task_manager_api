[![CI/CD Pipeline](https://github.com/Roza212/task_manager_api/actions/workflows/tests.yml/badge.svg)](https://github.com/Roza212/task_manager_api/actions/workflows/tests.yml)

# QA Task Manager REST API

Welcome to my QA portfolio project! This repository contains a fully functional **Task Manager REST API** that I built from scratch using FastAPI, and then rigorously tested through a comprehensive Quality Assurance process. 

The goal of this project was not just to build an API, but to demonstrate a complete end-to-end software testing lifecycle. It features a formal test plan, extensive manual testing, automated pytest suites, raw SQL data validation, and a fully integrated CI/CD pipeline.

---

## 🛠️ Tech Stack

### Development
- **Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens), `passlib` with `bcrypt`

### Quality Assurance & Testing
- **Test Framework:** `pytest` (using `TestClient` for API mocking)
- **CI/CD:** GitHub Actions (Ubuntu runner)
- **Test Reporting:** `pytest-html` for beautiful, self-contained HTML reports
- **Data Validation:** Raw SQL queries via Python `sqlite3`

---

## 🧪 Testing Accomplished

To ensure enterprise-grade stability, this project was subjected to multiple layers of testing:
1. **Test Planning:** Wrote a formal Test Plan detailing the testing strategy and scenarios.
2. **Manual Testing:** Executed 35 distinct manual test cases verifying authentication flows, task CRUD operations, and cross-user isolation.
3. **Automated Testing:** Programmed 31 automated tests using `pytest`. Leveraged advanced features like `@pytest.mark.parametrize` for negative payload testing and modular database fixtures.
4. **SQL Validation:** Validated database integrity, constraints, and relational mapping using 7 raw SQL queries.
5. **Continuous Integration:** Configured a GitHub Actions CI/CD pipeline to automatically run the entire test suite on every push to the `main` branch.

---

## 📁 Folder Structure

```text
.
├── .github/workflows/   # CI/CD Pipeline Configuration (tests.yml)
├── app/                 # FastAPI Source Code
│   ├── main.py          # Application Entrypoint & DB Initialization
│   ├── auth.py          # JWT Generation & Password Hashing
│   ├── database.py      # SQLAlchemy Engine & Session Setup
│   ├── models.py        # Database Tables (User, Task)
│   ├── schemas.py       # Pydantic Validation Models
│   └── routers/         # API Route Controllers
├── docs/                # Project Documentation & Test Reports
├── scripts/             # Python & SQL Validation Scripts
├── templates/           # HTML Templates (QA Dashboard)
├── tests/               # Automated Pytest Suite
│   ├── conftest.py      # Pytest Fixtures & Test DB Setup
│   ├── test_auth.py     # Authentication Endpoints Tests
│   └── test_tasks.py    # Task Management Endpoints Tests
├── Test_Cases.xlsx      # 35 Documented Manual Test Cases
└── requirements.txt     # Python Dependencies
```

---

## 🚀 Setup & Run Instructions

To run this API on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Roza212/task_manager_api.git
   cd task_manager_api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # On Windows
   source venv/bin/activate       # On Mac/Linux
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Explore the API:**
   - Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Visual QA Dashboard: [http://localhost:8000/qa/dashboard](http://localhost:8000/qa/dashboard)

---

## 🤖 How to Run Automated Tests

The automated test suite uses a completely isolated, temporary SQLite database (`test_qa_tasks.db`) to ensure tests do not pollute your main application data.

To run the test suite and generate a fresh HTML report:
```bash
pytest tests/ -v --html=docs/test_report.html --self-contained-html
```
*(You can view the generated `test_report.html` file directly in the browser or via the local QA Dashboard endpoint.)*

---

## 📊 How to Run SQL Validation

To verify the integrity of the live database, I wrote a suite of raw SQL queries that bypass the ORM to check for orphaned tasks, duplicate emails, and correct foreign key mapping.

To execute the database validation checks programmatically:
```bash
python scripts/validate_db.py
```
*(This script will connect to `qa_tasks.db`, execute the queries in `scripts/sql_validation.sql`, and print a Pass/Fail summary to the console.)*

---

## 💡 What I Learned

Building and QA-ing this project from the ground up taught me a tremendous amount about the intersection of software development and quality assurance:
- **Test Isolation:** I learned the critical importance of using dedicated test databases and Pytest fixtures (`conftest.py`) to wipe tables between tests, preventing state leakage and false negatives.
- **Parametrization:** I discovered how much time can be saved by using `@pytest.mark.parametrize` to run a single test function against multiple invalid JSON payloads, keeping the test suite DRY (Don't Repeat Yourself).
- **CI/CD Debugging:** I learned that CI/CD environments (like Ubuntu runners) are highly sensitive to file encoding (like Windows UTF-16 BOMs) and cross-platform pathing, requiring careful configuration of `requirements.txt` and GitHub Actions YML files.
- **Security Testing:** Writing negative test cases to intentionally try and access other users' tasks (Data Isolation/Authorization testing) reinforced the importance of verifying `403 Forbidden` responses, not just `200 OK` success paths.
