"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)."""

import pytest


class TestSignupEndpoint:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid_new_participant(self, client):
        """
        Arrange: Initialize TestClient with valid email and existing activity.
        Act: Make a POST request to signup for an activity.
        Assert: Verify response is 200 and participant is added to the activity.
        """
        # Arrange
        email = "test_student@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200, "Expected status code 200"
        result = response.json()
        assert "message" in result, "Response should contain a message"
        assert email in result["message"], f"Message should mention {email}"
        assert activity_name in result["message"], f"Message should mention {activity_name}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"], \
            f"Expected {email} to be in {activity_name} participants"

    def test_signup_duplicate_participant_returns_400(self, client):
        """
        Arrange: Initialize TestClient with an email already signed up for an activity.
        Act: Attempt to POST signup with duplicate email.
        Assert: Verify response is 400 error.
        """
        # Arrange
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400, "Expected status code 400 for duplicate signup"
        result = response.json()
        assert "detail" in result, "Error response should contain detail"
        assert "already signed up" in result["detail"].lower(), \
            "Error message should indicate student is already signed up"

    def test_signup_same_email_different_activities(self, client):
        """
        Arrange: Add a participant to one activity.
        Act: Sign up the same email to a different activity.
        Assert: Verify response is 200 and participant is added to the new activity.
        """
        # Arrange
        email = "multi_activity@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # First signup for activity1
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200, "Failed to add participant to first activity"
        
        # Act - Add same email to different activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response2.status_code == 200, "Expected status code 200 for different activity"
        result = response2.json()
        assert "message" in result, "Response should contain a message"
        
        # Verify participant was added to both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity1]["participants"], \
            f"Expected {email} to be in {activity1} participants"
        assert email in activities[activity2]["participants"], \
            f"Expected {email} to be in {activity2} participants"

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Initialize TestClient with non-existent activity name.
        Act: POST signup to non-existent activity.
        Assert: Verify response is 404 error.
        """
        # Arrange
        email = "test@mergington.edu"
        activity_name = "Non Existent Activity"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404, "Expected status code 404 for non-existent activity"
        result = response.json()
        assert "detail" in result, "Error response should contain detail"
        assert "not found" in result["detail"].lower(), \
            "Error message should indicate activity not found"

    def test_signup_missing_email_parameter_returns_422(self, client):
        """
        Arrange: Initialize TestClient with missing email parameter.
        Act: POST signup without email query parameter.
        Assert: Verify response is 422 validation error.
        """
        # Arrange
        activity_name = "Chess Club"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup")
        
        # Assert
        assert response.status_code == 422, "Expected status code 422 for missing required parameter"
        result = response.json()
        assert "detail" in result, "Validation error should contain detail"
