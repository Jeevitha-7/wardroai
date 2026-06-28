# 👗 WardroAI – Offline AI Fashion Wardrobe Analyzer

## Problem Statement

People often struggle to organize their wardrobes and understand the details of their clothing collection. Existing fashion AI applications mostly rely on cloud services and internet connectivity.

WardroAI is an offline-first, CPU-powered AI application that converts unstructured clothing images into structured wardrobe data.

---

## Features

- Upload clothing images
- Detect clothing category
- Detect dominant color
- Detect pattern
- Predict occasion
- Predict season
- Generate structured JSON output
- Visualize outfit combinations
- Store wardrobe locally

---

## Input

- JPG
- PNG
- Clothing photographs

---

## Example Structured Output

```json
{
  "category": "Kurti",
  "color": "Blue",
  "pattern": "Floral",
  "occasion": "Casual",
  "season": "Summer",
  "confidence": 95.6
}
```

---

## Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Runtime
- ONNX Runtime CPU

### Libraries
- OpenCV
- Pillow
- NumPy

### Database
- SQLite

---

## Compliance

✅ CPU First  
✅ Offline First  
✅ Open Source  
✅ Structured Output