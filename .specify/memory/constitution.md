# WardroAI Constitution

## Core Principles

1. WardroAI must run offline on CPU by default.
2. Image analysis must not depend on cloud APIs or remote inference services.
3. Streamlit is the primary user interface.
4. User images, SQLite history, and generated analysis data remain local by default.
5. User-visible analyzer behavior changes must update tests, examples, and documentation.

## Quality Gates

- `npm run format:check`
- `npm run lint`
- `npm run type_check`
- `npm test`
- `npm run coverage`

## Governance

Feature work should start from a spec under `specs/`, use the templates in `.specify/templates/`, and preserve the offline-first architecture unless a future constitution amendment explicitly changes that constraint.
