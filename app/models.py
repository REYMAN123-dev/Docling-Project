from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class FileUploadResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any]
    filename: str
    file_type: Optional[str] = None
    file_hash: Optional[str] = None
    created_at: Optional[str] = None

class FileRecordResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None 