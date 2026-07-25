# SmartHire AI — ENVIRONMENT.md (Day 3)

## Tools Installed on This Machine
| Tool | Version | Purpose |
|---|---|---|
| Node.js | v24.18.0 | JavaScript runtime for both frontend build tools and backend server |
| npm | (bundled with Node) | Package manager — installs all project dependencies |
| Git | 2.55.0 | Version control, connects project to GitHub |
| VS Code | latest | Code editor with integrated terminal |

## Environment Variables

### server/.env (created Day 3 — NEVER committed to Git)
```
PORT=5000
```

### server/.env (will be extended on Day 4)
```
PORT=5000
GEMINI_API_KEY=your_key_here
AI_PROVIDER=gemini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=smarthire_ai
```

### server/.env.example (safe to commit — no real values)
```
PORT=5000
GEMINI_API_KEY=
AI_PROVIDER=gemini
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
```

## Why .env is gitignored
`.env` contains real secrets (API keys, database passwords). If pushed to GitHub, anyone could see and misuse them. `.env.example` shows what variables are needed without exposing real values — this is standard practice in every professional codebase.

## Ports Used
| Port | Used By |
|---|---|
| 5173 | React dev server (Vite default) |
| 5000 | Express backend API |
| 3306 | MySQL (default, used from Day 4) |
