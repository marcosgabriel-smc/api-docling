from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, granite_picture_description, smolvlm_picture_description
from docling.datamodel.base_models import InputFormat, ImageRefMode, ContentLayer, DocItemLabel
from enum import Enum
from typing import Optional, Set, Dict, Any
from sys import maxsize
import asyncio
from functools import lru_cache
import hashlib
import json
from datetime import datetime, timedelta

class VisionModel(str, Enum):
    GRANITE = "granite"
    SMOLVLM = "smolvlm"

class ExportFormat(str, Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    TEXT = "text"

class RateLimiter:
    def __init__(self, max_requests: int = 100, time_window: int = 3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        now = datetime.now()
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < timedelta(seconds=self.time_window)
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        self.requests[client_id].append(now)
        return True

class DocumentService:
    def __init__(self):
        self.converter = DocumentConverter()
        self.rate_limiter = RateLimiter()
        self.processing_tasks: Dict[str, asyncio.Task] = {}
    
    def _generate_cache_key(self, source: str, params: Dict[str, Any]) -> str:
        """Generate a unique cache key for the request parameters"""
        params_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(f"{source}:{params_str}".encode()).hexdigest()
    
    @lru_cache(maxsize=1000)
    def _get_cached_result(self, cache_key: str) -> Optional[str]:
        """Get cached result if available"""
        return None  # Implement actual caching logic here
    
    def _cache_result(self, cache_key: str, result: str) -> None:
        """Cache the result"""
        pass  # Implement actual caching logic here
    
    async def _process_document(self, source: str, params: Dict[str, Any]) -> str:
        """Process document asynchronously"""
        # Simulate long-running task
        await asyncio.sleep(0.1)
        return self.converter.convert(source).document.export_to_markdown(**params)
    
    async def convert_document(
        self, 
        source: str, 
        client_id: str,
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
        # Check rate limit
        if not self.rate_limiter.is_allowed(client_id):
            raise ValueError("Rate limit exceeded")
        
        # Prepare parameters
        params = {
            "from_element": from_element,
            "to_element": to_element,
            "labels": labels,
            "included_content_layers": included_content_layers
        }
        
        # Add format-specific parameters
        if export_format == ExportFormat.MARKDOWN:
            params.update({
                "escape_underscores": escape_underscores,
                "image_placeholder": image_placeholder,
                "enable_chart_tables": enable_chart_tables,
                "image_mode": image_mode,
                "indent": indent,
                "text_width": text_width,
                "page_break_placeholder": page_break_placeholder
            })
        elif export_format == ExportFormat.HTML:
            params.update({
                "enable_chart_tables": enable_chart_tables_html,
                "formula_to_mathml": formula_to_mathml,
                "html_lang": html_lang,
                "html_head": html_head,
                "split_page_view": split_page_view
            })
        
        # Check cache
        cache_key = self._generate_cache_key(source, params)
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        # Process document
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
        
        # Process document asynchronously
        result = await self._process_document(source, params)
        
        # Cache result
        self._cache_result(cache_key, result)
        
        return result 