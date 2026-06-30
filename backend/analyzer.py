import os
import tempfile
import uuid
from dataclasses import dataclass

import cv2
import numpy as np

try:
    from .catalog_matcher import match_catalog
except ImportError:  # pragma: no cover - supports running from backend/ directly
    from catalog_matcher import match_catalog

os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "wardroai-matplotlib"))

try:
    import mediapipe as mp
except ImportError:  # pragma: no cover - optional at runtime
    mp = None


COLOR_PALETTE = {
    "Black": (20, 20, 20),
    "Charcoal": (55, 55, 58),
    "White": (245, 245, 245),
    "Gray": (135, 135, 135),
    "Cream": (236, 224, 198),
    "Beige": (205, 184, 145),
    "Red": (190, 45, 45),
    "Burgundy": (126, 20, 45),
    "Pink": (220, 130, 165),
    "Blue": (45, 95, 185),
    "Denim Blue": (70, 110, 160),
    "Navy": (24, 42, 86),
    "Green": (55, 135, 78),
    "Olive": (105, 120, 62),
    "Brown": (120, 78, 48),
    "Yellow": (218, 182, 48),
}


STYLE_ITEM_TYPES = {
    "Casual": {
        "Topwear": "T-shirt / casual top",
        "Bottomwear": "jeans / casual bottom",
        "Footwear": "sneakers / casual shoes",
    },
    "Streetwear": {
        "Topwear": "oversized top / jacket",
        "Bottomwear": "cargo pants / dark trousers",
        "Footwear": "sneakers / boots",
    },
    "Formal": {
        "Topwear": "shirt / blouse",
        "Bottomwear": "formal trousers / skirt",
        "Footwear": "formal shoes",
    },
    "Traditional": {
        "Topwear": "kurti / blouse",
        "Bottomwear": "palazzo pants / skirt / lehenga",
        "Footwear": "sandals / flats",
    },
    "Indian": {
        "Topwear": "blouse / kurti",
        "Bottomwear": "lehenga / skirt",
        "Footwear": "sandals / flats",
    },
    "Athleisure": {
        "Topwear": "active top / hoodie",
        "Bottomwear": "joggers / leggings",
        "Footwear": "trainers",
    },
}


TOPWEAR_TYPES = {
    "Traditional": "kurti",
    "Indian": "blouse",
    "Formal": "shirt",
    "Streetwear": "jacket",
    "Athleisure": "active top",
    "Casual": "T-shirt",
}


BOTTOMWEAR_TYPES = {
    "Traditional": "palazzo pants",
    "Indian": "lehenga",
    "Formal": "formal trousers",
    "Streetwear": "cargo pants",
    "Athleisure": "joggers",
    "Casual": "jeans",
}


OCCASION_STYLE_FIT = {
    "College": {"Casual": 95, "Streetwear": 88, "Athleisure": 78, "Traditional": 70, "Indian": 72, "Formal": 62},
    "Office": {"Formal": 94, "Casual": 72, "Traditional": 78, "Indian": 76, "Streetwear": 54, "Athleisure": 46},
    "Party": {"Streetwear": 86, "Formal": 82, "Traditional": 80, "Indian": 88, "Casual": 74, "Athleisure": 52},
    "Wedding": {"Traditional": 96, "Indian": 98, "Formal": 86, "Casual": 48, "Streetwear": 42, "Athleisure": 30},
    "Travel": {"Casual": 88, "Athleisure": 86, "Streetwear": 74, "Traditional": 62, "Indian": 60, "Formal": 50},
    "Workout": {"Athleisure": 96, "Casual": 62, "Streetwear": 50, "Formal": 20, "Traditional": 18, "Indian": 16},
}


@dataclass
class Region:
    name: str
    box: tuple[int, int, int, int]
    confidence: int


def decode_image(contents):
    image_array = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Uploaded file is not a valid image")
    return image


def clip_box(box, width, height):
    x1, y1, x2, y2 = box
    x1 = max(0, min(width - 1, int(x1)))
    y1 = max(0, min(height - 1, int(y1)))
    x2 = max(x1 + 1, min(width, int(x2)))
    y2 = max(y1 + 1, min(height, int(y2)))
    return x1, y1, x2, y2


