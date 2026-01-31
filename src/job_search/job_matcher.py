"""
Job matching and ranking system
"""
import sys
from pathlib import Path
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from src.utils.logger import logger

class JobMatcher:
    """Match and rank jobs for a resume"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def calculate_semantic_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate semantic similarity between resume and job"""
        resume_emb = self.embedding_model.encode([resume_text])[0]
        job_emb = self.embedding_model.encode([job_text])[0]
        
        similarity = cosine_similarity([resume_emb], [job_emb])[0][0]
        return float(similarity)
    
    def calculate_skills_match(self, resume_skills: List[str], 
                               job_skills: List[str]) -> float:
        """Calculate skills overlap"""
        if not job_skills:
            return 0.0
        
        resume_skills_lower = [s.lower().strip() for s in resume_skills]
        job_skills_lower = [s.lower().strip() for s in job_skills]
        
        # Exact matches
        exact_matches = len(set(resume_skills_lower) & set(job_skills_lower))
        
        # Partial matches (substring)
        partial_matches = 0
        for job_skill in job_skills_lower:
            for resume_skill in resume_skills_lower:
                if job_skill in resume_skill or resume_skill in job_skill:
                    partial_matches += 0.5
                    break
        
        total_match = exact_matches + partial_matches
        max_possible = len(job_skills)
        
        return min(total_match / max_possible, 1.0) if max_possible > 0 else 0.0
    
    def calculate_experience_match(self, candidate_years: float, 
                                   required_years: float) -> float:
        """Calculate experience level match"""
        if required_years == 0:
            return 1.0
        
        if candidate_years >= required_years:
            return 1.0
        elif candidate_years >= required_years * 0.8:
            return 0.8
        elif candidate_years >= required_years * 0.6:
            return 0.6
        else:
            return 0.3
    
    def score_job(self, resume_data: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive job score"""
        # Build resume text
        resume_text = self._build_resume_text(resume_data)
        
        # Build job text
        job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('requirements', '')}"
        
        # Calculate factors
        semantic_score = self.calculate_semantic_similarity(resume_text, job_text)
        
        # Skills match
        resume_skills = resume_data.get('skills', [])
        job_skills = self._extract_skills_from_job(job)
        skills_score = self.calculate_skills_match(resume_skills, job_skills)
        
        # Experience match
        candidate_years = resume_data.get('years_of_experience', 0) or 0
        required_years = self._extract_required_experience(job)
        experience_score = self.calculate_experience_match(candidate_years, required_years)
        
        # Weighted final score
        weights = {
            "semantic": 0.4,
            "skills": 0.35,
            "experience": 0.25
        }
        
        final_score = (
            semantic_score * weights["semantic"] +
            skills_score * weights["skills"] +
            experience_score * weights["experience"]
        )
        
        return {
            "final_score": round(final_score, 3),
            "breakdown": {
                "semantic": round(semantic_score, 3),
                "skills": round(skills_score, 3),
                "experience": round(experience_score, 3)
            },
            "job": job
        }
    
    def rank_jobs(self, resume_data: Dict[str, Any], 
                  jobs: List[Dict[str, Any]], top_k: int = 10) -> List[Dict[str, Any]]:
        """Rank jobs by match score"""
        scored_jobs = []
        
        for job in jobs:
            score_result = self.score_job(resume_data, job)
            scored_jobs.append(score_result)
        
        # Sort by final score
        scored_jobs.sort(key=lambda x: x['final_score'], reverse=True)
        
        return scored_jobs[:top_k]
    
    def _build_resume_text(self, resume_data: Dict[str, Any]) -> str:
        """Build text representation of resume"""
        parts = []
        
        if resume_data.get('summary'):
            parts.append(resume_data['summary'])
        
        if resume_data.get('experiences'):
            for exp in resume_data['experiences']:
                if exp.get('title'):
                    parts.append(f"Role: {exp['title']}")
                if exp.get('description'):
                    parts.append(exp['description'])
        
        if resume_data.get('skills'):
            parts.append(f"Skills: {', '.join(resume_data['skills'])}")
        
        return " ".join(parts)
    
    def _extract_skills_from_job(self, job: Dict[str, Any]) -> List[str]:
        """Extract skills from job description"""
        # Simple extraction - can be improved with NER
        text = f"{job.get('description', '')} {job.get('requirements', '')}"
        
        # Common skills to look for
        common_skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'django', 'flask', 'spring', 'sql', 'mongodb', 'postgresql',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'linux',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_required_experience(self, job: Dict[str, Any]) -> float:
        """Extract required years of experience from job description"""
        import re
        text = f"{job.get('description', '')} {job.get('requirements', '')}"
        
        # Look for patterns like "5+ years", "3-5 years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s+experience',
            r'(\d+)-(\d+)\s*years?\s+experience',
            r'minimum\s+(\d+)\s+years?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return float(match.group(1))  # Take minimum
                return float(match.group(1))
        
        return 0.0  # No requirement found
