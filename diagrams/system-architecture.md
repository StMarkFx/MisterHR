graph TB
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef backend fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef database fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef ai fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef external fill:#ffcdd2,stroke:#b71c1c,stroke-width:2px

    subgraph "Frontend Layer (Vercel)"
        A[Next.js 14 + React]:::frontend
        B[TailwindCSS]:::frontend
        C[Supabase Auth]:::frontend
        D[SWR State Mgmt]:::frontend
    end

    subgraph "Backend Layer (Railway)"
        E[FastAPI + Uvicorn]:::backend
        F[LangChain Agents]:::backend
        G[Pydantic Models]:::backend
        H[Async Processing]:::backend
    end

    subgraph "Database Layer (Supabase)"
        I[PostgreSQL]:::database
        J[Row Level Security]:::database
        K[Real-time Subscriptions]:::database
        L[File Storage]:::database
    end

    subgraph "AI Layer (Railway)"
        M[ResumeParserAgent]:::ai
        N[JDAnalyzerAgent]:::ai
        O[MatchingAgent]:::ai
        P[ContentGeneratorAgent]:::ai
        Q[FeedbackAgent]:::ai
        R[BatchProcessingAgent]:::ai
    end

    subgraph "External Services"
        S[OpenAI API]:::external
        T[Supabase Auth]:::external
        U[Supabase Storage]:::external
    end

    A --> E
    C --> J
    E --> I
    F --> S
    H --> U
    M --> R
    O --> P

    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style I fill:#e8f5e8
    style M fill:#fff3e0
    style S fill:#ffcdd2
```

# System Architecture Overview - MisterHR

## Core Architecture Components

### Frontend Layer
- **Next.js 14**: React framework with App Router, SSR/SSG capabilities
- **TailwindCSS**: Utility-first styling, component-based architecture
- **Supabase Auth**: Authentication with role-based access control
- **SWR**: Light-weight server state management

### Backend Layer
- **FastAPI**: High-performance async Python web framework
- **LangChain**: Multi-agent AI orchestration framework
- **Pydantic**: Request/response validation and auto-documentation
- **Async Processing**: Non-blocking I/O for long-running AI tasks

### Database Layer
- **PostgreSQL**: Robust relational database via Supabase
- **Row Level Security**: Enforced data isolation between users/roles
- **Real-time Subscriptions**: Live updates for collaborative features
- **File Storage**: Secure document and resume storage

### AI Agent Layer
- **ResumeParserAgent**: PDF/DOCX extraction to structured JSON
- **JDAnalyzerAgent**: Job description parsing and requirements extraction
- **MatchingAgent**: Semantic similarity scoring between profiles/jobs
- **ContentGeneratorAgent**: AI-powered resume/cover letter generation
- **FeedbackAgent**: Optimization suggestions and gap analysis
- **BatchProcessingAgent**: Multi-resume workflow coordination

### External Dependencies
- **OpenAI API**: GPT models for natural language processing
- **Supabase Services**: Authentication, database, and file storage
- **Vercel/Railway**: Hosting and deployment platforms

## Data Flow Patterns

### User Authentication Flow
```
Applicant/Recruiter → Supabase Auth → JWT Token → Role-based Access
```

### Resume Processing Flow
```
Upload CV → Supabase Storage → ResumeParserAgent → Structured JSON → Database
```

### AI Generation Flow
```
Job Description + Profile → LangChain Orch. → OpenAI API → Generated Content → User
```

### Matching Algorithm Flow
```
Job Requirements + Candidate Profile → MatchingAgent → Similarity Score → Ranking
