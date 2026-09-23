from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def setup_function():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]


def test_unregister_participant_removes_email():
    response = client.delete("/activities/Chess Club/participants/daniel@mergington.edu")

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
