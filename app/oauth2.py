"""
OAuth2 authentication and JWT token management.

This module handles JWT token creation, verification, and user authentication
for the Task Management API. It provides OAuth2 password bearer authentication
scheme and user authorization functions.
"""

import jwt
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from app.schemas.token import TokenData

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with expiration time.
    
    Args:
        data (dict): The payload data to encode in the token, typically contains user_id
        
    Returns:
        str: The encoded JWT access token
        
    Example:
        >>> token = create_access_token({"user_id": 1})
        >>> isinstance(token, str)
        True
    """
    to_encode = data.copy()    
    expire = datetime.now() + timedelta(minutes=int(settings.access_token_expire_minutes))
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str, credential_exceptions: HTTPException) -> TokenData:
    """
    Verify and decode a JWT access token.
    
    Args:
        token (str): The JWT token to verify
        credential_exceptions (HTTPException): Exception to raise if verification fails
        
    Returns:
        TokenData: Decoded token data containing user ID
        
    Raises:
        HTTPException: If token is invalid, expired, or malformed
        
    Example:
        >>> from fastapi import HTTPException, status
        >>> exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid")
        >>> token = create_access_token({"user_id": 1})
        >>> token_data = verify_access_token(token, exception)
        >>> token_data.id == 1
        True
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exceptions
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credential_exceptions
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(get_db)) -> User:
    """
    Get the current authenticated user from the JWT token.
    
    This function is used as a FastAPI dependency to authenticate and authorize
    users for protected endpoints.
    
    Args:
        token (str): JWT token from the Authorization header
        db (Session): Database session dependency
        
    Returns:
        User: The authenticated user object
        
    Raises:
        HTTPException: If token is invalid or user is not found
        
    Example:
        Used as a FastAPI dependency:
        ```python
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
        ```
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credential_exception)
    user = db.query(User).filter(User.id == token.id).first()
    
    return user