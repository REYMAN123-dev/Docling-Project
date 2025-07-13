#!/usr/bin/env python3
"""
Main entry point for the Docling File Processor application
"""

import uvicorn
import os
from app.main import app

if __name__ == "__main__":
    # Get port from environment variable (for Render) or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # Use localhost for local development
        port=port,
        reload=False,  # Disable reload for testing
        log_level="debug"
    ) 
