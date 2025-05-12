# Docling Microservice

A FastAPI-based microservice that provides document conversion capabilities using the Docling library.


## PENDING
- Fix tests

## Features

- Document conversion to Markdown, HTML, and Text formats
- Code understanding enrichment (enabled by default)
- Formula understanding enrichment (enabled by default)
- Picture classification and description (enabled by default)
- API Key authentication
- RESTful API endpoints
- CORS support

## Prerequisites

- Python 3.10+
- Virtual environment (venv)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hj-docling
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
API_KEY=your_secure_api_key
```

## Running the Service

Start the service with:
```bash
uvicorn main:app --reload
```

The service will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## API Endpoints

### Convert to Markdown
```http
POST /api/v1/document/convert/markdown
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "/path/to/document.pdf" (OR URL),
    "from_element": 0,
    "to_element": 1000000
}
```

### Convert to HTML
```http
POST /api/v1/document/convert/html
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "/path/to/document.pdf" (OR URL),
    "from_element": 0,
    "to_element": 1000000
}
```

### Convert to Text
```http
POST /api/v1/document/convert/text
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "/path/to/document.pdf" (OR URL),
    "from_element": 0,
    "to_element": 1000000
}
```

Response for all endpoints:
```json
{
    "content": "Converted document content",
    "format": "markdown|html|text"
}
```

## Example cURL

```
curl -X POST "http://localhost:8000/api/v1/document/convert/text" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "source": "/mnt/c/Users/Marcos Gabriel/Documents/web-dev/helpjuice/Velocity Running Co - Sales Report.pdf"
  }'
```

## Request Parameters

### Source
The `source` parameter can be:
- A URL (starting with `http://` or `https://`)
- A local file path (starting with `/`, `./`, or `../`)

For Windows paths in WSL, use the `/mnt/c/` prefix:
```json
{
    "source": "/mnt/c/Users/username/Documents/document.pdf"
}
```

### Element Range
- `from_element`: Start element index (inclusive), defaults to 0
- `to_element`: End element index (exclusive), defaults to 1000000

## Error Responses

### Invalid API Key (401)
```json
{
    "error": "Unauthorized",
    "detail": "Invalid API Key"
}
```

### Invalid Request Parameters (400)
```json
{
    "error": "Bad Request",
    "detail": "Error message"
}
```

### Validation Error (422)
```json
{
    "error": "Validation Error",
    "detail": "Error message"
}
```

## Project Structure

```
hj-docling/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── document.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   └── services/
│       └── document_service.py
├── tests/
├── .env
├── .env.example
├── .gitignore
├── main.py
└── requirements.txt
```

## Security

- API Key authentication is required for all endpoints
- CORS is enabled (configure allowed origins in production)
- Environment variables for sensitive data

## Development

To run the service in development mode with auto-reload:
```bash
uvicorn main:app --reload
```