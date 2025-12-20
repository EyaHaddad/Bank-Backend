"""
Comprehensive integration tests for User API endpoints.

This module tests all CRUD operations and edge cases for the /api/users endpoints.
"""
import os
import pytest

# Set test database URL before any imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
# Add testserver to allowed hosts for testing
os.environ["ALLOWED_HOSTS"] = '["localhost", "127.0.0.1", "testserver"]'

from fastapi.testclient import TestClient
from uuid import uuid4

from tests.test_db import engine, TestingSessionLocal
from src.main import app
from src.database.core import get_db, Base


# ============================================================================
# Test Setup and Fixtures
# ============================================================================

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
    from src.entities.user import User
    from src.entities.account import Account
    from src.entities.transaction import Transaction
    from src.entities.beneficiary import Beneficiary
    
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ============================================================================
# Helper Functions
# ============================================================================

def create_test_user(email: str = None, firstname: str = "Test", lastname: str = "User") -> dict:
    """Helper to create a test user and return the response data."""
    if email is None:
        email = f"test_{uuid4().hex[:8]}@example.com"
    
    payload = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "password": "SecureP@ssw0rd123",
    }
    response = client.post("/api/users/", json=payload)
    return response


def get_auth_token(email: str, password: str) -> str:
    """Helper to authenticate and get JWT token."""
    response = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


# ============================================================================
# Tests: CREATE User (POST /api/users/)
# ============================================================================

