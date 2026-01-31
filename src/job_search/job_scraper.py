"""
Job scraping from free sources (GitHub Jobs, RemoteOK, etc.)
"""
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import time
import re

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from src.utils.logger import logger

class JobScraper:
    """Scrape jobs from free sources"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': settings.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    
    def search_arbeitnow(self, query: str, location: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search Arbeitnow (free API, no key required)"""
        jobs = []
        try:
            url = "https://www.arbeitnow.com/api/job-board-api"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            raw = response.json()
            items = raw.get("data", raw) if isinstance(raw, dict) else (raw if isinstance(raw, list) else [])
            for job in items[:50]:
                if len(jobs) >= 20:
                    break
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
                    "description": self._clean_html(str(job.get("description", ""))),
                    "requirements": str(job.get("requirements", "") or ""),
                    "url": job.get("url", ""),
                    "source": "arbeitnow",
                    "posted_date": str(job.get("created_at", "")),
                })
            logger.info(f"Found {len(jobs)} jobs from Arbeitnow")
            time.sleep(settings.SCRAPING_DELAY)
        except Exception as e:
            logger.error(f"Error scraping Arbeitnow: {e}")
        return jobs
    
    def search_remoteok(self, query: str) -> List[Dict[str, Any]]:
        """Search RemoteOK (free job board)"""
        jobs = []
        try:
            url = "https://remoteok.com/api"
            params = {"tags": query.lower().replace(" ", ",")} if query else {}
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                data = data.get("data", []) if isinstance(data, dict) else []
            count = 0
            for job in data:
                if count >= 20:
                    break
                if not isinstance(job, dict) or not job.get("position"):
                    continue
                jobs.append({
                    "id": f"remoteok_{job.get('id', '')}",
                    "title": job.get("position", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", "") or "Remote",
                    "description": self._clean_html(job.get("description", "")),
                    "requirements": "",
                    "url": f"https://remoteok.com/remote-jobs/{job.get('id', '')}",
                    "source": "remoteok",
                    "posted_date": str(job.get("epoch", "")),
                })
                count += 1
            logger.info(f"Found {len(jobs)} jobs from RemoteOK")
            time.sleep(settings.SCRAPING_DELAY)
        except Exception as e:
            logger.error(f"Error scraping RemoteOK: {e}")
        return jobs
    
    def search_indeed_rss(self, query: str, location: str = "USA") -> List[Dict[str, Any]]:
        """Search Indeed via RSS feed (free, limited)"""
        jobs = []
        try:
            # Indeed RSS feed
            url = "https://www.indeed.com/rss"
            params = {
                "q": query,
                "l": location,
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:20]  # Limit to 20
            
            for item in items:
                title = item.find('title')
                link = item.find('link')
                description = item.find('description')
                
                if title and link:
                    jobs.append({
                        "id": f"indeed_{hash(link.text)}",
                        "title": title.text if title else '',
                        "company": self._extract_company_from_description(description.text if description else ''),
                        "location": location,
                        "description": self._clean_html(description.text if description else ''),
                        "requirements": "",
                        "url": link.text if link else '',
                        "source": "indeed",
                        "posted_date": "",
                    })
            
            logger.info(f"Found {len(jobs)} jobs from Indeed RSS")
            time.sleep(settings.SCRAPING_DELAY)
            
        except Exception as e:
            logger.error(f"Error scraping Indeed RSS: {e}")
        
        return jobs
    
    def _clean_html(self, html: str) -> str:
        """Clean HTML tags from text"""
        if not html:
            return ""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def _extract_company_from_description(self, description: str) -> str:
        """Extract company name from description"""
        # Simple extraction - can be improved
        match = re.search(r'Company:\s*([^\n]+)', description, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return "Unknown"
    
    def search_all_sources(self, query: str, location: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search all configured sources (free APIs only)"""
        all_jobs = []
        if "arbeitnow" in settings.JOB_SOURCES:
            all_jobs.extend(self.search_arbeitnow(query, location))
        if "remoteok" in settings.JOB_SOURCES:
            all_jobs.extend(self.search_remoteok(query))
        if "indeed" in settings.JOB_SOURCES:
            all_jobs.extend(self.search_indeed_rss(query, location or "USA"))
        
        # Deduplicate by title and company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        logger.info(f"Total unique jobs found: {len(unique_jobs)}")
        return unique_jobs
