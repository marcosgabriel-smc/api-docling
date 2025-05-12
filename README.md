# Docling Microservice

A FastAPI-based microservice that provides document conversion capabilities using the Docling library.


## PENDING
- Fix tests

## Features

- Document conversion to Markdown, HTML, and Text formats
- Code understanding enrichment
- Formula understanding enrichment
- Picture classification and description
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
POST /api/v1/document/convert
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "https://example.com/doc.pdf",
    "enrich_code": true,
    "enrich_formula": true,
    "enrich_pictures": true,
    "picture_scale": 2,
    "enrich_picture_description": true,
    "vision_model": "granite",
    "export_config": {
        "format": "html",
        "html_params": {
            "formula_to_mathml": true,
            "html_lang": "en",
            "split_page_view": true
        }
    }
}
```

Response:
```json
{
    "content": "Converted document content"
}
```

### Enrich Code
```http
POST /api/v1/document/enrich-code
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "https://example.com/doc.pdf",
    "export_config": {
        "format": "markdown",
        "markdown_params": {
            "escape_underscores": true,
            "indent": 2,
            "text_width": 80
        }
    }
}
```

### Enrich Formula
```http
POST /api/v1/document/enrich-formula
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "https://example.com/doc.pdf",
    "export_config": {
        "format": "html",
        "html_params": {
            "formula_to_mathml": true
        }
    }
}
```

### Enrich Pictures
```http
POST /api/v1/document/enrich-pictures
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "https://example.com/doc.pdf",
    "picture_scale": 2,
    "export_config": {
        "format": "markdown",
        "markdown_params": {
            "image_placeholder": "<!-- image -->",
            "enable_chart_tables": true
        }
    }
}
```

### Enrich Picture Description
```http
POST /api/v1/document/enrich-picture-description
Headers:
  X-API-Key: your_api_key
  Content-Type: application/json

Body:
{
    "source": "https://example.com/doc.pdf",
    "vision_model": "granite",
    "export_config": {
        "format": "html",
        "html_params": {
            "enable_chart_tables": true
        }
    }
}
```

## Export Format Options

### Markdown Export Parameters
```json
{
    "format": "markdown",
    "markdown_params": {
        "from_element": 0,
        "to_element": 1000000,
        "escape_underscores": true,
        "image_placeholder": "<!-- image -->",
        "enable_chart_tables": true,
        "image_mode": "PLACEHOLDER",
        "indent": 4,
        "text_width": -1,
        "page_break_placeholder": null
    }
}
```

### HTML Export Parameters
```json
{
    "format": "html",
    "html_params": {
        "from_element": 0,
        "to_element": 1000000,
        "enable_chart_tables": true,
        "formula_to_mathml": true,
        "html_lang": "en",
        "html_head": "null",
        "split_page_view": false
    }
}
```

### Text Export Parameters
```json
{
    "format": "text",
    "text_params": {
        "from_element": 0,
        "to_element": 1000000
    }
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