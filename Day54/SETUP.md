# SmartHire AI — SETUP.md (Day 3)

## Prerequisites Installed
- Node.js v24.18.0
- Git 2.55.0
- VS Code

## Project Structure Created
```
smarthire-ai/
├── client/     (React + Vite frontend)
├── server/     (Node.js + Express backend)
├── docs/       (planning documents)
├── database/   (schema.sql - to be added Day 4)
└── .gitignore
```

## How to Run Locally

1. Open the `smarthire-ai` folder in VS Code (File → Open Folder)
2. Open a terminal (Terminal → New Terminal)
3. Start the backend:
   ```
   cd server
   node server.js
   ```
   Runs on http://localhost:5000
4. Open a second terminal tab (+ icon), start the frontend:
   ```
   cd client
   npm run dev
   ```
   Runs on http://localhost:5173

## Verification
- Frontend: http://localhost:5173 shows the React + Vite starter page
- Backend: http://localhost:5000/api/health returns `{"status":"ok","message":"SmartHire AI backend is running"}`

## Dependencies Installed

**server/package.json:**
- express — web server framework
- cors — allows frontend to call backend across ports
- dotenv — loads environment variables from .env
- mysql2 — MySQL database driver (used from Day 4)
- multer — handles file uploads (used from Day 4)

**client/**
- React + Vite default dependencies (installed automatically by `npm create vite`)

## Next Step (Day 4)
Real feature implementation begins: resume upload UI, backend parsing, and the first AI-connected endpoint.
