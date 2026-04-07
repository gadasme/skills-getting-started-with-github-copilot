"""Tests for the remove participant endpoint (DELETE /activities/{activity_name}/participants)."""

import pytest


class TestRemoveParticipantEndpoint:
    """Test suite for the DELETE /activities/{activity_name}/participants endpoint."""

    def test_remove_existing_participant(self, client):
        """
        Arrange: Add a participant to an activity first.
        Act: DELETE request to remove the participant.
        Assert: Verify response is 200 and participant is removed.
        """
        # Arrange
        email = "remove_test@mergington.edu"
        activity_name = "Programming Class"
        
        # First, add the participant
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200, "Failed to setup test by adding participant"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"], \
            f"Setup failed: {email} was not added to {activity_name}"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200, "Expected status code 200"
        result = response.json()
        assert "message" in result, "Response should contain a message"
        assert email in result["message"], f"Message should mention {email}"
        assert activity_name in result["message"], f"Message should mention {activity_name}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"], \
            f"Expected {email} to be removed from {activity_name} participants"

    def test_remove_nonexistent_participant_returns_404(self, client):
        """
        Arrange: Initialize TestClient with valid activity but non-existent email.
        Act: DELETE request to remove non-existent participant.
        Assert: Verify response is 404 error.
        """
        # Arrange
        email = "nonexistent@mergington.edu"
        activity_name = "Programming Class"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404, "Expected status code 404 for non-existent participant"
        result = response.json()
        assert "detail" in result, "Error response should contain detail"
        assert "not found" in result["detail"].lower(), \
            "Error message should indicate participant not found"

    def test_remove_from_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Initialize TestClient with non-existent activity name.
        Act: DELETE request to remove participant from non-existent activity.
        Assert: Verify response is 404 error.
        """
        # Arrange
        email = "test@mergington.edu"
        activity_name = "Non Existent Activity"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404, "Expected status code 404 for non-existent activity"
        result = response.json()
        assert "detail" in result, "Error response should contain detail"
        assert "not found" in result["detail"].lower(), \
            "Error message should indicate activity not found"

    def test_remove_missing_email_parameter_returns_422(self, client):
        """
        Arrange: Initialize TestClient with missing email parameter.
        Act: DELETE request without email query parameter.
        Assert: Verify response is 422 validation error.
        """
        # Arrange
        activity_name = "Programming Class"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants")
        
        # Assert
        assert response.status_code == 422, "Expected status code 422 for missing required parameter"
        result = response.json()
        assert "detail" in result, "Validation error should contain detail"
