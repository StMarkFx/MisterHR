"""
MisterHR Test Configuration

Shared fixtures and configuration for all tests.
"""

import pytest
from pathlib import Path
from typing import Dict, Any
import os

# Test fixtures directory
TEST_DATA_DIR = Path(__file__).parent / "fixtures"

def pytest_configure(config):
    """Add custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")

@pytest.fixture
def test_resume_data() -> Dict[str, Any]:
    """Sample resume data for testing."""
    return {
        "personal_info": {
            "name": "John Developer",
            "email": "john@example.com",
            "phone": "+1-555-0123",
            "title": "Senior Software Engineer",
            "location": "San Francisco, CA"
        },
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "duration": "2021-2023",
                "years": 2,
                "achievements": ["Led team of 5 developers", "Reduced deployment time by 60%"],
                "technologies": ["Python", "React", "Docker"]
            }
        ],
        "education": [
            {
                "degree": "Master of Computer Science",
                "institution": "Stanford University",
                "year": 2020,
                "grade": "3.8 GPA"
            }
        ],
        "skills": {
            "technical": ["Python", "React", "Node.js", "PostgreSQL"],
            "soft": ["Leadership", "Communication", "Problem Solving"],
            "proficiency_levels": {
                "Python": "expert",
                "React": "advanced",
                "PostgreSQL": "intermediate"
            }
        },
        "projects": [
            {
                "name": "Cloud Migration Initiative",
                "description": "Led migration from on-premises to cloud infrastructure",
                "technologies": ["AWS", "Terraform", "Docker"],
                "impact": "60% cost reduction, improved scalability"
            }
        ],
        "certifications": [
            {
                "name": "AWS Certified Solutions Architect",
                "issuer": "Amazon Web Services",
                "year": 2022
            }
        ],
        "online_presence": {
            "github": "https://github.com/johndeveloper",
            "linkedin": "https://linkedin.com/in/johndeveloper",
            "portfolio": "https://johndeveloper.dev",
            "verified": False
        }
    }

@pytest.fixture
def test_job_data() -> Dict[str, Any]:
    """Sample job data for testing."""
    return {
        "job_title": "Senior Python Developer",
        "company_name": "Innovative Solutions Inc.",
        "location": "Remote",
        "salary_range": "$120,000 - $150,000",
        "required_skills": ["Python", "Django", "PostgreSQL", "AWS", "Docker"],
        "preferred_skills": ["React", "Kubernetes", "CI/CD", "TypeScript"],
        "responsibilities": [
            "Design and develop scalable web applications using Python and Django",
            "Optimize database performance and implement caching strategies",
            "Collaborate with cross-functional teams to deliver high-quality software",
            "Mentor junior developers and conduct code reviews",
            "Implement DevOps practices including CI/CD pipelines"
        ],
        "experience_level": "senior",
        "years_experience_min": 5,
        "years_experience_max": 8,
        "benefits": ["Health Insurance", "401(k) matching", "Remote work", "Professional development"],
        "keywords": ["python", "django", "postgresql", "aws", "docker", "kubernetes", "ci/cd"]
    }

@pytest.fixture
def sample_pdf_path():
    """Path to sample PDF resume."""
    return Path(__file__).parent.parent / "StMark_Adebayo_CV.pdf"

@pytest.fixture
def test_agent_config():
    """Basic agent configuration for testing."""
    from base_agent import AgentConfig
    return AgentConfig(
        name="TestAgent",
        model="gpt-4-turbo-preview",
        temperature=0.3,
        max_tokens=2048,
        timeout=30
    )
