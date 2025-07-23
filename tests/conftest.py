"""
Test configuration and fixtures for the Task Management API test suite.

This module contains pytest fixtures and configuration for testing the Task Management API.
It sets up a separate test database, provides authentication fixtures, and handles
dependency injection for isolated testing environments.

Key Features:
    - Isolated test database configuration
    - User authentication fixtures
    - Database session management
    - Authenticated test client setup
"""

from sqlalchemy.engine.url import URL
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.models.base import Base
from app.oauth2 import create_access_token
import pytest

# Create test database URL with '_test' suffix to avoid conflicts with production database
DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=f'{settings.database_name}_test'
)

# Create test database engine and session factory
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        
@pytest.fixture
def session():
    """
    Create a fresh database session for each test.
    
    This fixture ensures test isolation by dropping and recreating all database
    tables before each test. It provides a clean database state and properly
    manages the database session lifecycle.
    
    Yields:
        Session: SQLAlchemy database session for testing
        
    Test Lifecycle:
        1. Drop all existing tables to ensure clean state
        2. Create all tables from model definitions
        3. Create new database session
        4. Yield session to test function
        5. Close session after test completion

    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture()       
def client(session):
    """
    Create a FastAPI test client with database dependency override.
    
    This fixture creates a test client that uses the test database session
    instead of the production database. It overrides the get_db dependency
    to ensure all API calls during testing use the isolated test database.
    
    Args:
        session: Database session fixture for testing
        
    Yields:
        TestClient: FastAPI test client configured for testing
        
    Configuration:
        - Overrides the get_db dependency with test session
        - Ensures all API endpoints use the test database
        - Provides proper session cleanup after each request
        
    Example:
        Used in tests to make API calls:
        >>> response = client.get("/tasks/")
        >>> assert response.status_code == 200
    """
    def override_get_db():
        """Override function to provide test database session."""
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
        

@pytest.fixture
def setup_user(client):
    """
    Create a test user for authentication testing.
    
    This fixture creates a new user account that can be used in tests
    requiring authentication. It returns the complete user data including
    the plain text password for login testing.
    
    Args:
        client (TestClient): FastAPI test client fixture
        
    Returns:
        dict: User data including id, email, created_at, and password
        
    Raises:
        AssertionError: If user creation fails (status code != 201)
        
    User Data:
        - Email: danielogbuti@gmail.com
        - Password: password123
        - Additional fields: id, created_at (from API response)
        
    Example:
        >>> user = setup_user
        >>> assert user["email"] == "danielogbuti@gmail.com"
        >>> assert "id" in user
        >>> assert "password" in user
        
    Note:
        The password is added back to the response data to enable
        login testing with the created user credentials.
    """
    user_data = {
        "email": "danielogbuti@gmail.com",
        "password": "password123"
        }
    response = client.post("/users/", json=user_data)
    
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(setup_user):
    """
    Generate a JWT access token for the test user.
    
    This fixture creates a valid JWT access token for the test user
    that can be used to authenticate API requests during testing.
    
    Args:
        setup_user (dict): Test user data from setup_user fixture
        
    Returns:
        str: JWT access token for the test user
        
    Token Contents:
        - user_id: The ID of the test user
        - exp: Token expiration time (based on app settings)
        - Encoded with the application's secret key and algorithm
        
    Example:
        >>> token_value = token
        >>> assert isinstance(token_value, str)
        >>> assert len(token_value) > 50  # JWT tokens are typically long
        
    Usage:
        This token can be used in Authorization headers:
        Authorization: Bearer {token_value}
    """
    return create_access_token(data={"user_id": setup_user["id"]})  

@pytest.fixture
def authorized_client(client, token):
    """
    Create an authenticated test client with JWT token.
    
    This fixture extends the basic test client by adding authentication
    headers with a valid JWT token. It enables testing of protected
    endpoints that require user authentication.
    
    Args:
        client (TestClient): Basic FastAPI test client
        token (str): JWT access token from token fixture
        
    Returns:
        TestClient: Test client with authentication headers configured
        
    Headers Added:
        - Authorization: Bearer {jwt_token}
        - Preserves any existing headers from the base client
        
    Example:
        >>> response = authorized_client.get("/tasks/")
        >>> # This request will include authentication headers
        >>> assert response.status_code != 401  # Should not be unauthorized
        
    Use Cases:
        - Testing protected endpoints
        - User-specific data operations
        - Authentication-required CRUD operations
        - Role-based access testing
        
    Note:
        This client automatically includes authentication headers
        for all requests, eliminating the need to manually add
        Authorization headers in individual tests.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

