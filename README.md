# LexLabor AI

A small Flask app that helps employees document, understand, and escalate workplace
issues using an AI model (via [Groq](https://groq.com/)). It's a single-page frontend
(`templates/index.html`, using Tailwind CSS + Alpine.js from CDNs — no build step)
talking to a small set of Flask API routes (`api/index.py`).

## Features

- **Incident Auditor** (`/api/audit`) — describe what happened, get back likely
  labor-law violations, a severity rating, and relevant filing deadlines.
- **Escalation Architect** (`/api/escalate`) — generates a formal grievance letter
  draft for a chosen target (HR, a labor bureau, a lawyer) plus a list of evidence
  you're still missing.
- **Policy De-Obfuscator** (`/api/deobfuscate`) — paste dense handbook/policy text,
  get a plain-English translation and any hidden risks called out.
- **Timeline Generator** (`/api/timeline`) — turn a messy, unordered description of
  events into a clean chronological timeline.
- **Panic Mode** — press `Esc` anywhere to instantly swap the app for a fake
  spreadsheet, in case you need to look busy. Press `Esc` again (or the "Resume
  Work" button) to go back.

## Project structure

```
api/
  index.py          # Flask app: serves the page and the 4 API routes
templates/
  index.html         # The entire frontend (single page, Alpine.js + Tailwind)
requirements.txt      # Python dependencies
.env                   # Local secrets (never committed - see below)
```

## Setup

1. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   venv\Scripts\activate        # on Windows
   # source venv/bin/activate   # on macOS/Linux
   pip install -r requirements.txt
   ```

2. **Add your Groq API key.** Get a free key at [console.groq.com](https://console.groq.com/),
   then create/edit `.env` in the project root so it contains:

   ```
   GROQ_API_KEY=your_key_here
   ```

   `.env` is listed in `.gitignore` so it will never be committed.

3. **Run the app locally:**

   ```bash
   python api/index.py
   ```

   Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Deploying

The `api/` folder layout is set up for [Vercel](https://vercel.com/)'s Python
serverless functions. When deploying there, set `GROQ_API_KEY` as an environment
variable in the Vercel project settings instead of using `.env`.

## Notes

- This app has no authentication or rate limiting — anyone who can reach a
  deployed instance can use your Groq API quota. Fine for local/personal use;
  add auth before sharing a public deployment.
- Errors from the AI/API layer are currently returned to the browser as raw
  exception text. That's convenient for local debugging but worth tightening
  up before a public deployment.
