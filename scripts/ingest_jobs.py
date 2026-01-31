"""
Script to ingest jobs into vector database
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.job_search.job_scraper import JobScraper
from src.vector_db.vector_store import VectorStore
from src.utils.logger import logger

def main():
    """Ingest jobs from free sources"""
    scraper = JobScraper()
    vector_store = VectorStore()
    
    # Search queries
    queries = [
        "backend developer",
        "frontend developer",
        "full stack developer",
        "data scientist",
        "devops engineer",
        "software engineer",
        "machine learning engineer"
    ]
    
    all_jobs = []
    
    for query in queries:
        logger.info(f"Searching for: {query}")
        jobs = scraper.search_all_sources(query)
        all_jobs.extend(jobs)
    
    # Deduplicate
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    logger.info(f"Found {len(unique_jobs)} unique jobs")
    
    # Ingest into vector database
    if unique_jobs:
        vector_store.add_jobs_batch(unique_jobs)
        logger.info(f"Successfully ingested {len(unique_jobs)} jobs")
        logger.info(f"Total jobs in database: {vector_store.get_job_count()}")
    else:
        logger.warning("No jobs to ingest")

if __name__ == "__main__":
    main()
