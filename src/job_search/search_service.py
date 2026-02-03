"""
Unified search service for job search operations
"""
from typing import List, Dict, Any, Optional
from src.job_search.job_scraper import JobScraper
from src.vector_db.vector_store import VectorStore
from src.utils.logger import logger

class SearchService:
    """Unified search service for job search operations"""
    
    def __init__(self):
        self.scraper = JobScraper()
        self.vector_store = VectorStore()
    
    def search_jobs(self, query: str, 
                   location: Optional[str] = None, 
                   top_k: int = 20,
                   use_vector_db: bool = True) -> List[Dict[str, Any]]:
        """Search for jobs using either vector database or web scraping"""
        if use_vector_db:
            return self._search_vector_db(query, top_k)
        else:
            return self._search_web_sources(query, location)
    
    def _search_vector_db(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Search jobs using vector database"""
        logger.info(f"Searching vector database for: {query}")
        return self.vector_store.search_jobs(query, top_k=top_k)
    
    def _search_web_sources(self, query: str, location: Optional[str]) -> List[Dict[str, Any]]:
        """Search jobs using web scraping"""
        logger.info(f"Searching web sources for: {query}")
        
        # Search multiple sources
        jobs = []
        
        # Search Arbeitnow
        try:
            arbeitnow_jobs = self.scraper.search_arbeitnow(query, location)
            jobs.extend(arbeitnow_jobs)
        except Exception as e:
            logger.error(f"Error searching Arbeitnow: {e}")
        
        # Search RemoteOK
        try:
            remoteok_jobs = self.scraper.search_remoteok(query)
            jobs.extend(remoteok_jobs)
        except Exception as e:
            logger.error(f"Error searching RemoteOK: {e}")
        
        # Search Indeed RSS
        try:
            indeed_jobs = self.scraper.search_indeed_rss(query, location or "USA")
            jobs.extend(indeed_jobs)
        except Exception as e:
            logger.error(f"Error searching Indeed: {e}")
        
        return jobs
    
    def get_job_count(self) -> int:
        """Get total number of jobs in vector database"""
        return self.vector_store.get_job_count()
    
    def ingest_jobs(self, jobs: List[Dict[str, Any]]):
        """Ingest jobs into vector database"""
        logger.info(f"Ingesting {len(jobs)} jobs into vector database")
        self.vector_store.add_jobs_batch(jobs)