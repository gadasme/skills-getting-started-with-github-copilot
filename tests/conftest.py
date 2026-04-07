"""Shared pytest fixtures for FastAPI application tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Arrange: Create a FastAPI TestClient for testing endpoints.
    
    Returns:
        TestClient: A test client that can make requests to the FastAPI application.
    """
    return TestClient(app)
