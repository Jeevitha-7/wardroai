# WardroAI Specification

## Objective

Convert unstructured fashion images into structured wardrobe information while running completely offline on CPU.

---

## Input

- Clothing Images
- JPG
- PNG

---

## Processing Pipeline

Image Upload
↓
Image Processing
↓
Clothing Classification
↓
Color Extraction
↓
Pattern Detection
↓
Occasion Prediction
↓
Season Prediction
↓
JSON Generation

---

## Output Schema

{
    "item_id":1,
    "category":"Kurti",
    "color":"Blue",
    "pattern":"Floral",
    "occasion":"Casual",
    "season":"Summer",
    "confidence":95.6
}

---

## Runtime

- Python
- Streamlit
- ONNX Runtime CPU
- OpenCV
- SQLite

---

## Constraints

- CPU only
- Offline only
- No cloud APIs