flowchart TD
    classDef role_selection fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef action fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef system_action fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef success fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef feedback fill:#fff3e0,stroke:#f57c00,stroke-width:2px

    subgraph "Onboarding"
        A[User lands on app]:::action
        B[Choose role: Applicant]:::role_selection
        C[Sign up with email]:::action
        D[Supabase Auth creates account]:::system_action
        E[Role stored in DB]:::system_action
    end

    subgraph "Profile Creation"
        F[Upload CV or Manual Entry]:::action
        G[PyMuPDF parses PDF/DOCX]:::system_action
        H[ResumeParserAgent extracts data]:::system_action
        I[Structured JSON saved to profile]:::system_action
        J[Display ATS-style preview]:::success
    end

    subgraph "Resume Generation"
        K[Paste Job Description]:::action
        L[JDAnalyzerAgent parses requirements]:::system_action
        M[MatchingAgent compares fit]:::system_action
        N[ContentGeneratorAgent creates resume]:::system_action
        O[FeedbackAgent analyzes gaps]:::system_action
        P[Generate cover letter]:::system_action
        Q[Display tailored content]:::success
    end

    subgraph "Optimization Loop"
        R[Review match score]:::feedback
        S[View strengths & gaps]:::feedback
        T[Update profile manually]:::action
        U[Re-generate with improvements]:::action
    end

    subgraph "Success Outcomes"
        V[Download PDF resume]:::success
        W[Export cover letter]:::success
        X[Apply with confidence]:::success
        Y[Track application history]:::success
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P --> Q
    Q --> R
    R --> S
    S --> T
    T --> U
    U --> R
    R --> V
    V --> W
    W --> X
    X --> Y

    style A fill:#e3f2fd
    style C fill:#e3f2fd
    style F fill:#e3f2fd
    style K fill:#e3f2fd
    style T fill:#e3f2fd
```

# Applicant User Journey - MisterHR

## Complete End-to-End Experience

### Phase 1: Discovery & Onboarding
**Touchpoints**: Landing page → Role selection → Authentication
**Goals**: Clear value proposition, frictionless signup, immediate engagement
**Success Metrics**: 75% conversion from landing to signup

### Phase 2: Profile Establishment
**Touchpoints**: CV upload → AI parsing → Profile preview
**Goals**: Accurate data extraction, ATS-compliant formatting
**Success Metrics**: 90%+ parsing accuracy, 5-min setup time

### Phase 3: Resume Customization Engine
**Touchpoints**: JD input → AI analysis → Content generation
**Goals**: Personalized outputs matching job requirements
**Success Metrics**: 85% relevance improvement vs manual resumes

### Phase 4: Continuous Optimization
**Touchpoints**: Feedback dashboard → Gap analysis → Iterative improvement
**Goals**: Data-driven resume enhancement, skill gap identification
**Success Metrics**: 70% user engagement with feedback features

### Phase 5: Application Success
**Touchpoints**: Export functionality → Application tracking → Success measurement
**Goals**: Seamless application process, measurable outcomes
**Success Metrics**: 80% download completion rate

### User Experience Flow Details

#### Onboarding Experience
1. **First Impression**: Clean landing page explaining dual-sided value
2. **Role Clarity**: Simple toggle between Applicant/Recruiter
3. **Frictionless Signup**: Email/password with optional Google SSO
4. **Instant Value**: Profile creation starts immediately

#### AI-Powered Profiling
1. **Multiple Input Methods**: Upload PDF/DOCX or manual text entry
2. **Intelligent Parsing**: Structured extraction of experience, skills, education
3. **Preview & Edit**: ATS-style live preview with manual corrections
4. **Progressive Enhancement**: Start simple, improve over time

#### Personalized Generation
1. **Context-Aware**: JD requirements drive content structure
2. **Multi-Agent Processing**: Specialized agents handle different aspects
3. **Real-Time Feedback**: Immediate match scores and suggestions
4. **A/B Testing**: Multiple output options for user preference

#### Optimization Features
1. **Data-Driven Insights**: Analytics on keyword matching, gaps
2. **Actionable Suggestions**: Specific improvements with examples
3. **Iterative Refinement**: Quick regeneration with new inputs
4. **Progress Tracking**: Visual history of optimization over time

#### Success Transition
1. **Professional Export**: High-quality PDF generation
2. **Application Tracking**: History of generation attempts
3. **Confidence Metrics**: Success indicators and benchmarks
4. **Community Comparison**: Anonymous benchmarking features

### Critical User Experience Design Principles

#### Information Architecture
- **Progressive Disclosure**: Show essential info first, reveal details on demand
- **Contextual Help**: Tooltips and guidance for complex features
- **Clear Navigation**: Intuitive flow between major function areas

#### Performance Expectations
- **Immediate Feedback**: Instant responses for all user actions
- **Progress Indicators**: Clear loading states for AI operations
- **Error Recovery**: Helpful error messages with recovery paths
- **Offline Capability**: Basic functionality without connection

#### Accessibility Standards
- **WCAG Compliant**: Full keyboard navigation and screen reader support
- **Multiple Formats**: Support for different resume formats worldwide
- **Language Options**: Clear UI with minimal text dependencies
- **Mobile Responsive**: Full functionality on all device sizes

#### Engagement Features
- **Gamification**: Progress badges, achievement milestones
- **Social Proof**: Success stories, testimonials intercom
- **Personalization**: Remembered preferences and recent activity
- **Proactive Help**: Contextual tips based on user behavior

### Technical Flow Integration

#### Frontend State Management
```
User Action → UI Update → API Call → LangChain Agents → Response → UI Update
```

#### Data Persistence Layers
```
Local Storage → Supabase Auth → PostgreSQL Tables → Real-time Updates
```

#### AI Processing Pipeline
```
Input Processing → Document Parsing → LLM Analysis → Content Generation → Quality Validation