def fallback_regions(width, height):
    left = int(width * 0.18)
    right = int(width * 0.82)
    return {
        "Topwear": Region("Topwear", clip_box((left, height * 0.12, right, height * 0.46), width, height), 58),
        "Bottomwear": Region("Bottomwear", clip_box((left, height * 0.43, right, height * 0.78), width, height), 56),
        "Footwear": Region("Footwear", clip_box((left, height * 0.76, right, height * 0.98), width, height), 50),
    }


def landmark_xy(landmarks, index, width, height):
    point = landmarks[index]
    return np.array([point.x * width, point.y * height])


def pose_regions(image):
    height, width = image.shape[:2]
    if mp is None or not hasattr(mp, "solutions") or not hasattr(mp.solutions, "pose"):
        return fallback_regions(width, height), "fallback-zones"

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    try:
        pose = mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False)
        result = pose.process(rgb)
        pose.close()
    except Exception:
        return fallback_regions(width, height), "fallback-zones"

    if not result.pose_landmarks:
        return fallback_regions(width, height), "fallback-zones"

    landmarks = result.pose_landmarks.landmark
    pose_enum = mp.solutions.pose.PoseLandmark
    required = [
        pose_enum.LEFT_SHOULDER.value,
        pose_enum.RIGHT_SHOULDER.value,
        pose_enum.LEFT_HIP.value,
        pose_enum.RIGHT_HIP.value,
        pose_enum.LEFT_KNEE.value,
        pose_enum.RIGHT_KNEE.value,
        pose_enum.LEFT_ANKLE.value,
        pose_enum.RIGHT_ANKLE.value,
    ]

    if min(landmarks[index].visibility for index in required) < 0.35:
        return fallback_regions(width, height), "fallback-zones"

    shoulders = [landmark_xy(landmarks, pose_enum.LEFT_SHOULDER.value, width, height), landmark_xy(landmarks, pose_enum.RIGHT_SHOULDER.value, width, height)]
    hips = [landmark_xy(landmarks, pose_enum.LEFT_HIP.value, width, height), landmark_xy(landmarks, pose_enum.RIGHT_HIP.value, width, height)]
    knees = [landmark_xy(landmarks, pose_enum.LEFT_KNEE.value, width, height), landmark_xy(landmarks, pose_enum.RIGHT_KNEE.value, width, height)]
    ankles = [landmark_xy(landmarks, pose_enum.LEFT_ANKLE.value, width, height), landmark_xy(landmarks, pose_enum.RIGHT_ANKLE.value, width, height)]

    torso_points = np.array(shoulders + hips)
    lower_points = np.array(hips + knees + ankles)
    shoulder_y = min(point[1] for point in shoulders)
    hip_y = max(point[1] for point in hips)
    knee_y = max(point[1] for point in knees)
    ankle_y = max(point[1] for point in ankles)
    body_width = max(70, np.ptp(torso_points[:, 0]) * 1.7)

    center_x = np.mean(torso_points[:, 0])
    lower_center_x = np.mean(lower_points[:, 0])

    top_box = (
        center_x - body_width * 0.58,
        shoulder_y - height * 0.035,
        center_x + body_width * 0.58,
        hip_y + height * 0.06,
    )
    bottom_box = (
        lower_center_x - body_width * 0.54,
        hip_y - height * 0.03,
        lower_center_x + body_width * 0.54,
        ankle_y - height * 0.025,
    )
    footwear_box = (
        lower_center_x - body_width * 0.55,
        knee_y + (ankle_y - knee_y) * 0.58,
        lower_center_x + body_width * 0.55,
        min(height, ankle_y + height * 0.08),
    )

    return {
        "Topwear": Region("Topwear", clip_box(top_box, width, height), 88),
        "Bottomwear": Region("Bottomwear", clip_box(bottom_box, width, height), 84),
        "Footwear": Region("Footwear", clip_box(footwear_box, width, height), 78),
    }, "mediapipe-pose"


def clean_pixels(region):
    flat_bgr = region.reshape(-1, 3)
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV).reshape(-1, 3)
    saturation = hsv[:, 1]
    value = hsv[:, 2]

    mask = (value > 30) & (value < 246) & ((saturation > 28) | (value < 190))
    selected = flat_bgr[mask]
    return selected if len(selected) >= 20 else flat_bgr


