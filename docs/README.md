# MisterHR System Architecture Diagrams

This directory contains comprehensive Mermaid diagrams documenting the MisterHR platform architecture, user journeys, and technical implementation details.

## Available Diagrams

### 1. System Architecture (`system-architecture.md`)
- **Type**: Graph TB (Top-Bottom) layered architecture
- **Content**: Complete system architecture showing frontend, backend, database, AI agents, and external services
- **Purpose**: High-level overview of all system components and their relationships

### 2. AI Agent Orchestration (`ai-agent-orchestration.md`)
- **Type**: Sequence diagram + Documentation
- **Content**: LangChain agent communication flows, synchronous/asynchronous processing patterns
- **Purpose**: Detail AI agent roles, responsibilities, and inter-agent communication

### 3. Applicant User Journey (`user-journey-applicant.md`)
- **Type**: Flowchart TD (Top-Down)
- **Content**: Complete end-to-end experience from onboarding to application success
- **Purpose**: User experience flow for job applicants using the platform

### 4. Recruiter User Journey (`user-journey-recruiter.md`)
- **Type**: Flowchart TD (Top-Down)
- **Content**: Full recruitment workflow from job creation to hire analysis
- **Purpose**: User experience flow for recruiters managing hiring processes

### 5. Database Schema (`database-schema.md`)
- **Type**: Entity Relationship Diagram (erDiagram)
- **Content**: PostgreSQL schema with relationships, row-level security policies, and indexes
- **Purpose**: Data model documentation with security and performance considerations

## How to View Diagrams

### VS Code Preview (Recommended)
1. Install the "Mermaid" extension for VS Code
2. Open any `.md` file in this directory
3. The diagrams will render automatically

### Online Preview
1. Copy the Mermaid source code
2. Paste into [Mermaid Live Editor](https://mermaid.live)
3. View rendered diagrams

### Export to Images
```bash
# Using mmdc (Mermaid CLI)
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.md -o diagram.png
```

## Diagram Standards

### Color Coding
- **Blue (#1976d2)**: Primary actions and user interactions
- **Green (#2e7d32)**: Success states and confirmations
- **Purple (#7b1fa2)**: System processes and backend operations
- **Orange (#f57c00)**: Processing states and analytics

### Accessibility
- All diagrams include alt-text descriptions
- Color-blind friendly color combinations
- Clear labeling and explanations

### Version Control
- Diagrams are version-controlled alongside code
- Updated during architectural changes
- Reviewed as part of technical documentation

## Usage Guidelines

### For Developers
- **Reference Architecture**: Use system-architecture.md for component relationships
- **API Design**: Check user journeys for integration points
- **Database Queries**: Reference schema diagrams for relationship understanding
- **Debugging**: Use sequence diagrams to trace complex flows

### For Stakeholders
- **Product Understanding**: Applicant/Recruiter journeys for feature validation
- **Technical Overview**: System architecture for scope understanding
- **Implementation Status**: Cross-reference with BuildProcess.md

### For New Team Members
- **Onboarding**: Start with system-architecture.md for 10,000-foot view
- **Deep Dive**: Use specific diagrams based on area of focus
- **Architecture Patterns**: Study agent orchestration for multi-agent design

## Contributing

### Diagram Updates
1. Ensure Mermaid syntax is valid
2. Include detailed documentation in markdown
3. Test rendering in multiple environments
4. Update this README if adding new diagrams

### Standards to Maintain
- Consistent color scheme across diagrams
- Clear, descriptive labels
- Comprehensive explanations
- Cross-references to other diagrams

## Integration with Documentation

These diagrams are referenced in:

- **PRD.md**: MVP focus section uses these diagrams
- **BuildProcess.md**: Technical implementation phases reference specific diagrams
- **README.md**: Quick links to architectural overview

---

## Quick Links
- [System Architecture](system-architecture.md)
- [AI Agent Flow](ai-agent-orchestration.md)
- [Applicant Experience](user-journey-applicant.md)
- [Recruiter Workflow](user-journey-recruiter.md)
- [Database Schema](database-schema.md)

**Build Status**: All diagrams are production-ready and reflect the current MVP architecture.
