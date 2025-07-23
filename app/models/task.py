"""
Task database model for the Task Management API.

This module defines the Task model which represents tasks in the database,
including their relationship to users and task metadata.
"""

from app.models.base import Base
from sqlalchemy import String, Integer, Column, TIMESTAMP, text, ForeignKey, Date
from sqlalchemy.orm import relationship

class Task(Base):
    """
    Task model representing user tasks in the system.
    
    This model stores task information including title, description, status,
    due dates, and ownership. Each task belongs to a specific user and tracks
    creation and modification timestamps.
    
    Attributes:
        id (int): Primary key, unique identifier for the task
        owner_id (int): Foreign key reference to the user who owns this task
        title (str): Task title or name
        description (str): Optional detailed description of the task
        status (str): Current status of the task (default: "INCOMPLETE")
        due_date (date): Date when the task is due
        created_at (datetime): Timestamp when the task was created
        updated_at (datetime): Timestamp when the task was last modified
        owner (User): SQLAlchemy relationship to the User who owns this task
        
    Table:
        tasks: The database table name for this model
        
    Relationships:
        - Many-to-One with User (many tasks can belong to one user)
    """
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="INCOMPLETE")
    due_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), 
                        onupdate=text('now()'), nullable=False)
    
    # Relationship to User model
    owner = relationship("User")