"""
Job role classifier using vector embeddings (free, local)
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sentence_transformers import SentenceTransformer
from config.settings import settings
from src.utils.logger import logger

class RoleClassifier:
    """Classify resumes into job roles using semantic similarity"""
    
    def __init__(self):
        # Force CPU usage if configured
        device = None if settings.FORCE_CPU else None
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL, device=device)
        self.roles = self._load_roles()
        self.role_embeddings = self._create_role_embeddings()
    
    def _load_roles(self) -> List[Dict[str, Any]]:
        """Load job role definitions"""
        roles_file = Path(settings.DATA_DIR) / "roles.json"
        
        if roles_file.exists():
            with open(roles_file, 'r') as f:
                roles = json.load(f)
        else:
            # Default roles
            roles = [
                {
                    "name": "Backend Developer",
                    "description": "Server-side development, APIs, databases, microservices"
                },
                {
                    "name": "Frontend Developer",
                    "description": "UI/UX development, React, Angular, Vue, user interfaces"
                },
                {
                    "name": "Full Stack Developer",
                    "description": "Both frontend and backend development, end-to-end applications"
                },
                {
                    "name": "Data Scientist",
                    "description": "Machine learning, data analysis, statistics, predictive modeling"
                },
                {
                    "name": "Data Engineer",
                    "description": "Data pipelines, ETL, data warehousing, big data processing"
                },
                {
                    "name": "DevOps Engineer",
                    "description": "CI/CD, cloud infrastructure, automation, containerization"
                },
                {
                    "name": "Software Engineer",
                    "description": "General software development, programming, system design"
                },
                {
                    "name": "ML Engineer",
                    "description": "Machine learning models, deep learning, model deployment"
                },
                {
                    "name": "Product Manager",
                    "description": "Product strategy, roadmap, stakeholder management, requirements"
                },
                {
                    "name": "QA Engineer",
                    "description": "Testing, test automation, quality assurance, bug tracking"
                }
            ]
            
            # Save default roles
            roles_file.parent.mkdir(parents=True, exist_ok=True)
            with open(roles_file, 'w') as f:
                json.dump(roles, f, indent=2)
        
        logger.info(f"Loaded {len(roles)} job roles")
        return roles
    
    def _create_role_embeddings(self):
        """Create embeddings for all roles"""
        role_texts = [
            f"{role['name']}: {role['description']}" 
            for role in self.roles
        ]
        embeddings = self.embedding_model.encode(role_texts)
        return embeddings
    
    def classify(self, resume_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Classify resume into job roles"""
        # Generate resume embedding
        resume_embedding = self.embedding_model.encode([resume_text])[0]
        
        # Calculate similarities
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        similarities = cosine_similarity(
            [resume_embedding],
            self.role_embeddings
        )[0]
        
        # Get top-k matches
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "role": self.roles[idx]['name'],
                "score": float(similarities[idx]),
                "description": self.roles[idx]['description']
            })
        
        logger.info(f"Classified resume as: {results[0]['role']} (score: {results[0]['score']:.2f})")
        return results
    
    def classify_from_entities(self, resume_data: Dict[str, Any], top_k: int = 3) -> List[Dict[str, Any]]:
        """Classify from structured resume data"""
        # Build text from resume data
        text_parts = []
        
        if resume_data.get('summary'):
            text_parts.append(resume_data['summary'])
        
        if resume_data.get('experiences'):
            for exp in resume_data['experiences']:
                if exp.get('title'):
                    text_parts.append(f"Role: {exp['title']}")
                if exp.get('description'):
                    text_parts.append(exp['description'])
        
        if resume_data.get('skills'):
            text_parts.append(f"Skills: {', '.join(resume_data['skills'])}")
        
        resume_text = " ".join(text_parts)
        return self.classify(resume_text, top_k)
