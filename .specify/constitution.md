# WardroAI Constitution

## Core Principles

1. WardroAI must run offline on CPU.
2. Image analysis must not depend on cloud APIs.
3. Streamlit is the primary user interface.
4. User images and local analysis history must stay local by default.
5. Feature changes should include clear acceptance criteria.
6. Documentation must be updated when user-visible behavior changes.

## Quality Gates

- `npm run format:check`
- `npm run lint`
- `npm run type_check`
- `npm test`
- `npm run coverage`
- Secret scanning before sharing release branches

## Governance

This constitution guides implementation and review decisions for WardroAI features. Feature work should start from a spec under `specs/`, use the templates in `.specify/templates/`, and preserve the offline-first architecture unless a future constitution amendment explicitly changes that constraint.
