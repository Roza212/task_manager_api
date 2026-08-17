import pytest
from fastapi.testclient import TestClient

def test_signup_valid(client: TestClient):
    response = client.post("/auth/signup", json={"email": "newuser@example.com", "password": "password123"})
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert data["email"] == "newuser@example.com"
    assert "password" not in data

def test_signup_duplicate_email(client: TestClient):
    # First signup
    client.post("/auth/signup", json={"email": "duplicate@example.com", "password": "password123"})
    
    # Second signup with the same email
    response = client.post("/auth/signup", json={"email": "duplicate@example.com", "password": "password123"})
    assert response.status_code == 400

@pytest.mark.parametrize("payload, expected_status", [
    ({"email": "test@example.com"}, 422), # Missing password
    ({"password": "password123"}, 422), # Missing email
    ({"email": "notanemail", "password": "password123"}, 422), # Invalid email format
    ({"email": "", "password": "password123"}, 422), # Empty email
])
def test_signup_invalid_data(client: TestClient, payload, expected_status):
    response = client.post("/auth/signup", json=payload)
    assert response.status_code == expected_status


def test_login_valid(client: TestClient):
    # Setup: Create a user first
    client.post("/auth/signup", json={"email": "login@example.com", "password": "password123"})
    
    # Note: Login endpoint uses form data (OAuth2PasswordRequestForm) instead of JSON
    response = client.post("/auth/login", data={"username": "login@example.com", "password": "password123"})
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client: TestClient):
    # Setup: Create a user first
    client.post("/auth/signup", json={"email": "wrongpass@example.com", "password": "password123"})
    
    # Login with incorrect password
    response = client.post("/auth/login", data={"username": "wrongpass@example.com", "password": "wrongpassword"})
    assert response.status_code == 401

def test_login_nonexistent_email(client: TestClient):
    # Login with an unregistered email
    response = client.post("/auth/login", data={"username": "nonexistent@example.com", "password": "password123"})
    assert response.status_code == 401

def test_login_missing_password(client: TestClient):
    # Login with missing password in form data
    response = client.post("/auth/login", data={"username": "missingpass@example.com"})
    assert response.status_code == 422
