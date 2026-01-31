# Project Structure

## Overview

This is a complete, production-ready AI Resume Parser & Job Recommender system built with **100% free and open-source** technologies.

## Directory Structure

```
AI-RESUME-PARSER-JOB-RECOMMEDER/
│
├── src/                          # Main source code
│   ├── api/                      # FastAPI REST API
│   │   └── main.py              # API endpoints
│   │
│   ├── parsers/                  # Resume parsing
│   │   └── resume_parser.py     # LLM-based resume parser
│   │
│   ├── classifiers/              # Job role classification
│   │   └── role_classifier.py   # Semantic role classifier
│   │
│   ├── job_search/               # Job search and matching
│   │   ├── job_scraper.py       # Web scraping from free sources
│   │   └── job_matcher.py       # Job matching and ranking
│   │
│   ├── vector_db/                  # Vector database operations
│   │   └── vector_store.py      # Chroma vector store wrapper
│   │
│   ├── utils/                     # Utilities
│   │   ├── llm_client.py        # LLM client (Ollama/HuggingFace)
│   │   ├── logger.py            # Logging configuration
│   │   └── pdf_parser.py        # PDF/DOCX parsing
│   │
│   └── pipeline.py               # Main orchestration pipeline
│
├── config/                        # Configuration
│   └── settings.py              # Application settings
│
├── data/                          # Data storage
│   ├── jobs/                     # Job data
│   ├── resumes/                  # Resume storage
│   └── chroma_db/                # Chroma database files
│
├── scripts/                        # Utility scripts
│   ├── setup.sh                 # Setup script
│   └── ingest_jobs.py           # Job ingestion script
│
├── tests/                         # Tests
│   └── test_parser.py           # Basic tests
│
├── docker/                        # Docker files (if needed)
│
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── Makefile                     # Make commands
├── run.py                       # Main entry point
├── example_usage.py             # Example usage script
└── README.md                    # Documentation
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
  - GitHub Jobs (API)
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

### Local
```bash
python run.py
```

### Docker
```bash
docker-compose up -d
```

### Production
- Use gunicorn with uvicorn workers
- Add reverse proxy (Nginx)
- Set up monitoring
- Configure logging

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
- Can add Redis for caching

## Security

- Input validation with Pydantic
- File upload size limits
- CORS configuration
- Environment variables for secrets
