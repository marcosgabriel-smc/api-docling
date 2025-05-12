from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.security import validate_api_key

app = FastAPI(title="Docling Microservice")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API key validation middleware
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    await validate_api_key(request)
    response = await call_next(request)
    return response

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Docling Microservice!"} 