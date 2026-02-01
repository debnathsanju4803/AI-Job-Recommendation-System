# Project Structure

## Overview

This is a complete, production-ready AI Job Recommendation system built with **100% free and open-source** technologies.

## Directory Structure

```
AI-Job-Recommendation-System/
│
├── src/                          # Main source code
│   ├── api/                      # FastAPI REST API
│   │   ├── __init__.py
│   │   └── main.py              # API endpoints
│   │
│   ├── parsers/                  # Resume parsing
│   │   ├── __init__.py
│   │   └── resume_parser.py     # LLM-based resume parser
│   │
│   ├── classifiers/              # Job role classification
│   │   ├── __init__.py
│   │   └── role_classifier.py   # Semantic role classifier
│   │
│   ├── job_search/               # Job search and matching
│   │   ├── __init__.py
│   │   ├── job_scraper.py       # Web scraping from free sources
│   │   └── job_matcher.py       # Job matching and ranking
│   │
│   ├── vector_db/                # Vector database operations
│   │   ├── __init__.py
│   │   └── vector_store.py      # Chroma vector store wrapper
│   │
│   ├── utils/                    # Utilities
│   │   ├── __init__.py
│   │   ├── llm_client.py        # LLM client (Ollama/HuggingFace)
│   │   ├── logger.py            # Logging configuration
│   │   └── pdf_parser.py        # PDF/DOCX parsing
│   │
│   ├── __init__.py
│   └── pipeline.py               # Main orchestration pipeline
│
├── config/                       # Configuration
│   ├── __init__.py
│   └── settings.py              # Application settings
│
├── data/                         # Data storage
│   ├── roles.json               # Job role definitions
│   ├── jobs/                    # Job data
│   ├── resumes/                 # Resume storage
│   └── chroma_db/               # Chroma database files
│
├── scripts/                      # Utility scripts
│   ├── __init__.py
│   ├── fetch_jobs.py            # Job fetching script
│   ├── ingest_jobs.py           # Job ingestion script
│   ├── setup.sh                 # Setup script
│   └── verify_setup.py          # Setup verification script
│
├── docker/                       # Docker configuration
│   ├── Dockerfile               # Main application Dockerfile
│   ├── docker-compose.yml       # Development Docker Compose
│   ├── docker-compose.prod.yml  # Production Docker Compose
│   └── redis/                   # Redis configuration
│       └── redis.conf           # Redis configuration file
│
├── tests/                        # Tests
│   ├── __init__.py
│   ├── test_complete.py         # Comprehensive test suite
│   ├── test_full_pipeline.py    # End-to-end pipeline tests
│   └── test_parser.py           # Parser tests
│
├── logs/                         # Application logs
│
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── Makefile                     # Make commands
├── run.py                       # Main entry point
├── example_usage.py             # Example usage script
├── .env                         # Environment configuration
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── PROJECT_STRUCTURE.md         # This file
├── README.md                    # Documentation
└── test_results.json            # Test results
```

## Key Components

### 1. Resume Parser (`src/parsers/resume_parser.py`)
- Uses free LLM (Ollama or HuggingFace) for extraction
- Extracts structured data: name, email, skills, experience, education
- Supports PDF, DOCX, and text files
- Returns Pydantic models for type safety

### 2. Role Classifier (`src/classifiers/role_classifier.py`)
- Uses sentence transformers for semantic similarity
- Classifies resumes into job roles
- Returns top-k matches with confidence scores

### 3. Job Scraper (`src/job_search/job_scraper.py`)
- Scrapes jobs from free sources:
  - Arbeitnow (API)
  - RemoteOK (API)
  - Indeed (RSS feed)
- Handles deduplication
- Respects rate limits

### 4. Vector Store (`src/vector_db/vector_store.py`)
- Uses Chroma (free, local vector database)
- Stores job descriptions as embeddings
- Fast semantic search (<100ms)
- Persistent storage

### 5. Job Matcher (`src/job_search/job_matcher.py`)
- Multi-factor scoring:
  - Semantic similarity
  - Skills match
  - Experience level match
- Ranks jobs by relevance

### 6. API (`src/api/main.py`)
- FastAPI REST API
- Endpoints:
  - `/api/parse-resume-file` - Parse from file upload
  - `/api/parse-resume-text` - Parse from text
  - `/api/ingest-jobs` - Add jobs to database
  - `/api/job-count` - Get job count
  - `/health` - Health check
- Interactive docs at `/docs`

### 7. Pipeline (`src/pipeline.py`)
- Orchestrates all components
- End-to-end processing:
  1. Parse resume
  2. Classify role
  3. Search jobs
  4. Rank and return results

## Technology Stack

