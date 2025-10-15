"""
Content Generator Agent for MisterHR

This agent generates tailored resumes, cover letters, and application content
based on job requirements and candidate profiles using LLM-powered writing.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from string import Template
from .base_agent import BaseAgent, AgentConfig

class ContentGeneratorAgent(BaseAgent):
    """
    Content Generator Agent

    Creates personalized application content:
    1. Tailored Resume Generation
    2. Cover Letter Creation
    3. Skills Highlight Customization
    4. Achievement Optimization
    5. Keyword Integration
    6. Tone & Style Adaptation
    7. Content A/B Testing

    Uses advanced LLM prompts for compelling content creation
    """

    def __init__(self, config: AgentConfig):
        super().__init__(config)

        # Initialize LangChain components
        self.llm = None

        # Content generation templates
        self.resume_sections = {
            'summary': 'professional_summary',
            'experience': 'work_experience',
            'skills': 'technical_skills',
            'education': 'education',
            'projects': 'personal_projects',
            'certifications': 'certifications'
        }

        # Tone and style configurations
        self.tone_profiles = {
            'professional': {
                'formality': 'high',
                'enthusiasm': 'moderate',
                'keywords': ['achieved', 'implemented', 'developed', 'managed']
            },
            'confident': {
                'formality': 'high',
                'enthusiasm': 'high',
                'keywords': ['successfully', 'expertly', 'proficiently', 'masterfully']
            },
            'technical': {
                'formality': 'high',
                'enthusiasm': 'low',
                'keywords': ['optimized', 'architected', 'engineered', 'scaled']
            }
        }

    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters."""
        resume_data = kwargs.get('resume_data')
        job_data = kwargs.get('job_data')
        content_type = kwargs.get('content_type', 'resume')

        if not resume_data or not job_data:
            return False

        if content_type not in ['resume', 'cover_letter', 'both']:
            return False

        return True

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Generate tailored content for job application.

        Args:
            resume_data (dict): Structured resume data
            job_data (dict): Analyzed job requirements
            content_type (str): 'resume', 'cover_letter', or 'both'
            tone (str): Writing tone preference

        Returns:
            Dict with generated content and metadata
        """
        resume_data = kwargs.get('resume_data', {})
        job_data = kwargs.get('job_data', {})
        content_type = kwargs.get('content_type', 'both')
        tone = kwargs.get('tone', 'professional')

        try:
            results = {
                'generated_at': datetime.now(),
                'job_title': job_data.get('job_title', 'Position'),
                'content_type': content_type,
                'tone': tone,
                'content': {},
                'keyword_optimization': {},
                'metadata': {}
            }

            # Generate requested content types
            if content_type in ['resume', 'both']:
                resume_content, resume_keywords = await self._generate_tailored_resume(
                    resume_data, job_data, tone
                )
                results['content']['resume'] = resume_content
                results['keyword_optimization']['resume'] = resume_keywords

            if content_type in ['cover_letter', 'both']:
                cover_letter_content, cover_keywords = await self._generate_cover_letter(
                    resume_data, job_data, tone
                )
                results['content']['cover_letter'] = cover_letter_content
                results['keyword_optimization']['cover_letter'] = cover_keywords

            # Calculate content effectiveness score
            results['metadata'] = {
                'content_score': self._evaluate_content_quality(results),
                'keyword_density': self._calculate_keyword_density(results),
                'ats_compatibility': self._assess_ats_compatibility(results)
            }

            return results

        except Exception as e:
            self.logger.error(f"Content generation failed: {str(e)}")
            raise

    async def _generate_tailored_resume(self, resume_data: Dict[str, Any],
                                       job_data: Dict[str, Any], tone: str) -> tuple:
        """Generate a tailored resume for the specific job."""
        if self.llm:
            return await self._generate_resume_with_llm(resume_data, job_data, tone)
        else:
            return self._generate_resume_with_templates(resume_data, job_data, tone)

    async def _generate_resume_with_llm(self, resume_data: Dict[str, Any],
                                       job_data: Dict[str, Any], tone: str) -> tuple:
        """Use LLM to generate tailored resume content."""
        job_keywords = self._extract_job_keywords(job_data)
        candidate_strengths = self._identify_candidate_strengths(resume_data, job_data)

        prompt = f"""
        Generate a tailored resume for this job application. Focus on highlighting the most relevant experience and skills that match the job requirements.

        JOB POSITION: {job_data.get('job_title', 'Software Engineer')}
        COMPANY: {job_data.get('company_name', 'Company')}
        KEY REQUIREMENTS: {', '.join(job_data.get('required_skills', []))}
        EXPERIENCE LEVEL: {job_data.get('experience_level', 'mid')}

        CANDIDATE INFORMATION:
        Name: {resume_data.get('personal_info', {}).get('name', 'Candidate')}
        Current Title: {resume_data.get('personal_info', {}).get('title', 'Professional')}
        Experience: {len(resume_data.get('experience', []))} positions
        Key Skills: {', '.join(resume_data.get('skills', {}).get('technical', []))}

        INSTRUCTIONS:
        1. Create a professional summary (2-3 sentences) that directly addresses the job requirements
        2. Prioritize and rephrase experience bullet points to emphasize relevant achievements
        3. Strategically place the most relevant skills and experiences near the top
        4. Incorporate {len(job_keywords)} key terms from the job description: {', '.join(job_keywords[:8])}
        5. Use {tone} tone throughout
        6. Ensure ATS compatibility (no graphics, standard sections)
        7. Keep the resume to 1-2 pages worth of content

        Return the tailored resume content in clean text format with standard sections: Summary, Experience, Skills, Education.
        """

        try:
            response = await self.llm.ainvoke(prompt)

            # Extract keywords that were incorporated
            content = response.content
            incorporated_keywords = self._analyze_keyword_usage(content, job_keywords)

            return content, incorporated_keywords

        except Exception as e:
            self.logger.warning(f"LLM resume generation failed: {str(e)}, falling back to templates")
            return self._generate_resume_with_templates(resume_data, job_data, tone)

    def _generate_resume_with_templates(self, resume_data: Dict[str, Any],
                                       job_data: Dict[str, Any], tone: str) -> tuple:
        """Generate resume using template-based approach."""

        # Create tailored professional summary
        summary = self._generate_professional_summary(resume_data, job_data, tone)

        # Tailor experience section
        tailored_experience = self._tailor_experience_section(resume_data, job_data)

        # Optimize skills section
        optimized_skills = self._optimize_skills_section(resume_data, job_data)

        # Keep education relatively unchanged
        education = resume_data.get('education', [])

        # Combine into resume content
        resume_content = f"""
