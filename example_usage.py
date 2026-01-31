"""
Example usage of the resume parser and job recommender
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.pipeline import ResumeJobPipeline
from config.settings import settings

def main():
    """Example usage"""
    print("=" * 60)
    print("AI Resume Parser & Job Recommender - Example Usage")
    print("=" * 60)
    
    # Initialize pipeline
    print("\n1. Initializing pipeline...")
    pipeline = ResumeJobPipeline()
    
    # Example resume text
    resume_text = """
    John Doe
    Software Engineer
    Email: john.doe@email.com
    Phone: +1-555-1234
    
    SUMMARY
    Experienced software engineer with 5 years of experience in backend development.
    Proficient in Python, Node.js, and cloud technologies.
    
    EXPERIENCE
    Senior Backend Developer | Tech Corp | 2020 - Present
    - Developed RESTful APIs using Python and FastAPI
    - Designed microservices architecture
    - Worked with AWS, Docker, and Kubernetes
    
    Software Engineer | Startup Inc | 2018 - 2020
    - Built web applications using Node.js
    - Implemented CI/CD pipelines
    
    EDUCATION
    Bachelor of Science in Computer Science
    State University | 2018
    
    SKILLS
    Python, Node.js, JavaScript, AWS, Docker, Kubernetes, PostgreSQL, MongoDB
    """
    
    print("\n2. Processing resume...")
    try:
        result = pipeline.process_resume_text(
            resume_text,
            top_k_jobs=5,
            use_vector_db=True
        )
        
        print(f"\n✓ Resume parsed successfully!")
        print(f"\nExtracted Information:")
        print(f"  Name: {result['resume_data'].get('name', 'N/A')}")
        print(f"  Email: {result['resume_data'].get('email', 'N/A')}")
        print(f"  Skills: {', '.join(result['resume_data'].get('skills', [])[:5])}")
        print(f"  Experience: {result['resume_data'].get('years_of_experience', 0)} years")
        
        print(f"\n✓ Classified Role: {result['classified_role']}")
        
        print(f"\n✓ Found {result['total_jobs_found']} jobs")
        print(f"\nTop {len(result['recommended_jobs'])} Recommended Jobs:")
        for i, job in enumerate(result['recommended_jobs'], 1):
            print(f"\n  {i}. {job['job'].get('title', 'N/A')} at {job['job'].get('company', 'N/A')}")
            print(f"     Score: {job['final_score']:.3f}")
            print(f"     Breakdown: Semantic={job['breakdown']['semantic']:.2f}, "
                  f"Skills={job['breakdown']['skills']:.2f}, "
                  f"Experience={job['breakdown']['experience']:.2f}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nNote: Make sure:")
        print("  1. Ollama is running (if using Ollama)")
        print("  2. Vector database has jobs (run: python scripts/ingest_jobs.py)")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
