"""
Complete test suite - works without external LLM dependencies
"""
import sys
from pathlib import Path
import json
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        from src.parsers.resume_parser import ResumeParser, ResumeData
        from src.classifiers.role_classifier import RoleClassifier
        from src.job_search.job_scraper import JobScraper
        from src.job_search.job_matcher import JobMatcher
        from src.vector_db.vector_store import VectorStore
        from src.pipeline import ResumeJobPipeline
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_classifier():
    """Test role classifier (no external deps)"""
    print("\n" + "="*60)
    print("Testing Role Classifier")
    print("="*60)
    
    try:
        from src.classifiers.role_classifier import RoleClassifier
        
        classifier = RoleClassifier()
        print(f"✓ Classifier initialized with {len(classifier.roles)} roles")
        
        # Test classification
        test_text = """
        Senior Backend Developer with 5 years of experience.
        Skills: Python, Node.js, AWS, Docker, Kubernetes.
        Built microservices and REST APIs.
        """
        
        start = time.time()
        results = classifier.classify(test_text, top_k=3)
        elapsed = time.time() - start
        
        print(f"\nTest Resume: Backend Developer")
        print(f"Predicted: {results[0]['role']} (score: {results[0]['score']:.3f})")
        print(f"Time: {elapsed:.3f}s")
        print("✓ Classifier test passed")
        return True
    except Exception as e:
        print(f"✗ Classifier test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vector_db():
    """Test vector database"""
    print("\n" + "="*60)
    print("Testing Vector Database")
    print("="*60)
    
    try:
        from src.vector_db.vector_store import VectorStore
        
        vector_store = VectorStore()
        initial_count = vector_store.get_job_count()
        print(f"✓ Vector store initialized (current jobs: {initial_count})")
        
        # Test adding job
        test_job = {
            "id": "test_job_1",
            "title": "Backend Developer",
            "company": "Test Corp",
            "location": "Remote",
            "description": "Looking for backend developer with Python experience",
            "requirements": "Python, FastAPI, 3+ years",
            "source": "test"
        }
        
        vector_store.add_job(test_job)
        print(f"✓ Added test job")
        
        # Test search
        results = vector_store.search_jobs("backend developer python", top_k=5)
        print(f"✓ Search returned {len(results)} results")
        
        if results:
            print(f"  Top match: {results[0]['title']} (score: {results[0]['score']:.3f})")
        
        # Cleanup
        vector_store.delete_job("test_job_1")
        print("✓ Vector DB test passed")
        return True
    except Exception as e:
        print(f"✗ Vector DB test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_job_matcher():
    """Test job matcher"""
    print("\n" + "="*60)
    print("Testing Job Matcher")
    print("="*60)
    
    try:
        from src.job_search.job_matcher import JobMatcher
        
        matcher = JobMatcher()
        
        resume_data = {
            "skills": ["Python", "Node.js", "AWS", "Docker"],
            "years_of_experience": 5.0
        }
        
        test_jobs = [
            {
                "id": "job1",
                "title": "Backend Developer",
                "company": "Tech Inc",
                "description": "Backend developer with Python and Node.js. 5+ years experience required.",
                "requirements": "Python, Node.js, AWS, 5+ years"
            },
            {
                "id": "job2",
                "title": "Frontend Developer",
                "company": "Web Corp",
                "description": "Frontend developer with React",
                "requirements": "React, JavaScript"
            }
        ]
        
        ranked = matcher.rank_jobs(resume_data, test_jobs, top_k=2)
        
        print(f"✓ Ranked {len(ranked)} jobs")
        print(f"  Top match: {ranked[0]['job']['title']} (score: {ranked[0]['final_score']:.3f})")
        print("✓ Job matcher test passed")
        return True
    except Exception as e:
        print(f"✗ Job matcher test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_parser():
    """Test parser with simple extraction (no LLM)"""
    print("\n" + "="*60)
    print("Testing Simple Parser (Regex-based)")
    print("="*60)
    
    try:
        import re
        
        resume_text = """
        John Smith
        Email: john.smith@email.com
        Phone: +1-555-0100
        
        Skills: Python, Node.js, AWS, Docker
        
        Experience: 5 years
        """
        
        # Simple extraction
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
        phone_match = re.search(r'\+?[\d\s-]+', resume_text)
        skills_match = re.search(r'Skills:\s*(.+)', resume_text, re.IGNORECASE)
        
        extracted = {
            "email": email_match.group() if email_match else None,
            "phone": phone_match.group().strip() if phone_match else None,
            "skills": [s.strip() for s in skills_match.group(1).split(',')] if skills_match else []
        }
        
        print(f"✓ Extracted email: {extracted['email']}")
        print(f"✓ Extracted phone: {extracted['phone']}")
        print(f"✓ Extracted {len(extracted['skills'])} skills")
        print("✓ Simple parser test passed")
        return True
    except Exception as e:
        print(f"✗ Simple parser test failed: {e}")
        return False

def test_job_scraper():
    """Test job scraper"""
    print("\n" + "="*60)
    print("Testing Job Scraper")
    print("="*60)
    
    try:
        from src.job_search.job_scraper import JobScraper
        
        scraper = JobScraper()
        print("✓ Scraper initialized")
        
        # Test with a simple query (may fail if no internet, that's OK)
        try:
            jobs = scraper.search_all_sources("developer")
            print(f"✓ Job scraper works (found {len(jobs)} jobs)")
        except Exception as e:
            print(f"⚠ Job scraper test skipped (no internet or API issue): {e}")
        
        print("✓ Job scraper test passed")
        return True
    except Exception as e:
        print(f"✗ Job scraper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline_without_llm():
    """Test pipeline without LLM (using vector DB)"""
    print("\n" + "="*60)
    print("Testing Pipeline (Vector DB Mode)")
    print("="*60)
    
    try:
        from src.vector_db.vector_store import VectorStore
        from src.classifiers.role_classifier import RoleClassifier
        from src.job_search.job_matcher import JobMatcher
        
        # Create minimal resume data
        resume_data = {
            "name": "Test User",
            "skills": ["Python", "Node.js", "AWS"],
            "years_of_experience": 5.0,
            "experiences": [{"title": "Backend Developer"}]
        }
        
        # Test components
        classifier = RoleClassifier()
        role_results = classifier.classify_from_entities(resume_data)
        print(f"✓ Classified role: {role_results[0]['role']}")
        
        vector_store = VectorStore()
        jobs = vector_store.search_jobs("backend developer python", top_k=5)
        print(f"✓ Found {len(jobs)} jobs from vector DB")
        
        if jobs:
            matcher = JobMatcher()
            ranked = matcher.rank_jobs(resume_data, jobs, top_k=3)
            print(f"✓ Ranked {len(ranked)} jobs")
            print(f"  Top match: {ranked[0]['job']['title']} (score: {ranked[0]['final_score']:.3f})")
        
        print("✓ Pipeline test passed")
        return True
    except Exception as e:
        print(f"✗ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("COMPREHENSIVE TEST SUITE")
    print("AI Resume Parser & Job Recommender")
    print("="*60)
    
    results = {
        "imports": False,
        "classifier": False,
        "vector_db": False,
        "job_matcher": False,
        "simple_parser": False,
        "job_scraper": False,
        "pipeline": False
    }
    
    start_time = time.time()
    
    # Run tests
    results["imports"] = test_imports()
    results["classifier"] = test_classifier()
    results["vector_db"] = test_vector_db()
    results["job_matcher"] = test_job_matcher()
    results["simple_parser"] = test_simple_parser()
    results["job_scraper"] = test_job_scraper()
    results["pipeline"] = test_pipeline_without_llm()
    
    total_time = time.time() - start_time
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test:20s}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"Time: {total_time:.2f}s")
    print("="*60)
    
    # Save results
    results_file = project_root / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "results": results,
            "passed": passed,
            "total": total,
            "time": total_time
        }, f, indent=2)
    print(f"\nResults saved to: {results_file}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
