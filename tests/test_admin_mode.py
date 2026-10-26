from fastapi.testclient import TestClient
from src.app import activities, app

client = TestClient(app)


def test_students_can_view_activities_without_login():
    response = client.get("/activities")
    assert response.status_code == 200


def test_signup_requires_teacher_login():
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 401
    assert response.json()["detail"] == "Teacher authentication required"


def test_teacher_can_signup_and_unregister_student():
    login = client.post("/auth/login", json={"username": "teacher", "password": "password"})
    assert login.status_code == 200

    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]

    remove = client.delete("/activities/Chess%20Club/unregister?email=test@mergington.edu")
    assert remove.status_code == 200
    assert "test@mergington.edu" not in activities["Chess Club"]["participants"]

    logout = client.post("/auth/logout")
    assert logout.status_code == 200


def test_invalid_teacher_credentials_are_rejected():
    response = client.post("/auth/login", json={"username": "teacher", "password": "wrong"})
    assert response.status_code == 401
