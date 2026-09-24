from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_adds_new_participant():
    # Arrange
    activities["Chess Club"]["participants"] = ["michael@mergington.edu"]
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_email_returns_400():
    # Arrange
    email = "michael@mergington.edu"
    activities["Chess Club"]["participants"] = [email]

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404():
    # Arrange
    activity_name = "Not A Real Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_full_activity_returns_400():
    # Arrange
    activities["Chess Club"]["max_participants"] = 1
    activities["Chess Club"]["participants"] = ["michael@mergington.edu"]
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
