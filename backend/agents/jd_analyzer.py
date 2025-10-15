"""
Job Description Analyzer Agent for MisterHR

This agent parses job descriptions and extracts key requirements using LLM analysis.
It identifies skills, experience levels, qualifications, and other job criteria.
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent, AgentConfig

class JDAnalyzerAgent(BaseAgent):
    """
    Job Description Analyzer Agent

    Extracts and analyzes job posting requirements:
    1. Job Title and Level
    2. Required Skills (Technical & Soft)
    3. Experience Requirements
    4. Education Requirements
    5. Key Responsibilities
    6. Preferred Qualifications
    7. Salary Information
    8. Company Information

    Uses LLM for intelligent parsing and categorization
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)

        # Initialize LangChain LLM (will be set by orchestrator)
        self.llm = None

        # Categories to extract
        self.categories = [
            "job_title", "experience_level", "required_skills",
            "preferred_skills", "education", "responsibilities",
            "qualifications", "benefits", "location", "salary_range"
        ]

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters."""
        jd_text = kwargs.get('jd_text') or kwargs.get('content')
        if not jd_text or not isinstance(jd_text, str):
            return False

        # Basic length check
        if len(jd_text.strip()) < 50:
            return False

        return True

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Analyze job description and extract structured requirements.

        Args:
            jd_text (str): Job description text
            content (str): Alternative parameter for JD content

        Returns:
            Dict with analyzed job requirements
        """
        jd_text = kwargs.get('jd_text') or kwargs.get('content', '')
        if not jd_text:
            raise ValueError("Job description text is required")

        try:
            # Use LLM for intelligent analysis
            if self.llm:
                analysis = await self._analyze_with_llm(jd_text)
            else:
                # Fallback to rule-based parsing
                analysis = self._analyze_with_rules(jd_text)

            # Validate and score analysis
            analysis['metadata'] = {
                'analyzed_at': datetime.now(),
                'text_length': len(jd_text),
                'confidence_score': self._calculate_confidence(analysis),
                'method': 'llm' if self.llm else 'rules'
            }

            return analysis

        except Exception as e:
            self.logger.error(f"JD analysis failed: {str(e)}")
            raise

    async def _analyze_with_llm(self, jd_text: str) -> Dict[str, Any]:
        """Analyze JD using LLM for intelligent extraction."""
        prompt = f"""
        Analyze this job description and extract structured information:

        JOB DESCRIPTION:
        {jd_text}

        Please extract the following information in JSON format:

        {{
            "job_title": "string - exact job title",
            "experience_level": "entry|junior|mid|senior|lead|executive",
            "years_experience_min": number,
            "years_experience_max": number,
            "required_skills": ["list", "of", "technical", "skills"],
            "preferred_skills": ["list", "of", "preferred", "skills"],
            "education": ["required", "degrees", "or", "certifications"],
            "responsibilities": ["key", "responsibilities"],
            "qualifications": ["additional", "requirements"],
            "benefits": ["company", "benefits", "mentioned"],
            "location": "job location or remote",
            "salary_range": "any salary information mentioned",
            "company_name": "company name if mentioned"
        }}

        Focus on technical skills, experience requirements, and key qualifications.
        Be specific and extract direct information from the job posting.
        """

        try:
            response = await self.llm.ainvoke(prompt)
            # Parse LLM response (assuming JSON output)
            import json
            analysis = json.loads(response.content)
            return analysis
        except Exception as e:
            self.logger.warning(f"LLM analysis failed, falling back to rules: {str(e)}")
            return self._analyze_with_rules(jd_text)

    def _analyze_with_rules(self, jd_text: str) -> Dict[str, Any]:
        """Fallback rule-based JD analysis."""
        text_lower = jd_text.lower()

        # Extract job title (first line or prominent text)
        lines = jd_text.split('\n')[:3]
        job_title = ""
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 50 and not any(char in line.lower() for char in ['@', 'http']):
                job_title = line
                break

        # Experience level detection
        experience_level = self._determine_experience_level(text_lower)

        # Required years of experience
        year_patterns = [
            r'(\d+)(?:\+|\s*-\s*\d+)*\s*years?(?:\s*of)?\s*experience',
            r'experience(?:\s*level)?:\s*(\d+)',
            r'minimum\s*(\d+)\s*years?'
        ]

        years_min = 0
        years_max = 0
        for pattern in year_patterns:
            match = re.search(pattern, text_lower)
            if match:
                years = int(match.group(1))
                years_min = years
                years_max = years + 2  # Assume some flexibility
                break

        # Skills extraction (basic keyword matching)
        tech_skills = self._extract_technical_skills(text_lower)
        soft_skills = self._extract_soft_skills(text_lower)

        # Education requirements
        education = self._extract_education_requirements(text_lower)

        # Location
        location = self._extract_location(jd_text)

        return {
            "job_title": job_title,
            "experience_level": experience_level,
            "years_experience_min": years_min,
            "years_experience_max": years_max,
            "required_skills": tech_skills[:10],  # Top 10 skills
            "preferred_skills": soft_skills[:5],  # Preferred soft skills
            "education": education,
            "responsibilities": [],  # Would need more complex parsing
            "qualifications": [],
            "benefits": [],
            "location": location,
            "salary_range": "",
            "company_name": ""
        }

    def _determine_experience_level(self, text: str) -> str:
        """Determine experience level from keywords."""
        senior_keywords = ['senior', 'lead', 'principal', 'architect', 'head', 'director', 'manager']
        mid_keywords = ['mid', 'intermediate', 'experienced', '3+', '4+', '5+']
        junior_keywords = ['junior', 'entry', 'graduate', 'fresh', '1+', '2+']

        text_lower = text.lower()

        senior_count = sum(1 for kw in senior_keywords if kw in text_lower)
        mid_count = sum(1 for kw in mid_keywords if kw in text_lower)
        junior_count = sum(1 for kw in junior_keywords if kw in text_lower)

        max_count = max(senior_count, mid_count, junior_count)

        if max_count == 0:
            return "mid"  # Default

        if senior_count == max_count:
            return "senior"
        elif mid_count == max_count:
            return "mid"
        else:
            return "junior"

    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills using keyword matching."""
        skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'typescript', 'php'],
            'web_dev': ['react', 'angular', 'vue', 'node', 'django', 'flask', 'express', 'html', 'css'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'sql', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'heroku'],
            'data_science': ['pandas', 'numpy', 'tensorflow', 'pyspark', 'jupyter', 'scikit-learn', 'ml', 'ai'],
            'mobile': ['android', 'ios', 'swift', 'kotlin', 'react native', 'flutter'],
            'tools': ['git', 'github', 'gitlab', 'jenkins', 'jira', 'slack', 'postman']
        }

        found_skills = []
        for category, skills in skill_keywords.items():
            for skill in skills:
                if skill in text:
                    found_skills.append(skill.title())

        return list(set(found_skills))  # Unique skills

    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills."""
        soft_skill_keywords = [
            'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
            'creative', 'attention to detail', 'time management', 'adaptability', 'collaboration'
        ]

        found_skills = []
        for skill in soft_skill_keywords:
            if skill.replace(' ', '') in text or skill in text:
                found_skills.append(skill.title())

        return found_skills

    def _extract_education_requirements(self, text: str) -> List[str]:
        """Extract education requirements."""
        education_keywords = [
            'bachelor', "master", 'phd', 'degree', 'computer science', 'engineering',
            'mathematics', 'business', 'equivalent experience', 'certification'
        ]

        requirements = []
        for keyword in education_keywords:
            if keyword in text:
                requirements.append(keyword.title())

        return list(set(requirements))

    def _extract_location(self, text: str) -> str:
        """Extract job location."""
        location_patterns = [
            r'(?:location|based in)[:\s]*([A-Za-z\s,]+)(?:\s*\||\n|$)',
            r'(?:remote|hybrid|onsite)\s*[-:]?\s*([A-Za-z\s,]+)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s*([A-Z]{2})\b'
        ]

        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1) if match.lastindex == 1 else f"{match.group(1)}, {match.group(2)}"
                return location.strip()

        # Check for remote work
        if 'remote' in text.lower():
            return 'Remote'
        elif 'hybrid' in text.lower():
            return 'Hybrid'

        return 'Not specified'

    def _calculate_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis."""
        score = 0.0
        total_checks = 4

        # Job title found
        if analysis.get('job_title'):
            score += 0.25

        # Skills extracted
        if analysis.get('required_skills') and len(analysis['required_skills']) > 0:
            score += 0.25

        # Experience level determined
        if analysis.get('experience_level'):
            score += 0.25

        # Location found
        if analysis.get('location') and analysis['location'] != 'Not specified':
            score += 0.25

        return min(1.0, score)
