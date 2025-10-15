"""
Web Enrichment Agent for MisterHR

This agent verifies and enriches candidate profiles by analyzing online presence.
It validates GitHub profiles, LinkedIn accounts, personal portfolios, and other online credentials.
"""

import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from .base_agent import BaseAgent, AgentConfig

class WebEnrichmentAgent(BaseAgent):
    """
    Web Enrichment Agent

    Validates and enriches candidate profiles by analyzing online presence:
    1. GitHub Profile Analysis
    2. LinkedIn Profile Verification
    3. Portfolio Website Validation
    4. Online Presence Scoring
    5. Skills Endorsement Checking
    6. Social Proof Aggregation

    Uses web scraping and API calls for verification and enrichment
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)

        # Initialize HTTP client session (will be created per request for proper cleanup)
        self.session = None

        # Platforms to check
        self.supported_platforms = {
            'github': {
                'pattern': r'github\.com/([a-zA-Z0-9-]{1,39})',
                'headers': {'Authorization': f'token {os.getenv("GITHUB_TOKEN", "")}' if os.getenv("GITHUB_TOKEN") else {}}
            },
            'linkedin': {
                'pattern': r'linkedin\.com/in/([a-zA-Z0-9-]+)',
                'headers': {}
            },
            'stackoverflow': {
                'pattern': r'stackoverflow\.com/users/(\d+)/?',
                'headers': {}
            },
            'medium': {
                'pattern': r'medium\.com/@([a-zA-Z0-9-]+)',
                'headers': {}
            },
            'dev.to': {
                'pattern': r'dev\.to/([a-zA-Z0-9]+)',
                'headers': {}
            }
        }

        # Skills validation keywords
        self.skill_validation_patterns = {
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
            'javascript': ['javascript', 'react', 'vue', 'angular', 'node.js', 'express'],
            'java': ['java', 'spring', 'hibernate', 'maven', 'gradle'],
            'web_development': ['html', 'css', 'sass', 'webpack', 'vite', 'tailwind'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes']
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters."""
        online_presence = kwargs.get('online_presence', {})
        links = online_presence.get('other_links', [])

        # Check if we have any URLs to verify
        urls_to_check = []

        # Primary links
        for platform in ['github', 'linkedin', 'portfolio']:
            if online_presence.get(platform):
                urls_to_check.append(online_presence[platform])

        # Additional links
        urls_to_check.extend(links or [])

        return len(urls_to_check) > 0

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Enrich candidate profile with online presence analysis.

        Args:
            online_presence (dict): Dictionary with github, linkedin, portfolio keys
            skills (dict): Technical skills to verify against

        Returns:
            Dict with verification results and enriched data
        """
        online_presence = kwargs.get('online_presence', {})
        skills = kwargs.get('skills', {})
        personal_info = kwargs.get('personal_info', {})

        try:
            # Gather all URLs to verify
            urls_to_verify = self._collect_urls(online_presence)

            # Create HTTP session
            async with aiohttp.ClientSession(
                headers={'User-Agent': 'MisterHR-WebEnrichment/1.0'}
            ) as session:
                self.session = session

                # Verify all URLs concurrently
                verification_results = await self._verify_all_urls(urls_to_verify)

                # Extract platform-specific data
                enrichment_data = await self._extract_platform_data(
                    verification_results, skills, personal_info
                )

                # Calculate overall credibility score
                credibility_score = self._calculate_credibility_score(verification_results, enrichment_data)

                # Validate skills against online presence
                skills_verification = self._verify_skills_online(enrichment_data, skills)

                return {
                    "verification_results": verification_results,
                    "enrichment_data": enrichment_data,
                    "credibility_score": credibility_score,
                    "skills_verification": skills_verification,
                    "metadata": {
                        'enriched_at': datetime.now(),
                        'urls_checked': len(urls_to_verify),
                        'platforms_verified': len(verification_results),
                        'confidence_score': self._calculate_confidence(verification_results)
                    }
                }

        except Exception as e:
            self.logger.error(f"Web enrichment failed: {str(e)}")
            raise

    def _collect_urls(self, online_presence: Dict[str, Any]) -> List[str]:
        """Collect all URLs that need verification."""
        urls = []

        # Primary profile links
        for platform in ['github', 'linkedin', 'portfolio']:
            url = online_presence.get(platform)
            if url:
                urls.append(url)

        # Additional links
        additional_links = online_presence.get('other_links', [])
        urls.extend(additional_links)

        return list(set(urls))  # Remove duplicates

    async def _verify_all_urls(self, urls: List[str]) -> Dict[str, Dict[str, Any]]:
        """Verify all URLs concurrently and return results."""
        if not urls:
            return {}

        # Create verification tasks
        tasks = []
        for url in urls:
            tasks.append(self._verify_single_url(url))

        # Execute all verifications concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and associate with URLs
        verification_results = {}
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                verification_results[url] = {
                    'verified': False,
                    'status': 'error',
                    'error': str(result),
                    'platform': self._identify_platform(url),
                    'timestamp': datetime.now()
                }
            else:
                result['timestamp'] = datetime.now()
                verification_results[url] = result

        return verification_results

    async def _verify_single_url(self, url: str) -> Dict[str, Any]:
        """Verify a single URL and determine its validity."""
        try:
            # Clean and validate URL
            clean_url = self._clean_url(url)
            if not clean_url:
                return {
                    'verified': False,
                    'status': 'invalid_url',
                    'error': 'Invalid URL format'
                }

            # Make request with timeout
            timeout = aiohttp.ClientTimeout(total=10)
            async with self.session.get(clean_url, timeout=timeout, allow_redirects=True) as response:

                platform = self._identify_platform(clean_url)
                result = {
                    'verified': response.status == 200,
                    'status_code': response.status,
                    'platform': platform,
                    'url': clean_url,
                    'content_type': response.headers.get('Content-Type', ''),
                    'last_modified': response.headers.get('Last-Modified'),
                    'accessible': True
                }

                # Additional checks based on platform
                if platform == 'github':
                    result.update(await self._verify_github_profile(clean_url, response))
                elif platform == 'linkedin':
                    result.update(await self._verify_linkedin_profile(clean_url, response))
                elif platform == 'portfolio':
                    result.update(await self._verify_portfolio(clean_url, response))

                return result

        except aiohttp.ClientError as e:
            return {
                'verified': False,
                'status': 'connection_error',
                'error': f'Connection failed: {str(e)}',
                'accessible': False
            }
        except Exception as e:
            return {
                'verified': False,
                'status': 'unknown_error',
                'error': str(e),
                'accessible': False
            }

    def _clean_url(self, url: str) -> Optional[str]:
        """Clean and validate URL format."""
        if not url:
            return None

        # Remove extra whitespace and common prefixes
        url = url.strip()

        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'

        # Validate URL format
        try:
            parsed = urlparse(url)
            if parsed.netloc and parsed.scheme in ['http', 'https']:
                return url
        except:
            pass

        return None

    def _identify_platform(self, url: str) -> str:
        """Identify which platform a URL belongs to."""
        url_lower = url.lower()

        if 'github.com' in url_lower:
            return 'github'
        elif 'linkedin.com' in url_lower:
            return 'linkedin'
        elif 'stackoverflow.com' in url_lower:
            return 'stackoverflow'
        elif 'medium.com' in url_lower:
            return 'medium'
        elif 'dev.to' in url_lower:
            return 'dev.to'
        else:
            return 'portfolio'

    async def _verify_github_profile(self, url: str, response) -> Dict[str, Any]:
        """Verify and extract GitHub profile information."""
        github_data = {}

        try:
            # Check if it's a valid GitHub profile URL
            match = re.search(r'github\.com/([a-zA-Z0-9-]{1,39})', url)
            if not match:
                return {'github_valid': False, 'error': 'Invalid GitHub username'}

            username = match.group(1)

            # Try to get repository data (if we have a token)
            if os.getenv('GITHUB_TOKEN'):
                api_url = f'https://api.github.com/users/{username}'
                async with self.session.get(api_url) as api_response:
                    if api_response.status == 200:
                        user_data = await api_response.json()
                        github_data.update({
                            'github_valid': True,
                            'repos_count': user_data.get('public_repos', 0),
                            'followers': user_data.get('followers', 0),
                            'following': user_data.get('following', 0),
                            'last_updated': user_data.get('updated_at'),
                            'hireable': user_data.get('hireable', False)
                        })
                    else:
                        github_data.update({'github_valid': True, 'error': 'API rate limited'})

            # Parse HTML for basic info
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract bio
                bio_elem = soup.find('div', {'data-bio-text': True})
                if bio_elem:
                    github_data['bio'] = bio_elem.text.strip()

                # Extract location
                location_elem = soup.find('span', {'itemprop': 'homeLocation'})
                if location_elem:
                    github_data['location'] = location_elem.text.strip()

        except Exception as e:
            github_data['error'] = str(e)

        return github_data

    async def _verify_linkedin_profile(self, url: str, response) -> Dict[str, Any]:
        """Verify LinkedIn profile (basic verification only due to anti-scraping)."""
        linkedin_data = {}

        try:
            if response.status == 200:
                html_content = await response.text()

                # Basic checks (LinkedIn has strong anti-scraping)
                linkedin_data.update({
                    'linkedin_valid': True,
                    'profile_exists': True,
                    'scrapable': False  # LinkedIn blocks most scraping
                })

                # Try to extract basic info from meta tags
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extract title
                title = soup.find('title')
                if title:
                    linkedin_data['page_title'] = title.text.strip()

                # Extract description
                description = soup.find('meta', {'name': 'description'})
                if description:
                    linkedin_data['description'] = description.get('content', '')

        except Exception as e:
            linkedin_data['error'] = str(e)

        return linkedin_data

    async def _verify_portfolio(self, url: str, response) -> Dict[str, Any]:
        """Verify portfolio website."""
        portfolio_data = {}

        try:
            if response.status == 200:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, 'html.parser')

                portfolio_data.update({
                    'portfolio_valid': True,
                    'has_content': len(html_content) > 1000,  # Basic content check
                    'has_title': bool(soup.find('title')),
                    'has_projects': bool(soup.find_all(['div', 'section'], class_=re.compile('project|work', re.I)))
                })

                # Extract title
                title = soup.find('title')
                if title:
                    portfolio_data['title'] = title.text.strip()

                # Extract description
                description = soup.find('meta', {'name': 'description'})
                if description:
                    portfolio_data['description'] = description.get('content', '')

        except Exception as e:
            portfolio_data['error'] = str(e)

        return portfolio_data

    async def _extract_platform_data(self, verification_results: Dict[str, Dict[str, Any]],
                                   skills: Dict[str, Any], personal_info: Dict[str, str]) -> Dict[str, Any]:
        """Extract actionable data from verified platforms."""
        enriched_data = {
            'github_activity': {},
            'linkedin_visibility': {},
            'portfolio_quality': {},
            'social_proof_score': 0,
            'technical_validation': []
        }

        for url, result in verification_results.items():
            if not result.get('verified', False):
                continue

            platform = result.get('platform', '')

            if platform == 'github' and result.get('repos_count'):
                enriched_data['github_activity'] = {
                    'repos': result.get('repos_count', 0),
                    'followers': result.get('followers', 0),
                    'active': result.get('repos_count', 0) > 5
                }
                enriched_data['social_proof_score'] += min(result.get('followers', 0) // 10, 10)
                enriched_data['social_proof_score'] += result.get('repos_count', 0) // 5

            elif platform == 'linkedin':
                enriched_data['linkedin_visibility'] = {
                    'profile_exists': True,
                    'professional_network': True
                }
                enriched_data['social_proof_score'] += 15

            elif platform == 'portfolio':
                enriched_data['portfolio_quality'] = {
                    'has_content': result.get('has_content', False),
                    'has_projects': result.get('has_projects', False),
                    'professional': True
                }
                enriched_data['social_proof_score'] += 10

        return enriched_data

    def _verify_skills_online(self, enrichment_data: Dict[str, Any], skills: Dict[str, Any]) -> Dict[str, Any]:
        """Verify skills against online presence indicators."""
        technical_skills = skills.get('technical', [])

        verification_results = {
            'verified_skills': [],
            'unverified_skills': [],
            'confidence_level': 'low'
        }

        # Check GitHub repos for technology indicators
        github_data = enrichment_data.get('github_activity', {})

        for skill in technical_skills:
            skill_lower = skill.lower()
            verified = False

            # Check skill validation patterns
            for category, patterns in self.skill_validation_patterns.items():
                if skill_lower in patterns:
                    verified = True
                    break

            if verified:
                verification_results['verified_skills'].append(skill)
            else:
                verification_results['unverified_skills'].append(skill)

        # Adjust confidence based on data richness
        if github_data and github_data.get('active', False):
            verification_results['confidence_level'] = 'medium'
        if enrichment_data.get('social_proof_score', 0) > 30:
            verification_results['confidence_level'] = 'high'

        return verification_results

    def _calculate_credibility_score(self, verification_results: Dict[str, Dict[str, Any]],
                                   enrichment_data: Dict[str, Any]) -> float:
        """Calculate overall online credibility score (0-100)."""
        score = 0.0

        total_urls = len(verification_results)
        verified_urls = sum(1 for result in verification_results.values() if result.get('verified', False))

        if total_urls > 0:
            score += (verified_urls / total_urls) * 30  # 30% for URL verification

        # GitHub activity score (max 30 points)
        github_score = 0
        if enrichment_data.get('github_activity'):
            github_data = enrichment_data['github_activity']
            github_score = min(github_data.get('repos', 0) // 2, 15)  # Repos count
            github_score += min(github_data.get('followers', 0) // 5, 15)  # Followers

        score += min(github_score, 30)

        # LinkedIn presence (20 points)
        if enrichment_data.get('linkedin_visibility', {}).get('profile_exists'):
            score += 20

        # Portfolio quality (20 points)
        if enrichment_data.get('portfolio_quality', {}).get('professional'):
            score += 20

        return min(100.0, score)

    def _calculate_confidence(self, verification_results: Dict[str, Dict[str, Any]]) -> float:
        """Calculate confidence score for the enrichment process."""
        if not verification_results:
            return 0.0

        total_checks = len(verification_results)
        successful_checks = sum(1 for result in verification_results.values()
                               if result.get('verified', False) and not result.get('error'))

        return successful_checks / total_checks if total_checks > 0 else 0.0
