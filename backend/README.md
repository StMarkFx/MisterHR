# MisterHR Backend - FastAPI AI Agent System

*High-performance Python backend powering intelligent hiring with multi-agent LangChain orchestration*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-1a73e8.svg)](https://langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)](https://openai.com/)

---

## 📋 **Table of Contents**
- [🏗️ Architecture](#️-architecture)
- [🤖 AI Agents](#-ai-agents)
- [🚀 Quick Start](#-quick-start)
- [📡 API Endpoints](#-api-endpoints)
- [🧪 Testing](#-testing)
- [📚 Documentation](#-documentation)

---

## 🏗️ **Architecture**

The backend follows a **multi-agent orchestration pattern** built on FastAPI, featuring:

### **Core Components**
```
backend/
├── main.py              # FastAPI application entry point
├── agents/              # AI agent ecosystem
│   ├── base_agent.py    # Abstract agent foundation
│   ├── agent_orchestrator.py  # Workflow coordination
│   ├── resume_parser.py       # CV parsing agent
│   ├── jd_analyzer.py         # Job requirements agent
│   ├── matching_agent.py      # Candidate matching agent
│   ├── content_generator.py   # Content creation agent
│   └── web_enrichment.py      # Portfolio verification agent
```

### **Design Patterns**
- **Agent Pattern**: Each agent specializes in one responsibility with async execution
- **Orchestrator Pattern**: Coordinates complex multi-agent workflows
- **Strategy Pattern**: Rule-based with LLM fallback for reliability
- **Observer Pattern**: Metrics collection and health monitoring

---

## 🤖 **AI Agents**

### **Agent Ecosystem Overview**

| Agent | Purpose | Key Features | Tech Stack |
|-------|---------|--------------|------------|
| **ResumeParserAgent** | Extract structured data from CVs | PDF/DOCX parsing, NLP categorization | spaCy, PyMuPDF |
| **WebEnrichmentAgent** | Verify online portfolios | GitHub/LinkedIn API calls, validation | aiohttp, requests |
| **JDAnalyzerAgent** | Extract job requirements | LLM + rule-based extraction | OpenAI GPT-4, NLP |
| **MatchingAgent** | Calculate candidate-job fit | Semantic similarity, scoring algorithm | scikit-learn, embeddings |
| **ContentGeneratorAgent** | Generate tailored content | Resume/cover letter optimization | OpenAI, templating |
| **AgentOrchestrator** | Coordinate workflows | Async task management, error handling | asyncio, concurrent.futures |

### **Agent Specifications**

#### **ResumeParserAgent**
```python
# Extracts 8 core categories from CV content
{
  "personal_info": {...},
  "experience": [...],
  "education": [...],
  "skills": {...},
  "projects": [...],
  "certifications": [...],
  "online_links": {...}
}
```

#### **JDAnalyzerAgent**
```python
# Analyzes job descriptions for requirements
{
  "required_skills": [...],
  "preferred_skills": [...],
  "experience_level": "Senior",
  "education_requirements": [...],
  "location": "...",
  "salary_range": {...}
}
```

#### **MatchingAgent**
```python
# Multi-factor candidate scoring
{
  "overall_score": 85.4,
  "skills_match": 92.1,
  "experience_match": 78.3,
  "education_match": 95.0,
  "cultural_fit": 80.2
}
```

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.10+
- Virtual environment recommended

### **Local Setup**
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Start development server
python main.py
```

The API will be available at `http://127.0.0.1:8000`

### **Environment Configuration**
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SECRET_KEY=your_secret_key
```

---

## 📡 **API Endpoints**

### **Core Endpoints**

#### **Health Check**
```http
GET /health
```
Returns system status and agent health metrics.

#### **Resume Processing**
```http
POST /api/process-resume
Content-Type: multipart/form-data

Form Data:
- file: PDF or DOCX resume file
```
Parses resume and returns structured data.

#### **Job Analysis**
```http
POST /api/analyze-job
Content-Type: application/json

{
  "job_description": "Full job description text...",
  "job_title": "Senior Software Engineer",
  "company": "Tech Corp"
}
```
Extracts requirements and criteria from job description.

#### **Candidate Matching**
```http
POST /api/match-candidate
Content-Type: application/json

{
  "resume_data": {...},
  "job_data": {...}
}
```
Calculates match score between candidate and job.

#### **Content Generation**
```http
POST /api/generate-content
Content-Type: application/json

{
  "content_type": "resume|cover_letter",
  "resume_data": {...},
  "job_data": {...}
}
```
Generates tailored resume or cover letter.

### **Agent Orchestration Endpoints**

#### **Batch Resume Processing** (Planned)
```http
POST /api/batch-process
```
Process multiple resumes simultaneously.

#### **Workflow Orchestration** (Planned)
```http
POST /api/orchestrate-workflow
```
Execute complex multi-agent workflows.

---

## 🧪 **Testing**

### **Run Backend Tests**
```bash
# From project root
cd backend
python -m pytest ../tests/ -v --cov=. --cov-report=html
```

### **Test Categories**
- **Unit Tests**: Individual agent functionality
- **Integration Tests**: Multi-agent workflows
- **API Tests**: Endpoint validation
- **Performance Tests**: Load testing and metrics

### **Code Coverage**
Target: 90%+ coverage across all modules.

---

## 📚 **Documentation**

### **API Documentation**
Once running, visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.

### **Architecture Diagrams**
Located in `../diagrams/` directory:
- [AI Agent Orchestration](diagrams/ai-agent-orchestration.md)
- [Database Schema](diagrams/database-schema.md)

### **Development Guidelines**
- Use async/await for all I/O operations
- Implement proper error handling and logging
- Follow PEP 8 style guidelines
- Include type hints for all function signatures
- Write comprehensive docstrings

---

## 🔧 **Development**

### **Adding a New Agent**

1. **Create Agent Class**
```python
from agents.base_agent import BaseAgent
from agents.agent_config import AgentConfig

class NewAgent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)

    async def execute(self, **kwargs) -> Dict[str, Any]:
        # Agent logic here
        pass
```

2. **Register with Orchestrator**
```python
# In agent_orchestrator.py
from agents.new_agent import NewAgent

self._agents['new_agent'] = NewAgent(config)
```

3. **Add API Endpoint**
```python
# In main.py
from agents.new_agent import NewAgent

@app.post("/api/new-endpoint")
async def new_endpoint(request: NewRequest):
    agent = NewAgent(config)
    return await agent.execute(**request.dict())
```

### **Agent Configuration**
Each agent is configured via `AgentConfig`:
```python
config = AgentConfig(
    name="resume_parser",
    max_execution_time=30.0,
    retry_attempts=3,
    llm_fallback=True,
    metrics_enabled=True
)
```

---

## 📊 **Performance & Monitoring**

### **Key Metrics**
- Response time per agent (<5s target)
- Success rates (>99% target)
- LLM API costs and usage
- Memory usage and optimization

### **Health Checks**
- Agent responsiveness
- External API availability
- Database connectivity
- Memory and CPU usage

### **Logging**
- Structured logging with correlation IDs
- Error tracking with stack traces
- Performance metrics collection
- Audit trail for AI operations

---

## 🔒 **Security**

### **Data Privacy**
- Resume data processing in memory only
- No permanent storage of sensitive information
- GDPR compliance considerations

### **API Security**
- Rate limiting per endpoint
- Input validation and sanitization
- Authentication for sensitive operations
- CORS configuration for frontend access

### **AI Safety**
- Input/output validation
- Fallback mechanisms for LLM failures
- Monitoring for hallucination detection
- Ethical AI usage guidelines

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Agent Execution Errors**
```python
# Check agent health
response = requests.get("http://127.0.0.1:8000/health")
print(response.json())
```

#### **LLM API Issues**
- Verify `OPENAI_API_KEY` in environment
- Check API quota and billing status
- Implement exponential backoff

#### **File Processing Errors**
- Ensure PyMuPDF and spaCy are installed
- Check file format compatibility
- Validate file size limits

---

## 🤝 **Contributing**

### **Backend Development Principles**
1. **Type Safety**: Use Pydantic models for all data structures
2. **Async First**: All I/O operations must be async
3. **Error Resilience**: Implement comprehensive error handling
4. **Testing**: 90%+ code coverage requirement
5. **Documentation**: Docstrings for all public methods

### **Code Standards**
- **Linting**: black, isort, mypy
- **Testing**: pytest with async support
- **Documentation**: Google-style docstrings
- **Version Control**: Branch protection, PR reviews

---

## 📈 **Roadmap**

### **Immediate Priorities**
- [ ] Complete agent orchestrator workflows
- [ ] Add batch processing capabilities
- [ ] Implement advanced caching mechanisms
- [ ] Add comprehensive error recovery

### **Future Enhancements**
- [ ] Model fine-tuning for domain-specific tasks
- [ ] Multi-language support for CV processing
- [ ] Advanced ML models for better matching
- [ ] Realtime agent communication protocols

---

Built with ❤️ for the future of intelligent hiring ✨
