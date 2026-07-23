'''
# SmartHire AI — Database Schema (v1.0)

Single-table design, matching the PRD Section 8 data model exactly. No user accounts (auth is out of scope).

## Table: `candidate_analyses`

```sql
CREATE TABLE candidate_analyses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_name VARCHAR(150) NOT NULL DEFAULT 'Unknown Candidate',
    resume_file_path VARCHAR(255) NULL,
    resume_text LONGTEXT NOT NULL,
    ats_score INT NOT NULL CHECK (ats_score BETWEEN 0 AND 100),
    ats_breakdown JSON NOT NULL,
    resume_summary TEXT NULL,
    strengths JSON NULL,
    improvement_suggestions JSON NOT NULL,
    interview_questions JSON NOT NULL,
    interview_readiness_score INT NOT NULL CHECK (interview_readiness_score BETWEEN 0 AND 100),
    recommended_roles JSON NULL,
    analysis_date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analysis_date ON candidate_analyses (analysis_date DESC);
```

## Field Notes

| Field | Notes |
|---|---|
| `candidate_name` | Extracted from resume text if possible; falls back to a default label |
| `resume_file_path` | NULL when the paste-text fallback was used (no file exists) |
| `resume_text` | Full extracted/pasted text — used as AI context and for re-analysis if needed |
| `ats_breakdown` | JSON: `{ formatting, keywords, structure, clarity }` sub-scores |
| `strengths` | JSON array of short strength statements |
| `improvement_suggestions` | JSON array: `[{ area, issue, recommendation }]` |
| `interview_questions` | JSON array: `[{ category, question, basedOn }]` |
| `recommended_roles` | Nullable — only populated if the v1.1/stretch feature is built |

## Constraints

- `ats_score` and `interview_readiness_score` are constrained to 0–100 at the DB level as a safety net against malformed AI output.
- `resume_text`, `ats_breakdown`, `improvement_suggestions`, `interview_questions` are `NOT NULL` — these are the Must-Have fields; a record without them is not a valid analysis.
- No foreign keys — single-table design, no relationships needed since there are no user/account tables in v1.0.

## Validation Against PRD User Stories

| User Story | Supported By |
|---|---|
| US-01 Upload PDF/DOCX | `resume_file_path`, `resume_text` |
| US-02 ATS score | `ats_score`, `ats_breakdown` |
| US-03 Improvement suggestions | `improvement_suggestions` |
| US-04 Interview questions | `interview_questions` |
| US-05 Readiness score | `interview_readiness_score` |
| US-06 Recruiter candidate list | All fields queryable via `SELECT id, candidate_name, ats_score, interview_readiness_score, analysis_date` |
| US-07 Recruiter full report | `SELECT *` by `id` returns everything needed |

Every user story from the PRD is fully covered by this single table — no missing fields, no unnecessary ones.
'''