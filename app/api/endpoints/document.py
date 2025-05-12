from fastapi import APIRouter, Query, Depends
from app.services.document_service import DocumentService
from app.core.security import validate_api_key

router = APIRouter()
document_service = DocumentService()

@router.post("/convert")
async def convert_document(
    source: str = Query(...),
    api_key: str = Depends(validate_api_key)
):
    markdown = await document_service.convert_document(source)
    return {"markdown": markdown} 