import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

@pytest.fixture
def mock_document_converter():
    """Mock the DocumentConverter for testing."""
    with patch('app.services.document_service.DocumentConverter') as mock:
        mock_instance = MagicMock()
        # Create a mock document with markdown export
        mock_document = MagicMock()
        mock_document.export_to_markdown.return_value = "# Test Markdown"
        # Create a mock conversion result
        mock_result = MagicMock()
        mock_result.document = mock_document
        mock_instance.convert.return_value = mock_result
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_requests():
    """Mock the requests library to prevent actual HTTP requests."""
    with patch('requests.get') as mock:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Mock PDF content"
        mock.return_value = mock_response
        yield mock

@pytest.fixture
def mock_input_document():
    """Mock the InputDocument class to prevent actual file processing."""
    with patch('docling.document_converter.InputDocument') as mock:
        mock_instance = MagicMock()
        mock_instance.valid = True
        mock_instance.file = "test.pdf"
        mock.return_value = mock_instance
        yield mock

def test_convert_document_endpoint(client, valid_api_key, mock_document_converter, mock_requests, mock_input_document):
    """Test the document conversion endpoint with valid input."""
    test_url = "https://example.com/test.pdf"
    response = client.post(
        "/api/v1/document/convert",
        params={"source": test_url},
        headers={"X-API-Key": valid_api_key}
    )
    assert response.status_code == 200
    assert response.json() == {"markdown": "# Test Markdown"}
    mock_document_converter.convert.assert_called_once_with(test_url)
    mock_requests.assert_called_once_with(test_url)
    mock_input_document.assert_called_once()

def test_convert_document_without_api_key(client):
    """Test the document conversion endpoint without API key."""
    with pytest.raises(HTTPException) as exc_info:
        client.post(
            "/api/v1/document/convert",
            params={"source": "https://example.com/test.pdf"}
        )
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid API Key"

def test_convert_document_without_source(client, valid_api_key):
    """Test the document conversion endpoint without source parameter."""
    response = client.post(
        "/api/v1/document/convert",
        headers={"X-API-Key": valid_api_key}
    )
    assert response.status_code == 422  # Validation error 