"""
Resume Parser Agent for MisterHR

This agent extracts structured data from PDF/DOCX resumes using PyMuPDF and spaCy.
It categorizes information into 8 key sections for comprehensive candidate profiling.
"""

import fitz  # PyMuPDF
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import json
import spacy
from .base_agent import BaseAgent, AgentConfig

class ResumeParserAgent(BaseAgent):
    """
    Resume Parser Agent

    Extracts structured data from CVs/resumes with 8 categories:
    1. Personal Information
    2. Professional Experience
    3. Education Background
    4. Technical Skills
    5. Soft Skills
    6. Projects & Achievements
    7. Certifications
    8. Online Presence Links

    Supports multiple formats: PDF, DOCX, TXT
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)

        # Initialize spaCy NLP model
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.nlp_enabled = True
        except OSError:
            self.logger.warning("spaCy en_core_web_sm model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
            self.nlp_enabled = False

        # Text processing patterns
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\(\d{3}\)\s*\d{3}[-.]?\d{4}'
        self.url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:\w*))?)?'

        # Experience level keywords
        self.senior_keywords = ['senior', 'lead', 'principal', 'architect', 'head', 'director']
        self.mid_keywords = ['mid-level', 'intermediate', 'experienced']
        self.junior_keywords = ['junior', 'entry-level', 'fresher', 'graduate']

        # Section headers for NLP-based section detection
        self.section_patterns = {
            'experience': ['experience', 'employment', 'work history', 'professional experience', 'work experience'],
            'education': ['education', 'academic background', 'academic qualifications'],
            'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
            'projects': ['projects', 'personal projects', 'professional projects'],
            'certifications': ['certifications', 'certificates', 'credentials'],
        }

        # Skill categorization
        self.skill_categories = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'typescript', 'php'],
            'web_dev': ['react', 'angular', 'vue', 'node', 'django', 'flask', 'express', 'html', 'css'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'sql', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'heroku'],
            'data_science': ['pandas', 'numpy', 'tensorflow', 'pyspark', 'jupyter', 'scikit-learn', 'ml', 'ai']
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters."""
        file_path = kwargs.get('file_path')
        content = kwargs.get('content')
        url = kwargs.get('url')

        if not any([file_path, content, url]):
            return False

        if file_path and not Path(file_path).exists():
            return False

        return True

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Parse resume and extract structured data.

        Args:
            file_path (str): Path to resume file
            content (str): Raw text content
            url (str): URL to resume file

        Returns:
            Dict with parsed resume data in 8 categories
        """
        file_path = kwargs.get('file_path')
        content = kwargs.get('content')
        url = kwargs.get('url')

        try:
            # Extract raw text from file
            if file_path:
                raw_text = self._extract_text_from_file(file_path)
            elif url:
                # TODO: Implement URL downloading
                raw_text = "Downloaded content from URL"
            else:
                raw_text = content or ""

            # Parse into structured data
            parsed_data = self._parse_resume_text(raw_text)

            return parsed_data

        except Exception as e:
            self.logger.error(f"Resume parsing failed: {str(e)}")
            raise

    def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF/DOCX files."""
        file_path_lower = file_path.lower()

        if file_path_lower.endswith('.pdf'):
            return self._extract_pdf_text(file_path)
        elif file_path_lower.endswith(('.docx', '.doc')):
            return self._extract_docx_text(file_path)
        elif file_path_lower.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()

        return text

    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX files using python-docx."""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        except Exception as e:
            raise ValueError(f"Error parsing DOCX file {file_path}: {str(e)}")

    def _parse_resume_text(self, text: str) -> Dict[str, Any]:
        """Parse raw resume text into structured JSON."""
        # Normalize text
        normalized_text = self._normalize_text(text)

        # Extract sections
        personal_info = self._extract_personal_info(normalized_text)
        experience = self._extract_experience(normalized_text)
        education = self._extract_education(normalized_text)
        skills = self._extract_skills(normalized_text)
        projects = self._extract_projects(normalized_text)
        certifications = self._extract_certifications(normalized_text)
        online_presence = self._extract_online_links(normalized_text)

        return {
            "personal_info": personal_info,
            "experience": experience,
            "education": education,
            "skills": skills,
            "projects": projects,
            "certifications": certifications,
            "online_presence": online_presence,
            "metadata": {
                "parsed_at": datetime.now(),
                "text_length": len(text),
                "confidence_score": self._calculate_confidence(
                    personal_info, experience, skills
                )
            }
        }

    def _normalize_text(self, text: str) -> str:
        """Normalize text for better parsing."""
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text.strip())

        # Fix common OCR issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

        return text

    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extract personal information."""
        info = {}

        # Extract email
        email_match = re.search(self.email_pattern, text)
        if email_match:
            info['email'] = email_match.group()

        # Extract phone
        phone_match = re.search(self.phone_pattern, text)
        if phone_match:
            info['phone'] = phone_match.group()

        # Extract name (first significant words before email/phone)
        lines = text.split('\n')[:5]  # Check first 5 lines
        potential_name = ""
        for line in lines:
            line = line.strip()
            if len(line.split()) <= 4 and not any(char in line for char in ['@', '(', '+']):
                potential_name = line
                break

        info['name'] = potential_name

        # Extract current title (look for common patterns)
        title_patterns = [
            r'(?:senior|junior|lead|principal)\s+(?:software\s+)?(?:engineer|developer|analyst)',
            r'(?:full.?stack|backend|frontend|data)\s+(?:developer|engineer)',
            r'(?:product|project|program)\s+manager'
        ]

        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['title'] = match.group()
                break

        # Extract location (city, state format)
        location_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s*([A-Z]{2})\b', text)
        if location_match:
            info['location'] = f"{location_match.group(1)}, {location_match.group(2)}"

        return info

    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience entries."""
        experiences = []

        # Split text into sections (basic section detection)
        sections = re.split(r'\n\s*(?=EXPERIENCE|EMPLOYMENT|WORK\s+HISTORY|PROFESSIONAL\s+EXPERIENCE)', text, re.IGNORECASE)
        if len(sections) > 1:
            exp_text = sections[1]
        else:
            exp_text = text

        # Find experience entries (basic pattern matching)
        exp_entries = re.split(r'\n\s*(?=\d{1,2}/\d{1,2}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b)', exp_text)

        for entry in exp_entries[:5]:  # Limit to top 5 experiences
            if len(entry.strip()) > 50:  # Minimum reasonable length
                parsed_exp = self._parse_experience_entry(entry)
                if parsed_exp:
                    experiences.append(parsed_exp)

        return experiences[:5]  # Return top 5 experiences

    def _parse_experience_entry(self, entry: str) -> Optional[Dict[str, Any]]:
        """Parse individual experience entry."""
        lines = [line.strip() for line in entry.strip().split('\n') if line.strip()]

        if len(lines) < 2:
            return None

        # Basic parsing (enhanced version would use NLP)
        title_company = lines[0].split(' at |, | - ')
        if len(title_company) >= 2:
            title = title_company[0].strip()
            company = title_company[1].strip()
        else:
            title = ""
            company = ""

        # Find dates in second line typically
        duration = ""
        for line in lines[:3]:
            date_match = re.search(r'(\d{1,2}/\d{1,2}(?:/\d{2,4})?)\s*-\s*(\d{1,2}/\d{1,2}(?:/\d{2,4})?|present|current)', line, re.IGNORECASE)
            if date_match:
                duration = date_match.group()
                break

        # Extract achievements/bullets
        achievements = []
        for line in lines:
            if line.startswith(('•', '-', '•', '➡️')) or re.match(r'^\d+\.\s|^[a-z]\)', line):
                achievements.append(line.strip())

        # Extract technologies mentioned
        tech_keywords = ['python', 'java', 'javascript', 'react', 'node', 'aws', 'docker', 'kubernetes', 'sql', 'git']
        technologies = []
        entry_lower = entry.lower()
        for tech in tech_keywords:
            if tech in entry_lower:
                technologies.append(tech.title())

        return {
            "title": title,
            "company": company,
            "duration": duration,
            "years": self._calculate_years_experience(duration),
            "achievements": achievements[:5],  # Top 5 achievements
            "technologies": list(set(technologies))  # Unique technologies
        }

    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information."""
        educations = []

        # Find education section
        edu_patterns = [
            r'EDUCATION',
            r'ACADEMIC\s+BACKGROUND',
            r'ACADEMIC\s+QUALIFICATIONS'
        ]

        edu_section = None
        for pattern in edu_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                edu_section = text[match.end():]
                break

        if not edu_section:
            return educations

        # Basic degree extraction (enhanced version would use better patterns)
        degree_patterns = [
            r'(?:Bachelor|Master|PhD|Doctorate|B\.S\.|M\.S\.|MBA|BBA)\s+(?:of\s+)?([\w\s]+)',
            r'(?:Computer Science|Engineering|Business|Mathematics|Econ.*)',
            r'Bachelor.?s?\s+(?:\w+\s)*',
            r'Master.?s?\s+(?:\w+\s)*'
        ]

        for pattern in degree_patterns:
            matches = re.finditer(pattern, edu_section, re.IGNORECASE)
            for match in matches:
                degree_full = match.group()
                educations.append({
                    "degree": degree_full.strip(),
                    "institution": "Institution parsing - Coming Soon",
                    "year": "Year parsing - Coming Soon"
                })
                break  # Take first match

        return educations[:3]  # Return top 3 educations

    def _extract_skills(self, text: str) -> Dict[str, Any]:
        """Extract and categorize skills."""
        text_lower = text.lower()

        # Extract technical skills by category
        technical_skills = []
        proficiency_levels = {}

        for category, skills in self.skill_categories.items():
            for skill in skills:
                if skill in text_lower:
                    technical_skills.append(skill.title())
                    proficiency_levels[skill.title()] = "intermediate"  # Basic classification

        # Simple soft skills extraction
        soft_skills_keywords = [
            'leadership', 'communication', 'problem solving', 'team player',
            'project management', 'analytical', 'creative', 'mentoring'
        ]

        soft_skills = []
        for skill in soft_skills_keywords:
            if skill in text_lower:
                soft_skills.append(skill.title())

        return {
            "technical": list(set(technical_skills)),  # Unique skills
            "soft": soft_skills,
            "proficiency_levels": proficiency_levels
        }

    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract project information."""
        projects = []

        # Basic project detection (would be enhanced with NLP)
        project_keywords = ['project', 'developed', 'built', 'created', 'contributed']
        project_sentences = []

        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in project_keywords):
                if len(sentence.strip()) > 20:
                    project_sentences.append(sentence.strip())

        # Convert to structured format (basic for now)
        for i, sentence in enumerate(project_sentences[:3]):  # Top 3 projects
            projects.append({
                "name": f"Project {i+1}",
                "description": sentence,
                "technologies": [],  # Would extract tech stack
                "impact": ""  # Would extract results/impact
            })

        return projects

    def _extract_certifications(self, text: str) -> List[Dict[str, str]]:
        """Extract certification information."""
        certifications = []

        # Basic certification detection
        cert_keywords = ['certified', 'certification', 'certificate', 'aws', 'microsoft', 'google', 'cfa']
        cert_sentences = []

        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in cert_keywords):
                cert_sentences.append(sentence.strip())

        for i, sentence in enumerate(cert_sentences[:3]):  # Top 3 certifications
            certifications.append({
                "name": sentence[:50] + "..." if len(sentence) > 50 else sentence,
                "issuer": "Issuer parsing - Coming Soon",
                "year": "Year parsing - Coming Soon"
            })

        return certifications

    def _extract_online_links(self, text: str) -> Dict[str, Any]:
        """Extract online presence links."""
        urls = re.findall(self.url_pattern, text)

        # Categorize URLs
        github_urls = [url for url in urls if 'github.com' in url]
        linkedin_urls = [url for url in urls if 'linkedin.com' in url]
        portfolio_urls = [url for url in urls if url not in github_urls + linkedin_urls]

        return {
            "github": github_urls[0] if github_urls else None,
            "linkedin": linkedin_urls[0] if linkedin_urls else None,
            "portfolio": portfolio_urls[0] if portfolio_urls else None,
            "other_links": portfolio_urls[1:] if len(portfolio_urls) > 1 else [],
            "verified": False  # Will be set by WebEnrichmentAgent
        }

    def _calculate_years_experience(self, duration: str) -> float:
        """Calculate years from duration string."""
        # Basic calculation (would be enhanced)
        if not duration or 'present' in duration.lower():
            return 0.0

        # Very basic year calculation
        try:
            if '-' in duration:
                parts = duration.split('-')
                if len(parts) == 2:
                    # Assume whole years for now
                    return min(5.0, abs(len(parts[0].strip()) - len(parts[1].strip())) / 10)
        except:
            pass

        return 0.0

    def _calculate_confidence(self, personal_info: dict, experience: list, skills: dict) -> float:
        """Calculate overall parsing confidence score."""
        score = 0.0

        # Personal info completeness
        if personal_info.get('name'):
            score += 0.2
        if personal_info.get('email'):
            score += 0.2
        if personal_info.get('title'):
            score += 0.1

        # Experience quality
        if experience and len(experience) > 0:
            score += 0.2

        # Skills presence
        if skills.get('technical') and len(skills['technical']) > 0:
            score += 0.2

        # Online presence
        if personal_info.get('github') or personal_info.get('linkedin'):
            score += 0.1

        return min(1.0, score)
