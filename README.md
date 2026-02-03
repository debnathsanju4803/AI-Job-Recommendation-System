# AI Job Recommendation System

A modern, free, and open-source system for parsing resumes and recommending matching jobs using AI. Built with **100% free and open-source** technologies.

## 🚀 Features

- **Resume Parsing**: Extract structured data from PDF, DOCX, and text resumes
- **Job Role Classification**: Automatically classify resumes using semantic similarity
- **Job Search**: Search jobs from multiple sources with web scraping
- **Vector Database**: Fast semantic job matching using Chroma
- **Multi-Factor Scoring**: Rank jobs based on skills, experience, and semantic similarity
- **Modern Frontend**: React + TypeScript + Material-UI
- **Docker Support**: Ready for deployment

## 🛠️ Technology Stack

### Backend (Python)
- **API**: FastAPI
- **LLM**: Ollama (local) or HuggingFace Transformers
- **Vector DB**: Chroma (local, persistent)
- **Embeddings**: Sentence Transformers
- **PDF Processing**: PyMuPDF
- **Web Scraping**: BeautifulSoup, Requests
- **Caching**: Redis
- **Rate Limiting**: SlowAPI

### Frontend (React)
- **Framework**: React 18 + TypeScript
- **UI Library**: Material-UI (MUI)
- **State Management**: Redux Toolkit
- **Build Tool**: Vite
- **Routing**: React Router DOM
- **Styling**: CSS-in-JS with MUI

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Docker & Docker Compose (optional)
- Ollama (optional, for local LLM)

## 🚀 Quick Start

### Local Setup

1. **Clone and setup**:
```bash
git clone <repository-url>
cd AI-Job-Recommendation-System
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
cd frontend && npm install && cd ..
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Start system**:
```bash
./start.sh
```

## 🔄 System Workflow

```mermaid
flowchart TD
    A[📤 User Upload Resume] --> B[📄 Extract Text<br/>(PyMuPDF)]
    B --> C[🤖 Parse Resume<br/>(Regex + LLM)]
    C --> D[🎯 Generate Embeddings<br/>(Sentence Transformers)]
    
    D --> E[🔍 Compare with Roles<br/>(Job Role DB)]
    E --> F[📊 Get Top Roles<br/>(Similarity Score)]
    
    F --> G[🌐 Scrape Jobs<br/>(Web Scraping)]
    G --> H[💾 Store in Vector DB<br/>(Chroma)]
    H --> I[🔍 Find Similar Jobs<br/>(Vector Search)]
    
    I --> J[📊 Multi-Factor Scoring<br/>(Skills + Experience + Match)]
    J --> K[📈 Rank Jobs<br/>(Relevance Score)]
    
    K --> L[📱 Frontend Display<br/>(React Dashboard)]
    
    style A fill:#e1f5fe
    style L fill:#f3e5f5
    style J fill:#fff3e0
    style K fill:#e8f5e8
```

### 📋 **Processing Flow:**

1. **📤 User Upload** → `POST /api/parse-resume-file`
2. **📄 Backend Processing** → `extract_text()` → `parse_resume()` → `generate_embeddings()`
3. **🤖 AI Analysis** → `classify_job_role()` → `find_matching_jobs()`
4. **📊 Scoring Engine** → Multi-factor scoring algorithm
5. **📈 Results** → Ranked job recommendations
6. **📱 Frontend Display** → React dashboard with filters and details

## 📖 API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Parse Resume
```bash
# From file
curl -X POST "http://localhost:8000/api/parse-resume-file" \
  -F "file=@resume.pdf" -F "top_k=10"

# From text
curl -X POST "http://localhost:8000/api/parse-resume-text" \
  -d '{"resume_text": "John Doe\nSoftware Engineer...", "top_k": 10}'
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## 📖 Usage

### Backend API
- **API Documentation**: Visit `http://localhost:8000/docs`
- **Health Check**: `curl http://localhost:8000/health`

### Frontend Application
- **Dashboard**: `http://localhost:3000` - Main application interface
- **Authentication**: Login/Register system
- **Resume Upload**: Upload and parse resumes
- **Job Results**: View AI-generated job recommendations
- **Job Database**: Browse available job listings

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

### Frontend Deployment (Cloudflare Pages)

1. **Build frontend**:
```bash
cd frontend
npm run build
```

2. **Deploy to Cloudflare Pages**:
   - Connect your GitHub repository
   - Set build command: `cd frontend && npm run build`
   - Set build output directory: `frontend/dist`

### Backend Deployment (Docker)

1. **Build and run**:
```bash
docker-compose up -d
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
- **Frontend Build**: ~30 seconds
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

## 🚀 Quick Links

- **Backend API**: http://localhost:8000
- **Frontend App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Startup Script**: `./start.sh`

## 🎯 Key Benefits

- **🚀 Modern Tech Stack**: React + TypeScript + FastAPI + Docker
- **⚡ Fast Performance**: Vite build, vector database, optimized API
- **🔒 Production Ready**: Authentication, security, deployment configs
- **📱 Beautiful UI**: Modern Material-UI design with responsive layout
- **📦 Easy Setup**: Single command startup with `./start.sh`

---

**Built with ❤️ using 100% free and open-source technologies**
