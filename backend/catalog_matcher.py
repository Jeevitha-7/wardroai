import json
import os

CATALOG_PATH = "data/catalog.json"

def load_catalog():
    if not os.path.exists(CATALOG_PATH):
        return []
    with open(CATALOG_PATH, "r") as f:
        return json.load(f)

def match_catalog(item):
    catalog = load_catalog()
    best = None
    best_score = 0

    for product in catalog:
        score = 0

        if product["category"].lower() == item["category"].lower():
            score += 45

        if product["color"].lower() == item["color"].lower():
            score += 40

        if item["color"].lower() in product["name"].lower():
            score += 10

        if score > best_score:
            best_score = score
            best = product

    if best is None:
        return {
            "detected_item": item["detected_item"],
            "category": item["category"],
            "color": item["color"],
            "matched_product_name": f"{item['color']} {item['category']}",
            "source": "Local Catalog",
            "estimated_price": "₹799 - ₹1999",
            "search_query": f"{item['color']} {item['category']} fashion",
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