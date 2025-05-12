from docling.document_converter import DocumentConverter

class DocumentService:
    def __init__(self):
        self.converter = DocumentConverter()
    
    async def convert_document(self, source: str) -> str:
        result = self.converter.convert(source)
        return result.document.export_to_markdown() 