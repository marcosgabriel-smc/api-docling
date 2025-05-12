from fastapi import APIRouter, HTTPException, status
from app.services.document_service import DocumentService, ExportFormat
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from urllib.parse import urlparse

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class SuccessResponse(BaseModel):
    content: str
    format: str

class BaseRequest(BaseModel):
    source: str = Field(..., description="Source document URL or path")
    from_element: int = Field(0, description="Start element index (inclusive)", ge=0)
    to_element: int = Field(1000000, description="End element index (exclusive)", gt=0)

    @field_validator('source')
    @classmethod
    def validate_source(cls, v):
        if v.startswith(('http://', 'https://')):
            try:
                result = urlparse(v)
                if not all([result.scheme, result.netloc]):
                    raise ValueError('Invalid URL format')
            except Exception as e:
                raise ValueError(f'Invalid URL: {str(e)}')
        elif not v.startswith(('/', './', '../')):
            raise ValueError('Local file path must be absolute or relative')
        return v

    @field_validator('to_element')
    @classmethod
    def validate_element_range(cls, v, info):
        if info.data.get('from_element', 0) >= v:
            raise ValueError('to_element must be greater than from_element')
        return v

router = APIRouter()
document_service = DocumentService()

@router.post("/convert/markdown", 
    response_model=SuccessResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request parameters"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    status_code=status.HTTP_200_OK)
async def convert_to_markdown(request: BaseRequest):
    try:
        result = await document_service.convert_document(
            source=request.source,
            export_format=ExportFormat.MARKDOWN,
            from_element=request.from_element,
            to_element=request.to_element
        )
        return SuccessResponse(content=result, format="markdown")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/convert/html",
    response_model=SuccessResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request parameters"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    status_code=status.HTTP_200_OK)
async def convert_to_html(request: BaseRequest):
    try:
        result = await document_service.convert_document(
            source=request.source,
            export_format=ExportFormat.HTML,
            from_element=request.from_element,
            to_element=request.to_element
        )
        return SuccessResponse(content=result, format="html")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post("/convert/text",
    response_model=SuccessResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request parameters"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    status_code=status.HTTP_200_OK)
async def convert_to_text(request: BaseRequest):
    try:
        result = await document_service.convert_document(
            source=request.source,
            export_format=ExportFormat.TEXT,
            from_element=request.from_element,
            to_element=request.to_element
        )
        return SuccessResponse(content=result, format="text")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        ) 