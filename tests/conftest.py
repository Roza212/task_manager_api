import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# 1. Create a separate SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_qa_tasks.db"

# connect_args={"check_same_thread": False} is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # 2. Before each test, wipe and recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # 3. Provide a client fixture overriding the get_db dependency
    def override_get_db():
        try:
            yield session
        finally:
            pass # Session is closed in the session fixture above
            
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    # Clean up overrides after test
    app.dependency_overrides.clear()

def _create_and_login_user(client: TestClient) -> dict:
    """Helper function to create a unique user and get auth headers."""
    unique_id = uuid.uuid4().hex
    email = f"testuser_{unique_id}@example.com"
    password = "testpassword123!"
    
    # Sign up
    client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    
    # Log in (OAuth2PasswordRequestForm expects form data, not json)
    login_res = client.post(
        "/auth/login",
        data={"username": email, "password": password}
    )
    
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture()
def auth_headers(client):
    """
    4. Provide a fixture that returns authentication headers 
    for a newly created unique user.
    """
    return _create_and_login_user(client)

@pytest.fixture()
def second_user_headers(client):
    """
    5. Provide a fixture that returns authentication headers 
    for a second, separate unique user (useful for cross-user tests).
    """
    return _create_and_login_user(client)
