# Test Plan: Task Manager REST API

## 1. Objective

The primary objective of this testing phase is to ensure the Task Manager API correctly handles user authentication and all CRUD (Create, Read, Update, Delete) operations for tasks without crashing or leaking data. Testing will validate that the endpoints are functionally correct, handle errors gracefully, and enforce basic security measures.

## 2. Scope

The testing efforts will cover the following functional and security areas:

- **Endpoint Functionality ("Happy Path"):** Verifying the 7 core endpoints (`POST /signup`, `POST /login`, `POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`).
- **Input Validation ("Sad Path"):** Testing API behavior with invalid data (e.g., missing required fields, invalid email formats, malformed JSON).
- **Authentication Validation:** Verifying that a valid token is required for all `/tasks` endpoints and that invalid/expired tokens are rejected.
- **Data Isolation (Authorization):** Ensuring users can only read, update, or delete tasks they own, and cannot access tasks belonging to other users.
- **HTTP Status Codes:** Confirming the API returns standard, accurate HTTP status codes (e.g., 200, 201, 400, 401, 403, 404).

## 3. Out of Scope

To focus on core functionality and security, the following areas are intentionally excluded from this test cycle:

- Performance, stress, and load testing.
- Advanced security/penetration testing (e.g., SQL injection, DDoS simulation).
- Complex database structural testing (Database validation will be strictly limited to verifying basic data persistence during API CRUD operations).
- Frontend or User Interface (UI) testing.
- Rate limiting, throttling, or third-party integrations (e.g., email delivery).

## 4. Test Approach

The testing strategy for the FastAPI Task Manager API will rely on a hybrid approach, starting with manual exploratory testing via the built-in Swagger UI to quickly validate core endpoint behavior.

Once baseline functionality is confirmed, I will develop a comprehensive automated test suite using `pytest` and FastAPI's `TestClient` to cover both positive and negative scenarios. Test data will be dynamically generated (e.g., using dynamic strings or libraries like `Faker`) to ensure unique inputs per run, and the SQLite test database will be wiped and recreated before each automated test suite execution to maintain a clean, predictable environment.

To ensure data integrity, these automated tests will be supplemented with direct SQL queries against the SQLite database to verify correct backend storage. Finally, the entire automated suite will be integrated into a GitHub Actions CI/CD pipeline to guarantee that all endpoints remain stable with every future code update.

## 5. Environment & Tools

- **Application Framework:** FastAPI
- **Manual API Testing:** Swagger UI (auto-generated at `/docs`)
- **Automated Testing:** Python with `pytest` and `TestClient`
- **Database Tool:** SQLite (and DB Browser for SQLite for manual verification)
- **CI/CD Pipeline:** GitHub Actions

## 6. Entry Criteria

Testing execution will begin only when the following conditions are met:

- **The API is runnable:** The FastAPI server starts locally without crashing.
- **The Database is connected:** The local SQLite database is configured, and the `Users` and `Tasks` tables exist.
- **Documentation is ready:** The Swagger UI (`/docs`) is accessible and lists all 7 endpoints with expected formats.
- **Tools are configured:** Testing tools (`pytest`, DB browser) are installed and configured.
- **The Test Plan is finished:** All "In Scope" test cases have been drafted and reviewed.

## 7. Exit Criteria

Testing will be considered complete, and the release candidate approved, when the following conditions are met:

- **100% Test Execution:** All planned manual and automated test cases have been executed.
- **No Critical Bugs:** There are no "High" or "Critical" severity bugs unresolved (e.g., server crashes, authorization bypasses).
- **Pipeline is Green:** All automated `pytest` scripts run and pass 100% successfully in the GitHub Actions CI/CD pipeline.
- **Bugs are Documented:** Minor, non-blocking bugs are documented as GitHub Issues.
- **Deliverables are Published:** This Test Plan, the formal Test Cases, and Bug Reports are published in the project's GitHub repository.

## 8. Defect Management

All defects discovered during manual and automated testing will be logged as individual "Issues" in the project's GitHub repository. To ensure clear communication and reproducibility, every bug report will adhere to the following standard template:

- **Title:** A concise, descriptive summary of the issue (e.g., "BUG: 500 Internal Error when POST /tasks is missing title").
- **Environment:** Details of where the bug was found (e.g., Swagger UI manual test, `pytest` automated run).
- **Steps to Reproduce:** A numbered, step-by-step list of the exact actions and data payloads used to trigger the bug.
- **Expected Result:** What the API _should_ have done according to the requirements (including the expected HTTP status code).
- **Actual Result:** What the API _actually_ did (including the actual HTTP status code and exact error message).
- **Severity:** Categorized as Critical, High, Medium, or Low to help prioritize fixes.
- **Evidence:** Code snippets of the JSON payload, screenshots of the Swagger UI, or terminal output demonstrating the failure.
