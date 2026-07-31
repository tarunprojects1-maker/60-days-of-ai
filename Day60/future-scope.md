# SmartHire AI — Future Scope

## Next 3 Months
- **Authentication** — candidate accounts (save resume history, track score improvement over time) and recruiter login (private dashboards per organization)
- **Job Role Recommendations** — complete the stretch feature scoped but not built in v1.0: AI-suggested roles based on extracted skills
- **Resume versioning** — let candidates re-analyze an updated resume and see score deltas
- **Rate limiting & abuse protection** — now that the app is public, add basic request throttling on `/api/analyze` to protect the Groq quota and prevent spam

## Next 6 Months
- **Applicant Tracking Pipeline** — recruiter-side stages (Applied → Screened → Interview → Offer), matching the v2.0 scope defined in the original PRD
- **Job postings + matching** — recruiters post roles, candidates get matched based on their analyzed resume
- **Multi-provider AI switch UI** — expose the existing adapter architecture (built Day 2, proven when we swapped Gemini → Groq) as a user-facing setting, not just a backend config
- **Export reports** — downloadable PDF version of the AI analysis report

## Next 12 Months
- **Team/organization accounts** for recruiters with multiple seats
- **Analytics dashboard** — hiring funnel metrics, average candidate quality trends
- **Mobile app** or PWA support
- **Paid tier** — always-on hosting (eliminating the current Render cold-start), higher AI usage limits, premium features like resume export and job matching

## Technical Debt to Address
- Move off Render/Netlify free tier for reliability (no cold starts) if the project gains real users
- Add automated tests (currently manual QA only — appropriate for a 10-day sprint, not for long-term maintenance)
- Tighten CORS policy from permissive to strictly origin-locked
