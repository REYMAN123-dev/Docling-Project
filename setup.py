#!/usr/bin/env python3
"""
Setup script for Docling File Processor
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print("✅ Python version is compatible")

def create_env_file():
    """Create .env file from template"""
    env_example = Path("env_example.txt")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_example.exists():
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your database credentials")
    else:
        print("❌ env_example.txt not found")

def install_dependencies():
    """Install Python dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def check_database_connection():
    """Check database connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("⚠️  DATABASE_URL not set in .env file")
            return False
        
        print("✅ Database URL configured")
        return True
    except ImportError:
        print("❌ python-dotenv not installed")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Docling File Processor...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create environment file
    create_env_file()
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    install_dependencies()
    
    # Check database configuration
    print("\n🔍 Checking database configuration...")
    check_database_connection()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your PostgreSQL credentials")
    print("2. Create PostgreSQL database: CREATE DATABASE docling_db;")
    print("3. Run the application: python run.py")
    print("4. Open http://localhost:8000 in your browser")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 