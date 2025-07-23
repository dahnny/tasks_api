from app.schemas.task import TaskCreate, TaskResponse

def test_task(authorized_client, setup_user):
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
    task = test_task(authorized_client, setup_user)
    response = authorized_client.get(f"/tasks/{task['id']}")
    assert response.status_code == 200
    task_data = response.json()
    assert task_data["id"] == task["id"]
    assert task_data["title"] == task["title"]
    assert task_data["description"] == task["description"]
    assert task_data["status"] == task["status"]
    assert task_data["due_date"] == task["due_date"]