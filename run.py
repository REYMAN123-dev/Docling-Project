#!/usr/bin/env python3
"""
Main entry point for the Docling File Processor application
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # Changed from 0.0.0.0 to localhost
        port=8000,
        reload=True,
        log_level="info"
    ) 