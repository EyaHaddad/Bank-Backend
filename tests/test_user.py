"""Integration tests for user endpoints."""
import os
import pytest

# Set test database URL before any imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient

from tests.test_db import engine, TestingSessionLocal
from src.main import app
from src.database.core import get_db, Base


def override_get_db():
    """Override the database dependency with test database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Create test database tables before tests and clean up after."""
    # Import all models to register them with Base metadata
    from src.entities.user import User
    from src.entities.account import Account
    from src.entities.transaction import Transaction
    from src.entities.beneficiary import Beneficiary
    
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_and_get_user():
    payload = {
        "firstname": "Test",
        "lastname": "User",
        "email": "test.user@example.com",
        "password": "s3cretP@ssw0rd",
    }

    response = client.post("/api/users/", json=payload)
    if response.status_code != 201:
        print(f"Error: {response.json()}")
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == payload["email"]
    assert created_user["firstname"] == payload["firstname"]
    assert created_user["lastname"] == payload["lastname"]
    assert "id" in created_user

    user_id = created_user["id"]
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200
    fetched_user = get_response.json()
    assert fetched_user["id"] == user_id
    assert fetched_user["email"] == payload["email"]


def test_user_not_found_returns_404():
    missing_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/api/users/{missing_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"