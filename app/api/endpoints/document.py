from fastapi import APIRouter, Query, Body
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

class ExportConfig(BaseModel):
    format: ExportFormat = Field(ExportFormat.MARKDOWN, description="Format to export the document to")
    markdown_params: Optional[MarkdownExportParams] = Field(None, description="Markdown export parameters")
    html_params: Optional[HtmlExportParams] = Field(None, description="HTML export parameters")
    text_params: Optional[TextExportParams] = Field(None, description="Text export parameters")

class ConvertRequest(BaseModel):
    source: str = Field(..., description="Source document URL or path")
    enrich_code: bool = Field(False, description="Enable code understanding enrichment")
    enrich_formula: bool = Field(False, description="Enable formula understanding enrichment")
    enrich_pictures: bool = Field(False, description="Enable picture classification enrichment")
    picture_scale: int = Field(2, description="Scale factor for generated picture images", ge=1, le=10)
    enrich_picture_description: bool = Field(False, description="Enable picture description enrichment")
    vision_model: VisionModel = Field(VisionModel.GRANITE, description="Vision model to use for picture description")
    export_config: ExportConfig = Field(..., description="Export configuration")

router = APIRouter()
document_service = DocumentService()

@router.post("/convert")
async def convert_document(request: ConvertRequest):
    # Extract export parameters based on format
    export_params = {}
    if request.export_config.format == ExportFormat.MARKDOWN and request.export_config.markdown_params:
        export_params = request.export_config.markdown_params.dict()
    elif request.export_config.format == ExportFormat.HTML and request.export_config.html_params:
        export_params = request.export_config.html_params.dict()
    elif request.export_config.format == ExportFormat.TEXT and request.export_config.text_params:
        export_params = request.export_config.text_params.dict()

    result = await document_service.convert_document(
        source=request.source,
        enrich_code=request.enrich_code,
        enrich_formula=request.enrich_formula,
        enrich_pictures=request.enrich_pictures,
        picture_scale=request.picture_scale,
        enrich_picture_description=request.enrich_picture_description,
        vision_model=request.vision_model,
        export_format=request.export_config.format,
        **export_params
    )
    return {"content": result}

@router.post("/enrich-code")
async def enrich_code(
    source: str = Query(...),
    export_config: ExportConfig = Body(...)
):
    export_params = {}
    if export_config.format == ExportFormat.MARKDOWN and export_config.markdown_params:
        export_params = export_config.markdown_params.dict()
    elif export_config.format == ExportFormat.HTML and export_config.html_params:
        export_params = export_config.html_params.dict()
    elif export_config.format == ExportFormat.TEXT and export_config.text_params:
        export_params = export_config.text_params.dict()

    result = await document_service.convert_document(
        source=source,
        enrich_code=True,
        export_format=export_config.format,
        **export_params
    )
    return {"content": result}

@router.post("/enrich-formula")
async def enrich_formula(
    source: str = Query(...),
    export_config: ExportConfig = Body(...)
):
    export_params = {}
    if export_config.format == ExportFormat.MARKDOWN and export_config.markdown_params:
        export_params = export_config.markdown_params.dict()
    elif export_config.format == ExportFormat.HTML and export_config.html_params:
        export_params = export_config.html_params.dict()
    elif export_config.format == ExportFormat.TEXT and export_config.text_params:
        export_params = export_config.text_params.dict()

    result = await document_service.convert_document(
        source=source,
        enrich_formula=True,
        export_format=export_config.format,
        **export_params
    )
    return {"content": result}

@router.post("/enrich-pictures")
async def enrich_pictures(
    source: str = Query(...),
    picture_scale: int = Query(2, description="Scale factor for generated picture images", ge=1, le=10),
    export_config: ExportConfig = Body(...)
):
    export_params = {}
    if export_config.format == ExportFormat.MARKDOWN and export_config.markdown_params:
        export_params = export_config.markdown_params.dict()
    elif export_config.format == ExportFormat.HTML and export_config.html_params:
        export_params = export_config.html_params.dict()
    elif export_config.format == ExportFormat.TEXT and export_config.text_params:
        export_params = export_config.text_params.dict()

    result = await document_service.convert_document(
        source=source,
        enrich_pictures=True,
        picture_scale=picture_scale,
        export_format=export_config.format,
        **export_params
    )
    return {"content": result}

@router.post("/enrich-picture-description")
async def enrich_picture_description(
    source: str = Query(...),
    vision_model: VisionModel = Query(VisionModel.GRANITE, description="Vision model to use for picture description"),
    export_config: ExportConfig = Body(...)
):
    export_params = {}
    if export_config.format == ExportFormat.MARKDOWN and export_config.markdown_params:
        export_params = export_config.markdown_params.dict()
    elif export_config.format == ExportFormat.HTML and export_config.html_params:
        export_params = export_config.html_params.dict()
    elif export_config.format == ExportFormat.TEXT and export_config.text_params:
        export_params = export_config.text_params.dict()

    result = await document_service.convert_document(
        source=source,
        enrich_picture_description=True,
        vision_model=vision_model,
        export_format=export_config.format,
        **export_params
    )
    return {"content": result} 