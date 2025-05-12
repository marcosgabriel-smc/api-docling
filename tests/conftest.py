import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.core.config import Settings

@pytest.fixture(autouse=True)
def override_settings():
    """Override settings for testing."""
    with patch('app.core.security.settings') as mock_settings:
        mock_settings.API_KEY = "test-api-key"
        mock_settings.API_KEY_NAME = "X-API-Key"
        yield mock_settings

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def valid_api_key():
    """Return a valid API key for testing."""
    return "test-api-key"  # This should match the mock settings 