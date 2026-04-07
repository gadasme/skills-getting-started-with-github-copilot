"""Tests for the activities list endpoint (GET /activities)."""

import pytest


class TestActivitiesEndpoint:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Initialize TestClient.
        Act: Make a GET request to /activities.
        Assert: Verify response status is 200 and contains all activities.
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200, "Expected status code 200"
        activities = response.json()
        
        # Verify all expected activities are present
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Club",
            "Music Ensemble",
            "Debate Team",
            "Science Club"
        ]
        
        for activity_name in expected_activities:
            assert activity_name in activities, \
                f"Expected activity '{activity_name}' not found in response"

    def test_get_activities_response_structure(self, client):
        """
        Arrange: Initialize TestClient.
        Act: Make a GET request to /activities.
        Assert: Verify each activity has correct structure (description, schedule, max_participants, participants).
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert - Check structure of each activity
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), \
                f"Activity '{activity_name}' should be a dictionary"
            assert set(activity_data.keys()) == required_fields, \
                f"Activity '{activity_name}' missing required fields. Expected {required_fields}, got {set(activity_data.keys())}"
            
            # Verify field types
            assert isinstance(activity_data["description"], str), \
                f"Activity '{activity_name}' description should be a string"
            assert isinstance(activity_data["schedule"], str), \
                f"Activity '{activity_name}' schedule should be a string"
            assert isinstance(activity_data["max_participants"], int), \
                f"Activity '{activity_name}' max_participants should be an integer"
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"

    def test_get_activities_participants_lists_exist(self, client):
        """
        Arrange: Initialize TestClient.
        Act: Make a GET request to /activities.
        Assert: Verify each activity has a participants list (empty or populated).
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert - Check each activity has participants list
        for activity_name, activity_data in activities.items():
            assert "participants" in activity_data, \
                f"Activity '{activity_name}' missing 'participants' field"
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants should be a list"
