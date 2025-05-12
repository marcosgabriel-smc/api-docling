from fastapi import FastAPI, Query, Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from docling.document_converter import DocumentConverter
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY") 

api_key_header = APIKeyHeader(name=API_KEY_NAME)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

@app.middleware("http")
async def validate_api_key(request: Request, call_next):
    api_key = request.headers.get(API_KEY_NAME)
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to the Docling Microservice!"}

@app.post("/convert")
async def convert_document(source: str = Query(...), api_key: str = Depends(get_api_key)):
    converter = DocumentConverter()
    result = converter.convert(source)
    return {"markdown": result.document.export_to_markdown()} 