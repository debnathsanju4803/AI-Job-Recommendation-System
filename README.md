# AI Job Recommendation System

A free, open-source system for parsing resumes and recommending matching jobs using AI. Built with **100% free and open-source** technologies.

## 🚀 Features

- **Resume Parsing**: Extract structured data from PDF, DOCX, and text resumes
- **Job Role Classification**: Automatically classify resumes using semantic similarity
- **Job Search**: Search jobs from multiple sources with web scraping
- **Vector Database**: Fast semantic job matching using Chroma
- **Multi-Factor Scoring**: Rank jobs based on skills, experience, and semantic similarity
- **REST API**: FastAPI-based REST API
- **Docker Support**: Ready for deployment

## 🛠️ Technology Stack

- **LLM**: Ollama (local) or HuggingFace Transformers
- **Vector DB**: Chroma (local, persistent)
- **Embeddings**: Sentence Transformers
- **API**: FastAPI
- **PDF Processing**: PyMuPDF
- **Web Scraping**: BeautifulSoup, Requests
- **Caching**: Redis
- **Rate Limiting**: SlowAPI

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- Ollama (optional, for local LLM)

## 🚀 Quick Start

### Local Setup

1. **Clone and setup**:
```bash
git clone <repository-url>
cd AI-Job-Recommendation-System
./scripts/setup.sh
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Start Ollama** (if using Ollama):
```bash
ollama serve
ollama pull llama3.1:8b
```

4. **Run the API**:
```bash
source venv/bin/activate
uvicorn src.api.main:app --reload
```

### Docker Setup

1. **Start services**:
```bash
docker-compose up -d
```

2. **Pull Ollama model**:
```bash
docker exec -it resume_parser_ollama ollama pull llama3.1:8b
```

3. **Ingest jobs**:
```bash
docker exec -it resume_parser_api python scripts/ingest_jobs.py
```

## 📖 API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Parse Resume from File
```bash
curl -X POST "http://localhost:8000/api/parse-resume-file" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf" \
  -F "top_k=10"
```

### Parse Resume from Text
```bash
curl -X POST "http://localhost:8000/api/parse-resume-text" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer...",
    "top_k": 10
  }'
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## 📁 Project Structure

```
AI-Job-Recommendation-System/
├── src/
│   ├── api/              # FastAPI endpoints
│   ├── parsers/          # Resume parsing
│   ├── classifiers/      # Job role classification
│   ├── job_search/       # Job search and matching
│   ├── vector_db/        # Vector database operations
│   ├── utils/            # Utilities
│   └── pipeline.py       # Main pipeline
├── config/               # Configuration
├── data/                 # Data storage
├── scripts/              # Utility scripts
├── frontend/             # React application
├── docker/               # Docker files
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image
├── docker-compose.yml    # Docker Compose config
└── README.md            # This file
```

## ⚙️ Configuration

### LLM Provider Options

**Ollama (Recommended)**:
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

**HuggingFace**:
```env
LLM_PROVIDER=huggingface
HF_MODEL=microsoft/Phi-3-mini-4k-instruct
HF_DEVICE=cpu  # or cuda for GPU
```

### Vector Database

Chroma (default, local):
```env
VECTOR_DB_PROVIDER=chroma
CHROMA_PERSIST_DIR=./data/chroma_db
```

## 🚢 Deployment

### Docker Deployment

1. Build and run:
```bash
docker-compose up -d
```

2. Check service status:
```bash
docker-compose ps
```

### Production Deployment

1. Set environment variables in `.env`
2. Use production WSGI server:
```bash
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📊 Performance

- **Resume Parsing**: ~3-5 seconds
- **Job Search**: <1 second (vector DB)
- **Job Ranking**: ~0.5 seconds per job
- **End-to-End**: ~10-20 seconds

## 🔒 Security

- Input validation with Pydantic
- File upload size limits
- CORS configuration

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for free local LLM
- [Chroma](https://www.trychroma.com/) for vector database
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [FastAPI](https://fastapi.tiangolo.com/) for API framework

---

**Built with ❤️ using 100% free and open-source technologies**
