import pytest
from fastapi import HTTPException

def test_root_endpoint(client, valid_api_key):
    """Test the root endpoint returns the correct welcome message."""
    response = client.get("/", headers={"X-API-Key": valid_api_key})
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Docling Microservice!"}

def test_root_endpoint_without_api_key(client):
    """Test the root endpoint requires API key."""
    with pytest.raises(HTTPException) as exc_info:
        client.get("/", headers={})
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid API Key" 