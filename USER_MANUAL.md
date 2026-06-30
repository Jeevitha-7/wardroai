# WardroAI User Manual

WardroAI analyzes a full outfit image locally and returns garment zones, colors, style fit, shopping suggestions, and structured JSON.

## Start the App

From the project root:

```bash
npm run setup
npm start
```

Open the URL printed in the terminal, usually:

```text
http://127.0.0.1:8501
```

If that port is busy, WardroAI automatically tries the next available port.

## Analyze an Outfit

1. Upload a JPG, PNG, JPEG, or WEBP outfit image.
2. Choose an occasion.
3. Choose a preferred style, or keep `Auto`.
4. Choose a preferred color, or keep `No preference`.
5. Select `Analyze Outfit`.

## Results

WardroAI displays:

- Outfit score and confidence score
- Topwear, bottomwear, and footwear labels
- Dominant colors and color families
- Detected garment zones
- Local catalog shopping matches
- Downloadable JSON output
- Local analysis history

## Best Image Tips

- Use a clear full-body photo.
- Keep topwear, bottomwear, and footwear visible.
- Avoid heavily cropped, blurry, or dark images.
- Use a plain background when possible.

## Privacy

WardroAI runs offline. Uploaded images are processed locally and analysis history is stored in a local SQLite database.
