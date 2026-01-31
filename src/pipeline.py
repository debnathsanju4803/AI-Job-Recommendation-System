"""
Main pipeline for resume parsing and job matching
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
from src.parsers.resume_parser import ResumeParser, ResumeData
from src.classifiers.role_classifier import RoleClassifier
from src.job_search.job_scraper import JobScraper
from src.job_search.job_matcher import JobMatcher
from src.vector_db.vector_store import VectorStore
from src.utils.logger import logger

class ResumeJobPipeline:
    """Complete pipeline for resume parsing and job matching"""
    
    def __init__(self):
        self.parser = ResumeParser()
        self.classifier = RoleClassifier()
        self.scraper = JobScraper()
        self.matcher = JobMatcher()
        self.vector_store = VectorStore()
    
    def process_resume(self, resume_path: Path, 
                      top_k_jobs: int = 10,
                      use_vector_db: bool = True) -> Dict[str, Any]:
        """Process resume and find matching jobs"""
        logger.info(f"Processing resume: {resume_path}")
        
        # Step 1: Parse resume
        resume_data = self.parser.parse_file(resume_path)
        resume_dict = resume_data.model_dump()
        
        # Step 2: Classify role
        role_results = self.classifier.classify_from_entities(resume_dict)
        primary_role = role_results[0]['role'] if role_results else "Software Engineer"
        
        # Step 3: Search for jobs
        if use_vector_db:
            # Use vector database
            query = self._build_search_query(resume_dict, primary_role)
            jobs = self.vector_store.search_jobs(query, top_k=top_k_jobs * 2)
        else:
            # Use web scraping
            query = f"{primary_role} {resume_dict.get('location', '')}"
            jobs = self.scraper.search_all_sources(query, resume_dict.get('location'))
        
        # Step 4: Rank jobs
        ranked_jobs = self.matcher.rank_jobs(resume_dict, jobs, top_k=top_k_jobs)
        
        return {
            "resume_data": resume_dict,
            "classified_role": primary_role,
            "role_alternatives": role_results[1:3] if len(role_results) > 1 else [],
            "recommended_jobs": ranked_jobs,
            "total_jobs_found": len(jobs)
        }
    
    def process_resume_text(self, resume_text: str,
                           top_k_jobs: int = 10,
                           use_vector_db: bool = True) -> Dict[str, Any]:
        """Process resume from text"""
        logger.info("Processing resume from text")
        
        # Step 1: Parse resume
        resume_data = self.parser.parse_text(resume_text)
        resume_dict = resume_data.model_dump()
        
        # Step 2: Classify role
        role_results = self.classifier.classify_from_entities(resume_dict)
        primary_role = role_results[0]['role'] if role_results else "Software Engineer"
        
        # Step 3: Search for jobs
        if use_vector_db:
            query = self._build_search_query(resume_dict, primary_role)
            jobs = self.vector_store.search_jobs(query, top_k=top_k_jobs * 2)
        else:
            query = f"{primary_role} {resume_dict.get('location', '')}"
            jobs = self.scraper.search_all_sources(query, resume_dict.get('location'))
        
        # Step 4: Rank jobs
        ranked_jobs = self.matcher.rank_jobs(resume_dict, jobs, top_k=top_k_jobs)
        
        return {
            "resume_data": resume_dict,
            "classified_role": primary_role,
            "role_alternatives": role_results[1:3] if len(role_results) > 1 else [],
            "recommended_jobs": ranked_jobs,
            "total_jobs_found": len(jobs)
        }
    
    def _build_search_query(self, resume_dict: Dict[str, Any], role: str) -> str:
        """Build search query from resume data"""
        parts = [role]
        
        if resume_dict.get('skills'):
            # Add top skills
            top_skills = resume_dict['skills'][:3]
            parts.extend(top_skills)
        
        if resume_dict.get('years_of_experience'):
            parts.append(f"{resume_dict['years_of_experience']} years experience")
        
        return " ".join(parts)
    
    def ingest_jobs(self, jobs: List[Dict[str, Any]]):
        """Ingest jobs into vector database"""
        logger.info(f"Ingesting {len(jobs)} jobs into vector database")
        self.vector_store.add_jobs_batch(jobs)
    
    def get_job_count(self) -> int:
        """Get number of jobs in vector database"""
        return self.vector_store.get_job_count()