def closest_color(rgb):
    color_name = "Unknown"
    shortest_distance = float("inf")
    for name, palette_rgb in COLOR_PALETTE.items():
        distance = np.linalg.norm(np.array(rgb) - np.array(palette_rgb))
        if distance < shortest_distance:
            shortest_distance = distance
            color_name = name
    return color_name


def dominant_color(region):
    if region.size == 0:
        return "Unknown", "#000000"

    pixels = clean_pixels(region)
    selected = np.float32(pixels)
    k = min(4, len(selected))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.8)
    _, labels, centers = cv2.kmeans(selected, k, None, criteria, 8, cv2.KMEANS_PP_CENTERS)

    labels = labels.flatten()
    counts = np.bincount(labels)
    centers = centers.astype(int)

    hsv_centers = cv2.cvtColor(centers.reshape(1, -1, 3).astype(np.uint8), cv2.COLOR_BGR2HSV).reshape(-1, 3)
    scores = counts.astype(float)
    scores *= np.where(hsv_centers[:, 1] > 40, 1.15, 1.0)
    scores *= np.where(hsv_centers[:, 2] > 235, 0.55, 1.0)

    dominant = centers[int(np.argmax(scores))]
    b, g, r = dominant.tolist()
    rgb = (int(r), int(g), int(b))
    return closest_color(rgb), "#{:02x}{:02x}{:02x}".format(*rgb)


def color_family(color):
    if color in {"Black", "Charcoal", "White", "Gray", "Cream", "Beige"}:
        return "Neutral"
    if color in {"Red", "Burgundy", "Pink", "Brown", "Yellow"}:
        return "Warm"
    return "Cool"


def infer_style(colors):
    colors = set(colors)
    if colors & {"Burgundy", "Pink", "Beige", "Cream"} and colors & {"Brown", "Yellow", "Red"}:
        return "Traditional"
    if colors & {"Black", "Charcoal", "Navy"} and colors & {"White", "Gray"}:
        return "Streetwear"
    if colors & {"Gray", "Black", "Navy"} and len(colors & {"Red", "Pink", "Yellow", "Burgundy"}) == 0:
        return "Formal"
    return "Casual"


def color_harmony(items):
    colors = [item["color"] for item in items]
    families = {item["color_family"] for item in items}
    if len(set(colors)) == 1:
        return "Monochrome"
    if "Neutral" in families and len(families) <= 2:
        return "Balanced neutral pairing"
    if len(families) == 1:
        return f"{next(iter(families))} palette"
    return "Mixed contrast"


def infer_garment_type(category, color, style, occasion):
    if category == "Footwear":
        return STYLE_ITEM_TYPES.get(style, STYLE_ITEM_TYPES["Casual"])[category]

    if category == "Topwear":
        if style == "Indian":
            return "blouse" if occasion in {"Wedding", "Party"} else "kurti"
        if occasion == "Wedding":
            return "blouse"
        if style == "Traditional":
            return "kurti"
        if style == "Formal" or occasion == "Office":
            return "shirt"
        if style == "Streetwear":
            return "jacket" if color in {"Black", "Charcoal", "Navy", "Olive"} else "oversized top"
        if style == "Athleisure" or occasion == "Workout":
            return "active top"
        if color in {"Cream", "Gray", "Black"}:
            return "top"
        return TOPWEAR_TYPES.get(style, "top")

    if color in {"Blue", "Denim Blue"}:
        return "jeans"
    if style == "Indian":
        return "lehenga" if occasion == "Wedding" else "skirt"
    if occasion == "Wedding":
        return "lehenga"
    if style == "Traditional":
        return "palazzo pants"
    if style == "Formal" or occasion == "Office":
        return "formal trousers"
    if style == "Streetwear":
        return "cargo pants"
    if style == "Athleisure" or occasion == "Workout":
        return "joggers"
    return BOTTOMWEAR_TYPES.get(style, "trousers")


def garment_name(category, color, item_type):
    return f"{color} {item_type}"


def build_item(category, region, image, style, occasion):
    x1, y1, x2, y2 = region.box
    crop = image[y1:y2, x1:x2]
    color, hex_color = dominant_color(crop)
    item_type = infer_garment_type(category, color, style, occasion)
    return {
        "item_name": garment_name(category, color, item_type),
        "detected_item": item_type,
        "category": category,
        "color": color,
        "dominant_color": color,
        "hex_color": hex_color,
        "color_family": color_family(color),
        "confidence": region.confidence,
        "region": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
    }


