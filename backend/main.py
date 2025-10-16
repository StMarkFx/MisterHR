"""
MisterHR Backend API - Multi-Agent LangChain Platform
Core FastAPI application with AI agent orchestration for resume optimization and candidate screening.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agents import AgentOrchestrator
from agents.base_agent import AgentConfig
from agents.resume_parser import ResumeParserAgent

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="MisterHR API",
    description="AI-powered platform for resume optimization and candidate screening using multi-agent LangChain framework",
    version="1.0.0",
    docs_url="/docs"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://misterhr.vercel.app"],  # Add production URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    message: str
    version: str

class ResumeParseRequest(BaseModel):
    """Resume parsing request model."""
    file_path: str  # Path to resume file

class ResumeParseResponse(BaseModel):
    """Resume parsing response model."""
    success: bool
    data: dict | None = None
    error: str | None = None

# Health check endpoint
@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API status."""
    return HealthResponse(
        status="healthy",
        message="MisterHR AI platform is running",
        version="1.0.0"
    )

# Resume parsing endpoint - Real agent integration
@app.post("/api/parse-resume", response_model=ResumeParseResponse)
async def parse_resume(request: ResumeParseRequest):
    """Parse resume from file using ResumeParserAgent."""
    try:
        global resume_parser_agent

        if not resume_parser_agent:
            return ResumeParseResponse(
                success=False,
                error="Resume parser agent not initialized"
            )

        # Use real ResumeParserAgent
        result = await resume_parser_agent.execute(file_path=request.file_path)
        return ResumeParseResponse(
            success=True,
            data=result
        )

    except Exception as e:
        return ResumeParseResponse(
            success=False,
            error=f"Resume parsing failed: {str(e)}"
        )

# Generate tailored resume endpoint (placeholder for now)
@app.post("/api/generate-resume")
async def generate_resume():
    """Generate tailored resume using ContentGeneratorAgent."""
    try:
        # TODO: Implement ContentGeneratorAgent integration
        return {"success": True, "message": "Resume generation initiated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume generation failed: {str(e)}"
        )

# Agent Orchestrator workflow test endpoint
@app.post("/api/test-orchestrator")
async def test_orchestrator(file_path: str):
    """Test basic resume parsing workflow (simplified for now)."""
    try:
        # For now, just test the individual ResumeParserAgent
        if not resume_parser_agent:
            return {"success": False, "error": "Resume parser not available"}

        result = await resume_parser_agent.execute(file_path=file_path)
        return {"success": True, "result": {
            "resume_data": result,
            "workflow_notes": "Simplified workflow - individual agent only"
        }}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Test Matching Agent endpoint
@app.post("/api/match-resume")
async def match_resume(resume_path: str, job_description: str):
    """Test job-resume matching with MatchingAgent."""
    try:
        # First parse the resume
        if not resume_parser_agent:
            return {"success": False, "error": "Resume parser not available"}

        resume_result = await resume_parser_agent.execute(file_path=resume_path)
        if not resume_result:
            return {"success": False, "error": "Resume parsing failed"}

        # For now, just return a basic match result (MatchingAgent integration next)
        # JD Analyzer not fully integrated yet, so simulate job data
        job_data = {
            "required_skills": ["python", "javascript", "react"],
            "preferred_skills": [" AWS", "docker"],
            "experience_level": "mid",
            "years_experience_min": 3,
            "responsibilities": ["develop software", "work in teams"]
        }

        # Simulate basic matching (would use real MatchingAgent)
        resume_skills = set(resume_result.get('skills', {}).get('technical', []))
        job_skills = set(job_data['required_skills'])
        skill_match = len(resume_skills.intersection(job_skills)) / len(job_skills) * 100

        return {
            "success": True,
            "resume_data": resume_result,
            "job_data": job_data,
            "matching_result": {
                "overall_score": round(skill_match, 2),
                "component_scores": {
                    "skills_match": round(skill_match, 2),
                    "experience_match": 50.0,  # Placeholder
                    "education_match": 75.0,   # Placeholder
                },
                "match_category": "good_match" if skill_match > 50 else "moderate_match",
                "analysis_notes": "Basic skill-based matching (MatchingAgent integration coming)"
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Global agent instances
resume_parser_agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    global resume_parser_agent
    print("🚀 Starting MisterHR Backend...")
    print("🔗 Agent orchestration system initializing...")

    try:
        # Initialize ResumeParserAgent
        agent_config = AgentConfig(
            name="ResumeParserAgent",
            model="gpt-4-turbo-preview",
            temperature=0.3,  # Lower temperature for parsing accuracy
            max_tokens=2048,
            timeout=30
        )
        resume_parser_agent = ResumeParserAgent(agent_config)
        print("✅ ResumeParserAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ResumeParserAgent: {str(e)}")

    print("✅ Backend ready for requests")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    global resume_parser_agent
    print("🛑 Shutting down MisterHR Backend...")
    # TODO: Clean up agent resources here
    resume_parser_agent = None
    print("✅ Backend shutdown complete")

if __name__ == "__main__":
    # For development mode
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload in development
        log_level="info"
    )
