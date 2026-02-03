"""
Main pipeline for resume parsing and job matching
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from src.parsers.resume_parser import ResumeParser, ResumeData
from src.classifiers.role_classifier import RoleClassifier
from src.job_search.search_service import SearchService
from src.job_search.job_matcher import JobMatcher
from src.vector_db.vector_store import VectorStore
from src.utils.logger import logger

class SearchMode(Enum):
    """Search mode for job matching"""
    VECTOR_DB = "vector_db"
    WEB_SCRAPING = "web_scraping"
    HYBRID = "hybrid"

@dataclass
class PipelineConfig:
    """Configuration for the resume job pipeline"""
    # Resume parsing
    max_resume_length: int = 8000
    clean_text: bool = True
    
    # Job matching
    default_top_k: int = 10
    role_classification_k: int = 3
    search_mode: SearchMode = SearchMode.VECTOR_DB
    
    # Search configuration
    use_vector_db: bool = True
    web_scraping_fallback: bool = True
    max_web_sources: int = 3
    
    # Ranking
    skills_weight: float = 0.4
    experience_weight: float = 0.3
    semantic_weight: float = 0.3

class ResumeJobPipeline:
    """Complete pipeline for resume parsing and job matching"""
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        self.config = config or PipelineConfig()
        
        # Initialize components
        self.parser = ResumeParser()
        self.classifier = RoleClassifier()
        self.search_service = SearchService()
        self.matcher = JobMatcher()
        self.vector_store = VectorStore()
    
    def update_config(self, **kwargs) -> None:
        """Update pipeline configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                logger.info(f"Updated config: {key} = {value}")
    
    def parse_resume(self, resume_path: Path) -> ResumeData:
        """Parse resume file and return structured data"""
        logger.info(f"Parsing resume: {resume_path}")
        return self.parser.parse_file(resume_path)
    
    def parse_resume_from_text(self, resume_text: str) -> ResumeData:
        """Parse resume text and return structured data"""
        logger.info("Parsing resume from text")
        return self.parser.parse_text(resume_text)
    
    def classify_resume_role(self, resume_data: ResumeData) -> List[Dict[str, Any]]:
        """Classify resume into job roles"""
        logger.info("Classifying resume role")
        return self.classifier.classify_from_entities(resume_data.model_dump())
    
    def search_jobs_for_resume(self, resume_data: ResumeData, 
                              top_k: int = 20,
                              use_vector_db: bool = True) -> List[Dict[str, Any]]:
        """Search jobs matching the resume"""
        logger.info("Searching jobs for resume")
        
        resume_dict = resume_data.model_dump()
        primary_role = resume_dict.get('experiences', [{}])[0].get('title', 'Software Engineer')
        
        query = self._build_search_query(resume_dict, primary_role)
        return self.search_service.search_jobs(
            query=query,
            location=resume_dict.get('location'),
            top_k=top_k,
            use_vector_db=use_vector_db
        )
    
    def rank_jobs_for_resume(self, resume_data: ResumeData, 
                           jobs: List[Dict[str, Any]], 
                           top_k: int = 10) -> List[Dict[str, Any]]:
        """Rank jobs based on resume match"""
        logger.info(f"Ranking {len(jobs)} jobs for resume")
        return self.matcher.rank_jobs(resume_data.model_dump(), jobs, top_k=top_k)
    
    def process_resume(self, resume_path: Path, 
                      top_k_jobs: int = 10,
                      use_vector_db: bool = True) -> Dict[str, Any]:
        """Process resume and find matching jobs"""
        logger.info(f"Processing resume: {resume_path}")
        
        # Modular approach - each step can be called independently
        resume_data = self.parse_resume(resume_path)
        role_results = self.classify_resume_role(resume_data)
        jobs = self.search_jobs_for_resume(resume_data, top_k_jobs * 2, use_vector_db)
        ranked_jobs = self.rank_jobs_for_resume(resume_data, jobs, top_k_jobs)
        
        primary_role = role_results[0]['role'] if role_results else "Software Engineer"
        
        return {
            "resume_data": resume_data.model_dump(),
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
        
        # Modular approach - each step can be called independently
        resume_data = self.parse_resume_from_text(resume_text)
        role_results = self.classify_resume_role(resume_data)
        jobs = self.search_jobs_for_resume(resume_data, top_k_jobs * 2, use_vector_db)
        ranked_jobs = self.rank_jobs_for_resume(resume_data, jobs, top_k_jobs)
        
        primary_role = role_results[0]['role'] if role_results else "Software Engineer"
        
        return {
            "resume_data": resume_data.model_dump(),
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
        self.search_service.ingest_jobs(jobs)
    
    def get_job_count(self) -> int:
        """Get number of jobs in vector database"""
        return self.search_service.get_job_count()
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status and configuration"""
        return {
            "config": {
                "max_resume_length": self.config.max_resume_length,
                "default_top_k": self.config.default_top_k,
                "search_mode": self.config.search_mode.value,
                "use_vector_db": self.config.use_vector_db,
                "skills_weight": self.config.skills_weight,
                "experience_weight": self.config.experience_weight,
                "semantic_weight": self.config.semantic_weight
            },
            "job_count": self.get_job_count(),
            "components": {
                "parser": "active",
                "classifier": "active", 
                "search_service": "active",
                "matcher": "active",
                "vector_store": "active"
            }
        }
    
    def batch_process_resumes(self, resume_paths: List[Path], 
                            top_k_jobs: int = 10,
                            use_vector_db: bool = True) -> List[Dict[str, Any]]:
        """Process multiple resumes in batch"""
        logger.info(f"Processing {len(resume_paths)} resumes in batch")
        
        results = []
        for resume_path in resume_paths:
            try:
                result = self.process_resume(resume_path, top_k_jobs, use_vector_db)
                result["resume_file"] = str(resume_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing resume {resume_path}: {e}")
                results.append({
                    "error": str(e),
                    "resume_file": str(resume_path)
                })
        
        return results
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search performance statistics"""
        return {
            "job_count": self.get_job_count(),
            "search_modes": [mode.value for mode in SearchMode],
            "config": {
                "use_vector_db": self.config.use_vector_db,
                "web_scraping_fallback": self.config.web_scraping_fallback,
                "max_web_sources": self.config.max_web_sources
            }
        }
    
