# WardroAI Offline Analyzer Spec

## Objective

Analyze outfit images locally and produce structured wardrobe metadata.

## Requirements

- Accept JPG, JPEG, PNG, and WEBP uploads.
- Detect topwear, bottomwear, and footwear regions.
- Extract dominant colors.
- Predict style and occasion fit.
- Include Indian outfit labels such as blouse, skirt, and lehenga.
- Save analysis history locally in SQLite.
- Export structured JSON.

## Non-Goals

- Cloud image analysis
- GPU-only model inference
- Online shopping checkout

## Acceptance Checks

- `npm start` launches the Streamlit app.
- `npm test` passes.
- Uploaded images produce a JSON result with outfit breakdown fields.
