# Feature Specification: WardroAI Offline Analyzer

## Summary

WardroAI analyzes outfit photos locally and returns structured wardrobe metadata for review in the Streamlit app.

## User Story

As a WardroAI user, I want to upload an outfit image and receive an offline fashion breakdown so that I can understand garment categories, colors, style fit, and local catalog matches without sending images to a cloud service.

## Functional Requirements

- Accept JPG, JPEG, PNG, and WEBP uploads through the Streamlit interface.
- Detect or estimate topwear, bottomwear, and footwear regions.
- Extract dominant colors and expose color metadata in the result JSON.
- Label outfit style, occasion, season, color harmony, confidence, and outfit score.
- Include local shopping matches from `backend/data/catalog.json`.
- Save analysis history locally in SQLite.
- Export structured JSON for each analysis.

## Constraints

- Must run offline on CPU.
- Must not call cloud image-analysis APIs.
- Must keep Streamlit as the primary user interface.
- Must treat `frontend/` as legacy unless a task explicitly targets it.

## Acceptance Criteria

- `npm start` launches the Streamlit app.
- `npm test` passes.
- `npm run coverage` passes the configured fail-under threshold.
- Uploaded images produce JSON with `outfit_breakdown`, `fashion_metadata`, and `shopping_matches`.
- Documentation examples stay aligned with analyzer output when behavior changes.
