from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from enum import Enum

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
        export_format: ExportFormat = ExportFormat.MARKDOWN,
        from_element: int = 0,
        to_element: int = 1000000
    ) -> str:
        # Enable all enrichment features
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_code_enrichment = True
        pipeline_options.do_formula_enrichment = True
        pipeline_options.generate_picture_images = True
        pipeline_options.images_scale = 2
        pipeline_options.do_picture_classification = True
        pipeline_options.do_picture_description = True
        
        self.converter = DocumentConverter(format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        })
        
        result = self.converter.convert(source)
        doc = result.document

        if export_format == ExportFormat.MARKDOWN:
            return doc.export_to_markdown(
                from_element=from_element,
                to_element=to_element
            )
        elif export_format == ExportFormat.HTML:
            return doc.export_to_html(
                from_element=from_element,
                to_element=to_element
            )
        else:  # TEXT
            return doc.export_to_text(
                from_element=from_element,
                to_element=to_element
            ) 