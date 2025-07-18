from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

# Database configuration - prioritize DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL is not set, use the online database as default
if not DATABASE_URL:
    # Use online database as default for production
    DATABASE_URL = "postgresql://postgres1:4gAV8sCmCzkpULhZM5vCEoIBoaPNnszx@dpg-d1q28k8dl3ps739b6ujg-a.oregon-postgres.render.com/docling_db"
    
    # Only use localhost if explicitly set for development
    DB_HOST = os.getenv("DB_HOST")
    if DB_HOST and DB_HOST != "localhost":
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "docling_db")
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        
        # URL encode the password to handle special characters
        encoded_password = urllib.parse.quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
        
        # Construct database URL from separate components
        DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Debug: Print the database URL being used (remove this in production)
print(f"🔗 Using database URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FileRecord(Base):
    __tablename__ = "file_records"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_hash = Column(String, unique=True, index=True)
    file_content = Column(LargeBinary)
    json_data = Column(Text)
    file_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine) 