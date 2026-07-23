'''

# SmartHire AI — API Design (v1.0)

No authentication on any endpoint (confirmed out of scope in PRD). All responses are JSON.

---

### `GET /api/health`
- **Purpose:** Confirm the server is running
- **Request:** none
- **Response:** `200 { "status": "ok" }`
- **Validation:** none
- **Auth:** none
- **Errors:** none expected

---

### `POST /api/upload`
- **Purpose:** Upload a resume file (PDF/DOCX) and extract its text
- **Request:** `multipart/form-data`, field `resume` (file, max 5MB, .pdf or .docx)
- **Response:** `200 { "resumeText": "...", "filePath": "..." }`
- **Validation:** file type restricted to PDF/DOCX; size ≤ 5MB
- **Auth:** none
- **Errors:**
  - `400 INVALID_FILE_TYPE` — wrong file extension
  - `400 FILE_TOO_LARGE` — exceeds 5MB
  - `422 PARSE_FAILED` — file uploaded but text extraction failed (frontend should show paste-text fallback)

---

### `POST /api/upload/text`
- **Purpose:** Accept manually pasted resume text (fallback path)
- **Request:** `application/json { "resumeText": "..." }`
- **Response:** `200 { "resumeText": "..." }`
- **Validation:** `resumeText` required, minimum 50 characters
- **Auth:** none
- **Errors:** `400 TEXT_TOO_SHORT`

---

### `POST /api/analyze`
- **Purpose:** Run full AI analysis (ATS score, suggestions, interview questions, readiness) and persist the result
- **Request:** `application/json { "resumeText": "...", "candidateName": "...", "resumeFilePath": "..." (optional) }`
- **Response:** `201 { "id": 12, "candidateName": "...", "atsScore": 78, "atsBreakdown": {...}, "resumeSummary": "...", "strengths": [...], "improvementSuggestions": [...], "interviewQuestions": [...], "interviewReadinessScore": 74, "analysisDate": "..." }`
- **Validation:** `resumeText` required, minimum 50 characters
- **Auth:** none
- **Errors:**
  - `400 MISSING_RESUME_TEXT`
  - `502 AI_PROVIDER_ERROR` — Gemini call failed or returned invalid JSON after retry
  - `500 DB_WRITE_ERROR` — analysis succeeded but failed to persist

---

### `GET /api/analysis/:id`
- **Purpose:** Retrieve a single full analysis record (used by candidate Results page and recruiter detail view)
- **Request:** URL param `id` (integer)
- **Response:** `200 { ...full record... }`
- **Validation:** `id` must be a valid integer
- **Auth:** none
- **Errors:**
  - `404 NOT_FOUND` — no record with that id
  - `400 INVALID_ID`

---

### `GET /api/candidates`
- **Purpose:** List all analyzed candidates for the recruiter dashboard (lightweight fields only)
- **Request:** optional query param `limit` (default 50)
- **Response:** `200 { "candidates": [ { "id", "candidateName", "atsScore", "interviewReadinessScore", "analysisDate" }, ... ] }`, sorted by `analysisDate DESC`
- **Validation:** `limit` must be a positive integer if provided
- **Auth:** none
- **Errors:** `500 DB_READ_ERROR`

---

### (Stretch, only if built) `POST /api/recommendations`
- **Purpose:** Generate job role recommendations from resume text
- **Request:** `application/json { "resumeText": "..." }`
- **Response:** `200 { "recommendedRoles": [...] }`
- **Validation:** `resumeText` required
- **Auth:** none
- **Errors:** `502 AI_PROVIDER_ERROR`

---

## Error Response Format (standard across all endpoints)

```json
{
  "error": {
    "code": "PARSE_FAILED",
    "message": "We couldn't read that file. Please paste your resume text instead."
  }
}
```

'''