class TestCreateUser:
    """Tests for user creation endpoint."""

    def test_create_user_success(self):
        """Test successful user creation with valid data."""
        payload = {
            "firstname": "Alice",
            "lastname": "Wonderland",
            "email": f"alice_{uuid4().hex[:8]}@example.com",
            "password": "SecureP@ssw0rd123",
        }
        
        response = client.post("/api/users/", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["firstname"] == payload["firstname"]
        assert data["lastname"] == payload["lastname"]
        assert data["email"] == payload["email"]
        assert "id" in data
        assert "password" not in data  # Password should never be returned

    def test_create_user_duplicate_email(self):
        """Test that creating a user with duplicate email returns 409."""
        email = f"duplicate_{uuid4().hex[:8]}@example.com"
        
        # Create first user
        response1 = create_test_user(email=email)
        assert response1.status_code == 201
        
        # Try to create second user with same email
        response2 = create_test_user(email=email)
        assert response2.status_code == 409
        assert "already exists" in response2.json()["detail"].lower()

    def test_create_user_invalid_email(self):
        """Test that invalid email format returns 422."""
        payload = {
            "firstname": "Bob",
            "lastname": "Builder",
            "email": "invalid-email",
            "password": "SecureP@ssw0rd123",
        }
        
        response = client.post("/api/users/", json=payload)
        
        assert response.status_code == 422

    def test_create_user_missing_required_fields(self):
        """Test that missing required fields return 422."""
        # Missing firstname
        response = client.post("/api/users/", json={
            "lastname": "Test",
            "email": "test@example.com",
            "password": "password123"
        })
        assert response.status_code == 422

        # Missing email
        response = client.post("/api/users/", json={
            "firstname": "Test",
            "lastname": "User",
            "password": "password123"
        })
        assert response.status_code == 422


# ============================================================================
# Tests: READ Users (GET /api/users/ and GET /api/users/{id})
# ============================================================================

class TestGetUsers:
    """Tests for user retrieval endpoints."""

    def test_get_all_users(self):
        """Test retrieving all users."""
        # Create a user first
        create_test_user()
        
        response = client.get("/api/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_user_by_id_success(self):
        """Test retrieving a specific user by ID."""
        # Create user
        create_response = create_test_user()
        user_id = create_response.json()["id"]
        
        response = client.get(f"/api/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id

    def test_get_user_not_found(self):
        """Test that non-existent user returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        
        response = client.get(f"/api/users/{fake_uuid}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_user_invalid_uuid(self):
        """Test that invalid UUID format returns 422."""
        response = client.get("/api/users/not-a-valid-uuid")
        
        assert response.status_code == 422


# ============================================================================
# Tests: UPDATE User (PUT /api/users/{id})
# ============================================================================

class TestUpdateUser:
    """Tests for user update endpoint."""

    def test_update_user_firstname(self):
        """Test updating user's firstname."""
        # Create user
        create_response = create_test_user(firstname="Original")
        user_id = create_response.json()["id"]
        
        # Update firstname
        response = client.put(f"/api/users/{user_id}", json={
            "firstname": "Updated"
        })
        
        assert response.status_code == 200
        assert response.json()["firstname"] == "Updated"

    def test_update_user_lastname(self):
        """Test updating user's lastname."""
        create_response = create_test_user(lastname="Original")
        user_id = create_response.json()["id"]
        
        response = client.put(f"/api/users/{user_id}", json={
            "lastname": "Updated"
        })
        
        assert response.status_code == 200
        assert response.json()["lastname"] == "Updated"

    def test_update_user_multiple_fields(self):
        """Test updating multiple fields at once."""
        create_response = create_test_user()
        user_id = create_response.json()["id"]
        
        response = client.put(f"/api/users/{user_id}", json={
            "firstname": "NewFirst",
            "lastname": "NewLast"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["firstname"] == "NewFirst"
        assert data["lastname"] == "NewLast"

    def test_update_user_not_found(self):
        """Test that updating non-existent user returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        
        response = client.put(f"/api/users/{fake_uuid}", json={
            "firstname": "Test"
        })
        
        assert response.status_code == 404

    def test_update_user_partial_update(self):
        """Test that partial updates don't affect other fields."""
        create_response = create_test_user(firstname="Keep", lastname="This")
        user_id = create_response.json()["id"]
        original_lastname = create_response.json()["lastname"]
        
        # Update only firstname
        response = client.put(f"/api/users/{user_id}", json={
            "firstname": "Changed"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["firstname"] == "Changed"
        assert data["lastname"] == original_lastname  # Should remain unchanged


# ============================================================================
# Tests: DELETE User (DELETE /api/users/{id})
# ============================================================================

class TestDeleteUser:
    """Tests for user deletion endpoint."""

    def test_delete_user_success(self):
        """Test successful user deletion."""
        # Create user
        create_response = create_test_user()
        user_id = create_response.json()["id"]
        
        # Delete user
        response = client.delete(f"/api/users/{user_id}")
        
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self):
        """Test that deleting non-existent user returns 404."""
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        
        response = client.delete(f"/api/users/{fake_uuid}")
        
        assert response.status_code == 404

    def test_delete_user_twice(self):
        """Test that deleting same user twice returns 404 on second attempt."""
        # Create and delete user
        create_response = create_test_user()
        user_id = create_response.json()["id"]
        
        client.delete(f"/api/users/{user_id}")
        
        # Try to delete again
        response = client.delete(f"/api/users/{user_id}")
        assert response.status_code == 404


# ============================================================================
# Tests: Change Password (POST /api/users/me/change-password)
# ============================================================================

class TestChangePassword:
    """Tests for password change endpoint."""

    def test_change_password_requires_authentication(self):
        """Test that change password requires authentication."""
        response = client.post("/api/users/me/change-password", json={
            "current_password": "old",
            "new_password": "new",
            "new_password_confirm": "new"
        })
        
        # Should return 401 without auth token
        assert response.status_code == 401

    # Note: Full change password tests require authentication setup
    # which depends on your auth implementation


# ============================================================================
# Tests: Get Current User (GET /api/users/me)
# ============================================================================

class TestGetCurrentUser:
    """Tests for current user endpoint."""

    def test_get_me_requires_authentication(self):
        """Test that /me endpoint requires authentication."""
        response = client.get("/api/users/me")
        
        assert response.status_code == 401


# ============================================================================
# Tests: Edge Cases and Security
# ============================================================================

class TestEdgeCasesAndSecurity:
    """Tests for edge cases and security considerations."""

    def test_password_not_in_response(self):
        """Test that password/hash is never returned in any response."""
        create_response = create_test_user()
        assert "password" not in create_response.json()
        assert "password_hash" not in create_response.json()
        
        user_id = create_response.json()["id"]
        get_response = client.get(f"/api/users/{user_id}")
        assert "password" not in get_response.json()
        assert "password_hash" not in get_response.json()

    def test_sql_injection_in_email(self):
        """Test that SQL injection attempts are handled safely."""
        malicious_email = "test'; DROP TABLE users; --@example.com"
        
        response = client.post("/api/users/", json={
            "firstname": "Test",
            "lastname": "User",
            "email": malicious_email,
            "password": "SecureP@ssw0rd123"
        })
        
        # Should fail validation, not cause SQL injection
        assert response.status_code == 422

    def test_xss_in_names(self):
        """Test that XSS attempts in names are stored safely."""
        xss_payload = "<script>alert('xss')</script>"
        
        response = create_test_user(firstname=xss_payload)
        
        # The data should be stored as-is (sanitization is frontend's job)
        # but it should not cause server errors
        assert response.status_code == 201

    def test_very_long_input(self):
        """Test handling of very long input strings."""
        long_string = "a" * 10000
        
        response = client.post("/api/users/", json={
            "firstname": long_string,
            "lastname": "Test",
            "email": "long@example.com",
            "password": "SecureP@ssw0rd123"
        })
        
        # Should either succeed or return validation error, not crash
        assert response.status_code in [201, 422]

    def test_unicode_in_names(self):
        """Test that unicode characters are handled properly."""
        response = create_test_user(
            firstname="日本語",
            lastname="Müller"
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["firstname"] == "日本語"
        assert data["lastname"] == "Müller"

    def test_empty_string_values(self):
        """Test handling of empty string values."""
        response = client.post("/api/users/", json={
            "firstname": "",
            "lastname": "Test",
            "email": f"empty_{uuid4().hex[:8]}@example.com",
            "password": "SecureP@ssw0rd123"
        })
        
        # Depending on validation, should either fail or succeed
        # but should not crash
        assert response.status_code in [201, 422]
