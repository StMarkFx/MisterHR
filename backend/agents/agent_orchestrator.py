"""
Agent Orchestrator for MisterHR

Manages multi-agent workflows and coordinates complex AI operations across all agents.
Handles agent communication, error recovery, progress tracking, and result consolidation.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import json

from .resume_parser import ResumeParserAgent, AgentConfig
from .jd_analyzer import JDAnalyzerAgent
from .web_enrichment import WebEnrichmentAgent
from .matching_agent import MatchingAgent
from .content_generator import ContentGeneratorAgent

class AgentOrchestrator:
    """
    Agent Orchestrator - Coordinates Multi-Agent Workflows

    Handles complex AI operations by orchestrating multiple specialized agents:
    1. Resume Processing Pipeline
    2. Job Analysis & Matching
    3. Content Generation Workflows
    4. Batch Processing Operations
    5. Error Recovery & Fallbacks

    Provides unified interface for complex AI workflows with progress tracking.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Agent configurations
        self.agent_configs = {
            'resume_parser': AgentConfig(
                name="ResumeParserAgent",
                model="gpt-4-turbo-preview",
                temperature=0.3,
                max_tokens=2048,
                timeout=30
            ),
            'jd_analyzer': AgentConfig(
                name="JDAnalyzerAgent",
                model="gpt-4-turbo-preview",
                temperature=0.2,
                max_tokens=1024,
                timeout=25
            ),
            'web_enrichment': AgentConfig(
                name="WebEnrichmentAgent",
                model="gpt-4-turbo-preview",
                temperature=0.1,
                max_tokens=512,
                timeout=45
            ),
            'matching': AgentConfig(
                name="MatchingAgent",
                model="gpt-4-turbo-preview",
                temperature=0.1,
                max_tokens=2048,
                timeout=30
            ),
            'content_generator': AgentConfig(
                name="ContentGeneratorAgent",
                model="gpt-4-turbo-preview",
                temperature=0.7,
                max_tokens=4096,
                timeout=60
            )
        }

        # Initialize agents
        self.agents = {}
        self._initialize_agents()

        # Workflow templates
        self.workflows = {
            'resume_processing': self._resume_processing_workflow,
            'job_application': self._job_application_workflow,
            'batch_matching': self._batch_matching_workflow,
            'content_generation': self._content_generation_workflow,
            'full_pipeline': self._full_pipeline_workflow
        }

    def _initialize_agents(self) -> None:
        """Initialize all agents with proper error handling."""
        try:
            self.agents['resume_parser'] = ResumeParserAgent(self.agent_configs['resume_parser'])
            self.agents['jd_analyzer'] = JDAnalyzerAgent(self.agent_configs['jd_analyzer'])
            self.agents['web_enrichment'] = WebEnrichmentAgent(self.agent_configs['web_enrichment'])
            self.agents['matching'] = MatchingAgent(self.agent_configs['matching'])
            self.agents['content_generator'] = ContentGeneratorAgent(self.agent_configs['content_generator'])
            self.logger.info("All agents initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize agents: {str(e)}")
            raise

    async def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a complete multi-agent workflow.

        Args:
            workflow_name (str): Name of the workflow to execute
            **kwargs: Workflow-specific parameters

        Returns:
            Dict with workflow results and metadata
        """
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        workflow_start = datetime.now()
        workflow_id = f"{workflow_name}_{int(workflow_start.timestamp())}"

        try:
            self.logger.info(f"Starting workflow: {workflow_name} (ID: {workflow_id})")

            # Execute the workflow
            workflow_func = self.workflows[workflow_name]
            result = await workflow_func(workflow_id, **kwargs)

            # Add workflow metadata
            result['workflow_metadata'] = {
                'workflow_id': workflow_id,
                'workflow_name': workflow_name,
                'started_at': workflow_start,
                'completed_at': datetime.now(),
                'total_duration': (datetime.now() - workflow_start).total_seconds(),
                'agent_performance': self._collect_agent_performance()
            }

            self.logger.info(f"Workflow completed: {workflow_name}")
            return result

        except Exception as e:
            self.logger.error(f"Workflow failed: {workflow_name} - {str(e)}")

            # Return error result with partial data if available
            return {
                'success': False,
                'error': str(e),
                'workflow_metadata': {
                    'workflow_id': workflow_id,
                    'workflow_name': workflow_name,
                    'started_at': workflow_start,
                    'failed_at': datetime.now(),
                    'error_type': type(e).__name__
                }
            }

    async def _resume_processing_workflow(self, workflow_id: str, **kwargs) -> Dict[str, Any]:
        """
        Complete resume processing workflow: Parse + Enrich.
        """
        file_path = kwargs.get('file_path')
        content = kwargs.get('content')
        url = kwargs.get('url')

        if not any([file_path, content, url]):
            raise ValueError("Resume file_path, content, or url required")

        progress_updates = []

        # Step 1: Parse resume
        progress_updates.append({'step': 'parsing', 'status': 'in_progress', 'timestamp': datetime.now()})
        resume_result = await self.agents['resume_parser']._execute_with_metrics(
            file_path=file_path, content=content, url=url
        )

        if not resume_result.get('success'):
            raise Exception(f"Resume parsing failed: {resume_result.get('error')}")

        resume_data = resume_result['data']
        progress_updates.append({'step': 'parsing', 'status': 'completed', 'timestamp': datetime.now()})

        # Step 2: Enrich with online presence (if available)
        online_presence = resume_data.get('online_presence', {})
        if online_presence.get('github') or online_presence.get('linkedin') or online_presence.get('portfolio'):
            progress_updates.append({'step': 'enrichment', 'status': 'in_progress', 'timestamp': datetime.now()})
            enrichment_result = await self.agents['web_enrichment']._execute_with_metrics(
                online_presence=online_presence,
                skills=resume_data.get('skills', {}),
                personal_info=resume_data.get('personal_info', {})
            )

            if enrichment_result.get('success'):
                # Merge enrichment data with resume data
                resume_data['enrichment_data'] = enrichment_result['data']
                resume_data['credibility_score'] = enrichment_result['data'].get('credibility_score', 0)

            progress_updates.append({'step': 'enrichment', 'status': 'completed', 'timestamp': datetime.now()})

        return {
            'success': True,
            'resume_data': resume_data,
            'progress_log': progress_updates,
            'processing_summary': self._create_processing_summary(resume_data, progress_updates)
        }

    async def _job_application_workflow(self, workflow_id: str, **kwargs) -> Dict[str, Any]:
        """
        Complete job application workflow: Parse resume + Analyze job + Match + Generate content.
        """
        resume_file = kwargs.get('resume_file')
        job_description = kwargs.get('job_description')
        content_type = kwargs.get('content_type', 'both')
        tone = kwargs.get('tone', 'professional')

        if not resume_file and not job_description:
            raise ValueError("Both resume and job description required for application workflow")

        progress_updates = []

        # Parallel processing: Resume parsing and Job analysis
        progress_updates.append({'step': 'parallel_processing', 'status': 'in_progress', 'timestamp': datetime.now()})

        resume_task = self.agents['resume_parser']._execute_with_metrics(
            file_path=resume_file
        )
        job_task = self.agents['jd_analyzer']._execute_with_metrics(
            jd_text=job_description
        )

        resume_result, job_result = await asyncio.gather(resume_task, job_task, return_exceptions=True)

        # Handle individual task errors
        if isinstance(resume_result, Exception):
            raise Exception(f"Resume parsing failed: {str(resume_result)}")
        if isinstance(job_result, Exception):
            raise Exception(f"Job analysis failed: {str(job_result)}")

        if not resume_result.get('success') or not job_result.get('success'):
            errors = []
            if not resume_result.get('success'):
                errors.append(f"Resume: {resume_result.get('error')}")
            if not job_result.get('success'):
                errors.append(f"Job: {job_result.get('error')}")
            raise Exception("Workflow failed: " + ", ".join(errors))

        resume_data = resume_result['data']
        job_data = job_result['data']

        progress_updates.append({'step': 'parallel_processing', 'status': 'completed', 'timestamp': datetime.now()})

        # Step 3: Match candidate to job
        progress_updates.append({'step': 'matching', 'status': 'in_progress', 'timestamp': datetime.now()})
        match_result = await self.agents['matching']._execute_with_metrics(
            resume_data=resume_data,
            job_data=job_data
        )

        if not match_result.get('success'):
            raise Exception(f"Matching failed: {match_result.get('error')}")

        progress_updates.append({'step': 'matching', 'status': 'completed', 'timestamp': datetime.now()})

        # Step 4: Generate tailored content
        progress_updates.append({'step': 'content_generation', 'status': 'in_progress', 'timestamp': datetime.now()})
        content_result = await self.agents['content_generator']._execute_with_metrics(
            resume_data=resume_data,
            job_data=job_data,
            content_type=content_type,
            tone=tone
        )

        if not content_result.get('success'):
            # Don't fail the whole workflow if content generation fails
            self.logger.warning(f"Content generation failed: {content_result.get('error')}")
            content_data = None
        else:
            content_data = content_result['data']

        progress_updates.append({'step': 'content_generation', 'status': 'completed', 'timestamp': datetime.now()})

        return {
            'success': True,
            'resume_data': resume_data,
            'job_data': job_data,
            'matching_result': match_result['data'],
            'content_result': content_data,
            'progress_log': progress_updates,
            'application_summary': self._create_application_summary(
                match_result['data'], content_data, job_data
            )
        }

    async def _batch_matching_workflow(self, workflow_id: str, **kwargs) -> Dict[str, Any]:
        """
        Batch matching workflow: Match multiple resumes to a job.
        """
        resume_files = kwargs.get('resume_files', [])
        job_description = kwargs.get('job_description')

        if not resume_files or not job_description:
            raise ValueError("Resume files and job description required for batch matching")

        progress_updates = []
        results = []

        # Step 1: Analyze job
        progress_updates.append({'step': 'job_analysis', 'status': 'in_progress', 'timestamp': datetime.now()})
        job_result = await self.agents['jd_analyzer']._execute_with_metrics(jd_text=job_description)

        if not job_result.get('success'):
            raise Exception(f"Job analysis failed: {job_result.get('error')}")

        job_data = job_result['data']
        progress_updates.append({'step': 'job_analysis', 'status': 'completed', 'timestamp': datetime.now()})

        # Step 2: Process resumes in parallel batches
        batch_size = kwargs.get('batch_size', 3)  # Process 3 at a time to avoid overload
        progress_updates.append({'step': 'batch_processing', 'status': 'in_progress', 'timestamp': datetime.now()})

        for i in range(0, len(resume_files), batch_size):
            batch = resume_files[i:i + batch_size]

            # Create matching tasks for this batch
            tasks = []
            for resume_file in batch:
                tasks.append(self._process_single_resume_for_matching(resume_file, job_data))

            # Execute batch
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for j, result in enumerate(batch_results):
                resume_data = batch[j]
                if isinstance(result, Exception):
                    results.append({
                        'resume': resume_data,
                        'success': False,
                        'error': str(result),
                        'match_score': 0
                    })
                else:
                    match_data = result['data']
                    results.append({
                        'resume': resume_data,
                        'success': True,
                        'match_data': match_data,
                        'overall_score': match_data.get('overall_score', 0),
                        'match_category': match_data.get('match_category', 'unknown')
                    })

        progress_updates.append({'step': 'batch_processing', 'status': 'completed', 'timestamp': datetime.now()})

        # Sort results by match score
        successful_results = [r for r in results if r.get('success')]
        successful_results.sort(key=lambda x: x.get('overall_score', 0), reverse=True)

        return {
            'success': True,
            'job_data': job_data,
            'results': results,
            'ranking': successful_results,
            'progress_log': progress_updates,
            'batch_summary': self._create_batch_summary(results, job_data)
        }

    async def _content_generation_workflow(self, workflow_id: str, **kwargs) -> Dict[str, Any]:
        """
        Standalone content generation workflow.
        """
        resume_data = kwargs.get('resume_data')
        job_data = kwargs.get('job_data')
        content_type = kwargs.get('content_type', 'resume')
        tone = kwargs.get('tone', 'professional')

        if not resume_data or not job_data:
            raise ValueError("Resume data and job data required for content generation")

        result = await self.agents['content_generator']._execute_with_metrics(
            resume_data=resume_data,
            job_data=job_data,
            content_type=content_type,
            tone=tone
        )

        if not result.get('success'):
            raise Exception(f"Content generation failed: {result.get('error')}")

        return {
            'success': True,
            'generated_content': result['data'],
            'generation_metadata': result.get('metadata', {})
        }

    async def _full_pipeline_workflow(self, workflow_id: str, **kwargs) -> Dict[str, Any]:
        """
        Complete end-to-end workflow: Resume → Job → Enrichment → Matching → Content.
        """
        # This combines all the above workflows into one comprehensive pipeline
        # For now, delegate to job application workflow
        return await self._job_application_workflow(workflow_id, **kwargs)

    async def _process_single_resume_for_matching(self, resume_file: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single resume for batch matching."""
        # Parse resume
        parse_result = await self.agents['resume_parser']._execute_with_metrics(file_path=resume_file)
        if not parse_result.get('success'):
            raise Exception(f"Resume parsing failed: {parse_result.get('error')}")

        resume_data = parse_result['data']

        # Skip enrichment for batch processing (too slow), but could be added optionally
        # Match against job
        match_result = await self.agents['matching']._execute_with_metrics(
            resume_data=resume_data,
            job_data=job_data
        )

        if not match_result.get('success'):
            raise Exception(f"Matching failed: {match_result.get('error')}")

        return match_result

    def _collect_agent_performance(self) -> Dict[str, Any]:
        """Collect performance metrics from all agents."""
        performance = {}

        for agent_name, agent in self.agents.items():
            performance[agent_name] = agent.get_health_status()

        return performance

    def _create_processing_summary(self, resume_data: Dict[str, Any], progress_log: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a summary of the resume processing workflow."""
        return {
            'personal_info_extracted': bool(resume_data.get('personal_info', {}).get('name')),
            'experience_entries': len(resume_data.get('experience', [])),
            'skills_identified': len(resume_data.get('skills', {}).get('technical', [])),
            'online_presence_verified': resume_data.get('online_presence', {}).get('verified') or False,
            'credibility_score': resume_data.get('credibility_score', 0),
            'processing_steps_completed': len([p for p in progress_log if p['status'] == 'completed'])
        }

    def _create_application_summary(self, match_data: Dict[str, Any], content_data: Optional[Dict[str, Any]], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of the job application workflow."""
        return {
            'overall_match_score': match_data.get('overall_score', 0),
            'match_category': match_data.get('match_category', 'unknown'),
            'critical_gaps': len(match_data.get('gaps', {}).get('critical_gaps', [])),
            'content_generated': bool(content_data and content_data.get('content')),
            'ats_compatibility': content_data.get('metadata', {}).get('ats_compatibility', 0) if content_data else 0,
            'keyword_optimization': content_data.get('metadata', {}).get('keyword_density', {}) if content_data else {},
            'recommendations_provided': len(match_data.get('recommendations', []))
        }

    def _create_batch_summary(self, results: List[Dict[str, Any]], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of batch matching results."""
        successful_matches = [r for r in results if r.get('success')]
        total_processed = len(results)

        if not successful_matches:
            return {'total_processed': total_processed, 'successful': 0, 'error': 'No successful matches'}

        scores = [r.get('overall_score', 0) for r in successful_matches]
        categories = [r.get('match_category', 'unknown') for r in successful_matches]

        return {
            'total_processed': total_processed,
            'successful_matches': len(successful_matches),
            'success_rate': len(successful_matches) / total_processed,
            'average_score': sum(scores) / len(scores),
            'score_distribution': {
                'excellent': categories.count('excellent_match'),
                'strong': categories.count('strong_match'),
                'good': categories.count('good_match'),
                'moderate': categories.count('moderate_match'),
                'weak': categories.count('weak_match')
            },
            'top_candidate_score': max(scores) if scores else 0,
            'job_title': job_data.get('job_title', 'Unknown Position')
        }

    # Convenience methods for common operations
    async def process_resume(self, **kwargs) -> Dict[str, Any]:
        """Convenience method for resume processing workflow."""
        return await self.execute_workflow('resume_processing', **kwargs)

    async def create_job_application(self, **kwargs) -> Dict[str, Any]:
        """Convenience method for job application workflow."""
        return await self.execute_workflow('job_application', **kwargs)

    async def batch_match_candidates(self, **kwargs) -> Dict[str, Any]:
        """Convenience method for batch matching workflow."""
        return await self.execute_workflow('batch_matching', **kwargs)

    async def generate_content(self, **kwargs) -> Dict[str, Any]:
        """Convenience method for content generation workflow."""
        return await self.execute_workflow('content_generation', **kwargs)

    def get_agent_health(self) -> Dict[str, Any]:
        """Get health status of all agents."""
        return {
            'overall_status': 'healthy',  # Could implement more sophisticated health checking
            'agents': self._collect_agent_performance(),
            'timestamp': datetime.now()
        }
