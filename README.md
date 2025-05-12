# Docling Microservice

A FastAPI-based microservice that provides document conversion capabilities using the Docling library.

## Features

- Document conversion to Markdown
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

### Convert Document
```http
POST /api/v1/document/convert?source=<document_url>
Headers:
  X-API-Key: your_api_key
```

Response:
```json
{
    "markdown": "Converted document in markdown format"
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


## PENDING
- Fix tests