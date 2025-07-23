"""
Pydantic schemas for task data validation and serialization.

This module defines the data schemas used for task-related API operations,
including request validation, response serialization, and update operations.
"""

from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    """
    Base task schema with common task fields.
    
    This schema contains the basic task information that is shared
    across different task-related operations.
    
    Attributes:
        title (str): Task title or name
        description (str): Detailed description of the task
        status (str): Current status of the task (e.g., "INCOMPLETE", "COMPLETE")
        due_date (datetime): Date and time when the task is due
    """
    title: str
    description: str
    status: str
    due_date: datetime
    
class TaskCreate(TaskBase):
    """
    Schema for task creation requests.
    
    Inherits all fields from TaskBase and is used when creating new tasks.
    The owner_id is automatically set from the authenticated user.
    """
    pass

class TaskResponse(TaskBase):
    """
    Schema for task data in API responses.
    
    This schema is used when returning task information in API responses.
    It includes all task data plus metadata like creation and update timestamps.
    
    Attributes:
        id (int): Unique task identifier
        created_at (datetime): Timestamp when the task was created
        updated_at (datetime): Timestamp when the task was last modified
    """
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration for ORM compatibility."""
        orm_mode = True
        
class TaskUpdate(BaseModel):
    """
    Schema for task update requests.
    
    This schema allows partial updates to tasks where all fields are optional.
    Only provided fields will be updated in the database.
    
    Attributes:
        title (str | None): Optional new title for the task
        description (str | None): Optional new description for the task
        status (str | None): Optional new status for the task
        due_date (datetime | None): Optional new due date for the task
    """
    title: str | None = None
    description: str | None = None
    status: str | None = None
    due_date: datetime | None = None

    class Config:
        """Pydantic configuration for ORM compatibility."""
        orm_mode = True
    