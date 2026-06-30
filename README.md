# WardroAI

WardroAI is a Streamlit-based offline outfit analyzer. Upload a full outfit image, choose an occasion and styling preference, and the app returns a structured fashion breakdown with detected garment zones, dominant colors, fit scores, local catalog suggestions, and JSON export.

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

## Project Structure

```text
wardroai/
├── app.py
├── backend/
│   ├── analyzer.py
│   ├── catalog_matcher.py
│   ├── database.py
│   ├── data/catalog.json
│   └── requirements.txt
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

## Analysis Notes

WardroAI runs locally. It uses MediaPipe pose landmarks to locate the body when possible, then analyzes topwear, bottomwear, and footwear regions with OpenCV color clustering. If pose landmarks are unavailable, it falls back to proportional image regions.

This is a practical offline analyzer, not a cloud fashion model. Accuracy is best with full-body photos where clothing and footwear are clearly visible.
