def dominant_color(region):
    pixels = clean_pixels(region)

    if len(pixels) == 0:
        return "Unknown", "#000000"

    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
    flat_hsv = hsv.reshape(-1, 3)
    flat_bgr = region.reshape(-1, 3)

    # prefer colorful pixels, ignore walls/background/skin-ish dull colors
    saturation = flat_hsv[:, 1]
    value = flat_hsv[:, 2]

    mask = (saturation > 60) & (value > 40) & (value < 245)

    selected = flat_bgr[mask]

    if len(selected) < 100:
        selected = pixels

    selected = np.float32(selected)

    k = 3 if len(selected) >= 3 else 1
    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        20,
        1.0,
    )

    _, labels, centers = cv2.kmeans(
        selected,
        k,
        None,
        criteria,
        10,
        cv2.KMEANS_RANDOM_CENTERS,
    )

    labels = labels.flatten()
    counts = np.bincount(labels)
    dominant = centers[np.argmax(counts)].astype(int)

    b, g, r = dominant.tolist()
    rgb = (int(r), int(g), int(b))

    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
    return closest_color(rgb), hex_color