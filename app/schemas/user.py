"""
Pydantic schemas for user data validation and serialization.

This module defines the data schemas used for user-related API operations,
including request validation and response serialization.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    """
    Base user schema with common user fields.
    
    This schema contains the basic user information that is shared
    across different user-related operations.
    
    Attributes:
        email (EmailStr): User's email address, validated for proper email format
        password (str): User's password (will be hashed before storage)
    """
    email: EmailStr
    password: str
    
class UserCreate(UserBase):
    """
    Schema for user creation requests.
    
    Inherits all fields from UserBase and is used when creating new users
    through the registration endpoint.
    """
    pass

class UserResponse(BaseModel):
    """
    Schema for user data in API responses.
    
    This schema is used when returning user information in API responses.
    It excludes sensitive information like passwords and includes metadata
    like creation timestamps.
    
    Attributes:
        id (int): Unique user identifier
        email (EmailStr): User's email address
        created_at (datetime): Timestamp when the user account was created
    """
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM compatibility."""
        orm_mode = True


