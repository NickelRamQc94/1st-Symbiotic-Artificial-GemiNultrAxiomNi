# GitHub Copilot prompts

## Documentation
- Generate a concise README from the repository's actual files.
- Summarize the repository purpose without inventing capabilities.
- Describe the architecture and data flow in Mermaid text.

## Code quality
- Refactor this module for clarity without changing its public API.
- Add focused tests for the reported regression and preserve existing behavior.
- Generate safe configuration defaults and document every security-sensitive option.

## Multi-repository work
- Scan only the named repositories for inconsistencies and report file-level evidence.
- Generate a unified API surface from existing exported symbols.
- Propose a synchronization script with dry-run mode, idempotency, and rollback guidance.

## Safety rules
- Do not claim a medical diagnosis or treatment recommendation.
- Do not expose secrets, tokens, or private data.
- Ask before making destructive changes or publishing externally.
