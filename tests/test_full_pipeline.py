"""
Comprehensive test suite for the entire pipeline
"""
import sys
from pathlib import Path
import json
import time
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.parsers.resume_parser import ResumeParser
from src.classifiers.role_classifier import RoleClassifier
from src.job_search.job_scraper import JobScraper
from src.job_search.job_matcher import JobMatcher
from src.vector_db.vector_store import VectorStore
from src.pipeline import ResumeJobPipeline
from src.utils.logger import logger

class TestSuite:
    """Comprehensive test suite"""
    
    def __init__(self):
        self.results = {
            "parser": {},
            "classifier": {},
            "job_scraper": {},
            "vector_db": {},
            "matcher": {},
            "pipeline": {}
        }
        self.test_resumes = self._create_test_resumes()
    
    def _create_test_resumes(self) -> List[Dict[str, str]]:
        """Create test resume samples"""
        return [
            {
                "name": "Backend Developer Resume",
                "text": """
                John Smith
                Senior Backend Developer
                Email: john.smith@email.com
                Phone: +1-555-0100
                Location: San Francisco, CA
                
                SUMMARY
                Experienced backend developer with 6 years of expertise in building scalable 
                microservices and RESTful APIs. Proficient in Python, Node.js, and cloud technologies.
                
                EXPERIENCE
                Senior Backend Developer | TechCorp Inc. | 2020 - Present
                - Designed and implemented microservices architecture using Python and FastAPI
                - Built RESTful APIs handling 1M+ requests per day
                - Deployed services on AWS using Docker and Kubernetes
                - Optimized database queries reducing response time by 40%
                - Led team of 3 junior developers
                
                Backend Developer | StartupXYZ | 2018 - 2020
                - Developed Node.js applications using Express.js
                - Implemented CI/CD pipelines with Jenkins
                - Worked with MongoDB and PostgreSQL databases
                
                EDUCATION
                Bachelor of Science in Computer Science
                State University | 2018
                GPA: 3.8/4.0
                
                SKILLS
                Python, Node.js, JavaScript, FastAPI, Express.js, AWS, Docker, Kubernetes, 
                PostgreSQL, MongoDB, Redis, Git, Linux, Microservices, REST APIs
                
                CERTIFICATIONS
                AWS Certified Solutions Architect
                Kubernetes Administrator (CKA)
                """
            },
            {
                "name": "Data Scientist Resume",
                "text": """
                Jane Doe
                Data Scientist
                Email: jane.doe@email.com
                Phone: +1-555-0200
                Location: New York, NY
                
                SUMMARY
                Data scientist with 4 years of experience in machine learning, statistical analysis,
                and data visualization. Strong background in Python, SQL, and ML frameworks.
                
                EXPERIENCE
                Data Scientist | DataTech Solutions | 2020 - Present
                - Built predictive models using scikit-learn and TensorFlow
                - Analyzed large datasets (100M+ rows) using Python and SQL
                - Created data visualizations with Tableau and matplotlib
                - Improved model accuracy by 25% through feature engineering
                - Collaborated with engineering team to deploy ML models
                
                Junior Data Analyst | Analytics Corp | 2019 - 2020
                - Performed statistical analysis on business data
                - Created dashboards and reports
                - Wrote SQL queries for data extraction
                
                EDUCATION
                Master of Science in Data Science
                Tech University | 2019
                
                Bachelor of Science in Statistics
                State College | 2017
                
                SKILLS
                Python, R, SQL, Machine Learning, Deep Learning, TensorFlow, PyTorch,
                scikit-learn, pandas, numpy, Tableau, matplotlib, seaborn, statistics
                
                CERTIFICATIONS
                Google Data Analytics Professional Certificate
                """
            },
            {
                "name": "Full Stack Developer Resume",
                "text": """
                Alex Johnson
                Full Stack Developer
                Email: alex.johnson@email.com
                Phone: +1-555-0300
                Location: Seattle, WA
                
                SUMMARY
                Full stack developer with 5 years of experience building web applications.
                Expertise in React, Node.js, and cloud deployment.
                
                EXPERIENCE
                Full Stack Developer | WebDev Inc. | 2019 - Present
                - Developed responsive web applications using React and Node.js
                - Built RESTful APIs and GraphQL endpoints
                - Implemented authentication and authorization systems
                - Deployed applications on AWS and Azure
                - Worked with PostgreSQL and MongoDB databases
                
                Frontend Developer | DesignStudio | 2018 - 2019
                - Created user interfaces using React and Vue.js
                - Implemented responsive designs with CSS and Bootstrap
                
                EDUCATION
                Bachelor of Science in Computer Science
                University of Technology | 2018
                
                SKILLS
                JavaScript, TypeScript, React, Vue.js, Node.js, Express.js, HTML, CSS,
                PostgreSQL, MongoDB, AWS, Azure, Git, REST APIs, GraphQL
                """
            }
        ]
    
    def test_parser(self) -> Dict[str, Any]:
        """Test resume parser"""
        print("\n" + "="*60)
        print("TESTING RESUME PARSER")
        print("="*60)
        
        parser = ResumeParser()
        results = {
            "total": len(self.test_resumes),
            "successful": 0,
            "failed": 0,
            "details": []
        }
        
        for resume in self.test_resumes:
            try:
                start_time = time.time()
                parsed = parser.parse_text(resume["text"])
                elapsed = time.time() - start_time
                
                # Check extraction quality
                extracted_fields = {
                    "name": parsed.name is not None,
                    "email": parsed.email is not None,
                    "skills": len(parsed.skills) > 0,
                    "experiences": len(parsed.experiences) > 0,
                    "education": len(parsed.education) > 0
                }
                
                field_count = sum(extracted_fields.values())
                accuracy = (field_count / 5) * 100
                
                results["successful"] += 1
                results["details"].append({
                    "resume": resume["name"],
                    "accuracy": round(accuracy, 2),
                    "fields_extracted": field_count,
                    "time": round(elapsed, 2),
                    "name": parsed.name,
                    "email": parsed.email,
                    "skills_count": len(parsed.skills),
                    "experiences_count": len(parsed.experiences)
                })
                
                print(f"\n✓ {resume['name']}")
                print(f"  Accuracy: {accuracy:.1f}%")
                print(f"  Fields: {field_count}/5")
                print(f"  Time: {elapsed:.2f}s")
                print(f"  Name: {parsed.name}")
                print(f"  Skills: {len(parsed.skills)} found")
                
            except Exception as e:
                results["failed"] += 1
                results["details"].append({
                    "resume": resume["name"],
                    "error": str(e)
                })
                print(f"\n✗ {resume['name']}: {e}")
        
        avg_accuracy = sum(d["accuracy"] for d in results["details"] if "accuracy" in d) / results["successful"] if results["successful"] > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"Parser Results: {results['successful']}/{results['total']} successful")
        print(f"Average Accuracy: {avg_accuracy:.1f}%")
        print(f"{'='*60}")
        
        self.results["parser"] = results
        return results
    
    def test_classifier(self) -> Dict[str, Any]:
        """Test role classifier"""
        print("\n" + "="*60)
        print("TESTING ROLE CLASSIFIER")
        print("="*60)
        
        classifier = RoleClassifier()
        results = {
            "total": len(self.test_resumes),
            "correct": 0,
            "details": []
        }
        
        expected_roles = {
            "Backend Developer Resume": "Backend Developer",
            "Data Scientist Resume": "Data Scientist",
            "Full Stack Developer Resume": "Full Stack Developer"
        }
        
        for resume in self.test_resumes:
            try:
                start_time = time.time()
                classifications = classifier.classify(resume["text"], top_k=3)
                elapsed = time.time() - start_time
                
                top_role = classifications[0]["role"]
                expected = expected_roles.get(resume["name"], "")
                is_correct = expected.lower() in top_role.lower() or top_role.lower() in expected.lower()
                
                if is_correct:
                    results["correct"] += 1
                
                results["details"].append({
                    "resume": resume["name"],
                    "expected": expected,
                    "predicted": top_role,
                    "score": classifications[0]["score"],
                    "correct": is_correct,
                    "alternatives": [c["role"] for c in classifications[1:3]],
                    "time": round(elapsed, 3)
                })
                
                status = "✓" if is_correct else "✗"
                print(f"\n{status} {resume['name']}")
                print(f"  Expected: {expected}")
                print(f"  Predicted: {top_role} (score: {classifications[0]['score']:.3f})")
                print(f"  Time: {elapsed:.3f}s")
                
            except Exception as e:
                results["details"].append({
                    "resume": resume["name"],
                    "error": str(e)
                })
                print(f"\n✗ {resume['name']}: {e}")
        
        accuracy = (results["correct"] / results["total"]) * 100 if results["total"] > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"Classifier Results: {results['correct']}/{results['total']} correct")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"{'='*60}")
        
        self.results["classifier"] = results
        return results
    
    def test_job_scraper(self) -> Dict[str, Any]:
        """Test job scraper"""
        print("\n" + "="*60)
        print("TESTING JOB SCRAPER")
        print("="*60)
        
        scraper = JobScraper()
        results = {
            "sources_tested": [],
            "total_jobs": 0,
            "details": []
        }
        
        test_queries = ["backend developer", "data scientist"]
        
        for query in test_queries:
            try:
                print(f"\nSearching for: {query}")
                start_time = time.time()
                jobs = scraper.search_all_sources(query)
                elapsed = time.time() - start_time
                
                # Count by source
                by_source = {}
                for job in jobs:
                    source = job.get("source", "unknown")
                    by_source[source] = by_source.get(source, 0) + 1
                
                results["total_jobs"] += len(jobs)
                results["details"].append({
                    "query": query,
                    "jobs_found": len(jobs),
                    "by_source": by_source,
                    "time": round(elapsed, 2)
                })
                
                print(f"  Found: {len(jobs)} jobs in {elapsed:.2f}s")
                for source, count in by_source.items():
                    print(f"    - {source}: {count} jobs")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                results["details"].append({
                    "query": query,
                    "error": str(e)
                })
        
        print(f"\n{'='*60}")
        print(f"Scraper Results: {results['total_jobs']} total jobs found")
        print(f"{'='*60}")
        
        self.results["job_scraper"] = results
        return results
    
    def test_vector_db(self) -> Dict[str, Any]:
        """Test vector database"""
        print("\n" + "="*60)
        print("TESTING VECTOR DATABASE")
        print("="*60)
        
        try:
            vector_store = VectorStore()
            
            # Test adding jobs
            test_jobs = [
                {
                    "id": "test_1",
                    "title": "Backend Developer",
                    "company": "Tech Corp",
                    "location": "San Francisco",
                    "description": "Looking for backend developer with Python and Node.js experience",
                    "requirements": "5+ years experience, Python, FastAPI, AWS",
                    "source": "test"
                },
                {
                    "id": "test_2",
                    "title": "Data Scientist",
                    "company": "Data Inc",
                    "location": "New York",
                    "description": "Data scientist position requiring ML and statistics knowledge",
                    "requirements": "Master's degree, Python, TensorFlow, SQL",
                    "source": "test"
                }
            ]
            
            print("\nAdding test jobs...")
            start_time = time.time()
            vector_store.add_jobs_batch(test_jobs)
            add_time = time.time() - start_time
            
            initial_count = vector_store.get_job_count()
            print(f"  Added {len(test_jobs)} jobs in {add_time:.3f}s")
            print(f"  Total jobs in DB: {initial_count}")
            
            # Test search
            print("\nTesting search...")
            queries = [
                "backend developer python",
                "data scientist machine learning"
            ]
            
            search_results = []
            for query in queries:
                start_time = time.time()
                results = vector_store.search_jobs(query, top_k=5)
                elapsed = time.time() - start_time
                
                search_results.append({
                    "query": query,
                    "results": len(results),
                    "time": round(elapsed, 3),
                    "top_score": results[0]["score"] if results else 0
                })
                
                print(f"  Query: '{query}'")
                print(f"    Found: {len(results)} results in {elapsed:.3f}s")
                if results:
                    print(f"    Top match: {results[0]['title']} (score: {results[0]['score']:.3f})")
            
            # Cleanup
            vector_store.delete_job("test_1")
            vector_store.delete_job("test_2")
            
            results = {
                "status": "success",
                "add_time": round(add_time, 3),
                "search_results": search_results,
                "initial_count": initial_count
            }
            
            print(f"\n{'='*60}")
            print("Vector DB: All tests passed")
            print(f"{'='*60}")
            
            self.results["vector_db"] = results
            return results
            
        except Exception as e:
            print(f"\n✗ Vector DB Error: {e}")
            results = {"status": "failed", "error": str(e)}
            self.results["vector_db"] = results
            return results
    
    def test_matcher(self) -> Dict[str, Any]:
        """Test job matcher"""
        print("\n" + "="*60)
        print("TESTING JOB MATCHER")
        print("="*60)
        
        matcher = JobMatcher()
        
        # Test resume data
        resume_data = {
            "name": "John Smith",
            "skills": ["Python", "Node.js", "AWS", "Docker", "PostgreSQL"],
            "years_of_experience": 5.0,
            "experiences": [{
                "title": "Backend Developer",
                "company": "Tech Corp",
                "description": "Built APIs and microservices"
            }]
        }
        
        # Test jobs
        test_jobs = [
            {
                "id": "job1",
                "title": "Senior Backend Developer",
                "company": "Tech Inc",
                "description": "Looking for backend developer with Python, Node.js, and AWS experience. 5+ years required.",
                "requirements": "Python, Node.js, AWS, Docker, 5+ years experience"
            },
            {
                "id": "job2",
                "title": "Frontend Developer",
                "company": "Web Corp",
                "description": "Frontend developer position. React and JavaScript required.",
                "requirements": "React, JavaScript, 3+ years"
            },
            {
                "id": "job3",
                "title": "Backend Engineer",
                "company": "API Solutions",
                "description": "Backend engineer with Python and PostgreSQL. 4+ years experience.",
                "requirements": "Python, PostgreSQL, 4+ years"
            }
        ]
        
        try:
            print("\nMatching resume to jobs...")
            start_time = time.time()
            ranked = matcher.rank_jobs(resume_data, test_jobs, top_k=3)
            elapsed = time.time() - start_time
            
            print(f"\nRanked {len(ranked)} jobs in {elapsed:.3f}s")
            print("\nRankings:")
            for i, job_result in enumerate(ranked, 1):
                print(f"\n  {i}. {job_result['job']['title']} at {job_result['job']['company']}")
                print(f"     Final Score: {job_result['final_score']:.3f}")
                print(f"     Breakdown:")
                print(f"       - Semantic: {job_result['breakdown']['semantic']:.3f}")
                print(f"       - Skills: {job_result['breakdown']['skills']:.3f}")
                print(f"       - Experience: {job_result['breakdown']['experience']:.3f}")
            
            # Check if best match is correct
            best_match = ranked[0]
            is_correct = "backend" in best_match['job']['title'].lower()
            
            results = {
                "status": "success",
                "total_jobs": len(test_jobs),
                "ranked": len(ranked),
                "best_match_correct": is_correct,
                "top_score": best_match['final_score'],
                "time": round(elapsed, 3),
                "rankings": [
                    {
                        "title": r['job']['title'],
                        "score": r['final_score'],
                        "breakdown": r['breakdown']
                    }
                    for r in ranked
                ]
            }
            
            print(f"\n{'='*60}")
            print(f"Matcher: Best match is {'correct' if is_correct else 'incorrect'}")
            print(f"Top score: {best_match['final_score']:.3f}")
            print(f"{'='*60}")
            
            self.results["matcher"] = results
            return results
            
        except Exception as e:
            print(f"\n✗ Matcher Error: {e}")
            import traceback
            traceback.print_exc()
            results = {"status": "failed", "error": str(e)}
            self.results["matcher"] = results
            return results
    
    def test_full_pipeline(self) -> Dict[str, Any]:
        """Test complete pipeline"""
        print("\n" + "="*60)
        print("TESTING FULL PIPELINE")
        print("="*60)
        
        pipeline = ResumeJobPipeline()
        results = {
            "total": len(self.test_resumes),
            "successful": 0,
            "details": []
        }
        
        for resume in self.test_resumes[:1]:  # Test with first resume only
            try:
                print(f"\nProcessing: {resume['name']}")
                start_time = time.time()
                
                result = pipeline.process_resume_text(
                    resume["text"],
                    top_k_jobs=5,
                    use_vector_db=False  # Use web scraping instead
                )
                
                elapsed = time.time() - start_time
                
                results["successful"] += 1
                results["details"].append({
                    "resume": resume["name"],
                    "time": round(elapsed, 2),
                    "parsed": result["resume_data"]["name"] is not None,
                    "classified_role": result["classified_role"],
                    "jobs_found": result["total_jobs_found"],
                    "recommendations": len(result["recommended_jobs"])
                })
                
                print(f"  ✓ Completed in {elapsed:.2f}s")
                print(f"  Role: {result['classified_role']}")
                print(f"  Jobs found: {result['total_jobs_found']}")
                print(f"  Recommendations: {len(result['recommended_jobs'])}")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                import traceback
                traceback.print_exc()
                results["details"].append({
                    "resume": resume["name"],
                    "error": str(e)
                })
        
        print(f"\n{'='*60}")
        print(f"Pipeline: {results['successful']}/{results['total']} successful")
        print(f"{'='*60}")
        
        self.results["pipeline"] = results
        return results
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*60)
        print("COMPREHENSIVE TEST SUITE")
        print("AI Resume Parser & Job Recommender")
        print("="*60)
        
        start_time = time.time()
        
        # Run tests
        self.test_parser()
        self.test_classifier()
        self.test_job_scraper()
        self.test_vector_db()
        self.test_matcher()
        self.test_full_pipeline()
        
        total_time = time.time() - start_time
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        parser_acc = sum(d["accuracy"] for d in self.results["parser"]["details"] if "accuracy" in d) / self.results["parser"]["successful"] if self.results["parser"]["successful"] > 0 else 0
        classifier_acc = (self.results["classifier"]["correct"] / self.results["classifier"]["total"]) * 100 if self.results["classifier"]["total"] > 0 else 0
        
        print(f"\nParser Accuracy: {parser_acc:.1f}%")
        print(f"Classifier Accuracy: {classifier_acc:.1f}%")
        print(f"Job Scraper: {self.results['job_scraper']['total_jobs']} jobs found")
        print(f"Vector DB: {'✓ Working' if self.results['vector_db'].get('status') == 'success' else '✗ Failed'}")
        print(f"Job Matcher: {'✓ Working' if self.results['matcher'].get('status') == 'success' else '✗ Failed'}")
        print(f"Pipeline: {self.results['pipeline']['successful']}/{self.results['pipeline']['total']} successful")
        print(f"\nTotal Test Time: {total_time:.2f}s")
        print("="*60)
        
        # Save results
        results_file = project_root / "test_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    suite = TestSuite()
    suite.run_all_tests()
