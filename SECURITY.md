# Security Policy

## Supported Versions

WardroAI is currently maintained from the main repository branch.

## Reporting a Vulnerability

Please report suspected security issues privately to the repository maintainers. Do not open a public issue containing secrets, exploit details, or private user data.

Include:

- A short description of the issue
- Steps to reproduce
- Affected files or commands
- Any relevant logs with secrets removed

## Security Expectations

- Do not commit API keys, tokens, credentials, database dumps, or private images.
- Use `.env.example` for documenting configuration.
- Run secret scanning before sharing release branches.
- Keep dependencies reviewed and update vulnerable packages promptly.

## Local Data

WardroAI stores analysis history in SQLite locally. Treat local databases as user data and do not commit them.
