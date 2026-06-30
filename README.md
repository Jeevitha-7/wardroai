---
title: WardroAI
emoji: 👕
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.45.1"
app_file: app.py
pinned: false
---

# WardroAI

WardroAI is a Streamlit-based offline outfit analyzer. Upload a full outfit image, choose an occasion and styling preference, and the app returns a structured fashion breakdown with detected garment zones, dominant colors, fit scores, local catalog suggestions, and JSON export.

WardroAI is designed for local-first experimentation. The primary app runs in Streamlit, the analyzer uses CPU-friendly Python image processing, and the product matcher reads from a local catalog file. User images and analysis history stay on the machine unless you explicitly move them elsewhere.

## Features

- Streamlit single-app interface
- Offline CPU image processing
- MediaPipe pose-aware garment zones when a person is detected
- Fallback garment zones for images without reliable pose landmarks
- Topwear, bottomwear, and footwear breakdown
- Dominant color detection with color swatches
- Occasion, style, color harmony, and outfit scoring
- SQLite analysis history
- Local catalog matching
- Downloadable structured JSON

## Requirements

- Python 3.10 or newer
- Node.js 20 or newer
- npm
- A CPU-only local development environment

WardroAI does not require a GPU or cloud image-analysis API.

## Project Structure

```text
wardroai/
├── app.py
├── backend/
│   ├── analyzer.py
│   ├── catalog_matcher.py
│   ├── database.py
│   ├── data/catalog.json
│   ├── main.py
│   └── requirements.txt
├── scripts/
│   └── start_streamlit.py
├── specs/
│   └── wardroai-offline-analyzer/
│       └── spec.md
├── frontend/
│   └── legacy React/Vite files
├── package.json
└── README.md
```

The Streamlit app is now the main application. The old React frontend is kept only as legacy code.

## Setup

From the project root:

```bash
npm run setup
```

If you prefer plain Python commands:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
```

Install Node tooling from the lockfile:

```bash
npm ci
```

## Run

```bash
npm start
```

Open:

```text
http://127.0.0.1:8501
```

Equivalent plain Python command:

```bash
source backend/.venv/bin/activate
streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

## Common Commands

```bash
npm run setup          # create backend virtualenv and install Python dependencies
npm start              # launch Streamlit
npm run lint           # Python compile check and ESLint
npm run lint:biome     # Biome lint
npm run lint:oxlint    # Oxlint for legacy frontend source
npm run lint:knip      # unused dependency/dead code check
npm run format:check   # Prettier formatting check
npm run type_check     # TypeScript type check
npm test               # frontend placeholder test runner and backend unit tests
npm run coverage       # backend coverage report with fail-under threshold
```

## Output

The analyzer returns structured JSON with these main sections:

- `outfit_breakdown`: topwear, bottomwear, footwear, dominant colors, labels, and confidence values
- `fashion_metadata`: style, occasion, season, color harmony, recommendation, and notes
- `shopping_matches`: local catalog matches from `backend/data/catalog.json`
- `runtime`: local execution mode and device details

## Development Workflow

Use the Streamlit app as the source of truth for user-facing behavior. When analyzer behavior changes, update:

- backend tests under `tests/`
- README or user documentation examples
- feature specs under `specs/`
- JSON output expectations where relevant

Spec-driven work should use `.specify/templates/` and store feature specs under `specs/<feature-name>/spec.md`. The project constitution lives at `.specify/memory/constitution.md`.

## Privacy And Offline Behavior

WardroAI should run offline on CPU. Do not add cloud APIs for image analysis. Local SQLite history, generated analysis data, and uploaded images should not be committed to the repository.

## Analysis Notes

WardroAI runs locally. It uses MediaPipe pose landmarks to locate the body when possible, then analyzes topwear, bottomwear, and footwear regions with OpenCV color clustering. If pose landmarks are unavailable, it falls back to proportional image regions.

This is a practical offline analyzer, not a cloud fashion model. Accuracy is best with full-body photos where clothing and footwear are clearly visible.

## Troubleshooting

- If `npm start` cannot find Streamlit, run `npm run setup` again.
- If Python imports fail, activate `backend/.venv` and reinstall `backend/requirements.txt`.
- If a quality gate fails, run the specific command shown in the error output before committing.
