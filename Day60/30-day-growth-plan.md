# SmartHire AI — 30-Day Growth Plan

Each day builds on the previous. Use the companion `daily-build-prompt.md` each day, replacing only the day number.

**Week 1: Authentication Foundation**
- Day 1: Design auth schema (candidates + recruiters tables), plan JWT vs session approach
- Day 2: Implement candidate signup/login API endpoints
- Day 3: Implement recruiter signup/login API endpoints
- Day 4: Build frontend auth forms (login/signup pages)
- Day 5: Add protected routes + auth context in React
- Day 6: Migrate existing analyses to be linked to candidate accounts
- Day 7: Test full auth flow end-to-end, fix bugs

**Week 2: Candidate History & Job Recommendations**
- Day 8: Build "My Analyses" history page for logged-in candidates
- Day 9: Add resume re-analysis with score-delta comparison
- Day 10: Design job recommendation data model (target roles/skills mapping)
- Day 11: Build `generateJobRecommendations()` AI adapter function
- Day 12: Add recommendations section to Results page
- Day 13: Add recommendation caching to reduce AI calls
- Day 14: Test and polish job recommendations feature

**Week 3: Recruiter Pipeline**
- Day 15: Design applicant pipeline schema (status stages)
- Day 16: Build recruiter login-gated dashboard (replacing public access)
- Day 17: Add pipeline stage management API
- Day 18: Build drag-or-click stage transition UI
- Day 19: Add recruiter notes per candidate
- Day 20: Add candidate search/filter on recruiter dashboard
- Day 21: Test full recruiter workflow end-to-end

**Week 4: Production Hardening & Launch Prep**
- Day 22: Add rate limiting to `/api/analyze` (protect AI quota)
- Day 23: Move off free-tier hosting cold-starts — evaluate paid tier or alternative always-on free option
- Day 24: Add automated backend tests (Jest) for core routes
- Day 25: Add PDF export for analysis reports
- Day 26: Full accessibility audit (WCAG AA pass)
- Day 27: Performance audit (Lighthouse), optimize bundle size
- Day 28: Security audit (dependency scan, tighten CORS)
- Day 29: Update all documentation (README, PRD, architecture docs) to reflect v2.0 scope
- Day 30: Tag and release v2.0.0, write launch retrospective
