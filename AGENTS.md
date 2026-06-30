# Agent Guide

This repository contains WardroAI, a Streamlit-first offline fashion analysis app.

## Project Rules

- Preserve offline CPU execution.
- Do not introduce cloud APIs for image analysis.
- Keep the Streamlit app as the primary user interface.
- Treat `frontend/` as legacy React/Vite code unless a task explicitly asks for it.
- Do not commit `backend/.venv`, generated caches, local databases, or build output.

## Useful Commands

```bash
npm run setup
npm start
npm run lint
npm test
```

## Key Files

- `app.py`: main Streamlit UI
- `backend/analyzer.py`: image analysis and outfit labeling
- `backend/catalog_matcher.py`: local product matching
- `backend/database.py`: SQLite history
- `scripts/start_streamlit.py`: robust `npm start` launcher

## Change Notes

When changing analyzer behavior, update tests and documentation examples so app behavior, JSON output, and user guidance stay aligned.
