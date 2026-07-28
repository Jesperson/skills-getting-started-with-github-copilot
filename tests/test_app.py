import pytest
from fastapi.testclient import TestClient

from src.app import app, reset_activities


@pytest.fixture(autouse=True)
def reset_state():
    reset_activities()
    yield
    reset_activities()


client = TestClient(app)


def test_signup_for_activity_adds_participant():
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@mergington.edu for Chess Club"
    assert "test@mergington.edu" in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant():
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in response.json()["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    response = client.delete("/activities/Unknown/participants/test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
