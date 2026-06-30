import io
import unittest

from PIL import Image

from backend.analyzer import analyze_image_bytes


def outfit_image(top_rgb=(126, 20, 45), bottom_rgb=(205, 184, 145), shoe_rgb=(120, 75, 45)):
    image = Image.new("RGB", (480, 900), "white")
    pixels = image.load()

    for y in range(80, 420):
        for x in range(120, 360):
            pixels[x, y] = top_rgb

    for y in range(390, 720):
        for x in range(130, 350):
            pixels[x, y] = bottom_rgb

    for y in range(710, 850):
        for x in range(145, 335):
            pixels[x, y] = shoe_rgb

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


class AnalyzerTests(unittest.TestCase):
    def test_indian_wedding_labels_blouse_and_lehenga(self):
        result = analyze_image_bytes(
            outfit_image(),
            "indian.png",
            {"occasion": "Wedding", "style": "Indian", "preferred_color": "No preference"},
        )

        self.assertEqual(result["outfit_breakdown"]["topwear"]["detected_item"], "blouse")
        self.assertEqual(result["outfit_breakdown"]["bottomwear"]["detected_item"], "lehenga")

    def test_casual_denim_labels_jeans(self):
        result = analyze_image_bytes(
            outfit_image(top_rgb=(40, 90, 185), bottom_rgb=(70, 110, 160)),
            "casual.png",
            {"occasion": "College", "style": "Casual", "preferred_color": "No preference"},
        )

        self.assertEqual(result["outfit_breakdown"]["topwear"]["detected_item"], "T-shirt")
        self.assertEqual(result["outfit_breakdown"]["bottomwear"]["detected_item"], "jeans")
        self.assertEqual(len(result["shopping_matches"]), 3)


if __name__ == "__main__":
    unittest.main()
