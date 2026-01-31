"""
Fetch real job data from internet sources
"""
import sys
from pathlib import Path
import requests
import json
import time
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.job_search.job_scraper import JobScraper
from src.vector_db.vector_store import VectorStore
from src.utils.logger import logger

def fetch_arbeitnow_jobs():
    """Fetch jobs from Arbeitnow (free API)"""
    jobs = []
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            raw = response.json()
            items = raw.get("data", raw) if isinstance(raw, dict) else (raw if isinstance(raw, list) else [])
            for job in items[:50]:
                if not isinstance(job, dict):
                    continue
                title = job.get("title") or job.get("position", "")
                if not title:
                    continue
                jobs.append({
                    "id": f"arbeitnow_{job.get('slug', job.get('id', hash(title)))}",
                    "title": title,
                    "company": job.get("company_name") or job.get("company", ""),
                    "location": job.get("location") or "Remote",
                    "description": (job.get("description") or "")[:2000],
                    "requirements": str(job.get("requirements", "") or ""),
                    "url": job.get("url", ""),
                    "source": "arbeitnow",
                    "posted_date": str(job.get("created_at", "")),
                })
            logger.info(f"Fetched {len(jobs)} jobs from Arbeitnow")
        time.sleep(1)
    except Exception as e:
        logger.error(f"Error fetching Arbeitnow jobs: {e}")
    return jobs

def fetch_remoteok_jobs():
    """Fetch jobs from RemoteOK"""
    jobs = []
    try:
        url = "https://remoteok.com/api"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if not isinstance(data, list):
                data = data.get("data", []) if isinstance(data, dict) else []
            for job in data:
                if len(jobs) >= 50:
                    break
                if not isinstance(job, dict) or not job.get("position"):
                    continue
                from bs4 import BeautifulSoup
                description = BeautifulSoup(str(job.get("description", "")), "html.parser").get_text()
                jobs.append({
                    "id": f"remoteok_{job.get('id', '')}",
                    "title": job.get("position", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", "") or "Remote",
                    "description": description[:1000],
                    "requirements": "",
                    "url": f"https://remoteok.com/remote-jobs/{job.get('id', '')}",
                    "source": "remoteok",
                    "posted_date": str(job.get("epoch", "")),
                })
            logger.info(f"Fetched {len(jobs)} jobs from RemoteOK")
    except Exception as e:
        logger.error(f"Error fetching RemoteOK jobs: {e}")
    
    return jobs

def create_sample_jobs():
    """Create sample jobs for testing"""
    sample_jobs = [
        {
            "id": "sample_1",
            "title": "Senior Backend Developer",
            "company": "TechCorp Inc",
            "location": "San Francisco, CA",
            "description": "We are looking for a Senior Backend Developer with 5+ years of experience in Python and Node.js. You will be responsible for designing and implementing microservices architecture, building RESTful APIs, and working with cloud technologies like AWS.",
            "requirements": "5+ years experience, Python, Node.js, FastAPI, AWS, Docker, Kubernetes, PostgreSQL, Microservices",
            "source": "sample",
            "posted_date": datetime.now().isoformat()
        },
        {
            "id": "sample_2",
            "title": "Data Scientist",
            "company": "DataTech Solutions",
            "location": "New York, NY",
            "description": "Data Scientist position requiring expertise in machine learning, statistical analysis, and data visualization. You will work with large datasets, build predictive models, and collaborate with engineering teams.",
            "requirements": "Master's degree, Python, Machine Learning, TensorFlow, SQL, Statistics, 3+ years experience",
            "source": "sample",
            "posted_date": datetime.now().isoformat()
        },
        {
            "id": "sample_3",
            "title": "Full Stack Developer",
            "company": "WebDev Inc",
            "location": "Seattle, WA",
            "description": "Full stack developer position. You will develop web applications using React and Node.js, build RESTful APIs, and deploy on cloud platforms.",
            "requirements": "React, Node.js, JavaScript, PostgreSQL, AWS, 4+ years experience",
            "source": "sample",
            "posted_date": datetime.now().isoformat()
        },
        {
            "id": "sample_4",
            "title": "Backend Engineer",
            "company": "API Solutions",
            "location": "Austin, TX",
            "description": "Backend engineer role focusing on API development and microservices. Experience with Python, FastAPI, and cloud deployment required.",
            "requirements": "Python, FastAPI, PostgreSQL, Docker, 3+ years experience",
            "source": "sample",
            "posted_date": datetime.now().isoformat()
        },
        {
            "id": "sample_5",
            "title": "ML Engineer",
            "company": "AI Innovations",
            "location": "Boston, MA",
            "description": "Machine Learning Engineer to build and deploy ML models. Experience with deep learning frameworks and model deployment required.",
            "requirements": "Python, TensorFlow, PyTorch, ML, Deep Learning, 4+ years experience",
            "source": "sample",
            "posted_date": datetime.now().isoformat()
        }
    ]
    return sample_jobs

def main():
    """Main function to fetch and ingest jobs"""
    print("="*60)
    print("Fetching Jobs from Internet")
    print("="*60)
    
    all_jobs = []
    
    # Fetch from free sources
    print("\n1. Fetching from Arbeitnow...")
    arbeitnow_jobs = fetch_arbeitnow_jobs()
    all_jobs.extend(arbeitnow_jobs)
    print(f"   Found: {len(arbeitnow_jobs)} jobs")
    
    print("\n2. Fetching from RemoteOK...")
    remoteok_jobs = fetch_remoteok_jobs()
    all_jobs.extend(remoteok_jobs)
    print(f"   Found: {len(remoteok_jobs)} jobs")
    
    # Add sample jobs for testing
    print("\n3. Adding sample jobs...")
    sample_jobs = create_sample_jobs()
    all_jobs.extend(sample_jobs)
    print(f"   Added: {len(sample_jobs)} sample jobs")
    
    # Deduplicate
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    print(f"\nTotal unique jobs: {len(unique_jobs)}")
    
    # Ingest into vector database
    if unique_jobs:
        print("\n4. Ingesting into vector database...")
        vector_store = VectorStore()
        vector_store.add_jobs_batch(unique_jobs)
        print(f"   ✓ Ingested {len(unique_jobs)} jobs")
        print(f"   Total jobs in DB: {vector_store.get_job_count()}")
        
        # Save to file for reference
        jobs_file = project_root / "data" / "jobs" / "jobs.json"
        jobs_file.parent.mkdir(parents=True, exist_ok=True)
        with open(jobs_file, 'w') as f:
            json.dump(unique_jobs, f, indent=2)
        print(f"   ✓ Saved to {jobs_file}")
    else:
        print("\n✗ No jobs to ingest")

if __name__ == "__main__":
    main()
