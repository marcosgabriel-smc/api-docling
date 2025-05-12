from fastapi import APIRouter, HTTPException, status
from app.services.document_service import DocumentService, VisionModel, ExportFormat, ImageRefMode, ContentLayer, DocItemLabel
from typing import Optional, Set
from pydantic import BaseModel, Field, field_validator, model_validator
import re
from urllib.parse import urlparse

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class SuccessResponse(BaseModel):
    content: str
    format: str
    metadata: Optional[dict] = None

class BaseExportParams(BaseModel):
    from_element: int = Field(0, description="Start element index (inclusive)", ge=0)
    to_element: int = Field(1000000, description="End element index (exclusive)", gt=0)
    labels: Optional[Set[DocItemLabel]] = Field(None, description="Set of document labels to include")
    included_content_layers: Optional[Set[ContentLayer]] = Field(None, description="Set of content layers to include")

    @field_validator('to_element')
    @classmethod
    def validate_element_range(cls, v, info):
        if info.data.get('from_element', 0) >= v:
            raise ValueError('to_element must be greater than from_element')
        return v

class MarkdownExportParams(BaseExportParams):
    escape_underscores: bool = Field(True, description="Whether to escape underscores in text content")
    image_placeholder: str = Field("<!-- image -->", description="Placeholder for images in markdown")
    enable_chart_tables: bool = Field(True, description="Enable chart tables in markdown")
    image_mode: ImageRefMode = Field(ImageRefMode.PLACEHOLDER, description="Mode for including images")
    indent: int = Field(4, description="Indent in spaces for nested lists", ge=0, le=8)
    text_width: int = Field(-1, description="Text width for markdown", ge=-1)
    page_break_placeholder: Optional[str] = Field(None, description="Placeholder for page breaks")

    @field_validator('image_placeholder')
    @classmethod
    def validate_image_placeholder(cls, v):
        if not re.match(r'^<!--.*-->$', v):
            raise ValueError('image_placeholder must be a valid HTML comment')
        return v

class HtmlExportParams(BaseExportParams):
    enable_chart_tables: bool = Field(True, description="Enable chart tables in HTML")
    formula_to_mathml: bool = Field(True, description="Convert formulas to MathML")
    html_lang: str = Field("en", description="HTML language attribute", min_length=2, max_length=5)
    html_head: str = Field("null", description="Custom HTML head content")
    split_page_view: bool = Field(False, description="Enable split page view in HTML")

    @field_validator('html_lang')
    @classmethod
    def validate_html_lang(cls, v):
        if not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', v):
            raise ValueError('html_lang must be a valid language code (e.g., "en" or "en-US")')
        return v

class TextExportParams(BaseExportParams):
    pass

class BaseRequest(BaseModel):
    source: str = Field(..., description="Source document URL or path")
    enrich_code: bool = Field(False, description="Enable code understanding enrichment")
    enrich_formula: bool = Field(False, description="Enable formula understanding enrichment")
    enrich_pictures: bool = Field(False, description="Enable picture classification enrichment")
    picture_scale: int = Field(2, description="Scale factor for generated picture images", ge=1, le=10)
    enrich_picture_description: bool = Field(False, description="Enable picture description enrichment")
    vision_model: VisionModel = Field(VisionModel.GRANITE, description="Vision model to use for picture description")

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

    @model_validator(mode='after')
    def validate_enrichment_options(self):
        if self.enrich_picture_description and not self.enrich_pictures:
            raise ValueError('enrich_picture_description requires enrich_pictures to be enabled')
        return self

class ConvertToMarkdownRequest(BaseRequest):
    markdown_params: MarkdownExportParams = Field(..., description="Markdown export parameters")

class ConvertToHtmlRequest(BaseRequest):
    html_params: HtmlExportParams = Field(..., description="HTML export parameters")

class ConvertToTextRequest(BaseRequest):
    text_params: TextExportParams = Field(..., description="Text export parameters")

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
async def convert_to_markdown(request: ConvertToMarkdownRequest):
    try:
        result = await document_service.convert_document(
            source=request.source,
            enrich_code=request.enrich_code,
            enrich_formula=request.enrich_formula,
            enrich_pictures=request.enrich_pictures,
            picture_scale=request.picture_scale,
            enrich_picture_description=request.enrich_picture_description,
            vision_model=request.vision_model,
            export_format=ExportFormat.MARKDOWN,
            **request.markdown_params.dict()
        )
        return SuccessResponse(
            content=result,
            format="markdown",
            metadata={
                "enrichments": {
                    "code": request.enrich_code,
                    "formula": request.enrich_formula,
                    "pictures": request.enrich_pictures,
                    "picture_description": request.enrich_picture_description
                }
            }
        )
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
async def convert_to_html(request: ConvertToHtmlRequest):
    try:
        result = await document_service.convert_document(
            source=request.source,
            enrich_code=request.enrich_code,
            enrich_formula=request.enrich_formula,
            enrich_pictures=request.enrich_pictures,
            picture_scale=request.picture_scale,
            enrich_picture_description=request.enrich_picture_description,
            vision_model=request.vision_model,
            export_format=ExportFormat.HTML,
            **request.html_params.dict()
        )
        return SuccessResponse(
            content=result,
            format="html",
            metadata={
                "enrichments": {
                    "code": request.enrich_code,
                    "formula": request.enrich_formula,
                    "pictures": request.enrich_pictures,
                    "picture_description": request.enrich_picture_description
                }
            }
        )
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
async def convert_to_text(request: ConvertToTextRequest):
    try:
        result = await document_service.convert_document(
            source=request.source,
            enrich_code=request.enrich_code,
            enrich_formula=request.enrich_formula,
            enrich_pictures=request.enrich_pictures,
            picture_scale=request.picture_scale,
            enrich_picture_description=request.enrich_picture_description,
            vision_model=request.vision_model,
            export_format=ExportFormat.TEXT,
            **request.text_params.dict()
        )
        return SuccessResponse(
            content=result,
            format="text",
            metadata={
                "enrichments": {
                    "code": request.enrich_code,
                    "formula": request.enrich_formula,
                    "pictures": request.enrich_pictures,
                    "picture_description": request.enrich_picture_description
                }
            }
        )
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