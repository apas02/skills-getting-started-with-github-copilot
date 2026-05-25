from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_remove_participant_from_activity():
    original_participants = activities["Chess Club"]["participants"].copy()

    try:
        response = client.delete(
            "/activities/Chess%20Club/participants",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants


def test_remove_participant_returns_error_when_not_registered():
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "not-registered@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"
