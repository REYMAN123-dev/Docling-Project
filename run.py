#!/usr/bin/env python3
"""
Main entry point for the Docling File Processor application
"""

import uvicorn
import os
from app.main import app

if __name__ == "__main__":
    # Get port from environment variable (for Render) or default to 5000
    port = int(os.getenv("PORT", 5000))
    
    # Check if we're running on Render (has PORT env var) or locally
    is_render = os.getenv("PORT") is not None
    
    if is_render:
        # Render deployment - bind to all interfaces
        host = "0.0.0.0"
        reload = False
    else:
        # Local development - bind to localhost
        host = "127.0.0.1"
        reload = True
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    ) 
