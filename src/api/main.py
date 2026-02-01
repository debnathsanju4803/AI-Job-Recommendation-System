"""
FastAPI application for resume parser and job recommender
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from pathlib import Path
import tempfile
import shutil

from config.settings import settings
from src.pipeline import ResumeJobPipeline
from src.utils.logger import logger

# Import rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Free, open-source AI Resume Parser and Job Recommender"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Initialize pipeline
pipeline = ResumeJobPipeline()

# Setup caching with Redis
@app.on_event("startup")
async def startup():
    if settings.REDIS_HOST:
        redis_backend = RedisBackend(f"{settings.REDIS_HOST}:{settings.REDIS_PORT}")
        FastAPICache.init(redis_backend, prefix="resume-parser-cache")

# Request/Response models
class ResumeTextRequest(BaseModel):
    resume_text: str
    top_k: Optional[int] = 10
    use_vector_db: Optional[bool] = True

class JobIngestRequest(BaseModel):
    jobs: List[Dict[str, Any]]

class HealthResponse(BaseModel):
    status: str
    job_count: int

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Resume Parser & Job Recommender API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    try:
        job_count = pipeline.get_job_count()
        return HealthResponse(status="healthy", job_count=job_count)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/parse-resume-file")
@limiter.limit("10/minute")
async def parse_resume_file(
    request: Request,
    file: UploadFile = File(...),
    top_k: int = 10,
    use_vector_db: bool = True
):
    """Parse resume from uploaded file"""
    try:
        # Save uploaded file temporarily
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = Path(tmp_file.name)
        
        try:
            # Process resume
            result = pipeline.process_resume(tmp_path, top_k, use_vector_db)
            return JSONResponse(content=result)
        finally:
            # Clean up temp file
            tmp_path.unlink()
            
    except Exception as e:
        logger.error(f"Error parsing resume file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/parse-resume-text")
@limiter.limit("20/minute")
async def parse_resume_text(request: Request, request_body: ResumeTextRequest):
    """Parse resume from text"""
    try:
        result = pipeline.process_resume_text(
            request_body.resume_text,
            request_body.top_k,
            request_body.use_vector_db
        )
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error parsing resume text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingest-jobs")
@limiter.limit("5/minute")
async def ingest_jobs(request: Request, request_body: JobIngestRequest):
    """Ingest jobs into vector database"""
    try:
        pipeline.ingest_jobs(request_body.jobs)
        return {"message": f"Successfully ingested {len(request_body.jobs)} jobs"}
    except Exception as e:
        logger.error(f"Error ingesting jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/job-count")
async def get_job_count():
    """Get number of jobs in vector database"""
    try:
        count = pipeline.get_job_count()
        return {"job_count": count}
    except Exception as e:
        logger.error(f"Error getting job count: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
