# 🚀 **MisterHR** - AI-Powered Hiring Platform

*Two-sided AI assistant that transforms resume optimization and candidate screening*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.0-000000.svg)](https://nextjs.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-1a73e8.svg)](https://langchain.com/)
[![Supabase](https://img.shields.io/badge/Supabase-2.0.3-3ecf8e.svg)](https://supabase.com/)

---

## 📋 **Table of Contents**
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ **Features**

### 🧑‍💼 **For Job Applicants**
- **📄 Smart Resume Parsing** - Extract structured data from PDF/DOCX resumes
- **🎯 Tailored Resume Generation** - AI-powered optimization for specific job descriptions
- **📊 Feedback Dashboard** - Real-time match scores, strengths, and improvement suggestions
- **🌐 Online Portfolio Verification** - GitHub, LinkedIn, and portfolio validation
- **📈 Application Tracking** - History and performance analytics

### 👔 **For Recruiters**
- **🎯 Job Requirements Analysis** - AI extraction of key skills and criteria
- **⚡ Batch Resume Processing** - 50+ resume screening simultaneously
- **📋 Intelligent Candidate Ranking** - Multi-factor fit scoring and summarization
- **🕒 Time Savings** - Reduce screening time by 70%
- **📊 Analytics Dashboard** - Hiring pipeline and candidate insights

### 🤖 **AI Agent Architecture**
- **8 Specialized Agents** - Multi-agent LangChain orchestration
- **Rule-Based + LLM Enhancement** - Immediate functionality with AI upgrades
- **Real-Time Processing** - Async operations for scalability
- **Error Resilience** - Graceful degradation and retry logic

---

## 🏗️ **Architecture**

### **System Overview**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   Next.js       │◄──►│   FastAPI       │◄──►│   Supabase      │
│   TypeScript    │    │   LangChain     │    │   PostgreSQL    │
│   Vercel        │    │   Railway       │    │   RLS Security  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │  AI Agents      │    │  External APIs  │    │   File Storage  │
    │  Multi-Agent    │    │  LLM Services   │    │   Secure Upload │
    │  Orchestration  │    │  Rate Limited   │    │   URL Access    │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **AI Agent Ecosystem**
| Agent | Purpose | Implementation | Status |
|-------|---------|----------------|--------|
| **ResumeParserAgent** | Parse CV data into 8 categories | Rule-based NLP | ✅ Complete |
| **WebEnrichmentAgent** | Verify GitHub, LinkedIn, portfolio | External APIs | 🔄 In Progress |
| **JDAnalyzerAgent** | Extract job requirements | LLM + NLP | ⏳ Planned |
| **MatchingAgent** | Calculate candidate-job fit | Semantic similarity | ⏳ Planned |
| **ContentGeneratorAgent** | Tailored resume/cover letter | LLM writing | ⏳ Planned |
| **FeedbackAgent** | Optimization suggestions | LLM analysis | ⏳ Planned |
| **VerificationAgent** | Skills validation & cross-check | Rule + API | ⏳ Planned |
| **BatchProcessingAgent** | Multi-resume orchestration | Async coordination | ⏳ Planned |

### **Technology Stack**

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Frontend** | Next.js + React + TypeScript | 14+ | Modern web application |
| **Backend** | FastAPI + Python | 3.10+ | High-performance API |
| **Database** | Supabase + PostgreSQL | - | Secure data management |
| **AI Framework** | LangChain | 0.1.0 | Multi-agent orchestration |
| **LLM Service** | OpenAI GPT-4 | - | Advanced AI capabilities |
| **File Processing** | PyMuPDF + spaCy | - | Document parsing |
| **Deployment** | Vercel + Railway | - | Scalable hosting |
| **Authentication** | Supabase Auth | - | Secure user management |

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.10 or higher
- Node.js 18+ and npm
- Git
- Virtual environment (recommended)

### **Local Development Setup**

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/misterhr.git
   cd misterhr
   ```

2. **Backend Setup**
   ```bash
   # Create Python virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Start development server
   cd backend
   python main.py
   ```
   Server will start at: http://127.0.0.1:8000
 
3. **Frontend Setup** (Parallel Terminal)
   ```bash
   cd frontend

   # Install dependencies
   npm install

   # Start development server
   npm run dev
   ```
   Frontend will be available at: http://localhost:3000

4. **Database Setup**
   - Create Supabase project at [supabase.com](https://supabase.com)
   - Copy database URL and API keys to `.env` file
   - Run database migrations (coming soon)

### **Environment Configuration**

Copy `.env` and configure your environment variables:
```bash
# Database
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key

# AI (Optional - for premium features)
OPENAI_API_KEY=your_openai_key

# Application
SECRET_KEY=generate_secure_random_key
```

### **Test Installation**

Visit http://127.0.0.1:8000 to verify backend is running:
```json
{
  "status": "healthy",
  "message": "MisterHR AI platform is running",
  "version": "1.0.0"
}
```

---

## 📚 **Documentation**

### **Architecture Diagrams**
Located in `diagrams/` directory:
- [System Architecture](diagrams/system-architecture.md)
- [AI Agent Orchestration](diagrams/ai-agent-orchestration.md)
- [Applicant User Journey](diagrams/user-journey-applicant.md)
- [Recruiter User Journey](diagrams/user-journey-recruiter.md)
- [Database Schema](diagrams/database-schema.md)

### **Development**
- [Build Process](BuildProcess.md) - Detailed development timeline
- [Product Requirements](PRD.md) - MVP specifications
- [Contributing Guidelines](CONTRIBUTING.md) - Development workflow

---

## 🧪 **Testing**

### **Backend Tests**
```bash
cd backend
pytest tests/ -v --cov=. --cov-report=html
```

### **Frontend Tests**
```bash
cd frontend
npm test
```

### **Integration Tests**
```bash
# Full system integration (coming soon)
npm run test:e2e
```

---

## 🚀 **Deployment**

### **Production Setup**

1. **Database**: Set up Supabase production instance
2. **Backend**: Deploy to Railway or similar
3. **Frontend**: Deploy to Vercel with build commands
4. **Environment**: Configure production environment variables
5. **Monitoring**: Set up logging and error tracking

### **Deployment Commands**
```bash
# Backend deployment
railway deploy

# Frontend deployment
vercel --prod
```

---

## 🤝 **Contributing**

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

### **Development Workflow**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Code Standards**
- **Backend**: Follow PEP 8, use type hints, maintain 90%+ test coverage
- **Frontend**: ESLint, Prettier, component-based architecture
- **Documentation**: All features must be documented
- **Security**: No sensitive data in commits, proper error handling

---

## 📊 **Project Status**

### **Current Progress**
- ✅ **Phase 1**: Foundation Setup - 100% Complete
- 🔄 **Phase 2**: Core AI Development - 25% Complete
- ⏳ **Phase 3**: Applicant Features - Not Started
- ⏳ **Phase 4**: Recruiter Features - Not Started
- ⏳ **Phase 5**: Testing & Deployment - Not Started

### **Milestones**
- **Week 1**: Project setup and foundation ✅
- **Week 2**: AI agents and resume parsing (Current)
- **Week 3**: Basic AI integration and testing
- **Week 4**: Applicant UI and user experience
- **Week 5**: Recruiter features and batch processing
- **Week 6**: Full system integration
- **Week 7**: Quality assurance and optimization
- **Week 8**: Production deployment and launch

---

## 🎯 **Roadmap**

### **Immediate (Q4 2024)**
- ✅ Resume parsing and analysis
- 🔄 Multi-format CV processing
- ⏳ Online portfolio verification
- ⏳ Basic candidate-job matching

### **Short Term (Q1 2025)**
- AI-powered resume tailoring
- Recruiter batch processing
- Real-time feedback dashboard
- Job description intelligence

### **Medium Term (Q2 2025)**
- Advanced LLM integration
- Multi-language support
- Job board integrations
- Advanced analytics

### **Long Term (2025+)**
- AI chat assistants
- Collaborative recruitment
- Predictive hiring analytics
- Mobile application

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 **Team & Support**

### **Core Contributors**
- **AI Engineer**: Claude (Anthropic) - Multi-agent architecture & implementation
- **Lead Developer**: @yourusername - Full-stack development
- **Product Designer**: UI/UX architecture and user experience

### **Getting Help**
- 📧 **Email**: your.email@example.com
- 💬 **Issues**: [GitHub Issues](https://github.com/yourusername/misterhr/issues)
- 📖 **Discussions**: [GitHub Discussions](https://github.com/yourusername/misterhr/discussions)

### **Community**
- 🌟 **Star** this repo if you find it useful!
- 🔗 **Follow** for updates on AI-powered recruitment
- 🤝 **Contribute** to make MisterHR even better

---

## 🙏 **Acknowledgments**

- **LangChain** for multi-agent orchestration framework
- **FastAPI** for high-performance Python APIs
- **Supabase** for secure database and authentication
- **OpenAI** for advanced AI capabilities
- **Next.js** community for modern React framework

---

# ⚡ **Quick Demo**

Want to see MisterHR in action? Check out our interactive demo:

```bash
# Parse a sample resume
curl -X POST "http://127.0.0.1:8000/api/parse-resume" \
  -H "Content-Type: application/json" \
  -d '{"content": "John Smith, Senior Developer at Tech Corp..."}'
```

**Built with ❤️ using cutting-edge AI to revolutionize hiring** ✨