def score_outfit(style, occasion, preferred_color, items, harmony):
    occasion_scores = OCCASION_STYLE_FIT.get(occasion, OCCASION_STYLE_FIT["College"])
    occasion_match = occasion_scores.get(style, 65)
    color_match = 100 if preferred_color == "No preference" else 55

    if preferred_color != "No preference":
        detected_colors = {item["color"] for item in items}
        color_match = 94 if preferred_color in detected_colors else 58

    harmony_bonus = {
        "Monochrome": 8,
        "Balanced neutral pairing": 10,
        "Mixed contrast": 4,
    }.get(harmony, 7)

    confidence = int(np.mean([item["confidence"] for item in items]))
    outfit_score = int(min(98, round((occasion_match * 0.45) + (color_match * 0.25) + (confidence * 0.2) + harmony_bonus)))
    return occasion_match, color_match, confidence, outfit_score


def notes_for(style, occasion, preferred_color, items, harmony, analysis_mode):
    palette = ", ".join(item["color"] for item in items)
    notes = [
        f"Analysis mode: {analysis_mode}.",
        f"Detected style profile: {style}.",
        f"Main palette: {palette}.",
        f"Color harmony: {harmony}.",
        f"Occasion fit was scored for {occasion}.",
    ]
    if preferred_color != "No preference":
        notes.append(f"Preferred color considered: {preferred_color}.")
    return notes


def recommendation_for(style, occasion, harmony, color_match):
    if color_match < 70:
        return "The outfit is usable, but it does not strongly match the preferred color. Add an accessory or layer in the requested color."
    if occasion == "Wedding" and style == "Traditional":
        return "Strong wedding fit. Keep accessories refined and choose footwear that matches the warm palette."
    if occasion == "Office" and style == "Formal":
        return "Good office fit. The outfit reads structured and work appropriate."
    if harmony == "Balanced neutral pairing":
        return "The neutral balance makes this easy to wear and simple to style."
    return "The outfit is wearable for the selected occasion; keep accessories simple so the palette stays clear."


def analyze_image_bytes(contents, filename="uploaded-image", preferences=None):
    preferences = preferences or {}
    occasion = preferences.get("occasion") or "College"
    requested_style = preferences.get("style") or "Auto"
    preferred_color = preferences.get("preferred_color") or "No preference"

    image = decode_image(contents)
    height, width = image.shape[:2]
    regions, analysis_mode = pose_regions(image)

    provisional_colors = []
    for category in ("Topwear", "Bottomwear", "Footwear"):
        x1, y1, x2, y2 = regions[category].box
        color, _ = dominant_color(image[y1:y2, x1:x2])
        provisional_colors.append(color)

    inferred_style = infer_style(provisional_colors)
    style = inferred_style if requested_style == "Auto" else requested_style

    items = [build_item(category, regions[category], image, style, occasion) for category in ("Topwear", "Bottomwear", "Footwear")]
    harmony = color_harmony(items)
    occasion_match, color_match, confidence, outfit_score = score_outfit(style, occasion, preferred_color, items, harmony)

    return {
        "analysis_id": str(uuid.uuid4()),
        "image_name": filename,
        "image_size": {"width": width, "height": height},
        "request": {
            "occasion": occasion,
            "requested_style": requested_style,
            "preferred_color": preferred_color,
        },
        "outfit_breakdown": {
            "topwear": items[0],
            "bottomwear": items[1],
            "footwear": items[2],
        },
        "fashion_metadata": {
            "style": style,
            "inferred_style": inferred_style,
            "occasion": occasion,
            "season": "All Season",
            "color_harmony": harmony,
            "occasion_match": occasion_match,
            "color_match": color_match,
            "recommendation": recommendation_for(style, occasion, harmony, color_match),
            "notes": notes_for(style, occasion, preferred_color, items, harmony, analysis_mode),
        },
        "confidence_score": confidence,
        "outfit_score": outfit_score,
        "runtime": {
            "mode": "offline",
            "device": "cpu",
            "inference": analysis_mode,
        },
        "shopping_matches": [match_catalog(item) for item in items],
    }


async def analyze_image(file, preferences=None):
    contents = await file.read()
    return analyze_image_bytes(contents, file.filename, preferences)
