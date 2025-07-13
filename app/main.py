from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from .database import get_db, init_db
from .file_processor import FileProcessor
from .models import FileUploadResponse, FileRecordResponse, ErrorResponse

load_dotenv()

app = FastAPI(
    title="Docling File Processor",
    description="A web application that processes files using Docling and LangChain, storing results in PostgreSQL",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize file processor
file_processor = FileProcessor()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and process a file using Docling"""
    
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        # Read file content
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Process the file
        result = file_processor.process_file(file_content, file.filename, db)
        
        return FileUploadResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/files/", response_model=list[FileRecordResponse])
async def list_files(db: Session = Depends(get_db)):
    """List all processed files"""
    from .database import FileRecord
    
    files = db.query(FileRecord).order_by(FileRecord.created_at.desc()).all()
    return [FileRecordResponse(
        id=file.id,
        filename=file.filename,
        file_type=file.file_type,
        created_at=file.created_at,
        updated_at=file.updated_at
    ) for file in files]

@app.get("/files/{file_id}/json")
async def get_file_json(file_id: int, db: Session = Depends(get_db)):
    """Get JSON data for a specific file"""
    from .database import FileRecord
    import json
    
    file_record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "filename": file_record.filename,
        "file_type": file_record.file_type,
        "created_at": file_record.created_at.isoformat(),
        "data": json.loads(file_record.json_data)
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 