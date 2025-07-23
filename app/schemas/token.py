"""
Pydantic schemas for JWT token data validation and serialization.

This module defines the data schemas used for authentication token operations,
including token responses and token payload validation.
"""

from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for JWT token responses.
    
    This schema is used when returning authentication tokens to clients
    after successful login operations.
    
    Attributes:
        access_token (str): The JWT access token string
        token_type (str): The type of token, typically "bearer"
    """
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    """
    Schema for JWT token payload data.
    
    This schema represents the data contained within a JWT token payload.
    It's used internally for token verification and user identification.
    
    Attributes:
        id (int | None): User ID extracted from the token payload, None if not present
    """
    id: int | None = None