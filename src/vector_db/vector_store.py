"""
Vector database for job descriptions using Chroma (free, local)
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from src.utils.logger import logger

class VectorStore:
    """Vector database for storing and searching job descriptions"""
    
    def __init__(self):
        # Force CPU usage if configured
        device = None if settings.FORCE_CPU else None
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL, device=device)
        
        # Initialize Chroma
        persist_dir = Path(settings.CHROMA_PERSIST_DIR)
        persist_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"Vector store initialized: {len(self.collection.get()['ids'])} jobs stored")
    
    def add_job(self, job: Dict[str, Any]) -> str:
        """Add a single job to the vector database"""
        job_id = job.get('id', f"job_{hash(str(job))}")
        
        # Create text for embedding
        job_text = self._create_job_text(job)
        
        # Generate embedding
        embedding = self.embedding_model.encode(job_text).tolist()
        
        # Prepare metadata
        metadata = {
            "title": job.get('title', ''),
            "company": job.get('company', ''),
            "location": job.get('location', ''),
            "source": job.get('source', 'unknown'),
            "description": job.get('description', '')[:500],  # Truncate for metadata
        }
        
        # Add to collection
        self.collection.add(
            ids=[job_id],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[job_text]
        )
        
        logger.debug(f"Added job to vector store: {job_id}")
        return job_id
    
    def add_jobs_batch(self, jobs: List[Dict[str, Any]]):
        """Add multiple jobs in batch"""
        if not jobs:
            return
        
        ids = []
        embeddings = []
        metadatas = []
        documents = []
        
        for job in jobs:
            job_id = job.get('id', f"job_{hash(str(job))}")
            job_text = self._create_job_text(job)
            embedding = self.embedding_model.encode(job_text).tolist()
            
            metadata = {
                "title": job.get('title', ''),
                "company": job.get('company', ''),
                "location": job.get('location', ''),
                "source": job.get('source', 'unknown'),
            }
            
            ids.append(job_id)
            embeddings.append(embedding)
            metadatas.append(metadata)
            documents.append(job_text)
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        
        logger.info(f"Added {len(jobs)} jobs to vector store")
    
    def search_jobs(self, query: str, top_k: int = 20, 
                   filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for jobs using semantic similarity"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Build where clause for filtering
        where_clause = None
        if filters:
            where_clause = {}
            if 'location' in filters:
                where_clause['location'] = {"$regex": filters['location']}
            if 'source' in filters:
                where_clause['source'] = filters['source']
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause if where_clause else None
        )
        
        # Format results
        jobs = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i, job_id in enumerate(results['ids'][0]):
                jobs.append({
                    "id": job_id,
                    "score": 1 - results['distances'][0][i],  # Convert distance to similarity
                    "title": results['metadatas'][0][i].get('title', ''),
                    "company": results['metadatas'][0][i].get('company', ''),
                    "location": results['metadatas'][0][i].get('location', ''),
                    "source": results['metadatas'][0][i].get('source', ''),
                    "description": results['documents'][0][i] if results['documents'] else '',
                })
        
        logger.info(f"Found {len(jobs)} jobs for query: {query[:50]}...")
        return jobs
    
    def _create_job_text(self, job: Dict[str, Any]) -> str:
        """Create text representation of job for embedding"""
        parts = [
            f"Title: {job.get('title', '')}",
            f"Company: {job.get('company', '')}",
            f"Description: {job.get('description', '')}",
            f"Requirements: {job.get('requirements', '')}",
        ]
        
        if job.get('required_skills'):
            parts.append(f"Skills: {', '.join(job.get('required_skills', []))}")
        
        return " ".join(parts)
    
    def get_job_count(self) -> int:
        """Get total number of jobs in database"""
        return self.collection.count()
    
    def delete_job(self, job_id: str):
        """Delete a job from the database"""
        self.collection.delete(ids=[job_id])
        logger.debug(f"Deleted job: {job_id}")
    
    def clear_all(self):
        """Clear all jobs from database"""
        # Delete collection and recreate
        self.client.delete_collection(settings.CHROMA_COLLECTION_NAME)
        self.collection = self.client.create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Cleared all jobs from vector store")
