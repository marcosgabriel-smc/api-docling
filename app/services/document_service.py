from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, granite_picture_description, smolvlm_picture_description
from docling.datamodel.base_models import InputFormat, ImageRefMode, ContentLayer, DocItemLabel
from enum import Enum
from typing import Optional, Set
from sys import maxsize

class VisionModel(str, Enum):
    GRANITE = "granite"
    SMOLVLM = "smolvlm"

class ExportFormat(str, Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    TEXT = "text"

class DocumentService:
    def __init__(self):
        self.converter = DocumentConverter()
    
    async def convert_document(
        self, 
        source: str, 
        enrich_code: bool = False, 
        enrich_formula: bool = False,
        enrich_pictures: bool = False,
        picture_scale: int = 2,
        enrich_picture_description: bool = False,
        vision_model: VisionModel = VisionModel.GRANITE,
        export_format: ExportFormat = ExportFormat.MARKDOWN,
        # Common export parameters
        from_element: int = 0,
        to_element: int = maxsize,
        labels: Optional[Set[DocItemLabel]] = None,
        included_content_layers: Optional[Set[ContentLayer]] = None,
        # Markdown specific parameters
        escape_underscores: bool = True,
        image_placeholder: str = "<!-- image -->",
        enable_chart_tables: bool = True,
        image_mode: ImageRefMode = ImageRefMode.PLACEHOLDER,
        indent: int = 4,
        text_width: int = -1,
        page_break_placeholder: Optional[str] = None,
        # HTML specific parameters
        enable_chart_tables_html: bool = True,
        formula_to_mathml: bool = True,
        html_lang: str = "en",
        html_head: str = "null",
        split_page_view: bool = False
    ) -> str:
        if any([enrich_code, enrich_formula, enrich_pictures, enrich_picture_description]):
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_code_enrichment = enrich_code
            pipeline_options.do_formula_enrichment = enrich_formula
            
            if enrich_pictures:
                pipeline_options.generate_picture_images = True
                pipeline_options.images_scale = picture_scale
                pipeline_options.do_picture_classification = True
            
            if enrich_picture_description:
                pipeline_options.do_picture_description = True
                if vision_model == VisionModel.GRANITE:
                    pipeline_options.picture_description_options = granite_picture_description
                elif vision_model == VisionModel.SMOLVLM:
                    pipeline_options.picture_description_options = smolvlm_picture_description
            
            self.converter = DocumentConverter(format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            })
            
        result = self.converter.convert(source)
        doc = result.document

        if export_format == ExportFormat.MARKDOWN:
            return doc.export_to_markdown(
                from_element=from_element,
                to_element=to_element,
                labels=labels,
                escape_underscores=escape_underscores,
                image_placeholder=image_placeholder,
                enable_chart_tables=enable_chart_tables,
                image_mode=image_mode,
                indent=indent,
                text_width=text_width,
                included_content_layers=included_content_layers,
                page_break_placeholder=page_break_placeholder
            )
        elif export_format == ExportFormat.HTML:
            return doc.export_to_html(
                from_element=from_element,
                to_element=to_element,
                labels=labels,
                enable_chart_tables=enable_chart_tables_html,
                image_mode=image_mode,
                formula_to_mathml=formula_to_mathml,
                html_lang=html_lang,
                html_head=html_head,
                included_content_layers=included_content_layers,
                split_page_view=split_page_view
            )
        else:  # TEXT
            return doc.export_to_text(
                from_element=from_element,
                to_element=to_element,
                labels=labels
            ) 