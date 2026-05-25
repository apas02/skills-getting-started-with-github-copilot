from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Swimming Club",
        "Art Studio",
        "Drama Club",
        "Robotics Club",
        "Math Olympiad Training",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    response_data = response.json()

    assert set(response_data.keys()) == expected_activity_names

    for activity_name, activity_details in response_data.items():
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details


def test_signup_for_activity_success():
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email},
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
        assert new_email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_for_activity_already_signed_up():
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_invalid_activity():
    # Arrange
    activity_name = "Non-Existent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_activity_success():
    # Arrange
    activity_name = "Programming Class"
    email_to_remove = "emma@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_remove},
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email_to_remove} from {activity_name}"
        assert email_to_remove not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_remove_participant_not_registered():
    # Arrange
    activity_name = "Swimming Club"
    email = "not-registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_remove_participant_invalid_activity():
    # Arrange
    activity_name = "Non-Existent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"