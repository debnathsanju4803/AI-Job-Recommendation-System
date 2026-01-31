"""
Basic tests for resume parser
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from src.parsers.resume_parser import ResumeParser
        from src.classifiers.role_classifier import RoleClassifier
        from src.job_search.job_scraper import JobScraper
        from src.vector_db.vector_store import VectorStore
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
