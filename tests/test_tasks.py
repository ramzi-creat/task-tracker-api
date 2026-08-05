from app import __version__


def test_version_endpoint_returns_package_version(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


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


def test_patch_existing_task_in_progress_to_todo_returns_422(client):
    create_response = client.post("/tasks", json={"title": "Progress task", "status": "In Progress"})
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})
    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/missing-id")
    assert response.status_code == 404


# --- NEW TESTS FOR FEATURE 1 & 2 (Due Dates & Tags) ---

def test_create_task_with_due_date_and_tags(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task with due date and tags",
            "due_date": "2026-12-31",
            "tags": ["backend", "urgent"]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"] == "2026-12-31"
    assert "backend" in data["tags"]
    assert "urgent" in data["tags"]


def test_list_tasks_filter_by_tag(client):
    client.post("/tasks", json={"title": "Task with Python Tag", "tags": ["python"]})
    client.post("/tasks", json={"title": "Task with JS Tag", "tags": ["javascript"]})
    client.post("/tasks", json={"title": "Task with Python and Backend", "tags": ["python", "backend"]})

    response = client.get("/tasks", params={"tag": "python"})
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert {task["title"] for task in data} == {"Task with Python Tag", "Task with Python and Backend"}
    assert all("python" in task["tags"] for task in data)

from datetime import date, timedelta


def test_list_tasks_filter_overdue(client):
    today = date.today()
    past_date = (today - timedelta(days=5)).isoformat()
    future_date = (today + timedelta(days=5)).isoformat()

    client.post("/tasks", json={"title": "Overdue Task", "due_date": past_date, "status": "ToDo"})
    client.post("/tasks", json={"title": "Also Overdue", "due_date": past_date, "status": "ToDo"})
    client.post("/tasks", json={"title": "Future Task", "due_date": future_date, "status": "ToDo"})
    client.post("/tasks", json={"title": "Completed Past Task", "due_date": past_date, "status": "Done"})

    response = client.get("/tasks", params={"overdue": "true"})
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert {task["title"] for task in data} == {"Overdue Task", "Also Overdue"}
    assert all(task["status"] != "Done" for task in data)
    assert all(task["due_date"] is not None and task["due_date"] < today.isoformat() for task in data)


def test_tag_normalization(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Normalization test",
            "tags": ["  Spaces  ", "UPPERCASE"]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "Spaces" in data["tags"] or "spaces" in [t.lower() for t in data["tags"]]


def test_update_task_null_title_returns_422(client, created_task):
    task_id = created_task["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": None})
    assert response.status_code == 422


def test_put_missing_task_returns_404(client):
    response = client.put("/tasks/missing-id", json={"title": "Replacement title"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task with id missing-id not found"


def test_list_tasks_filter_by_status_is_case_insensitive(client):
    client.post("/tasks", json={"title": "Lowercase status task", "status": "ToDo"})

    response = client.get("/tasks", params={"status": "todo"})
    assert response.status_code == 200
    data = response.json()
    assert any(task["title"] == "Lowercase status task" for task in data)
