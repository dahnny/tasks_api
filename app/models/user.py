"""
User database model for the Task Management API.

This module defines the User model which represents users in the database,
including their email, password, and account creation timestamp.
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.models.base import Base

class User(Base):
    """
    User model representing registered users in the system.
    
    This model stores user account information including email credentials
    and account timestamps. Each user can own multiple tasks.
    
    Attributes:
        id (int): Primary key, unique identifier for the user
        email (str): User's email address, must be unique across all users
        password (str): Hashed password for authentication
        created_at (datetime): Timestamp when the user account was created
        
    Table:
        users: The database table name for this model
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
