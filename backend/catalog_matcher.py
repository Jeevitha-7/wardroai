import json
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parent / "data" / "catalog.json"


SIMILAR_COLORS = {
    "Blue": {"Denim Blue"},
    "Denim Blue": {"Blue"},
    "Cream": {"White", "Sand"},
    "White": {"Cream"},
    "Sand": {"Cream"},
    "Burgundy": {"Red", "Dusty Pink"},
    "Red": {"Burgundy"},
    "Dusty Pink": {"Burgundy"},
}


GARMENT_KEYWORDS = {
    "sneakers": {"sneaker", "sneakers"},
    "formal": {"formal"},
    "jeans": {"jean", "jeans", "denim"},
    "pants": {"pant", "pants", "trouser", "trousers", "cargo", "palazzo"},
    "top": {"top", "t-shirt", "shirt", "hoodie", "kurti", "jacket", "anarkali"},
}


INCOMPATIBLE_KEYWORDS = [
    ({"sneaker", "sneakers"}, {"formal"}),
    ({"formal"}, {"sneaker", "sneakers"}),
]

def load_catalog():
    if not CATALOG_PATH.exists():
        return []
    with CATALOG_PATH.open("r") as f:
        return json.load(f)

def match_catalog(item):
    catalog = load_catalog()
    best = None
    best_score = 0
    item_color = item["color"].lower()
    similar_colors = {color.lower() for color in SIMILAR_COLORS.get(item["color"], set())}

    for product in catalog:
        score = 0
        product_color = product["color"].lower()
        product_name = product["name"].lower()
        detected_name = item["detected_item"].lower()

        if product["category"].lower() == item["category"].lower():
            score += 45

        if product_color == item_color:
            score += 40
        elif product_color in similar_colors:
            score += 25

        if item_color in product_name:
            score += 10

        for keywords in GARMENT_KEYWORDS.values():
            if any(word in detected_name for word in keywords) and any(word in product_name for word in keywords):
                score += 15

        for detected_words, product_words in INCOMPATIBLE_KEYWORDS:
            if any(word in detected_name for word in detected_words) and any(word in product_name for word in product_words):
                score -= 35

        if score > best_score:
            best_score = score
            best = product

    if best is None or best_score < 65:
        return {
            "detected_item": item["detected_item"],
            "category": item["category"],
            "color": item["color"],
            "matched_product_name": item["item_name"],
            "source": "Local Catalog",
            "estimated_price": "₹799 - ₹1999",
            "search_query": f"{item['color']} {item['detected_item']} fashion",
            "match_score": 60
        }

    return {
        "detected_item": item["detected_item"],
        "category": item["category"],
        "color": item["color"],
        "matched_product_name": best["name"],
        "source": best["source"],
        "estimated_price": best["estimated_price"],
        "search_query": best["search_query"],
        "match_score": min(best_score, 96)
    }
