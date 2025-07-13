# Docling File Processor

A FastAPI web application that processes files using Docling and LangChain, storing results in PostgreSQL.

## Features

- 🚀 **Multi-format Support**: PDF, DOCX, TXT, CSV, PPTX, XLSX, DOC, PPT, XLS
- 🔍 **Smart Duplicate Detection**: Uses file hash to prevent reprocessing
- 📊 **Structured JSON Output**: Extracts meaningful data using Docling
- 💾 **PostgreSQL Storage**: Persistent storage with metadata
- 🌐 **Modern Web Interface**: Beautiful, responsive UI with drag-and-drop

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   DATABASE_URL=postgresql://postgres1:4gAV8sCmCzkpULhZM5vCEoIBoaPNnszx@dpg-d1q28k8dl3ps739b6ujg-a/docling_db
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Open** `http://localhost:8000` in your browser

## API Endpoints

- `GET /` - Web interface
- `POST /upload/` - Upload and process a file
- `GET /files/` - List all processed files
- `GET /files/{file_id}/json` - Get JSON data for a specific file

## Deployment

For Render deployment:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variable**: `DATABASE_URL=postgresql://postgres1:4gAV8sCmCzkpULhZM5vCEoIBoaPNnszx@dpg-d1q28k8dl3ps739b6ujg-a/docling_db` 