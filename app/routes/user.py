"""
User management routes for the Task Management API.

This module handles user-related endpoints including user registration
and profile retrieval functionality.
"""

from fastapi import APIRouter, status, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.utils import hash_password

# Create router for user endpoints
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, 
             status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user in the system.
    
    This endpoint creates a new user account with email and password.
    The password is automatically hashed before storage for security.
    Email addresses must be unique across all users.
    
    Args:
        user (UserCreate): User registration data including email and password
        db (Session): Database session dependency
        
    Returns:
        UserResponse: Created user data (excluding password)
        
    Raises:
        HTTPException: 400 Bad Request if email is already registered or user creation fails
        
    Example:
        POST /users/
        Body: {"email": "user@example.com", "password": "secret123"}
        Response: {"id": 1, "email": "user@example.com", "created_at": "2023-..."}
    """
    # Check if email is already registered
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Hash the password before storing
    user.password = hash_password(user.password)
    
    # Create new user instance
    new_user = User(
        email=user.email,
        password=user.password
    )
    
    # Save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Failed to create User"
        )
    
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Retrieve a user's profile information by user ID.
    
    This endpoint returns public user information for a given user ID.
    Sensitive information like passwords are excluded from the response.
    
    Args:
        user_id (int): The unique identifier of the user to retrieve
        db (Session): Database session dependency
        
    Returns:
        UserResponse: User profile data (excluding password)
        
    Raises:
        HTTPException: 400 Bad Request if user with given ID is not found
        
    Example:
        GET /users/1
        Response: {"id": 1, "email": "user@example.com", "created_at": "2023-..."}
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} not found"
        )
    return user