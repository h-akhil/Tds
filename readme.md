# LLM Analysis Quiz — Starter Skeleton

## Purpose
Small Flask app that accepts POSTs from the grader, validates `secret`, visits provided `url` (JavaScript pages supported using Playwright), computes answers with heuristics, and posts results.

## Setup (local)
1. Create venv:
   python -m venv .venv
   source .venv/bin/activate

2. Install deps:
   pip install -r requirements.txt
   python -m playwright install

3. Set environment variables (example):
   export QUIZ_SECRET="your_secret_here"
   export API_KEY=""   # optional
   export PORT=8000

4. Run:
   python app.py

## Docker
Build:
  docker build -t tds-quiz-solver .

Run:
  docker run -e QUIZ_SECRET="your_secret_here" -p 8000:8000 tds-quiz-solver

## Notes & Next steps
- Replace `compute_answer_for_page()` with robust logic:
  - If PDF needs reading: download and use pdfplumber/camelot.
  - For images/scan: use pytesseract.
  - For CSV/Excel: pandas.
- Use durable logging, better error handling, and metrics.
- Never commit secrets. Use environment variables or secret management.

