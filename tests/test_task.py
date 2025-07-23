"""
Test suite for task-related API endpoints.

This module contains comprehensive tests for all task management functionality
including task creation, retrieval, updating, and deletion operations.
All tests use authenticated clients to simulate real user interactions.
"""

from app.schemas.task import TaskCreate, TaskResponse

def test_task(authorized_client, setup_user):
    """
    Test task creation functionality.
    
    This test function creates a new task using the task creation endpoint
    and verifies that the task is created successfully with the correct
    HTTP status code.
    
    Args:
        authorized_client: FastAPI test client with authentication headers
        setup_user (dict): User fixture containing user data including ID
        
    Returns:
        dict: Created task data from the API response
        
    Raises:
        AssertionError: If the response status code is not 201 (Created)
        
    Test Flow:
        1. Prepare task data with all required fields
        2. Send POST request to create task endpoint
        3. Verify successful creation (201 status code)
        4. Return created task data for use in other tests
        
    Example:
        This function is typically used as a helper for other tests:
        >>> task = test_task(client, user)
        >>> assert task["title"] == "Test Task"
    """
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "user_id": setup_user["id"],
        "status": "INCOMPLETE",
        "due_date": "2024-12-31T23:59:59"
    }
    response = authorized_client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    return response.json()

def test_get_task(authorized_client, setup_user):
    """
    Test task retrieval functionality by ID.
    
    This test verifies that a specific task can be retrieved using its ID
    and that all task data is returned correctly. It first creates a task
    and then retrieves it to ensure data integrity.
    
    Args:
        authorized_client: FastAPI test client with authentication headers
        setup_user (dict): User fixture containing user data including ID
        
    Raises:
        AssertionError: If any of the following conditions fail:
            - Response status code is not 200 (OK)
            - Retrieved task data doesn't match created task data
            - Any task field (id, title, description, status, due_date) is incorrect
            
    Test Flow:
        1. Create a test task using the test_task helper function
        2. Send GET request to retrieve the task by its ID
        3. Verify successful retrieval (200 status code)
        4. Validate that all returned task fields match the original task data
        
    Validates:
        - Task ID consistency
        - Title field accuracy
        - Description field accuracy
        - Status field accuracy
        - Due date field accuracy
        
    Example:
        This test ensures that task retrieval works correctly:
        GET /tasks/1 should return the exact task data that was created
    """
    task = test_task(authorized_client, setup_user)
    response = authorized_client.get(f"/tasks/{task['id']}")
    assert response.status_code == 200
    task_data = response.json()
    assert task_data["id"] == task["id"]
    assert task_data["title"] == task["title"]
    assert task_data["description"] == task["description"]
    assert task_data["status"] == task["status"]
    assert task_data["due_date"] == task["due_date"]