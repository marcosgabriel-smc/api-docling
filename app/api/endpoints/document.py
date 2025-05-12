from fastapi import APIRouter, Body
from app.services.document_service import DocumentService, VisionModel, ExportFormat, ImageRefMode, ContentLayer, DocItemLabel
from typing import Optional, Set
from pydantic import BaseModel, Field

class BaseExportParams(BaseModel):
    from_element: int = Field(0, description="Start element index (inclusive)")
    to_element: int = Field(1000000, description="End element index (exclusive)")
    labels: Optional[Set[DocItemLabel]] = Field(None, description="Set of document labels to include")
    included_content_layers: Optional[Set[ContentLayer]] = Field(None, description="Set of content layers to include")

class MarkdownExportParams(BaseExportParams):
    escape_underscores: bool = Field(True, description="Whether to escape underscores in text content")
    image_placeholder: str = Field("<!-- image -->", description="Placeholder for images in markdown")
    enable_chart_tables: bool = Field(True, description="Enable chart tables in markdown")
    image_mode: ImageRefMode = Field(ImageRefMode.PLACEHOLDER, description="Mode for including images")
    indent: int = Field(4, description="Indent in spaces for nested lists")
    text_width: int = Field(-1, description="Text width for markdown")
    page_break_placeholder: Optional[str] = Field(None, description="Placeholder for page breaks")

class HtmlExportParams(BaseExportParams):
    enable_chart_tables: bool = Field(True, description="Enable chart tables in HTML")
    formula_to_mathml: bool = Field(True, description="Convert formulas to MathML")
    html_lang: str = Field("en", description="HTML language attribute")
    html_head: str = Field("null", description="Custom HTML head content")
    split_page_view: bool = Field(False, description="Enable split page view in HTML")

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

class ConvertToMarkdownRequest(BaseRequest):
    markdown_params: MarkdownExportParams = Field(..., description="Markdown export parameters")

class ConvertToHtmlRequest(BaseRequest):
    html_params: HtmlExportParams = Field(..., description="HTML export parameters")

class ConvertToTextRequest(BaseRequest):
    text_params: TextExportParams = Field(..., description="Text export parameters")

router = APIRouter()
document_service = DocumentService()

@router.post("/convert/markdown")
async def convert_to_markdown(request: ConvertToMarkdownRequest):
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
    return {"content": result}

@router.post("/convert/html")
async def convert_to_html(request: ConvertToHtmlRequest):
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
    return {"content": result}

@router.post("/convert/text")
async def convert_to_text(request: ConvertToTextRequest):
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
    return {"content": result} 