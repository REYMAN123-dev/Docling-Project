import hashlib
import json
import os
import re
import tempfile
from typing import Dict, Any, Optional, List
from docling.document_converter import DocumentConverter
from sqlalchemy.orm import Session
from .database import FileRecord

# Try to import magic, with fallback for Windows
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    print("Warning: python-magic not available. Using file extension fallback.")

class FileProcessor:
    def __init__(self):
        # Initialize DocumentConverter with default settings
        self.docling_converter = DocumentConverter()
        
    def calculate_file_hash(self, file_content: bytes) -> str:
        """Calculate SHA-256 hash of file content"""
        return hashlib.sha256(file_content).hexdigest()
    
    def detect_file_type(self, file_content: bytes, filename: str) -> str:
        """Detect file type using python-magic or file extension fallback"""
        if MAGIC_AVAILABLE:
            try:
                mime_type = magic.from_buffer(file_content, mime=True)
                
                # Map MIME types to file extensions
                mime_to_ext = {
                    'application/pdf': 'pdf',
                    'text/plain': 'txt',
                    'text/csv': 'csv',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
                    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
                    'application/msword': 'doc',
                    'application/vnd.ms-powerpoint': 'ppt',
                    'application/vnd.ms-excel': 'xls'
                }
                
                return mime_to_ext.get(mime_type, filename.split('.')[-1] if '.' in filename else 'unknown')
            except Exception as e:
                print(f"Warning: Magic detection failed: {e}. Using file extension fallback.")
                return self._get_file_extension(filename)
        else:
            return self._get_file_extension(filename)
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        if '.' in filename:
            ext = filename.split('.')[-1].lower()
            # Map common extensions
            extension_map = {
                'pdf': 'pdf',
                'docx': 'docx', 'doc': 'doc',
                'txt': 'txt', 'md': 'txt',
                'csv': 'csv',
                'pptx': 'pptx', 'ppt': 'ppt',
                'xlsx': 'xlsx', 'xls': 'xls'
            }
            return extension_map.get(ext, ext)
        return 'unknown'
    
    def extract_text_from_file(self, file_content: bytes, file_type: str, filename: str) -> str:
        """Extract text from file using Docling DocumentConverter"""
        try:
            # For plain text files, try to decode directly first
            if file_type in ['txt', 'csv', 'md']:
                try:
                    text_content = file_content.decode('utf-8', errors='ignore')
                    if text_content.strip():
                        return text_content
                except:
                    pass
            
            # For binary files or if direct decoding fails, use Docling
            # Create a temporary file for Docling to process
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name
            
            try:
                # Use Docling DocumentConverter to convert the file
                result = self.docling_converter.convert(temp_path)
                
                # Extract text from the DoclingDocument
                if hasattr(result, 'document') and hasattr(result.document, 'export_to_markdown'):
                    # Export to markdown format for text extraction
                    return result.document.export_to_markdown()
                elif hasattr(result, 'document') and hasattr(result.document, 'export_to_text'):
                    # If text export is available
                    return result.document.export_to_text()
                elif hasattr(result, 'document'):
                    # Fallback: try to get text from document structure
                    return str(result.document)
                else:
                    # Ultimate fallback
                    return str(result)
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            print(f"Warning: Docling text extraction failed: {e}")
            # Ultimate fallback - try to decode as text
            try:
                return file_content.decode('utf-8', errors='ignore')
            except:
                return str(file_content)
    
    def extract_entities_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text using regex patterns"""
        entities = []
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        for email in emails:
            entities.append({
                "type": "email",
                "value": email,
                "confidence": 0.9
            })
        
        # Phone numbers
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            entities.append({
                "type": "phone",
                "value": phone,
                "confidence": 0.8
            })
        
        # URLs
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        urls = re.findall(url_pattern, text)
        for url in urls:
            entities.append({
                "type": "url",
                "value": url,
                "confidence": 0.9
            })
        
        # Dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
        dates = re.findall(date_pattern, text)
        for date in dates:
            entities.append({
                "type": "date",
                "value": date,
                "confidence": 0.7
            })
        
        # Names (simple pattern)
        name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        names = re.findall(name_pattern, text)
        for name in names:
            entities.append({
                "type": "person",
                "value": name,
                "confidence": 0.6
            })
        
        return entities
    
    def extract_sections_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract document sections"""
        sections = []
        lines = text.split('\n')
        current_section = {"title": "Main Content", "content": "", "level": 1}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a heading
            if re.match(r'^[A-Z][A-Z\s]+$', line) or re.match(r'^[0-9]+\.\s+[A-Z]', line):
                # Save previous section
                if current_section["content"]:
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    "title": line,
                    "content": "",
                    "level": 2 if re.match(r'^[0-9]+\.', line) else 1
                }
            else:
                current_section["content"] += line + "\n"
        
        # Add the last section
        if current_section["content"]:
            sections.append(current_section)
        
        return sections
    
    def extract_json_with_docling(self, file_content: bytes, file_type: str, filename: str) -> Dict[str, Any]:
        """Extract structured JSON data using Docling DocumentConverter"""
        try:
            # Extract text from file using Docling
            text_content = self.extract_text_from_file(file_content, file_type, filename)
            
            # Try to get structured data from Docling as well
            docling_data = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as temp_file:
                    temp_file.write(file_content)
                    temp_path = temp_file.name
                
                try:
                    # Convert using Docling
                    result = self.docling_converter.convert(temp_path)
                    
                    # Try to extract structured data
                    if hasattr(result, 'document'):
                        # Convert document to dict if possible
                        try:
                            docling_data = result.document.model_dump() if hasattr(result.document, 'model_dump') else result.document.__dict__
                        except:
                            docling_data = {"raw_document": str(result.document)}
                    else:
                        docling_data = {"raw_result": str(result)}
                        
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
            except Exception as e:
                print(f"Warning: Docling structured extraction failed: {e}")
                docling_data = {"error": str(e)}
            
            # Extract additional entities and sections
            entities = self.extract_entities_from_text(text_content)
            sections = self.extract_sections_from_text(text_content)
            
            # Create comprehensive JSON structure
            result = {
                "full_text": text_content,  # Include the complete text
                "text_summary": text_content[:500] + "..." if len(text_content) > 500 else text_content,
                "metadata": {
                    "source": "docling_extraction",
                    "file_type": file_type,
                    "text_length": len(text_content),
                    "word_count": len(text_content.split()),
                    "line_count": len(text_content.split('\n')),
                    "extraction_method": "docling_document_converter"
                },
                "entities": entities,
                "sections": sections,
                "docling_extraction": docling_data,
                "statistics": {
                    "total_entities": len(entities),
                    "total_sections": len(sections),
                    "email_count": len([e for e in entities if e["type"] == "email"]),
                    "phone_count": len([e for e in entities if e["type"] == "phone"]),
                    "url_count": len([e for e in entities if e["type"] == "url"]),
                    "person_count": len([e for e in entities if e["type"] == "person"])
                }
            }
            
            return result
            
        except Exception as e:
            print(f"Warning: Docling extraction failed: {e}")
            # Fallback to basic text processing
            try:
                text_content = file_content.decode('utf-8', errors='ignore')
            except:
                text_content = str(file_content)
            
            entities = self.extract_entities_from_text(text_content)
            sections = self.extract_sections_from_text(text_content)
            
            return {
                "full_text": text_content,
                "text_summary": text_content[:500] + "..." if len(text_content) > 500 else text_content,
                "metadata": {
                    "source": "fallback_processing",
                    "file_type": file_type,
                    "error": str(e),
                    "text_length": len(text_content),
                    "word_count": len(text_content.split()),
                    "line_count": len(text_content.split('\n')),
                    "extraction_method": "fallback"
                },
                "entities": entities,
                "sections": sections,
                "statistics": {
                    "total_entities": len(entities),
                    "total_sections": len(sections),
                    "email_count": len([e for e in entities if e["type"] == "email"]),
                    "phone_count": len([e for e in entities if e["type"] == "phone"]),
                    "url_count": len([e for e in entities if e["type"] == "url"]),
                    "person_count": len([e for e in entities if e["type"] == "person"])
                }
            }
    
    def process_file(self, file_content: bytes, filename: str, db: Session) -> Dict[str, Any]:
        """Main method to process file and return JSON data using Docling DocumentConverter"""
        
        # Calculate file hash for duplicate detection
        file_hash = self.calculate_file_hash(file_content)
        
        # Check if file already exists in database
        existing_record = db.query(FileRecord).filter(FileRecord.file_hash == file_hash).first()
        
        if existing_record:
            return {
                "status": "already_available",
                "message": "File already available in database",
                "data": json.loads(existing_record.json_data),
                "filename": existing_record.filename,
                "created_at": existing_record.created_at.isoformat()
            }
        
        # Detect file type
        file_type = self.detect_file_type(file_content, filename)
        
        # Extract JSON using Docling DocumentConverter
        json_data = self.extract_json_with_docling(file_content, file_type, filename)
        
        # Store in database
        file_record = FileRecord(
            filename=filename,
            file_hash=file_hash,
            file_content=file_content,
            json_data=json.dumps(json_data, ensure_ascii=False),
            file_type=file_type
        )
        
        db.add(file_record)
        db.commit()
        
        return {
            "status": "processed",
            "message": "File processed successfully using Docling DocumentConverter",
            "data": json_data,
            "filename": filename,
            "file_type": file_type,
            "file_hash": file_hash
        }