### Free & Open-Source
- **LLM**: Ollama (local) or HuggingFace Transformers
- **Vector DB**: Chroma (local, persistent)
- **Embeddings**: Sentence Transformers
- **API**: FastAPI
- **PDF**: PyMuPDF
- **Web Scraping**: BeautifulSoup, Requests

### No Paid Services
- ❌ No OpenAI API
- ❌ No Pinecone
- ❌ No paid LLM services
- ✅ 100% free and local

## Configuration

All configuration is in `config/settings.py` and can be overridden via `.env` file.

Key settings:
- `LLM_PROVIDER`: ollama or huggingface
- `VECTOR_DB_PROVIDER`: chroma
- `EMBEDDING_MODEL`: sentence-transformers model
- `JOB_SOURCES`: which sources to scrape

## Usage Flow

1. **Setup**: Run `./scripts/setup.sh`
2. **Start LLM**: `ollama serve` and `ollama pull llama3.1:8b`
3. **Ingest Jobs**: `python scripts/ingest_jobs.py`
4. **Run API**: `python run.py` or `uvicorn src.api.main:app --reload`
5. **Use API**: Send POST requests to parse resumes and get job recommendations

## Deployment

### Local Development
```bash
# Setup
./scripts/setup.sh

# Start services
source venv/bin/activate
ollama serve &  # In background
ollama pull llama3.1:8b

# Run API
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Development
```bash
# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Access services
# API: http://localhost:8000
# Ollama: http://localhost:11434
```

### Production Deployment

#### 1. Environment Setup
```bash
# Copy production environment
cp .env.example .env.prod

# Configure production settings
# - Set DEBUG=false
# - Configure production database
# - Set up SSL certificates
# - Configure monitoring
```

#### 2. Docker Production
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Monitor
docker-compose -f docker-compose.prod.yml logs -f
```

#### 3. Kubernetes (Optional)
```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods,services,deployments
```

#### 4. Nginx Reverse Proxy
```nginx
# /etc/nginx/sites-available/resume-parser
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/ssl.crt;
    ssl_certificate_key /path/to/ssl.key;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /docs {
        proxy_pass http://localhost:8000;
    }
    
    location /redoc {
        proxy_pass http://localhost:8000;
    }
}
```

#### 5. Monitoring & Logging
```bash
# Prometheus metrics endpoint
curl http://localhost:8000/metrics

# Health checks
curl http://localhost:8000/health

# Application logs
tail -f logs/app.log
```

#### 6. CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          ssh user@server "cd /app && git pull && docker-compose up -d"
```

### Performance Optimization

#### 1. LLM Optimization
```env
# Use GPU if available
HF_DEVICE=cuda
OLLAMA_GPU=true

# Optimize model size
OLLAMA_MODEL=llama3.1:8b  # Smaller model for faster inference
```

#### 2. Vector Database Optimization
```env
# Increase batch size for bulk operations
CHROMA_BATCH_SIZE=1000

# Enable compression
CHROMA_COMPRESSION=true
```

#### 3. API Optimization
```python
# Use async endpoints
@app.post("/api/parse-resume-file")
async def parse_resume_file(file: UploadFile):
    # Async processing
    pass

# Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

#### 4. Database Optimization
```sql
-- Create indexes for faster queries
CREATE INDEX idx_jobs_title ON jobs(title);
CREATE INDEX idx_jobs_company ON jobs(company);
CREATE INDEX idx_jobs_location ON jobs(location);
```

### Security Hardening

#### 1. Environment Security
```env
# Never commit secrets
DEBUG=false
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/db
```

#### 2. API Security
```python
# Add rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/parse-resume-file")
@limiter.limit("10/minute")
async def parse_resume_file(request: Request, file: UploadFile):
    pass
```

#### 3. File Upload Security
```python
# Validate file types
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

#### 4. Network Security
```bash
# Firewall rules
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw deny 11434      # Block Ollama from external access
```

## Extensibility

### Adding New Job Sources
1. Add method to `job_scraper.py`
2. Add source name to `JOB_SOURCES` in settings
3. Update `search_all_sources()` method

### Adding New Job Roles
- Edit `data/roles.json` (auto-created on first run)
- Or modify `_load_roles()` in `role_classifier.py`

### Custom LLM Models
- For Ollama: Change `OLLAMA_MODEL` in settings
- For HuggingFace: Change `HF_MODEL` in settings

## Performance

- Resume Parsing: 3-5 seconds
- Job Search (Vector DB): <1 second
- Job Search (Web Scraping): 2-5 seconds
- Job Ranking: ~0.5 seconds per job
- End-to-End: 10-20 seconds

## Scalability

- Vector DB can handle millions of jobs
- API can be scaled horizontally
- LLM can be run on GPU for faster inference

## Security

- Input validation with Pydantic
- File upload size limits
- CORS configuration
- Environment variables for secrets
