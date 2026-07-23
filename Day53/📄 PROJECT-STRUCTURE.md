'''
markdown
# SmartHire AI — Project Structure (v1.0)

smarthire-ai/
├── client/ # React frontend (Vite)
│ ├── src/
│ │ ├── pages/
│ │ │ ├── UploadPage.jsx
│ │ │ ├── ResultsPage.jsx
│ │ │ ├── RecruiterDashboard.jsx
│ │ │ └── RecruiterCandidateDetail.jsx
│ │ ├── components/
│ │ │ ├── FileDropzone.jsx
│ │ │ ├── PasteTextFallback.jsx
│ │ │ ├── ATSScoreCard.jsx
│ │ │ ├── ScoreBreakdown.jsx
│ │ │ ├── SuggestionsList.jsx
│ │ │ ├── SuggestionCard.jsx
│ │ │ ├── InterviewQuestionsList.jsx
│ │ │ ├── ReadinessScoreBadge.jsx
│ │ │ ├── CandidateCard.jsx
│ │ │ └── NavHeader.jsx
│ │ ├── services/
│ │ │ └── api.js
│ │ ├── App.jsx
│ │ └── main.jsx
│ ├── .env.example
│ └── package.json
│
├── server/ # Node.js + Express backend
│ ├── routes/
│ │ ├── health.js
│ │ ├── upload.js
│ │ ├── analysis.js
│ │ └── candidates.js
│ ├── controllers/
│ │ ├── analysisController.js
│ │ └── candidatesController.js
│ ├── services/
│ │ ├── resumeParser.js
│ │ ├── readinessScore.js
│ │ └── ai/
│ │ ├── aiProvider.js
│ │ └── geminiAdapter.js
│ ├── config/
│ │ └── db.js
│ ├── uploads/ # gitignored
│ ├── .env.example
│ ├── server.js
│ └── package.json
│
├── database/
│ └── schema.sql
│
├── docs/
│ ├── PRD.docx
│ ├── Implementation_Blueprint.docx
│ ├── Pitch_Deck.pptx
│ ├── ARCHITECTURE.md
│ ├── SCHEMA.md
│ ├── API.md
│ ├── UI-WIREFRAMES.md
│ └── PROJECT-STRUCTURE.md
│
├── .gitignore
└── README.md


## Why this structure

- **`client/` and `server/` are fully separated** — matches the React + Express architecture, allows independent deployment if needed.
- **`services/ai/` isolates the AI provider** — only this folder changes if you ever swap Gemini for Claude/OpenAI.
- **`routes/` vs `controllers/`** — routes map URLs to functions; controllers hold the logic. Keeps `server.js` clean.
- **`docs/` centralizes every planning artifact** — full project context in one place.
- **No `models/` folder in v1.0** — single table, no ORM, raw SQL is simpler and sufficient for this scope.
'''