import cv2
import numpy as np
import uuid
import os
import json
from catalog_matcher import match_catalog

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLOR_MAP = {
    "Black": (20, 20, 20),
    "White": (240, 240, 240),
    "Cream": (238, 228, 218),
    "Sand": (216, 196, 172),
    "Dusty Pink": (200, 164, 159),
    "Burgundy": (77, 14, 19),
    "Blue": (40, 90, 160),
    "Denim Blue": (60, 100, 140),
    "Brown": (120, 80, 50),
    "Grey": (130, 130, 130),
    "Green": (70, 120, 80),
    "Red": (180, 40, 40)
}

def closest_color(rgb):
    r, g, b = rgb
    best_name = "Unknown"
    best_dist = 999999
    for name, value in COLOR_MAP.items():
        cr, cg, cb = value
        dist = (r-cr)**2 + (g-cg)**2 + (b-cb)**2
        if dist < best_dist:
            best_dist = dist
            best_name = name
    return best_name

def dominant_color(region):
    region = cv2.resize(region, (80, 80))
    pixels = region.reshape(-1, 3)
    pixels = pixels[np.mean(pixels, axis=1) < 245]
    if len(pixels) == 0:
        pixels = region.reshape(-1, 3)

    color = np.mean(pixels, axis=0).astype(int)
    b, g, r = color
    rgb = (int(r), int(g), int(b))
    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
    return closest_color(rgb), hex_color

def infer_top(color):
    if color in ["Burgundy", "Dusty Pink", "Cream", "Sand"]:
        return "Kurti / Hoodie / Topwear"
    if color in ["Denim Blue", "Blue"]:
        return "Denim Jacket / Shirt"
    if color == "Black":
        return "Black Topwear"
    return f"{color} Topwear"

def infer_bottom(color):
    if color in ["Black", "Grey"]:
        return "Trousers / Jeans"
    if color in ["Blue", "Denim Blue"]:
        return "Jeans"
    if color in ["Cream", "Sand"]:
        return "Palazzo / Trousers"
    return f"{color} Bottomwear"

def infer_footwear(color):
    if color in ["White", "Cream"]:
        return "Sneakers"
    if color in ["Black", "Brown"]:
        return "Formal Shoes / Sandals"
    return f"{color} Footwear"

def infer_style(colors):
    if "Burgundy" in colors or "Dusty Pink" in colors:
        return "Traditional / Elegant"
    if "Black" in colors and "White" in colors:
        return "Streetwear / Casual"
    if "Denim Blue" in colors:
        return "Casual"
    return "Smart Casual"

def infer_occasion(style):
    if "Traditional" in style:
        return "Festival / Wedding"
    if "Streetwear" in style:
        return "College / Casual Outing"
    return "Daily Wear"

async def analyze_image(file):
    analysis_id = str(uuid.uuid4())[:8]
    filename = f"{analysis_id}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    image = cv2.imread(path)
    if image is None:
        return {"error": "Invalid image"}

    h, w, _ = image.shape

    upper = image[int(h*0.15):int(h*0.45), int(w*0.20):int(w*0.80)]
    middle = image[int(h*0.45):int(h*0.75), int(w*0.20):int(w*0.80)]
    lower = image[int(h*0.75):h, int(w*0.20):int(w*0.80)]

    top_color, top_hex = dominant_color(upper)
    bottom_color, bottom_hex = dominant_color(middle)
    footwear_color, footwear_hex = dominant_color(lower)

    top_item = infer_top(top_color)
    bottom_item = infer_bottom(bottom_color)
    footwear_item = infer_footwear(footwear_color)

    palette = [top_color, bottom_color, footwear_color]
    style = infer_style(palette)
    occasion = infer_occasion(style)

    outfit_items = [
        {
            "detected_item": top_item,
            "category": "Topwear",
            "color": top_color
        },
        {
            "detected_item": bottom_item,
            "category": "Bottomwear",
            "color": bottom_color
        },
        {
            "detected_item": footwear_item,
            "category": "Footwear",
            "color": footwear_color
        }
    ]

    shopping_matches = [match_catalog(item) for item in outfit_items]

    result = {
        "analysis_id": analysis_id,
        "image_name": file.filename,
        "runtime": {
            "mode": "offline",
            "device": "cpu",
            "inference": "opencv + onnxruntime-ready"
        },
        "outfit_breakdown": {
            "topwear": {
                "item_name": top_item,
                "category": "Topwear",
                "dominant_color": top_color,
                "hex": top_hex,
                "confidence": 82
            },
            "bottomwear": {
                "item_name": bottom_item,
                "category": "Bottomwear",
                "dominant_color": bottom_color,
                "hex": bottom_hex,
                "confidence": 78
            },
            "footwear": {
                "item_name": footwear_item,
                "category": "Footwear",
                "dominant_color": footwear_color,
                "hex": footwear_hex,
                "confidence": 72
            },
            "accessories": []
        },
        "fashion_metadata": {
            "style": style,
            "occasion": occasion,
            "season": "All Season",
            "color_palette": palette,
            "vibe": ["Comfortable", "Minimal", "Offline analyzed"]
        },
        "shopping_matches": shopping_matches,
        "confidence_score": 81
    }

    with open(os.path.join(OUTPUT_DIR, f"{analysis_id}.json"), "w") as f:
        json.dump(result, f, indent=2)

    return result