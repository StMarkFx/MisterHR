erDiagram
    users ||--o{ profiles : has
    users ||--o{ jobs : creates
    users ||--o{ applications : submits
    jobs ||--o{ applications : receives
    users {
        uuid id PK
        varchar(255) email UK
        varchar(20) role "applicant|recruiter"
        varchar(255) name
        timestamp created_at
        timestamp updated_at
    }
    profiles {
        uuid id PK
        uuid user_id FK
        jsonb personal_info
        jsonb education
        jsonb experience
        jsonb skills
        jsonb projects
        jsonb certifications
        timestamp created_at
        timestamp updated_at
    }
    jobs {
        uuid id PK
        uuid user_id FK
        varchar(255) title
        text description
        jsonb criteria
        varchar(20) status "active|filled|closed"
        timestamp created_at
        timestamp updated_at
    }
    applications {
        uuid id PK
        uuid applicant_id FK
        uuid job_id FK
        text resume_url
        text cover_letter_url
        jsonb feedback
        varchar(20) status "submitted|reviewed|shortlisted|rejected|offered|hired"
        timestamp created_at
    }
```

# Database Schema - MisterHR

## Core Data Model

### Table Relationships
- **One-to-One**: Users ↔ Profiles (applicant-centric data)
- **One-to-Many**: Users → Jobs (recruiter creates multiple jobs)
- **One-to-Many**: Users → Applications (applicant submits multiple applications)
- **Many-to-One**: Applications ← Jobs (job receives multiple applications)

### Users Table (Authentication & Role Management)
```sql
-- Core user identity and role-based access
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('applicant', 'recruiter')) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Profiles Table (Applicant Profile Data)
```sql
-- Structured resume data with AI-extracted information
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    personal_info JSONB,  -- {name, title, contact, summary}
    education JSONB,      -- [{institution, degree, year, gpa}]
    experience JSONB,     -- [{company, role, dates, achievements, responsibilities}]
    skills JSONB,         -- [{category, skills: [skill, level]}]
    projects JSONB,       -- [{name, description, technologies, link}]
    certifications JSONB, -- [{name, issuer, date, expires}]
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Jobs Table (Recruiter Job Postings)
```sql
-- Job requirements and metadata for AI matching
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    criteria JSONB,       -- {experience, skills, education, salary, location}
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'filled', 'closed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Applications Table (Application Tracking)
```sql
-- Application lifecycle and AI feedback storage
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    applicant_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    resume_url TEXT,      -- Supabase Storage reference
    cover_letter_url TEXT,-- Supabase Storage reference
    feedback JSONB,       -- {match_score, strengths, gaps, suggestions}
    status VARCHAR(20) DEFAULT 'submitted' CHECK (status IN ('submitted', 'reviewed', 'shortlisted', 'rejected', 'offered', 'hired')),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Row Level Security (RLS) Policies

### Users Table Policies
```sql
-- Users can only see/edit their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);
```

### Profiles Table Policies
```sql
-- Only the owner can see/edit their profile
CREATE POLICY "Applicants can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Applicants can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = user_id);

-- Insert policy for profile creation
CREATE POLICY "Applicants can create own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### Jobs Table Policies
```sql
-- Recruiters can see all jobs, but only edit their own
CREATE POLICY "Recruiters can view all jobs" ON jobs
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM users
            WHERE id = auth.uid() AND role = 'recruiter'
        )
    );

CREATE POLICY "Recruiters can edit own jobs" ON jobs
    FOR ALL USING (auth.uid() = user_id);
```

### Applications Table Policies
```sql
-- Complex policy: applicants see their apps, recruiters see apps for their jobs
CREATE POLICY "Users can view relevant applications" ON applications
    FOR SELECT USING (
        auth.uid() = applicant_id OR  -- Applicant sees their applications
        EXISTS (                    -- Recruiter sees applications for their jobs
            SELECT 1 FROM jobs
            WHERE jobs.id = applications.job_id
            AND jobs.user_id = auth.uid()
        )
    );

-- Applicants can create applications, recruiters can update status
CREATE POLICY "Applicants can create applications" ON applications
    FOR INSERT WITH CHECK (auth.uid() = applicant_id);

CREATE POLICY "Recruiters can update application status" ON applications
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM jobs
            WHERE jobs.id = applications.job_id
            AND jobs.user_id = auth.uid()
        )
    );
```

## Index Strategy

### Performance Indexes
```sql
-- Fast user lookups by role
CREATE INDEX idx_users_role ON users(role);

-- Optimize profile queries for applicants
CREATE INDEX idx_profiles_user_id ON profiles(user_id);

-- Fast job listings for recruiters
CREATE INDEX idx_jobs_user_id_status ON jobs(user_id, status);

-- Optimize application queries by job and status
CREATE INDEX idx_applications_job_id_status ON applications(job_id, status);
CREATE INDEX idx_applications_applicant_id ON applications(applicant_id);

-- Partial index for active applications only
CREATE INDEX idx_applications_active ON applications(job_id)
    WHERE status IN ('submitted', 'reviewed', 'shortlisted');
```

### Full-Text Search Indexes
```sql
-- Full-text search on job descriptions
CREATE INDEX idx_jobs_description_gin ON jobs
    USING gin(to_tsvector('english', description));

-- Search optimization for resume content
CREATE INDEX idx_profiles_experience_gin ON profiles
    USING gin(to_tsvector('english', experience::text));

-- Skills search capability
CREATE INDEX idx_profiles_skills_gin ON profiles
    USING gin(to_tsvector('english', skills::text));
```

## Data Migration Strategy

### Schema Versioning
```sql
-- Migration tracking table
CREATE TABLE schema_migrations (
    version VARCHAR(14) PRIMARY KEY, -- Format: YYYYMMDDHHMMSS
    name VARCHAR(255) NOT NULL,
    applied_at TIMESTAMP DEFAULT NOW()
);
```

### Migration Scripts Structure
```
supabase/migrations/
├── 20231201000000_initial_schema.sql
├── 20231202000000_add_indexes.sql
├── 20231203000000_rls_policies.sql
├── 20231204000000_sample_data.sql
└── 20231205000000_performance_optimizations.sql
```

## Data Validation

### JSONB Schema Validation
```sql
-- Function to validate profile data structure
CREATE OR REPLACE FUNCTION validate_profile_data()
RETURNS trigger AS $$
BEGIN
    -- Validate personal_info structure
    IF NOT (NEW.personal_info ? 'name' AND NEW.personal_info ? 'contact') THEN
        RAISE EXCEPTION 'personal_info must contain name and contact';
    END IF;

    -- Validate education array structure
    IF NOT jsonb_typeof(NEW.education) = 'array' THEN
        RAISE EXCEPTION 'education must be an array';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach validation trigger
CREATE TRIGGER validate_profile_data_trigger
    BEFORE INSERT OR UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION validate_profile_data();
```

## Backup and Recovery

### Automated Backups
```sql
-- Daily backup schedule (via pg_cron or external tool)
-- Full database backup every 24 hours
-- Incremental backups every 6 hours
-- Point-in-time recovery capability
```

### Data Retention Policies
```sql
-- Soft delete for applications (mark as deleted, keep for 90 days)
-- Hard delete inactive profiles after 2 years
-- Anonymize personal data after account deletion
-- Audit log retention for 7 years
```

## Monitoring and Alerts

### Key Metrics to Track
- **Table Sizes**: Monitor growth rates for capacity planning
- **Query Performance**: Log slow queries (>100ms)
- **Connection Pool**: Track connection usage and spikes
- **Storage Usage**: Monitor Supabase storage consumption
- **API Latency**: Track database response times

### Alert Conditions
```sql
-- Alert on high connection count
SELECT COUNT(*) > 80% of max_connections;

-- Alert on slow queries
SELECT query_duration > 5000; -- 5 seconds

-- Alert on storage usage
SELECT storage_used_mb > (storage_limit_mb * 0.8);
```

This schema provides a solid foundation for MisterHR's dual-sided AI platform, ensuring data integrity, security, and performance as the application scales.
