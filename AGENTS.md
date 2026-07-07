# AGENTS.md

Guidance for human and AI contributors working in this repository.

## Scope

- This file applies to the whole repository.

## Core Principles

- Prefer common, well-maintained libraries and packages over custom ad hoc logic.
- Keep changes focused and minimal for the requested task.
- Do not modify unrelated files.

## Working Style

- Before changing behaviour, check existing patterns in nearby files and follow them.
- When behaviour changes are non-trivial, ask for confirmation before implementing.
- If a requirement is ambiguous and could alter behaviour, ask a clarifying yes/no question first.

## Libraries And Dependencies

- Reuse existing dependencies and idioms already present in the repo when possible.
- Add a new package only when it clearly improves reliability, readability, or maintainability.
- Prefer widely adopted packages over hand-rolled implementations.

## CLI Script Conventions

- For scripts that emit machine-readable output:
  - Write result content only to stdout.
  - Write progress, diagnostics, and errors to stderr.

## Testing Approach

- Prefer approval testing for CLI and file-conversion workflows, especially when outputs are large or hard to assert with small examples.
- Keep approved artifacts human-reviewable and deterministic so diffs are meaningful.
- On approval mismatches, generate a received artifact for review; do not auto-accept changes without explicit confirmation.

## Data Normalization And Scrubbing

- When normalizing volatile fields (timestamps, generated IDs, run metadata), prefer replacing values with stable placeholders rather than deleting fields.
- Preserve structure during scrubbing so output shape remains representative of real data.
- Document scrub rules in tests or helper code so behaviour is explicit and repeatable.

## XML Output Formatting

- Keep XML artifacts pretty-printed and consistently indented for readability and review.
- For comparisons, use a normalization/canonicalization step to avoid brittle failures from whitespace or attribute-order differences.

