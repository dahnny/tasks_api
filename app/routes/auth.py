"""
Authentication routes for the Task Management API.

This module handles user authentication endpoints including login functionality
and JWT token generation for secure API access.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils import verify_password
from app.oauth2 import create_access_token

# Create router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and return a JWT access token.
    
    This endpoint validates user credentials (email and password) and returns
    a JWT access token if authentication is successful. The token can be used
    to access protected endpoints.
    
    Args:
        user_credentials (OAuth2PasswordRequestForm): Form data containing username 
            (email) and password
        db (Session): Database session dependency
        
    Returns:
        dict: Contains access_token and token_type if authentication succeeds
        
    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid
        
    Example:
        POST /auth/login
        Form data: username=user@example.com, password=secret123
        Response: {"access_token": "eyJ...", "token_type": "bearer"}
    """
    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}