"""
Resume parser using free LLM models
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
from pydantic import BaseModel, Field
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.llm_client import LLMClient
from src.utils.pdf_parser import DocumentParser
from src.utils.logger import logger

class Education(BaseModel):
    """Education information"""
    degree: Optional[str] = Field(None, description="Degree name")
    field: Optional[str] = Field(None, description="Field of study")
    institution: Optional[str] = Field(None, description="University or college")
    graduation_year: Optional[int] = Field(None, description="Year of graduation")
    gpa: Optional[float] = Field(None, description="GPA if mentioned")

class Experience(BaseModel):
    """Work experience"""
    title: Optional[str] = Field(None, description="Job title")
    company: Optional[str] = Field(None, description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date or 'Present'")
    description: Optional[str] = Field(None, description="Job description")
    skills_used: List[str] = Field(default_factory=list, description="Skills used")

class ResumeData(BaseModel):
    """Structured resume data"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    experiences: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    years_of_experience: Optional[float] = None

class ResumeParser:
    """Parse resumes using LLM"""
    
    def __init__(self):
        self.llm = LLMClient()
        self.doc_parser = DocumentParser()
        self._schema = self._get_extraction_schema()
    
    def _get_extraction_schema(self) -> Dict[str, Any]:
        """Get JSON schema for extraction"""
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "location": {"type": "string"},
                "summary": {"type": "string"},
                "experiences": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "company": {"type": "string"},
                            "location": {"type": "string"},
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                            "description": {"type": "string"},
                            "skills_used": {"type": "array", "items": {"type": "string"}}
                        }
                    }
                },
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "degree": {"type": "string"},
                            "field": {"type": "string"},
                            "institution": {"type": "string"},
                            "graduation_year": {"type": "integer"},
                            "gpa": {"type": "number"}
                        }
                    }
                },
                "skills": {"type": "array", "items": {"type": "string"}},
                "certifications": {"type": "array", "items": {"type": "string"}},
                "languages": {"type": "array", "items": {"type": "string"}},
                "years_of_experience": {"type": "number"}
            }
        }
    
    def parse_file(self, file_path: Path) -> ResumeData:
        """Parse resume from file"""
        logger.info(f"Parsing resume file: {file_path}")
        
        # Extract text
        text = self.doc_parser.parse(file_path)
        
        # Parse with LLM
        return self.parse_text(text)
    
    def parse_text(self, resume_text: str) -> ResumeData:
        """Parse resume from text"""
        logger.info("Extracting structured data from resume text")
        
        # Clean and prepare text
        cleaned_text = self._clean_text(resume_text)
        
        # Extract with LLM
        try:
            extracted = self.llm.extract_structured(cleaned_text, self._schema)
            
            # Convert to Pydantic model
            resume_data = ResumeData(**extracted)
            
            # Post-process: calculate years of experience if not provided
            if not resume_data.years_of_experience and resume_data.experiences:
                resume_data.years_of_experience = self._calculate_experience_years(
                    resume_data.experiences
                )
            
            logger.info("Successfully parsed resume")
            return resume_data
            
        except Exception as e:
            logger.error(f"Error parsing resume: {e}")
            # Return minimal structure on error
            return ResumeData()
    
    def _clean_text(self, text: str) -> str:
        """Clean resume text"""
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join([line for line in lines if line])
        
        # Limit length (LLMs have token limits)
        max_length = 8000
        if len(text) > max_length:
            text = text[:max_length] + "..."
            logger.warning(f"Resume text truncated to {max_length} characters")
        
        return text
    
    def _calculate_experience_years(self, experiences: List[Experience]) -> float:
        """Calculate total years of experience from experiences"""
        # Simple calculation - can be improved
        total_months = 0
        for exp in experiences:
            if exp.start_date and exp.end_date:
                # Parse dates (simplified)
                try:
                    # This is simplified - implement proper date parsing
                    if exp.end_date.lower() != "present":
                        # Calculate months between dates
                        # For now, return approximate
                        total_months += 12  # Assume 1 year per experience
                except:
                    pass
        
        return round(total_months / 12, 1) if total_months > 0 else 0.0
