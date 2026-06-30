# Contributing to WardroAI

Thank you for helping improve WardroAI. This project is an offline, CPU-only wardrobe analyzer, so changes should preserve local execution and avoid cloud dependencies.

## Development Setup

```bash
npm run setup
npm start
```

Open the app at the URL printed by the terminal.

## Before Submitting Changes

Run the checks that apply to your change:

```bash
npm run lint
npm test
```

For dependency or release changes, also run:

```bash
npm run security:audit
```

## Contribution Guidelines

- Keep analysis offline and CPU-compatible.
- Do not commit generated caches, local databases, secrets, or virtual environments.
- Keep UI changes consistent with the Streamlit app in `app.py`.
- Update `README.md`, `USER_MANUAL.md`, or `CHANGELOG.md` when behavior changes.
- Prefer focused pull requests with a clear description and screenshots for UI updates.

## Commit Style

Use concise, conventional-style messages where possible:

```text
feat: add Indian outfit labels
fix: choose free Streamlit port on startup
docs: add user manual
```
