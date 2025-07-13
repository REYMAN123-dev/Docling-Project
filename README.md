# Docling File Processor

A modern web application that processes various file types using **Docling** and **LangChain**, extracting structured JSON data and storing results in **PostgreSQL**. The application includes duplicate detection to avoid reprocessing the same files.

## Features

- 🚀 **Multi-format Support**: PDF, DOCX, TXT, CSV, PPTX, XLSX, DOC, PPT, XLS
- 🔍 **Smart Duplicate Detection**: Uses file hash to prevent reprocessing
- 📊 **Structured JSON Output**: Extracts meaningful data using Docling
- 💾 **PostgreSQL Storage**: Persistent storage with metadata
- 🌐 **Modern Web Interface**: Beautiful, responsive UI with drag-and-drop
- 📥 **JSON Download**: Direct download of extracted JSON data
- ⚡ **Fast Processing**: Optimized with LangChain document loaders

## Tech Stack

- **Backend**: FastAPI (Python)
- **AI/ML**: LangChain, Docling
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **File Processing**: python-magic, various document loaders

## Installation

### Prerequisites

1. **Python 3.8+**
2. **PostgreSQL** installed and running
3. **Git** (for cloning)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd docling-file-processor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env with your database credentials
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=docling_db
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE docling_db;
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:8000`

### Windows Users

If you're on Windows and encounter dependency issues, see [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed instructions.

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Drag and drop any supported file type or click "Choose File"
3. The application will process the file and display the extracted JSON data
4. If the file was already processed, it will show the cached result
5. Click "Download JSON File" to save the extracted data

### API Endpoints

- `GET /` - Web interface
- `POST /upload/` - Upload and process a file
- `GET /files/` - List all processed files
- `GET /files/{file_id}/json` - Get JSON data for a specific file

### Example API Usage

```bash
# Upload a file
curl -X POST "http://localhost:8000/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"

# List all files
curl -X GET "http://localhost:8000/files/" \
  -H "accept: application/json"

# Get JSON data for a specific file
curl -X GET "http://localhost:8000/files/1/json" \
  -H "accept: application/json"
```

## Project Structure

```
docling-file-processor/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database models and configuration
│   ├── file_processor.py # File processing logic
│   └── models.py        # Pydantic models
├── static/
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       └── app.js       # Main JavaScript
├── templates/
│   └── index.html       # Main HTML template
├── requirements.txt     # Python dependencies
├── run.py             # Application entry point
├── setup.py           # Setup script
├── Dockerfile         # Container configuration
├── docker-compose.yml # Docker deployment
├── env_example.txt    # Environment variables template
├── test_sample.txt    # Sample file for testing
└── README.md          # This file
```

## How It Works

1. **File Upload**: User uploads a file through the web interface
2. **Hash Calculation**: System calculates SHA-256 hash of file content
3. **Duplicate Check**: Checks if file already exists in database
4. **File Processing**: If new file, processes using appropriate LangChain loader
5. **JSON Extraction**: Uses Docling to extract structured data
6. **Database Storage**: Stores file content, metadata, and JSON data
7. **Response**: Returns processed JSON or cached result with download option

## Supported File Types

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | .pdf | Portable Document Format |
| Word | .docx, .doc | Microsoft Word documents |
| Text | .txt, .md | Plain text files |
| CSV | .csv | Comma-separated values |
| PowerPoint | .pptx, .ppt | Microsoft PowerPoint |
| Excel | .xlsx, .xls | Microsoft Excel |

## Configuration

### Environment Variables

- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: docling_db)
- `DB_USER`: Database username (default: postgres)
- `DB_PASSWORD`: Database password
- `SECRET_KEY`: Application secret key
- `DEBUG`: Enable debug mode (True/False)

### Database Schema

The application creates a `file_records` table with the following structure:

- `id`: Primary key
- `filename`: Original filename
- `file_hash`: SHA-256 hash for duplicate detection
- `file_content`: Binary file content
- `json_data`: Extracted JSON data
- `file_type`: Detected file type
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in .env file
   - Verify database exists

2. **File Processing Error**
   - Check file format is supported
   - Ensure file is not corrupted
   - Verify sufficient disk space

3. **Import Errors**
   - Activate virtual environment
   - Reinstall requirements: `pip install -r requirements.txt`

### Logs

The application logs to console. For production, consider using a proper logging configuration.

## Development

### Running in Development Mode

```bash
python run.py
```

This runs the server with auto-reload enabled.

### Testing

You can test the API using the interactive docs at `http://localhost:8000/docs`

## Deployment

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Manual Deployment

1. Set up a production PostgreSQL database
2. Configure environment variables
3. Install dependencies
4. Run with a production WSGI server like Gunicorn

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please create an issue in the repository. 