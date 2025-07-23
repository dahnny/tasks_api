"""
Utility functions for password hashing and verification.

This module provides cryptographic functions for secure password handling
using bcrypt hashing algorithm through the passlib library.
"""

from passlib.context import CryptContext

# Configure password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The bcrypt hashed password to compare against
        
    Returns:
        bool: True if the password matches, False otherwise
        
    Example:
        >>> hashed = hash_password("secret123")
        >>> verify_password("secret123", hashed)
        True
        >>> verify_password("wrong", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        str: The bcrypt hashed password
        
    Example:
        >>> hashed = hash_password("secret123")
        >>> len(hashed) > 50  # bcrypt hashes are typically 60 characters
        True
    """
    return pwd_context.hash(password)