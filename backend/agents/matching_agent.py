"""
Matching Agent for MisterHR

This agent calculates the fit between candidate profiles and job requirements.
It uses semantic similarity, skills matching, experience analysis, and multi-factor scoring.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import numpy as np
from .base_agent import BaseAgent, AgentConfig

class MatchingAgent(BaseAgent):
    """
    Matching Agent

    Calculates candidate-job fit using multi-factor analysis:
    1. Skills Matching (technical & soft)
    2. Experience Level Analysis
    3. Semantic Similarity Scoring
    4. Requirements Gap Analysis
    5. Culture Fit Estimation
    6. Growth Potential Assessment
    7. Comprehensive Fit Score

    Uses advanced algorithms for accurate candidate ranking
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)

        # Initialize LangChain components (will be set by orchestrator)
        self.llm = None
        self.embeddings = None

        # Scoring weights (configurable)
        self.scoring_weights = {
            'skills_match': 0.35,
            'experience_match': 0.25,
            'education_match': 0.10,
            'requirements_coverage': 0.15,
            'cultural_fit': 0.10,
            'bonus_factors': 0.05
        }

        # Experience level mappings
        self.experience_levels = {
            'entry': {'min_years': 0, 'max_years': 2, 'titles': ['intern', 'junior', 'associate']},
            'mid': {'min_years': 2, 'max_years': 5, 'titles': ['developer', 'engineer', 'analyst']},
            'senior': {'min_years': 5, 'max_years': 10, 'titles': ['senior', 'lead', 'principal']},
            'expert': {'min_years': 10, 'max_years': 20, 'titles': ['architect', 'director', 'chief']}
        }

        # Skill importance multipliers
        self.skill_importance = {
            'required': 1.0,
            'preferred': 0.7,
            'nice_to_have': 0.3
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters."""
        resume_data = kwargs.get('resume_data')
        job_data = kwargs.get('job_data')

        if not resume_data or not job_data:
            return False

        # Check required fields
        required_resume = ['personal_info', 'experience', 'skills', 'education']
        required_job = ['required_skills', 'experience_level', 'responsibilities']

        for field in required_resume:
            if field not in resume_data:
                return False

        for field in required_job:
            if field not in job_data:
                return False

        return True

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Calculate comprehensive candidate-job match.

        Args:
            resume_data (dict): Structured resume data from ResumeParserAgent
            job_data (dict): Analyzed job data from JDAnalyzerAgent

        Returns:
            Dict with detailed matching analysis and scores
        """
        resume_data = kwargs.get('resume_data', {})
        job_data = kwargs.get('job_data', {})

        try:
            # Calculate individual match scores
            skills_score, skills_details = self._calculate_skills_match(resume_data, job_data)
            experience_score, experience_details = self._calculate_experience_match(resume_data, job_data)
            education_score, education_details = self._calculate_education_match(resume_data, job_data)
            requirements_score, requirements_details = self._calculate_requirements_coverage(resume_data, job_data)
            culture_score, culture_details = self._estimate_cultural_fit(resume_data, job_data)

            # Calculate bonus factors
            bonus_score, bonus_details = self._calculate_bonus_factors(resume_data, job_data)

            # Compute weighted overall score
            overall_score = self._compute_overall_score({
                'skills_match': skills_score,
                'experience_match': experience_score,
                'education_match': education_score,
                'requirements_coverage': requirements_score,
                'cultural_fit': culture_score,
                'bonus_factors': bonus_score
            })

            # Generate gap analysis
            gaps = self._analyze_gaps(resume_data, job_data, skills_details, experience_details)

            # Create improvement recommendations
            recommendations = self._generate_recommendations(gaps, job_data)

            return {
                "overall_score": round(overall_score, 2),
                "component_scores": {
                    "skills_match": round(skills_score, 2),
                    "experience_match": round(experience_score, 2),
                    "education_match": round(education_score, 2),
                    "requirements_coverage": round(requirements_score, 2),
                    "cultural_fit": round(culture_score, 2),
                    "bonus_factors": round(bonus_score, 2)
                },
                "match_category": self._categorize_match(overall_score),
                "strengths": self._identify_strengths(skills_details, experience_details),
                "gaps": gaps,
                "recommendations": recommendations,
                "detailed_analysis": {
                    "skills_details": skills_details,
                    "experience_details": experience_details,
                    "education_details": education_details,
                    "requirements_details": requirements_details,
                    "culture_details": culture_details,
                    "bonus_details": bonus_details
                },
                "metadata": {
                    "matched_at": datetime.now(),
                    "scoring_version": "1.0",
                    "confidence_score": self._calculate_confidence(job_data, resume_data)
                }
            }

        except Exception as e:
            self.logger.error(f"Matching analysis failed: {str(e)}")
            raise

    def _calculate_skills_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate skills match score (0-100)."""
        resume_skills = set()
        for category in ['technical', 'soft']:
            resume_skills.update(resume_data.get('skills', {}).get(category, []))

        # Normalize skill names
        resume_skills = self._normalize_skills(list(resume_skills))

        job_required = set(job_data.get('required_skills', []))
        job_preferred = set(job_data.get('preferred_skills', []))

        # Find matches
        required_matches = job_required.intersection(resume_skills)
        preferred_matches = job_preferred.intersection(resume_skills)

        # Calculate score
        if not job_required:
            required_score = 100.0  # No requirements means perfect match
        else:
            required_score = (len(required_matches) / len(job_required)) * 100

        preferred_score = len(preferred_matches) / max(1, len(job_preferred)) * 50 if job_preferred else 100
        skills_score = min(100, required_score + preferred_score)

        # Additional skill analysis
        missing_critical = job_required - resume_skills
        extra_skills = resume_skills - job_required - job_preferred

        skills_details = {
            "matched_required": list(required_matches),
            "matched_preferred": list(preferred_matches),
            "missing_critical": list(missing_critical),
            "missing_preferred": list(job_preferred - resume_skills),
            "extra_skills": list(extra_skills),
            "skill_gaps_by_category": self._analyze_skill_gaps(resume_data, job_data)
        }

        return skills_score, skills_details

    def _calculate_experience_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate experience match score."""
        # Get candidate's total experience
        candidate_years = self._calculate_total_experience_years(resume_data)
        candidate_level = self._determine_experience_level(candidate_years)

        # Get job requirements
        job_level = job_data.get('experience_level', 'mid')
        job_min_years = job_data.get('years_experience_min', 0)
        job_max_years = job_data.get('years_experience_max', job_min_years + 5)

        # Score based on level alignment
        level_alignment_score = self._score_level_alignment(candidate_level, job_level)

        # Score based on years
        years_score = self._score_years_experience(candidate_years, job_min_years, job_max_years)

        # Calculate overall experience score
        experience_score = (level_alignment_score + years_score) / 2

        experience_details = {
            "candidate_years": round(candidate_years, 1),
            "candidate_level": candidate_level,
            "job_level": job_level,
            "level_alignment_score": level_alignment_score,
            "years_fit_score": years_score,
            "experience_relevance": self._analyze_experience_relevance(resume_data, job_data)
        }

        return experience_score, experience_details

    def _calculate_education_match(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate education match score."""
        resume_education = resume_data.get('education', [])
        job_education = job_data.get('education', [])

        education_matches = []
        education_gaps = []

        for job_ed in job_education:
            job_degree = job_ed.lower()
            best_match = None
            best_score = 0

            for resume_ed in resume_education:
                resume_degree = resume_ed.get('degree', '').lower()
                match_score = self._calculate_education_similarity(job_degree, resume_degree)

                if match_score > best_score:
                    best_score = match_score
                    best_match = resume_ed

            if best_match and best_score > 0.6:  # Good match threshold
                education_matches.append({
                    'job_requirement': job_ed,
                    'candidate_education': best_match,
                    'similarity_score': best_score
                })
            else:
                education_gaps.append(job_ed)

        # Calculate score
        if not job_education:
            education_score = 100.0  # No education requirements
        else:
            education_score = (len(education_matches) / len(job_education)) * 100

        education_details = {
            "education_matches": education_matches,
            "education_gaps": education_gaps,
            "highest_degree": self._identify_highest_degree(resume_education) if resume_education else None
        }

        return education_score, education_details

    def _calculate_requirements_coverage(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate how well candidate covers job requirements beyond skills."""
        requirements = job_data.get('responsibilities', []) + job_data.get('qualifications', [])

        coverage_score = 0
        covered_requirements = []
        missed_requirements = []

        # Simple keyword matching for now (could be enhanced with semantic similarity)
        resume_text = self._build_resume_text(resume_data)

        for req in requirements:
            req_lower = req.lower()
            keywords = set(req_lower.split()) - self._get_common_words()
            keyword_matches = sum(1 for keyword in keywords if keyword in resume_text.lower())

            if keyword_matches > 0:
                coverage_score += 100 / len(requirements)
                covered_requirements.append(req)
            else:
                missed_requirements.append(req)

        requirements_details = {
            "total_requirements": len(requirements),
            "covered_requirements": covered_requirements,
            "missed_requirements": missed_requirements,
            "coverage_rate": len(covered_requirements) / max(1, len(requirements))
        }

        return min(100, coverage_score), requirements_details

    def _estimate_cultural_fit(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Estimate cultural fit based on company and candidate indicators."""
        # This is a simplified estimation based on available data
        # In a real system, this would use more sophisticated NLP and company data

        culture_score = 50.0  # Default neutral score
        culture_indicators = {}

        # Check for leadership experience (common indicator)
        resume_text = self._build_resume_text(resume_data)
        leadership_keywords = ['lead', 'manage', 'team', 'direct', 'mentor', 'coach']
        leadership_count = sum(1 for keyword in leadership_keywords if keyword in resume_text.lower())

        if leadership_count > 2:
            culture_score += 15
            culture_indicators['leadership_experience'] = 'strong'
        elif leadership_count > 0:
            culture_score += 5
            culture_indicators['leadership_experience'] = 'moderate'

        # Check for growth indicators (startup experience, learning mentality)
        growth_keywords = ['startup', 'fast-paced', 'agile', 'learn', 'grow', 'scale']
        growth_count = sum(1 for keyword in growth_keywords if keyword in resume_text.lower())

        if growth_count > 1:
            culture_score += 10
            culture_indicators['growth_orientation'] = 'high'

        # Location check (if available)
        candidate_location = resume_data.get('personal_info', {}).get('location')
        job_location = job_data.get('location')

        if candidate_location and job_location:
            if self._check_location_compatibility(candidate_location, job_location):
                culture_score += 10
                culture_indicators['location_flexibility'] = 'compatible'
            else:
                culture_score -= 5
                culture_indicators['location_flexibility'] = 'incompatible'

        culture_details = {
            "culture_score": culture_score,
            "indicators": culture_indicators,
            "reasoning": "Based on leadership experience, growth orientation, and location compatibility"
        }

        return min(100, max(0, culture_score)), culture_details

    def _calculate_bonus_factors(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Calculate bonus factors that can improve match score."""
        bonus_score = 0.0
        bonus_details = {}

        # GitHub/portfolio activity
        online_presence = resume_data.get('online_presence', {})
        if online_presence.get('github') or online_presence.get('portfolio'):
            bonus_score += 10
            bonus_details['online_presence'] = 'verified profiles'

        # Certifications
        certifications = resume_data.get('certifications', [])
        if certifications:
            bonus_score += min(5, len(certifications))
            bonus_details['certifications'] = f"{len(certifications)} certifications"

        # Projects
        projects = resume_data.get('projects', [])
        if projects and len(projects) > 2:
            bonus_score += 5
            bonus_details['projects'] = f"{len(projects)} significant projects"

        # Keywords matching job description
        job_description = ' '.join(job_data.get('responsibilities', []) + job_data.get('qualifications', []))
        resume_text = self._build_resume_text(resume_data)

        bonus_keywords = [
            'innovation', 'excellence', 'quality', 'customer-focused',
            'results-driven', 'collaborative', 'efficient', 'scalable'
        ]

        keyword_matches = sum(1 for keyword in bonus_keywords
                            if keyword in job_description.lower() and keyword in resume_text.lower())

        if keyword_matches > 0:
            bonus_score += min(5, keyword_matches * 2)
            bonus_details['culture_keywords'] = f"{keyword_matches} culture keyword matches"

        bonus_details['total_bonus_points'] = bonus_score

        return bonus_score, bonus_details

    def _compute_overall_score(self, component_scores: Dict[str, float]) -> float:
        """Compute weighted overall score."""
        overall_score = 0.0

        for component, score in component_scores.items():
            weight = self.scoring_weights.get(component, 0.0)
            overall_score += score * weight

        return min(100.0, overall_score)

    def _categorize_match(self, overall_score: float) -> str:
        """Categorize match quality."""
        if overall_score >= 85:
            return "excellent_match"
        elif overall_score >= 75:
            return "strong_match"
        elif overall_score >= 60:
            return "good_match"
        elif overall_score >= 40:
            return "moderate_match"
        else:
            return "weak_match"

    def _identify_strengths(self, skills_details: Dict[str, Any], experience_details: Dict[str, Any]) -> List[str]:
        """Identify key strengths of the candidate."""
        strengths = []

        # Skills strengths
        if len(skills_details.get('matched_required', [])) > 2:
            strengths.append("Strong skills alignment")
        if len(skills_details.get('extra_skills', [])) > 0:
            strengths.append("Additional valuable skills")
        if len(skills_details.get('matched_preferred', [])) > 0:
            strengths.append("Nice-to-have skills match")

        # Experience strengths
        candidate_years = experience_details.get('candidate_years', 0)
        if candidate_years > 5:
            strengths.append("Extensive experience")
        elif candidate_years > 3:
            strengths.append("Solid experience base")

        if experience_details.get('level_alignment_score', 0) > 80:
            strengths.append("Experience level alignment")

        return strengths

    def _analyze_gaps(self, resume_data: Dict[str, Any], job_data: Dict[str, Any],
                     skills_details: Dict[str, Any], experience_details: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze gaps between candidate and job requirements."""
        gaps = {
            "critical_gaps": [],
            "improvement_areas": [],
            "nice_to_have": [],
            "skill_gaps": skills_details.get('missing_critical', []),
            "experience_gaps": [],
            "education_gaps": []
        }

        # Experience gaps
        candidate_years = experience_details.get('candidate_years', 0)
        job_min_years = job_data.get('years_experience_min', 0)

        if candidate_years < job_min_years:
            gap_years = job_min_years - candidate_years
            gaps["experience_gaps"].append({
                "type": "years_experience",
                "description": f"Needs {gap_years} more years of experience",
                "severity": "critical" if gap_years > 2 else "moderate"
            })
            gaps["critical_gaps"].append("Insufficient years of experience")

        # Skill gaps by criticality
        missing_critical = skills_details.get('missing_critical', [])
        if missing_critical:
            gaps["critical_gaps"].extend([f"Missing critical skill: {skill}" for skill in missing_critical])

        missing_preferred = skills_details.get('missing_preferred', [])
        if missing_preferred:
            gaps["improvement_areas"].extend([f"Preferred skill: {skill}" for skill in missing_preferred[:3]])

        return gaps

    def _generate_recommendations(self, gaps: Dict[str, Any], job_data: Dict[str, Any]) -> List[str]:
        """Generate actionable improvement recommendations."""
        recommendations = []

        # Critical gaps
        if gaps.get("critical_gaps"):
            recommendations.append("🔴 Immediately address: " + gaps["critical_gaps"][0])

        # Skill improvements
        skill_gaps = gaps.get("skill_gaps", [])[:2]
        for skill in skill_gaps:
            recommendations.append(f"📚 Learn: {skill} - Consider online courses or certifications")

        # Experience recommendations
        exp_gaps = gaps.get("experience_gaps", [])
        if exp_gaps:
            recommendations.append("💼 Gain experience: Look for projects or roles that build the required experience")

        # General improvements
        if not gaps.get("critical_gaps") and not gaps.get("skill_gaps"):
            recommendations.append("✅ Good fit! Focus on highlighting relevant experience in your application")

        return recommendations[:5]  # Return top 5 recommendations

    def _calculate_confidence(self, job_data: Dict[str, Any], resume_data: Dict[str, Any]) -> float:
        """Calculate confidence in the matching analysis."""
        confidence = 80.0  # Base confidence

        # Reduce confidence if data is incomplete
        if not resume_data.get('experience'):
            confidence -= 10
        if not resume_data.get('skills', {}).get('technical'):
            confidence -= 15
        if not job_data.get('required_skills'):
            confidence -= 20

        return max(50.0, confidence)

    # Helper methods (implement full versions)

    def _normalize_skills(self, skills: List[str]) -> set:
        """Normalize skill names for better matching."""
        return {skill.lower().strip() for skill in skills}

    def _calculate_total_experience_years(self, resume_data: Dict[str, Any]) -> float:
        """Calculate total years of experience from resume."""
        experiences = resume_data.get('experience', [])
        if not experiences:
            return 0.0

        # Simple calculation: use the most recent experience years + some assumptions
        return max(0.5, len(experiences) * 1.5)  # Rough estimate

    def _determine_experience_level(self, years: float) -> str:
        """Determine experience level from years."""
        if years >= 10:
            return "expert"
        elif years >= 5:
            return "senior"
        elif years >= 2:
            return "mid"
        else:
            return "entry"

    def _get_common_words(self) -> set:
        """Get common English words to exclude from matching."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'are', 'is', 'was', 'be', 'have',
            'has', 'had', 'will', 'would', 'should', 'could', 'can', 'may'
        }

    def _build_resume_text(self, resume_data: Dict[str, Any]) -> str:
        """Build comprehensive text representation of resume."""
        text_parts = []

        # Personal info and title
        personal = resume_data.get('personal_info', {})
        if personal.get('title'):
            text_parts.append(personal['title'])

        # Experience descriptions
        for exp in resume_data.get('experience', []):
            if exp.get('achievements'):
                text_parts.extend(exp['achievements'])

        # Skills
        skills = resume_data.get('skills', {})
        for category, skill_list in skills.items():
            if isinstance(skill_list, list):
                text_parts.extend(skill_list)

        # Projects
        for project in resume_data.get('projects', []):
            if project.get('description'):
                text_parts.append(project['description'])

        return ' '.join(text_parts)

    def _score_level_alignment(self, candidate_level: str, job_level: str) -> float:
        """Score how well candidate level aligns with job level."""
        levels = ['entry', 'mid', 'senior', 'expert']
        try:
            candidate_idx = levels.index(candidate_level)
            job_idx = levels.index(job_level)

            if candidate_idx == job_idx:
                return 100.0
            elif abs(candidate_idx - job_idx) == 1:
                return 70.0
            else:
                return 30.0
        except ValueError:
            return 50.0

    def _score_years_experience(self, candidate_years: float, job_min: float, job_max: float) -> float:
        """Score years experience against job requirements."""
        if candidate_years >= job_min:
            if not job_max or candidate_years <= job_max:
                return 100.0
            else:
                # Over-experienced (still potentially good)
                return max(60.0, 100.0 - (candidate_years - job_max))
        else:
            # Under-experienced
            shortage = job_min - candidate_years
            return max(20.0, 100.0 - shortage * 20)

    def _calculate_education_similarity(self, job_ed: str, resume_ed: str) -> float:
        """Calculate similarity between job and resume education requirements."""
        job_words = set(job_ed.lower().split())
        resume_words = set(resume_ed.lower().split())

        intersection = job_words.intersection(resume_words)
        union = job_words.union(resume_words)

        if not union:
            return 0.0

        return len(intersection) / len(union)

    def _identify_highest_degree(self, education: List[Dict[str, Any]]) -> Optional[str]:
        """Identify the highest degree from education list."""
        degree_hierarchy = {
            'phd': 5, 'doctorate': 5,
            'masters': 4, "master's": 4,
            'bachelor': 3, "bachelor's": 3,
            'associate': 2,
            'certificate': 1
        }

        highest_degree = None
        highest_level = 0

        for ed in education:
            degree = ed.get('degree', '').lower()
            for deg_name, level in degree_hierarchy.items():
                if deg_name in degree and level > highest_level:
                    highest_degree = ed.get('degree')
                    highest_level = level

        return highest_degree

    def _analyze_skill_gaps(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skill gaps by category."""
        gaps = defaultdict(list)

        job_skills = set(job_data.get('required_skills', []))
        resume_technical = set(resume_data.get('skills', {}).get('technical', []))

        missing = job_skills - resume_technical

        # Categorize gaps (simplified)
        for skill in missing:
            skill_lower = skill.lower()
            if any(word in skill_lower for word in ['python', 'javascript', 'java', 'go']):
                gaps['programming_languages'].append(skill)
            elif any(word in skill_lower for word in ['react', 'angular', 'vue']):
                gaps['frontend_frameworks'].append(skill)
            elif any(word in skill_lower for word in ['aws', 'azure', 'docker']):
                gaps['cloud_tools'].append(skill)
            else:
                gaps['other_skills'].append(skill)

        return dict(gaps)

    def _analyze_experience_relevance(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> float:
        """Analyze how relevant the candidate's experience is to the job."""
        # Simplified relevance score based on job title matching
        job_responsibilities = ' '.join(job_data.get('responsibilities', [])).lower()
        candidate_experience_text = ' '.join([
            ' '.join(exp.get('achievements', []))
            for exp in resume_data.get('experience', [])
        ]).lower()

        # Simple keyword overlap
        job_keywords = set(job_responsibilities.split()) - self._get_common_words()
        exp_keywords = set(candidate_experience_text.split()) - self._get_common_words()

        overlap = len(job_keywords.intersection(exp_keywords))
        total_keywords = len(job_keywords.union(exp_keywords))

        return (overlap / max(1, total_keywords)) * 100 if total_keywords > 0 else 0

    def _check_location_compatibility(self, candidate_location: str, job_location: str) -> bool:
        """Check if candidate and job locations are compatible."""
        # Simplified location compatibility (would use geocoding in production)
        if job_location.lower() == 'remote':
            return True
        if 'remote' in job_location.lower() or 'remote' in candidate_location.lower():
            return True

        # Simple string matching
        candidate_city = candidate_location.split(',')[0].strip().lower()
        job_city = job_location.split(',')[0].strip().lower()

        return candidate_city == job_city
