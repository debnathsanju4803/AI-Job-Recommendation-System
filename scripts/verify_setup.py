"""
Verify setup and show what's working
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if all dependencies are installed"""
    print("="*60)
    print("Checking Dependencies")
    print("="*60)
    
    dependencies = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "sentence_transformers": "Sentence Transformers",
        "chromadb": "Chroma DB",
        "pymupdf": "PyMuPDF (fitz)",
        "docx": "python-docx",
        "bs4": "BeautifulSoup4",
        "sklearn": "scikit-learn",
        "numpy": "NumPy",
        "requests": "Requests"
    }
    
    installed = {}
    missing = []
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            installed[name] = True
            print(f"✓ {name}")
        except ImportError:
            installed[name] = False
            missing.append(name)
            print(f"✗ {name} - MISSING")
    
    print(f"\nInstalled: {len([v for v in installed.values() if v])}/{len(dependencies)}")
    
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        print("Run: ./scripts/setup.sh or pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All dependencies installed!")
        return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n" + "="*60)
    print("Testing Basic Functionality")
    print("="*60)
    
    all_ok = True
    
    # Test imports
    try:
        from src.classifiers.role_classifier import RoleClassifier
        print("✓ Role Classifier imports OK")
        
        classifier = RoleClassifier()
        test_result = classifier.classify("Backend developer with Python and Node.js", top_k=1)
        print(f"✓ Classification works: {test_result[0]['role']} (score: {test_result[0]['score']:.3f})")
    except Exception as e:
        print(f"✗ Role Classifier failed: {e}")
        all_ok = False
    
    # Test Vector DB
    try:
        from src.vector_db.vector_store import VectorStore
        print("✓ Vector Store imports OK")
        
        vs = VectorStore()
        count = vs.get_job_count()
        print(f"✓ Vector DB works (current jobs: {count})")
    except Exception as e:
        print(f"✗ Vector DB failed: {e}")
        all_ok = False
    
    # Test Job Matcher
    try:
        from src.job_search.job_matcher import JobMatcher
        print("✓ Job Matcher imports OK")
    except Exception as e:
        print(f"✗ Job Matcher failed: {e}")
        all_ok = False
    
    return all_ok

def main():
    """Main verification"""
    print("\n" + "="*60)
    print("SETUP VERIFICATION")
    print("AI Resume Parser & Job Recommender")
    print("="*60)
    
    deps_ok = check_dependencies()
    
    if deps_ok:
        func_ok = test_basic_functionality()
        
        print("\n" + "="*60)
        if func_ok:
            print("✓ SETUP VERIFIED - Everything is working!")
            print("="*60)
            print("\nYou can now:")
            print("1. Fetch jobs: python scripts/fetch_jobs.py")
            print("2. Run tests: python tests/test_complete.py")
            print("3. Start API: python run.py")
        else:
            print("⚠ Some functionality may not work")
            print("="*60)
    else:
        print("\n" + "="*60)
        print("✗ SETUP INCOMPLETE - Install missing dependencies")
        print("="*60)
        print("\nRun: ./scripts/setup.sh")

if __name__ == "__main__":
    main()
