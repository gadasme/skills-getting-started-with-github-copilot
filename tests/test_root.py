"""Tests for the root endpoint (GET /)."""

import pytest


class TestRootEndpoint:
    """Test suite for the root endpoint."""

    def test_root_redirects_to_index(self, client):
        """
        Arrange: Initialize TestClient.
        Act: Make a GET request to /.
        Assert: Verify the response redirects to /static/index.html.
        """
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307, "Expected redirect status code 307"
        assert "static/index.html" in response.headers.get("location", ""), \
            "Expected redirect location to contain /static/index.html"
