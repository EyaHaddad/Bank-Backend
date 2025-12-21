"""
Unit tests for authentication services.

This module tests password hashing, token generation/verification,
user authentication and registration.
"""
import os
import pytest
from datetime import timedelta
from uuid import uuid4

# Set test environment before imports
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ALLOWED_HOSTS"] = '["localhost", "127.0.0.1", "testserver"]'

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from src.modules.auth import service as auth_service
from src.modules.auth.schemas import RegisterUserRequest, LoginUserRequest
from src.modules.auth.exceptions import AuthenticationError, InvalidCredentialError, DuplicateEmailError
from src.models.user import User
from src.infrastructure.database import Base


# ============================================================================
# Test Database Setup
# ============================================================================

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Import all entities to register them
    from src.models.user import User
    from src.models.account import Account
    from src.models.transaction import Transaction
    from src.models.beneficiary import Beneficiary
    
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Create a test user with hashed password."""
    return User(
        firstname="Test",
        lastname="User",
        email="test@example.com",
        password_hash=auth_service.get_password_hash("password123"),
    )


# ============================================================================
# Tests: Password Hashing
# ============================================================================

class TestPasswordHashing:
    """Tests for password hashing and verification."""

    def test_get_password_hash_returns_hash(self):
        """Test that get_password_hash returns a valid hash."""
        password = "SecureP@ssw0rd"
        hashed = auth_service.get_password_hash(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Test verifying correct password returns True."""
        password = "password123"
        hashed = auth_service.get_password_hash(password)
        
        assert auth_service.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password returns False."""
        password = "password123"
        hashed = auth_service.get_password_hash(password)
        
        assert auth_service.verify_password("wrongpassword", hashed) is False

    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        hash1 = auth_service.get_password_hash("password1")
        hash2 = auth_service.get_password_hash("password2")
        
        assert hash1 != hash2

    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "samepassword"
        hash1 = auth_service.get_password_hash(password)
        hash2 = auth_service.get_password_hash(password)
        
        # Hashes should be different due to salting
        assert hash1 != hash2
        # But both should verify correctly
        assert auth_service.verify_password(password, hash1)
        assert auth_service.verify_password(password, hash2)


# ============================================================================
# Tests: User Authentication
# ============================================================================

class TestUserAuthentication:
    """Tests for user authentication."""

    def test_authenticate_user_success(self, db_session, test_user):
        """Test successful user authentication."""
        db_session.add(test_user)
        db_session.commit()
        
        user = auth_service.authenticate_user("test@example.com", "password123", db_session)
        
        assert user is not False
        assert user.email == test_user.email

    def test_authenticate_user_wrong_password(self, db_session, test_user):
        """Test authentication with wrong password returns False."""
        db_session.add(test_user)
        db_session.commit()
        
        result = auth_service.authenticate_user("test@example.com", "wrongpassword", db_session)
        
        assert result is False

    def test_authenticate_user_nonexistent(self, db_session):
        """Test authentication with non-existent user returns False."""
        result = auth_service.authenticate_user("nonexistent@example.com", "password123", db_session)
        
        assert result is False

    def test_authenticate_user_wrong_email(self, db_session, test_user):
        """Test authentication with wrong email returns False."""
        db_session.add(test_user)
        db_session.commit()
        
        result = auth_service.authenticate_user("wrong@example.com", "password123", db_session)
        
        assert result is False


# ============================================================================
# Tests: Token Creation and Verification
# ============================================================================

class TestTokenOperations:
    """Tests for JWT token operations."""

    def test_create_access_token(self):
        """Test creating an access token."""
        user_id = uuid4()
        token = auth_service.create_access_token(
            email="test@example.com",
            user_id=user_id,
            expires_delta=timedelta(minutes=30)
        )
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid(self):
        """Test verifying a valid token returns correct data."""
        user_id = uuid4()
        token = auth_service.create_access_token(
            email="test@example.com",
            user_id=user_id,
            expires_delta=timedelta(minutes=30)
        )
        
        token_data = auth_service.verify_token(token)
        
        assert token_data is not None
        assert token_data.get_uuid() == user_id

    def test_verify_token_invalid(self):
        """Test verifying an invalid token raises AuthenticationError."""
        with pytest.raises(AuthenticationError):
            auth_service.verify_token("invalid.token.here")

    def test_verify_token_expired(self):
        """Test verifying an expired token raises AuthenticationError."""
        user_id = uuid4()
        # Create token that expired 1 minute ago
        token = auth_service.create_access_token(
            email="test@example.com",
            user_id=user_id,
            expires_delta=timedelta(minutes=-1)
        )
        
        with pytest.raises(AuthenticationError):
            auth_service.verify_token(token)


# ============================================================================
# Tests: Login
# ============================================================================

class TestLogin:
    """Tests for user login."""

    def test_login_user_access_token_success(self, db_session, test_user):
        """Test successful login returns token."""
        db_session.add(test_user)
        db_session.commit()
        
        form_data = LoginUserRequest(
            email="test@example.com",
            password="password123"
        )
        
        token = auth_service.login_user_access_token(form_data, db_session)
        
        assert token is not None
        assert token.token_type == "bearer"
        assert token.access_token is not None

    def test_login_user_access_token_wrong_password(self, db_session, test_user):
        """Test login with wrong password raises InvalidCredentialError."""
        db_session.add(test_user)
        db_session.commit()
        
        form_data = LoginUserRequest(
            email="test@example.com",
            password="wrongpassword"
        )
        
        with pytest.raises(InvalidCredentialError):
            auth_service.login_user_access_token(form_data, db_session)

    def test_login_user_access_token_nonexistent_user(self, db_session):
        """Test login with non-existent user raises InvalidCredentialError."""
        form_data = LoginUserRequest(
            email="nonexistent@example.com",
            password="password123"
        )
        
        with pytest.raises(InvalidCredentialError):
            auth_service.login_user_access_token(form_data, db_session)


# ============================================================================
# Tests: User Registration
# ============================================================================

class TestUserRegistration:
    """Tests for user registration."""

    def test_register_user_success(self, db_session):
        """Test successful user registration."""
        request = RegisterUserRequest(
            first_name="New",
            last_name="User",
            email="new@example.com",
            password="SecureP@ss123",
            confirm_password="SecureP@ss123"
        )
        
        auth_service.register_user(db_session, request)
        
        user = db_session.query(User).filter_by(email="new@example.com").first()
        assert user is not None
        assert user.email == "new@example.com"
        assert user.firstname == "New"
        assert user.lastname == "User"
        # Password should be hashed
        assert user.password_hash != request.password
        assert auth_service.verify_password("SecureP@ss123", user.password_hash)

    def test_register_user_duplicate_email(self, db_session, test_user):
        """Test registration with duplicate email raises DuplicateEmailError."""
        db_session.add(test_user)
        db_session.commit()
        
        request = RegisterUserRequest(
            first_name="Another",
            last_name="User",
            email="test@example.com",  # Same email as test_user
            password="SecureP@ss123",
            confirm_password="SecureP@ss123"
        )
        
        with pytest.raises(DuplicateEmailError):
            auth_service.register_user(db_session, request)


# ============================================================================
# Tests: Integration (End-to-End)
# ============================================================================

class TestAuthIntegration:
    """Integration tests for complete auth flow."""

    def test_register_then_login(self, db_session):
        """Test user can register and then login."""
        # Register
        register_request = RegisterUserRequest(
            first_name="Integration",
            last_name="Test",
            email="integration@example.com",
            password="SecureP@ss123",
            confirm_password="SecureP@ss123"
        )
        auth_service.register_user(db_session, register_request)
        
        # Login
        login_request = LoginUserRequest(
            email="integration@example.com",
            password="SecureP@ss123"
        )
        token = auth_service.login_user_access_token(login_request, db_session)
        
        assert token.access_token is not None
        
        # Verify token
        token_data = auth_service.verify_token(token.access_token)
        user = db_session.query(User).filter_by(email="integration@example.com").first()
        assert token_data.get_uuid() == user.id 