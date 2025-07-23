"""
Task management routes for the Task Management API.

This module handles all task-related endpoints including creation, retrieval,
updating, and deletion of tasks. All endpoints require user authentication.
"""

from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from app.models.task import Task
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import get_current_user

# Create router for task endpoints
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", 
             status_code=status.HTTP_201_CREATED,
             response_model=TaskResponse)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.
    
    This endpoint creates a new task and automatically assigns it to the
    currently authenticated user. All task fields from the TaskCreate schema
    are required.
    
    Args:
        task (TaskCreate): Task data including title, description, status, and due_date
        db (Session): Database session dependency
        current_user (User): Authenticated user from JWT token
        
    Returns:
        TaskResponse: Created task data including ID and timestamps
        
    Raises:
        HTTPException: 400 Bad Request if task creation fails
        HTTPException: 401 Unauthorized if user is not authenticated
        
    Example:
        POST /tasks/
        Body: {
            "title": "Complete project",
            "description": "Finish the API documentation",
            "status": "INCOMPLETE",
            "due_date": "2024-12-31T23:59:59"
        }
        Response: {
            "id": 1,
            "title": "Complete project",
            "description": "Finish the API documentation", 
            "status": "INCOMPLETE",
            "due_date": "2024-12-31T23:59:59",
            "created_at": "2023-...",
            "updated_at": "2023-..."
        }
    """
    db_task = Task(owner_id=current_user.id, **task.dict()) 
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to Create Task"
        )
    
    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
) -> TaskResponse:
    """
    Retrieve a specific task by its ID.
    
    This endpoint returns detailed information about a task. Currently,
    any authenticated user can view any task, but this could be modified
    to restrict access to task owners only.
    
    Args:
        task_id (int): The unique identifier of the task to retrieve
        db (Session): Database session dependency
        current_user (User): Authenticated user from JWT token
        
    Returns:
        TaskResponse: Task data including all fields and timestamps
        
    Raises:
        HTTPException: 404 Not Found if task with given ID doesn't exist
        HTTPException: 401 Unauthorized if user is not authenticated
        
    Example:
        GET /tasks/1
        Response: {
            "id": 1,
            "title": "Complete project",
            "description": "Finish the API documentation",
            "status": "INCOMPLETE", 
            "due_date": "2024-12-31T23:59:59",
            "created_at": "2023-...",
            "updated_at": "2023-..."
        }
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {task_id} not found"
        )
    
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
) -> TaskResponse:
    """
    Update an existing task.
    
    This endpoint allows task owners to update their tasks. Only the task owner
    can modify their tasks. All fields in TaskUpdate are optional, allowing
    for partial updates.
    
    Args:
        task_id (int): The unique identifier of the task to update
        task (TaskUpdate): Task update data with optional fields
        db (Session): Database session dependency
        current_user (User): Authenticated user from JWT token
        
    Returns:
        TaskResponse: Updated task data with new timestamps
        
    Raises:
        HTTPException: 404 Not Found if task with given ID doesn't exist
        HTTPException: 403 Forbidden if user is not the task owner
        HTTPException: 401 Unauthorized if user is not authenticated
        
    Example:
        PUT /tasks/1
        Body: {"status": "COMPLETE"}
        Response: {
            "id": 1,
            "title": "Complete project",
            "description": "Finish the API documentation",
            "status": "COMPLETE",
            "due_date": "2024-12-31T23:59:59",
            "created_at": "2023-...",
            "updated_at": "2023-..." (updated timestamp)
        }
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {task_id} not found"
        )
    
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    # Update only provided fields
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    """
    Delete a task.
    
    This endpoint allows task owners to permanently delete their tasks.
    Only the task owner can delete their tasks. This operation cannot be undone.
    
    Args:
        task_id (int): The unique identifier of the task to delete
        db (Session): Database session dependency
        current_user (User): Authenticated user from JWT token
        
    Returns:
        None: Returns 204 No Content on successful deletion
        
    Raises:
        HTTPException: 404 Not Found if task with given ID doesn't exist
        HTTPException: 403 Forbidden if user is not the task owner
        HTTPException: 401 Unauthorized if user is not authenticated
        
    Example:
        DELETE /tasks/1
        Response: 204 No Content (empty body)
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {task_id} not found"
        )
    
    if db_task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    db.delete(db_task)
    db.commit()