PROFESSIONAL SUMMARY
{summary}

PROFESSIONAL EXPERIENCE
{self._format_experience(tailored_experience)}

TECHNICAL SKILLS
{self._format_skills(optimized_skills)}

EDUCATION
{self._format_education(education)}
        """.strip()

        # Analyze keyword usage
        job_keywords = self._extract_job_keywords(job_data)
        keyword_usage = self._analyze_keyword_usage(resume_content, job_keywords)

        return resume_content, keyword_usage

    async def _generate_cover_letter(self, resume_data: Dict[str, Any],
                                    job_data: Dict[str, Any], tone: str) -> tuple:
        """Generate a tailored cover letter."""
        if self.llm:
            return await self._generate_cover_letter_with_llm(resume_data, job_data, tone)
        else:
            return self._generate_cover_letter_with_template(resume_data, job_data, tone)

    async def _generate_cover_letter_with_llm(self, resume_data: Dict[str, Any],
                                             job_data: Dict[str, Any], tone: str) -> tuple:
        """Use LLM to generate personalized cover letter."""

        prompt = f"""
        Write a compelling cover letter for this job application. Make it personal, specific, and demonstrate genuine interest in both the role and company.

        JOB DETAILS:
        Position: {job_data.get('job_title', 'Software Engineer')}
        Company: {job_data.get('company_name', 'the company')}
        Key Requirements: {', '.join(job_data.get('required_skills', [])[:5])}
        Responsibilities: {', '.join(job_data.get('responsibilities', [])[:3])}

        CANDIDATE PROFILE:
        Name: {resume_data.get('personal_info', {}).get('name', 'Alex Johnson')}
        Current Role: {resume_data.get('personal_info', {}).get('title', 'Software Developer')}
        Years Experience: ~{len(resume_data.get('experience', [])) * 2} years
        Key Achievement: {resume_data.get('experience', [{}])[0].get('achievements', [''])[0] if resume_data.get('experience') else 'Led multiple successful projects'}

        REQUIREMENTS FOR COVER LETTER:
        1. Address the hiring manager by name if possible (use "Hiring Manager" if not known)
        2. Start with a strong hook that shows enthusiasm for the specific role
        3. Connect your experience directly to 2-3 key job requirements
        4. Include a specific example of relevant work or achievement
        5. Explain why you're interested in this company specifically
        6. End with a clear call-to-action and professional sign-off
        7. Keep it to 3-4 paragraphs (300-400 words)
        8. Use {tone} tone that's authentic and engaging

        Make it sound natural, not like a template. Reference specific job requirements and show you've done your homework.
        """

        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content

            # Extract incorporated job keywords
            job_keywords = self._extract_job_keywords(job_data)
            keyword_usage = self._analyze_keyword_usage(content, job_keywords)

            return content, keyword_usage

        except Exception as e:
            self.logger.warning(f"LLM cover letter generation failed: {str(e)}, using template")
            return self._generate_cover_letter_with_template(resume_data, job_data, tone)

    def _generate_cover_letter_with_template(self, resume_data: Dict[str, Any],
                                           job_data: Dict[str, Any], tone: str) -> tuple:
        """Generate cover letter using structured template."""

        candidate_name = resume_data.get('personal_info', {}).get('name', 'Alex Johnson')
        job_title = job_data.get('job_title', 'Software Engineer')
        company_name = job_data.get('company_name', 'the company')
        key_skills = job_data.get('required_skills', [])[:3]

        # Relevance score determines enthusiasm level
        relevance_score = self._calculate_relevance_score(resume_data, job_data)

        cover_letter = f"""[Your Name]
