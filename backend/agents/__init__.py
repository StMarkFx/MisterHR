"""
MisterHR AI Agents Package

This package contains all LangChain-based AI agents for the MisterHR platform.
Each agent specializes in different aspects of resume optimization and candidate screening.
"""

from .resume_parser import ResumeParserAgent
from .web_enrichment import WebEnrichmentAgent
from .jd_analyzer import JDAnalyzerAgent
from .matching import MatchingAgent
from .content_generator import ContentGeneratorAgent
from .feedback import FeedbackAgent
from .verification import VerificationAgent
from .batch_processing import BatchProcessingAgent

__all__ = [
    "ResumeParserAgent",
    "WebEnrichmentAgent",
    "JDAnalyzerAgent",
    "MatchingAgent",
    "ContentGeneratorAgent",
    "FeedbackAgent",
    "VerificationAgent",
    "BatchProcessingAgent"
]

# Agent Role Definitions
AGENT_ROLES = {
    "resume_parser": "Extracts structured data from PDF/DOCX resumes",
    "web_enrichment": "Verifies online presence and portfolio validity",
    "jd_analyzer": "Parses job requirements and criteria extraction",
    "matching": "Calculates candidate-job fit scores",
    "content_generator": "Creates tailored resumes and cover letters",
    "feedback": "Provides optimization suggestions and gap analysis",
    "verification": "Validates skills and experience claims",
    "batch_processing": "Orchestrates multi-resume workflow coordination"
}
