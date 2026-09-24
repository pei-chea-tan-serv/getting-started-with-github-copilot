from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email():
    # Arrange
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.delete("/activities/Chess Club/participants/daniel@mergington.edu")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_activity_returns_404():
    # Arrange
    activity_name = "Not A Real Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/daniel@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_email_not_in_activity_returns_404():
    # Arrange
    activities["Chess Club"]["participants"] = ["michael@mergington.edu"]

    # Act
    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"