[Your Address]
[City, State ZIP Code]
[Email Address]
[Phone Number]
[Date]

[Hiring Manager]
{company_name}
[Company Address]
[City, State ZIP Code]

Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company_name}, as advertised. With my background in {', '.join(key_skills)}, I am confident I can make significant contributions to your team's objectives.

In my current role as {resume_data.get('personal_info', {}).get('title', 'Software Developer')}, I have successfully {' and '.join(resume_data.get('experience', [{}])[0].get('achievements', ['delivered multiple projects'])[:2])}. This experience directly aligns with {company_name}'s needs for {' and '.join(job_data.get('responsibilities', ['technical excellence'])[:2] [:2])}.

What particularly draws me to {company_name} is {'your innovative approach to technology' if relevance_score > 70 else 'the opportunity to work on challenging projects'}. I am eager to bring my expertise in {', '.join(resume_data.get('skills', {}).get('technical', [])[:3])} to contribute to {'your mission' if company_name else 'the team\'s success'}.

I would welcome the opportunity to discuss how my background and skills can benefit {company_name}. Thank you for considering my application. I look forward to the possibility of contributing to your team.

Sincerely,
{candidate_name}
        """

        job_keywords = self._extract_job_keywords(job_data)
        keyword_usage = self._analyze_keyword_usage(cover_letter, job_keywords)

        return cover_letter, keyword_usage

    def _generate_professional_summary(self, resume_data: Dict[str, Any],
                                     job_data: Dict[str, Any], tone: str) -> str:
        """Generate a tailored professional summary."""
        candidate_title = resume_data.get('personal_info', {}).get('title', 'Software Developer')
        years_exp = len(resume_data.get('experience', [])) * 2  # Rough estimate
        key_skills = resume_data.get('skills', {}).get('technical', [])[:4]

        job_requirements = job_data.get('required_skills', [])[:3]
        job_level = job_data.get('experience_level', 'mid')

        summary = f"Experienced {candidate_title} with {years_exp}+ years of expertise in {', '.join(key_skills)}. "

        # Add job-specific content
        if job_requirements:
            summary += f"Specialized in {', '.join(job_requirements)} with proven track record of delivering "
            summary += "high-impact solutions in fast-paced environments. " if job_level in ['senior', 'lead'] else "quality software solutions. "

        summary += f"Passionate about leveraging {key_skills[0]} to drive innovation and deliver exceptional results."

        return summary

    def _tailor_experience_section(self, resume_data: Dict[str, Any],
                                  job_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Reorder and emphasize experience most relevant to the job."""
        experiences = resume_data.get('experience', [])
        job_keywords = set(self._extract_job_keywords(job_data))

        # Score each experience entry
        scored_experiences = []
        for exp in experiences:
            score = self._score_experience_relevance(exp, job_keywords)
            scored_experiences.append((score, exp))

        # Sort by relevance score (highest first)
        scored_experiences.sort(key=lambda x: x[0], reverse=True)

        # Return experiences, but add emphasized achievements
        tailored_experiences = []
        for score, exp in scored_experiences:
            tailored_exp = exp.copy()

            # Emphasize relevant achievements
            achievements = exp.get('achievements', [])
            if achievements:
                # Prioritize achievements that match job keywords
                prioritized_achievements = []
                for achievement in achievements:
                    if any(keyword.lower() in achievement.lower() for keyword in job_keywords):
                        prioritized_achievements.insert(0, achievement)  # Put relevant first
                    else:
                        prioritized_achievements.append(achievement)

                tailored_exp['achievements'] = prioritized_achievements[:4]  # Top 4

            tailored_experiences.append(tailored_exp)

        return tailored_experiences

    def _optimize_skills_section(self, resume_data: Dict[str, Any],
                                job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize skills section for ATS and relevance."""
        skills = resume_data.get('skills', {})
        job_required = set(job_data.get('required_skills', []))
        job_preferred = set(job_data.get('preferred_skills', []))

        technical_skills = set(skills.get('technical', []))
        soft_skills = set(skills.get('soft', []))

        # Prioritize required skills first, then preferred, then others
        prioritized_technical = []
        prioritized_technical.extend(list(job_required.intersection(technical_skills)))
        prioritized_technical.extend(list(job_preferred.intersection(technical_skills)))
        prioritized_technical.extend(list(technical_skills - job_required - job_preferred))

        return {
            'technical': prioritized_technical,
            'soft': list(soft_skills),
            'proficiency_levels': skills.get('proficiency_levels', {})
        }

    def _extract_job_keywords(self, job_data: Dict[str, Any]) -> List[str]:
        """Extract key terms and skills from job data."""
        keywords = []

        # Add skills
        keywords.extend(job_data.get('required_skills', []))
        keywords.extend(job_data.get('preferred_skills', []))

        # Add terms from job title
        job_title = job_data.get('job_title', '')
        keywords.extend([word for word in job_title.split() if len(word) > 2])

        # Add terms from responsibilities
        responsibilities = ' '.join(job_data.get('responsibilities', []))
        resp_words = [word for word in responsibilities.split() if len(word) > 3]
        keywords.extend(resp_words[:5])  # Top 5 words

        return list(set(keywords))  # Remove duplicates

    def _identify_candidate_strengths(self, resume_data: Dict[str, Any],
                                    job_data: Dict[str, Any]) -> List[str]:
        """Identify key strengths to highlight in the content."""
        strengths = []

        # Experience alignment
        exp_years = len(resume_data.get('experience', [])) * 2
        job_min_years = job_data.get('years_experience_min', 0)
        if exp_years >= job_min_years:
            strengths.append("extensive hands-on experience")

        # Skills match
        matching_skills = set(resume_data.get('skills', {}).get('technical', [])) & set(job_data.get('required_skills', []))
        if matching_skills:
            strengths.append(f"expertise in {list(matching_skills)[0]}")

        # Online presence
        online_presence = resume_data.get('online_presence', {})
        if online_presence.get('github') or online_presence.get('portfolio'):
            strengths.append("strong portfolio of work")

        return strengths

    def _score_experience_relevance(self, experience: Dict[str, Any],
                                   job_keywords: set) -> float:
        """Score how relevant an experience entry is to the job."""
        score = 0.0

        # Title relevance
        title = experience.get('title', '').lower()
        for keyword in job_keywords:
            if keyword.lower() in title:
                score += 2.0

        # Achievement relevance
        achievements = ' '.join(experience.get('achievements', [])).lower()
        for keyword in job_keywords:
            if keyword.lower() in achievements:
                score += 1.0

        # Technologies match
        technologies = set(experience.get('technologies', []))
        required_tech = job_keywords
        tech_overlap = len(technologies.intersection(required_tech))
        score += tech_overlap * 1.5

        return score

    def _analyze_keyword_usage(self, content: str, job_keywords: List[str]) -> Dict[str, Any]:
        """Analyze how well job keywords are incorporated into content."""
        content_lower = content.lower()
        keywords_found = []

        for keyword in job_keywords:
            if keyword.lower() in content_lower:
                keywords_found.append(keyword)

        density = len(keywords_found) / len(job_keywords) if job_keywords else 0

        return {
            'keywords_found': len(keywords_found),
            'total_keywords': len(job_keywords),
            'keyword_density': density,
            'missing_keywords': [k for k in job_keywords if k.lower() not in content_lower][:5]
        }

    def _calculate_relevance_score(self, resume_data: Dict[str, Any],
                                  job_data: Dict[str, Any]) -> float:
        """Calculate overall relevance score between resume and job."""
        score = 50.0  # Base score

        # Skills match
        resume_skills = set(resume_data.get('skills', {}).get('technical', []))
        job_skills = set(job_data.get('required_skills', []))
        if job_skills:
            skill_overlap = len(resume_skills.intersection(job_skills)) / len(job_skills)
            score += skill_overlap * 30

        # Experience level match
        exp_years = len(resume_data.get('experience', [])) * 2
        job_min_years = job_data.get('years_experience_min', 0)
        if exp_years >= job_min_years:
            score += 15

        return min(100.0, score)

    def _evaluate_content_quality(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the quality of generated content."""
        content = results.get('content', {})

        quality_scores = {}

        for content_type, text in content.items():
            score = 0.0
            reasons = []

            # Length check
            if len(text) > 500:
                score += 20
                reasons.append('adequate_length')
            else:
                reasons.append('too_short')

            # Keyword integration
            keyword_opt = results.get('keyword_optimization', {}).get(content_type, {})
            density = keyword_opt.get('keyword_density', 0)
            if density > 0.5:
                score += 25
                reasons.append('good_keyword_integration')
            elif density > 0.2:
                score += 15
                reasons.append('moderate_keyword_integration')
            else:
                reasons.append('low_keyword_integration')

            # ATS compatibility
            ats_score = self._assess_ats_compatibility({'content': {content_type: text}})
            if ats_score > 80:
                score += 20
                reasons.append('ats_friendly')
            elif ats_score > 60:
                score += 10
                reasons.append('moderately_ats_friendly')

            quality_scores[content_type] = {
                'score': min(100, score),
                'reasons': reasons
            }

        return quality_scores

    def _calculate_keyword_density(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate keyword density across all content."""
        densities = {}

        for content_type, text in results.get('content', {}).items():
            keyword_opt = results.get('keyword_optimization', {}).get(content_type, {})
            densities[content_type] = keyword_opt.get('keyword_density', 0.0)

        return densities

    def _assess_ats_compatibility(self, results: Dict[str, Any]) -> float:
        """Assess how ATS-friendly the content is."""
        ats_score = 100.0  # Start with perfect score

        # Check for confusing formatting (simplified assessment)
        for content_type, text in results.get('content', {}).items():
            # Penalize unusual characters
            unusual_chars = '•★☆▲■○●◆◇◊□■'
            unusual_count = sum(1 for char in unusual_chars if char in text)
            ats_score -= unusual_count * 2

            # Check for standard sections
            has_standard_sections = any(section in text.lower() for section in
                                      ['experience', 'education', 'skills', 'summary'])
            if not has_standard_sections:
                ats_score -= 20

        return max(0, ats_score)

    # Formatting helper methods
    def _format_experience(self, experiences: List[Dict[str, Any]]) -> str:
        """Format experience section."""
        formatted = []
        for exp in experiences[:4]:  # Top 4 experiences
            formatted.append(f"\n{exp.get('title', 'Position')}")
            formatted.append(f"{exp.get('company', 'Company')}, {exp.get('duration', 'Duration')}")
            for achievement in exp.get('achievements', [])[:3]:  # Top 3 achievements
                formatted.append(f"• {achievement}")

        return '\n'.join(formatted)

    def _format_skills(self, skills: Dict[str, Any]) -> str:
        """Format skills section."""
        formatted = []

        technical = skills.get('technical', [])
        if technical:
            formatted.append(f"Technical: {', '.join(technical)}")

        soft = skills.get('soft', [])
        if soft:
            formatted.append(f"Soft Skills: {', '.join(soft)}")

        return '\n'.join(formatted)

    def _format_education(self, education: List[Dict[str, Any]]) -> str:
        """Format education section."""
        formatted = []
        for edu in education[:2]:  # Top 2 education entries
            degree = edu.get('degree', 'Degree')
            institution = edu.get('institution', 'Institution')
            year = edu.get('year', 'Year')
            formatted.append(f"{degree} - {institution}, {year}")

        return '\n'.join(formatted)
