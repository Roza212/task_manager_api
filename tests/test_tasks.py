import pytest
from fastapi.testclient import TestClient

# =======================
# CREATE TASK (POST /tasks)
# =======================

def test_create_task_valid(client: TestClient, auth_headers: dict):
    response = client.post("/tasks", json={"title": "Buy groceries", "description": "Milk, eggs, bread"}, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["status"] == "open"
    assert "id" in data
    assert "owner_id" in data

def test_create_task_unauthorized(client: TestClient):
    response = client.post("/tasks", json={"title": "Unauthorized task"})
    assert response.status_code == 401

def test_create_task_missing_title(client: TestClient, auth_headers: dict):
    response = client.post("/tasks", json={"description": "Missing title"}, headers=auth_headers)
    assert response.status_code == 422

def test_create_task_title_too_long(client: TestClient, auth_headers: dict):
    long_title = "A" * 201
    response = client.post("/tasks", json={"title": long_title}, headers=auth_headers)
    assert response.status_code == 422

# =======================
# GET ALL TASKS (GET /tasks)
# =======================

def test_get_tasks_empty(client: TestClient, auth_headers: dict):
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_get_tasks_with_data(client: TestClient, auth_headers: dict):
    client.post("/tasks", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/tasks", json={"title": "Task 2"}, headers=auth_headers)
    
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_get_tasks_unauthorized(client: TestClient):
    response = client.get("/tasks")
    assert response.status_code == 401

# =======================
# GET TASK BY ID (GET /tasks/{id})
# =======================

def test_get_task_by_id_valid(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks", json={"title": "Specific task"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Specific task"

def test_get_task_by_id_not_found(client: TestClient, auth_headers: dict):
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404

def test_get_task_by_id_unauthorized(client: TestClient):
    response = client.get("/tasks/1")
    assert response.status_code == 401

# =======================
# UPDATE TASK (PUT /tasks/{id})
# =======================

def test_update_task_valid(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks", json={"title": "Old title"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    response = client.put(f"/tasks/{task_id}", json={"title": "New title", "status": "in_progress"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["status"] == "in_progress"

def test_update_task_partial(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks", json={"title": "Unchanged title", "description": "Original description"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    # Update only the description
    response = client.put(f"/tasks/{task_id}", json={"description": "Updated description"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Unchanged title"
    assert data["description"] == "Updated description"

def test_update_task_not_found(client: TestClient, auth_headers: dict):
    response = client.put("/tasks/9999", json={"title": "Updated"}, headers=auth_headers)
    assert response.status_code == 404

def test_update_task_invalid_data(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks", json={"title": "Valid task"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    # Title too long
    response = client.put(f"/tasks/{task_id}", json={"title": "A" * 201}, headers=auth_headers)
    assert response.status_code == 422

def test_update_task_unauthorized(client: TestClient):
    response = client.put("/tasks/1", json={"title": "Unauthorized update"})
    assert response.status_code == 401

# =======================
# DELETE TASK (DELETE /tasks/{id})
# =======================

def test_delete_task_valid(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks", json={"title": "To be deleted"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify it is deleted
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_task_not_found(client: TestClient, auth_headers: dict):
    response = client.delete("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404

def test_delete_task_unauthorized(client: TestClient):
    response = client.delete("/tasks/1")
    assert response.status_code == 401

# =======================
# SECURITY: CROSS-USER DATA ISOLATION
# =======================

def test_security_get_other_user_task(client: TestClient, auth_headers: dict, second_user_headers: dict):
    # User 1 creates a task
    create_response = client.post("/tasks", json={"title": "User 1 Task"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    # User 2 tries to read it
    response = client.get(f"/tasks/{task_id}", headers=second_user_headers)
    assert response.status_code == 403

def test_security_update_other_user_task(client: TestClient, auth_headers: dict, second_user_headers: dict):
    # User 1 creates a task
    create_response = client.post("/tasks", json={"title": "User 1 Task"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    # User 2 tries to update it
    response = client.put(f"/tasks/{task_id}", json={"title": "User 2 Hacker"}, headers=second_user_headers)
    assert response.status_code == 403

def test_security_delete_other_user_task(client: TestClient, auth_headers: dict, second_user_headers: dict):
    # User 1 creates a task
    create_response = client.post("/tasks", json={"title": "User 1 Task"}, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    # User 2 tries to delete it
    response = client.delete(f"/tasks/{task_id}", headers=second_user_headers)
    assert response.status_code == 403
