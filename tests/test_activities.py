from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_seeded_activity_shape():
    # Arrange
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    chess_club = response.json()["Chess Club"]
    assert chess_club["description"] == activities["Chess Club"]["description"]
    assert chess_club["schedule"] == activities["Chess Club"]["schedule"]
    assert chess_club["max_participants"] == activities["Chess Club"]["max_participants"]
    assert chess_club["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
