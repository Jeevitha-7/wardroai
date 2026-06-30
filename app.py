import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from analyzer import analyze_image_bytes  # noqa: E402
from database import get_analysis_by_id, get_history, init_db, save_analysis  # noqa: E402


OCCASIONS = ["College", "Office", "Party", "Wedding", "Travel", "Workout"]
STYLES = ["Auto", "Casual", "Streetwear", "Formal", "Traditional", "Indian", "Athleisure"]
COLORS = [
    "No preference",
    "Black",
    "White",
    "Gray",
    "Cream",
    "Beige",
    "Red",
    "Burgundy",
    "Pink",
    "Blue",
    "Denim Blue",
    "Navy",
    "Green",
    "Olive",
    "Brown",
    "Yellow",
]


def page_style():
    st.markdown(
        """
        <style>
          .stApp {
            background: #f5f1ea;
            color: #1e1f24;
          }
          [data-testid="stSidebar"] {
            background: #17191f;
          }
          [data-testid="stSidebar"] * {
            color: #f7f3eb;
          }
          h1, h2, h3 {
            letter-spacing: 0;
          }
          .hero {
            background: #ffffff;
            border: 1px solid #e3ded4;
            border-radius: 8px;
            padding: 22px 24px;
            margin-bottom: 18px;
          }
          .hero h1 {
            margin: 0 0 8px 0;
            font-size: 32px;
          }
          .hero p {
            color: #68645d;
            margin: 0;
            max-width: 780px;
          }
          .metric-card {
            background: #ffffff;
            border: 1px solid #e3ded4;
            border-radius: 8px;
            padding: 16px;
            min-height: 92px;
          }
          .metric-card span {
            color: #6d675f;
            font-size: 13px;
          }
          .metric-card strong {
            display: block;
            font-size: 26px;
            margin-top: 6px;
          }
          .result-card {
            background: #ffffff;
            border: 1px solid #e3ded4;
            border-radius: 8px;
            padding: 16px;
            height: 100%;
          }
          .result-card h4 {
            margin: 0 0 10px 0;
            color: #491d2c;
          }
          .detail-row {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            border-bottom: 1px solid #eee9df;
            padding: 8px 0;
          }
          .detail-row:last-child {
            border-bottom: 0;
          }
          .swatch {
            width: 14px;
            height: 14px;
            border: 1px solid rgba(0,0,0,.25);
            border-radius: 50%;
            display: inline-block;
            vertical-align: -2px;
            margin-right: 8px;
          }
          .note {
            background: #fffaf1;
            border: 1px solid #eadfcb;
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 8px;
          }
          .stButton > button {
            background: #491d2c;
            color: white;
            border: 0;
            border-radius: 8px;
            height: 42px;
            font-weight: 700;
          }
          .stButton > button:hover {
            background: #32141f;
            color: white;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
          <span>{label}</span>
          <strong>{value}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def detail_row(label, value):
    st.markdown(
        f"""
        <div class="detail-row">
          <b>{label}</b>
          <span>{value}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def item_card(title, item):
    st.markdown(f"<div class='result-card'><h4>{title}</h4>", unsafe_allow_html=True)
    detail_row("Detected item", item["detected_item"].title())
    detail_row("Color", f"<span class='swatch' style='background:{item['hex_color']}'></span>{item['color']}")
    detail_row("Color family", item["color_family"])
    detail_row("Confidence", f"{item['confidence']}%")
    st.markdown("</div>", unsafe_allow_html=True)


def draw_regions(image, result):
    annotated = image.copy().convert("RGB")
    draw = ImageDraw.Draw(annotated)
    colors = {
        "topwear": "#2f80ed",
        "bottomwear": "#27ae60",
        "footwear": "#c0392b",
    }

    for key, color in colors.items():
        item = result["outfit_breakdown"][key]
        region = item["region"]
        box = (region["x1"], region["y1"], region["x2"], region["y2"])
        draw.rectangle(box, outline=color, width=4)
        draw.text((box[0] + 6, box[1] + 6), key.title(), fill=color)

    return annotated


def result_summary(result):
    metadata = result["fashion_metadata"]
    cols = st.columns(4)
    with cols[0]:
        metric_card("Outfit score", f"{result['outfit_score']}%")
    with cols[1]:
        metric_card("Confidence", f"{result['confidence_score']}%")
    with cols[2]:
        metric_card("Occasion match", f"{metadata['occasion_match']}%")
    with cols[3]:
        metric_card("Color match", f"{metadata['color_match']}%")

    st.markdown("### Outfit Breakdown")
    top, bottom, foot = st.columns(3)
    with top:
        item_card("Topwear", result["outfit_breakdown"]["topwear"])
    with bottom:
        item_card("Bottomwear", result["outfit_breakdown"]["bottomwear"])
    with foot:
        item_card("Footwear", result["outfit_breakdown"]["footwear"])

    st.markdown("### Styling Recommendation")
    st.info(metadata["recommendation"])

    st.markdown("### Analysis Notes")
    for note in metadata["notes"]:
        st.markdown(f"<div class='note'>{note}</div>", unsafe_allow_html=True)


def shopping_table(result):
    rows = []
    for match in result["shopping_matches"]:
        rows.append(
            {
                "Detected": match["detected_item"],
                "Category": match["category"],
                "Color": match["color"],
                "Suggested match": match["matched_product_name"],
                "Source": match["source"],
                "Price": match["estimated_price"],
                "Match": f"{match['match_score']}%",
            }
        )
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def history_view():
    st.markdown("### Saved Analyses")
    history = get_history()
    if not history:
        st.caption("No saved analyses yet.")
        return

    for row in history[:12]:
        with st.expander(f"{row['image_name']} - {row['style']} - {row['confidence']}%"):
            st.caption(row["created_at"])
            stored = get_analysis_by_id(row["id"])
            if "error" not in stored:
                st.json(stored)


def main():
    st.set_page_config(page_title="WardroAI", page_icon=None, layout="wide")
    page_style()
    init_db()

    with st.sidebar:
        st.title("WardroAI")
        st.caption("Offline outfit analysis")
        uploaded = st.file_uploader("Upload outfit image", type=["jpg", "jpeg", "png", "webp"])
        occasion = st.selectbox("Occasion", OCCASIONS, index=0)
        style = st.selectbox("Preferred style", STYLES, index=0)
        preferred_color = st.selectbox("Preferred color", COLORS, index=0)
        analyze_clicked = st.button("Analyze Outfit", use_container_width=True)

        st.divider()
        st.caption("Runs locally using CPU image processing, pose landmarks, SQLite history, and a local product catalog.")

    st.markdown(
        """
        <div class="hero">
          <h1>WardroAI Outfit Analyzer</h1>
          <p>Upload a full outfit photo, choose the occasion, and get a structured breakdown with garment zones, colors, fit scores, and styling guidance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if uploaded is None:
        left, right = st.columns([1.1, 0.9])
        with left:
            st.subheader("Start with a clear outfit photo")
            st.write("Best results come from a full-body image with the top, bottom, and footwear visible.")
        with right:
            st.markdown("### What you will get")
            st.write("Garment zone detection")
            st.write("Dominant colors with swatches")
            st.write("Occasion, style, and color match scores")
            st.write("Shopping/catalog match suggestions")
        history_view()
        return

    image = Image.open(uploaded).convert("RGB")

    upload_key = f"{uploaded.name}:{uploaded.size}"

    if analyze_clicked or st.session_state.get("upload_key") != upload_key:
        with st.spinner("Analyzing outfit locally..."):
            result = analyze_image_bytes(
                uploaded.getvalue(),
                uploaded.name,
                {
                    "occasion": occasion,
                    "style": style,
                    "preferred_color": preferred_color,
                },
            )
            save_analysis(result)
            st.session_state.result = result
            st.session_state.image = image
            st.session_state.upload_key = upload_key

    result = st.session_state.result
    image = st.session_state.image

    overview_tab, image_tab, shopping_tab, json_tab, history_tab = st.tabs(
        ["Overview", "Detected Zones", "Shopping Matches", "Structured JSON", "History"]
    )

    with overview_tab:
        result_summary(result)

    with image_tab:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Original")
            st.image(image, use_container_width=True)
        with c2:
            st.markdown("### Analyzed Garment Zones")
            st.image(draw_regions(image, result), use_container_width=True)
            st.caption(f"Analysis mode: {result['runtime']['inference']}")

    with shopping_tab:
        st.markdown("### Local Catalog Suggestions")
        shopping_table(result)

    with json_tab:
        st.download_button(
            "Download JSON",
            json.dumps(result, indent=2),
            file_name=f"{Path(uploaded.name).stem}-wardroai-analysis.json",
            mime="application/json",
        )
        st.json(result)

    with history_tab:
        history_view()


if __name__ == "__main__":
    main()
