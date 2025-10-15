sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API Gateway
    participant R as ResumeParserAgent
    participant J as JDAnalyzerAgent
    participant M as MatchingAgent
    participant C as ContentGeneratorAgent
    participant FB as FeedbackAgent
    participant B as BatchProcessingAgent
    participant O as Orchestrator

    Note over U,B: Resume Generation Flow
    U->>F: Paste Job Description
    F->>A: POST /api/generate-resume
    A->>O: Delegate to LangChain Orchestrator

    O->>R: Analyze uploaded resume
    R-->>O: Structured resume JSON

    O->>J: Analyze job description
    J-->>O: Job requirements & keywords

    O->>M: Compare resume vs job
    M-->>O: Match score & gaps

    O->>C: Generate tailored resume
    C-->>O: ATS-optimized content

    O->>FB: Generate feedback
    FB-->>O: Strengths & improvements

    O-->>A: Complete results
    A-->>F: Response with resume + feedback
    F-->>U: Display generated content

    Note over U,B: Batch Processing Flow (Recruiter)
    U->>F: Upload multiple resumes
    F->>A: POST /api/batch-process

    A->>O: Initiate batch processing
    O->>B: Create batch workflow

    loop For each resume
        B->>R: Parse individual resume
        R-->>B: Resume data
        B->>J: Compare with job reqs
        J-->>B: Job analysis
        B->>M: Calculate match scores
        M-->>B: Ranking & summaries
    end

    B-->>O: Batch results completed
    O-->>A: Consolidated rankings
    A-->>F: Shortlist dashboard
    F-->>U: Ranked candidates

    Note over U,B: Agent Communication Patterns
    R->>O: tool_calls, function_results
    J->>O: structured_requirements, skills_list
    M->>O: similarity_score, gap_analysis
    C->>O: generated_content, optimization_notes
    FB->>O: feedback_summary, improvement_suggestions
```

# AI Agent Orchestration - MisterHR Multi-Agent System

## LangChain Agent Architecture

### Agent Roles & Responsibilities

#### 1. ResumeParserAgent
**Purpose**: Extract structured data from CVs/resumes
**Input**: PDF/DOCX files, raw text
**Output**: Structured JSON with experience, education, skills
**Tech**: PyMuPDF for PDF parsing, spaCy for NLP

#### 2. JDAnalyzerAgent
**Purpose**: Parse job descriptions for key requirements
**Input**: Job posting text, company details
**Output**: Skills matrix, experience requirements, keywords
**Tech**: LLM classification, entity extraction

#### 3. MatchingAgent
**Purpose**: Calculate resume-job fit scores
**Input**: Parsed resume data + job requirements
**Output**: Similarity score (0-100), gap analysis
**Tech**: Semantic similarity, embedding comparison

#### 4. ContentGeneratorAgent
**Purpose**: Create tailored resumes and cover letters
**Input**: Original resume + job requirements + match analysis
**Output**: ATS-optimized content, personalized messaging
**Tech**: Prompt engineering, LLM generation

#### 5. FeedbackAgent
**Purpose**: Provide optimization suggestions
**Input**: Generated content + match analysis
**Output**: Specific improvements, keyword gaps, strengths
**Tech**: Comparative analysis, rule-based suggestions

#### 6. BatchProcessingAgent
**Purpose**: Coordinate multi-resume workflow management
**Input**: Multiple resume files + job description
**Output**: Ranked candidate list, bulk summaries
**Tech**: Async processing, queue management

### Communication Protocols

#### Synchronous Flow (Resume Generation)
1. **User Input** → Orchestrator receives request
2. **Sequential Processing** → Agents execute in dependency order
3. **Result Aggregation** → Combine outputs into final response
4. **Response Delivery** → Return generated content to user

#### Asynchronous Flow (Batch Processing)
1. **Initiation** → Start batch job with queue ID
2. **Parallel Execution** → Process multiple resumes concurrently
3. **Progress Tracking** → Real-time status updates
4. **Result Compilation** → Aggregate rankings and summaries

### Error Handling & Resilience

#### Circuit Breaker Pattern
```
Agent Failure → Fallback Response → Retry Logic → Manual Override
```

#### Graceful Degradation
- Primary LLM unavailable → Simplified matching algorithm
- Document parsing fails → Text-based processing
- Storage issues → Local file handling

#### Performance Optimization
- **Caching**: LLM responses for similar requests
- **Batching**: Group similar processing requests
- **Async Processing**: Non-blocking I/O operations
- **Rate Limiting**: API usage controls and quotas

## Agent Configuration

### Prompt Management
```yaml
# Version-controlled prompts
prompts:
  resume_parser:
    version: "1.0.0"
    template: "Extract the following from this resume..."
    parameters: [format, entities]

  content_generator:
    version: "2.1.5"
    template: "Based on this resume and job requirements..."
    parameters: [tone, style, keywords]
```

### Agent Parameters
```json
{
  "resume_parser": {
    "max_tokens": 1000,
    "temperature": 0.1,
    "model": "gpt-4-turbo"
  },
  "content_generator": {
    "creativity": 0.7,
    "format": "ATS-optimized",
    "max_length": 5000
  }
}
```

### Monitoring & Observability

#### Metrics Tracking
- **Response Time**: Per agent processing duration
- **Accuracy Score**: LLM output validation metrics
- **Error Rate**: Agent failure and retry statistics
- **Resource Usage**: API calls, token consumption, storage

#### Logging Architecture
```
INFO: Agent execution started
DEBUG: Input validation passed
WARN: API rate limit approaching
ERROR: Token limit exceeded, using fallback
