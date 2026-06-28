# 👗 ClosetIQ – Offline AI Outfit Recommender

> **Build AI that runs anywhere.**
>
> ClosetIQ is an **offline-first**, **CPU-powered AI fashion assistant** that recommends the best outfit from your existing wardrobe based on the occasion and preferred style. It converts wardrobe images into structured clothing data and visualizes the recommended outfit on a mannequin silhouette—all without requiring an internet connection.

---

## 🚀 Problem Statement

People often have a full wardrobe but still struggle to decide what to wear for different occasions. Existing fashion recommendation apps rely heavily on cloud services and online APIs, making them unusable without internet connectivity.

ClosetIQ solves this by providing an **offline AI-powered outfit recommendation system** that works entirely on a laptop or mobile device using CPU inference.

---

## 💡 Solution

ClosetIQ stores your wardrobe locally and analyzes clothing images to create a structured digital wardrobe.

When a user selects:

- 🎉 Occasion
- 👔 Preferred Style
- 🎨 Preferred Color (Optional)

the AI recommends the best outfit from the wardrobe, evaluates how well it matches the occasion, and displays the selected clothes on a mannequin silhouette.

---

## ✨ Features

- ✅ Offline-first (No internet required)
- ✅ CPU-only inference
- ✅ Local wardrobe database
- ✅ AI-powered clothing analysis
- ✅ Outfit recommendation based on occasion
- ✅ Fashion compatibility scoring
- ✅ Color harmony evaluation
- ✅ Style matching
- ✅ Visual outfit preview on mannequin
- ✅ Structured JSON output
- ✅ Export recommendations

---

# 🧠 How It Works

```
Wardrobe Images
        │
        ▼
Offline AI Analysis (CPU)
        │
        ▼
Structured Clothing Metadata
        │
        ▼
SQLite Database
        │
        ▼
User Input
(Occasion + Style)
        │
        ▼
Recommendation Engine
        │
        ▼
Recommended Outfit
        │
        ├────────► Structured JSON
        │
        └────────► Outfit Preview on Mannequin
```

---

# 📥 Input

The wardrobe is already stored locally.

The user only selects:

- Occasion
- Preferred Style
- Preferred Color (Optional)

Example:

```
Occasion : College

Style : Casual

Preferred Color : Blue
```

---

# 📤 Output

## Structured Output

```json
{
  "occasion": "College",
  "requested_style": "Casual",
  "recommended_outfit": {
    "top": "Blue Denim Jacket",
    "inner": "White T-Shirt",
    "bottom": "Black Jeans",
    "footwear": "White Sneakers"
  },
  "fashion_score": 94,
  "occasion_match": 96,
  "style_match": true,
  "color_harmony": "Excellent",
  "confidence": 97,
  "reason": [
    "Suitable for casual college wear",
    "Balanced color combination",
    "Comfortable for long hours"
  ]
}
```

---

## Visual Output

The selected clothes are automatically placed on a mannequin silhouette.

```
        👤
   👕 Denim Jacket
   👔 White T-Shirt
   👖 Black Jeans
   👟 White Sneakers
```

---

# 🛠 Tech Stack

## Frontend

- Streamlit

## Backend

- Python

## AI Runtime

- ONNX Runtime (CPU)

## AI Models

- MobileNetV3
- EfficientNet Lite
- YOLOv8n (ONNX)

## Image Processing

- OpenCV
- Pillow

## Database

- SQLite

## Data Processing

- NumPy
- Pandas

---

# 📁 Project Structure

```
ClosetIQ/
│
├── app/
│   ├── main.py
│   ├── recommendation.py
│   ├── mannequin.py
│   ├── wardrobe.py
│   └── utils.py
│
├── database/
│   └── wardrobe.db
│
├── models/
│   ├── mobilenet.onnx
│   └── efficientnet.onnx
│
├── assets/
│   ├── wardrobe/
│   ├── mannequin/
│   └── icons/
│
├── output/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://gitlab.com/your-username/closetiq.git
cd closetiq
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app/main.py
```

---

# 📸 Demo Workflow

1. Store wardrobe images locally.
2. AI extracts clothing metadata.
3. User selects occasion and preferred style.
4. Recommendation engine finds the best outfit.
5. Outfit is displayed on a mannequin silhouette.
6. JSON report is generated.
7. User can export the recommendation.

---

# 🎯 Hackathon Compatibility

✔ CPU-First

- Runs entirely on CPU
- No CUDA
- No GPU required

✔ Offline-First

- No cloud APIs
- No internet required
- All models stored locally

✔ Structured Output

Converts clothing images into structured metadata and recommendation reports.

✔ Open Source

Licensed under GNU AGPL v3.0.

---

# 🚀 Future Enhancements

- Weather-aware outfit recommendations
- Seasonal wardrobe suggestions
- Duplicate clothing detection
- Capsule wardrobe generation
- Laundry reminders
- Personalized fashion learning
- Multi-user wardrobe profiles
- Mobile (Android) version
- Voice-based outfit selection

---

# 👥 Team

Team Name: **[Your Team Name]**

Members

- jyotsna
- jeevitha

---

# 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the `LICENSE` file for details.

---

## ⭐ Why ClosetIQ?

ClosetIQ demonstrates that **AI can be practical, private, and powerful without relying on the cloud.** By combining offline computer vision, structured data extraction, and intelligent outfit recommendations, it showcases a real-world application of CPU-first AI that works anytime, anywhere—even with the Wi-Fi turned off.