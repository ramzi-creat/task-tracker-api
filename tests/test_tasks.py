def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post("/tasks", json={"title": "My task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My task"
    assert data["description"] == ""
    assert data["status"] == "ToDo"
    assert data["priority"] == "Medium"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "priority": "INVALID"})
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "extra_field": "nope"})
    assert response.status_code == 422


def test_create_task_accepts_frontend_status_and_assignee(client):
    response = client.post(
        "/tasks",
        json={"title": "Front-end task", "status": "To Do", "assignee": "Alex"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "ToDo"
    assert data["assignee"] == "Alex"


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})
    client.post("/tasks", json={"title": "Another high", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(task["priority"] == "High" for task in data)


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    task_id = "nonexistent-id"
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


def test_patch_partial_update_keeps_other_fields(client, created_task):
    task_id = created_task["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"description": "Updated description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == created_task["title"]
    assert data["description"] == "Updated description"
    assert data["status"] == created_task["status"]
    assert data["priority"] == created_task["priority"]
    assert data["completed"] == created_task["completed"]
    assert data["id"] == task_id


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/missing-id", json={"title": "New title"})
    assert response.status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "In Progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "In Progress"


def test_patch_valid_transition_inprogress_to_todo_returns_200(client):
    response = client.post("/tasks", json={"title": "Progress task", "status": "In Progress"})
    task_id = response.json()["id"]
    patch_response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "ToDo"


def test_patch_valid_transition_done_to_todo_returns_200(client):
    response = client.post("/tasks", json={"title": "Done task", "status": "Done"})
    task_id = response.json()["id"]
    patch_response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "ToDo"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert response.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert response.status_code == 422


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/missing-id")
    assert response.status_code == 404
