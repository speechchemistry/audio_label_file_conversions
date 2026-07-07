# Spec: Optional Media Linking in saymore_tsv_to_saymore_eaf.py

## Status
Draft, implementation on hold pending test framework setup.

## Scope
This spec defines a planned change to allow explicit media file linking in generated EAF output from `saymore_tsv_to_saymore_eaf.py`.

No code changes are included in this spec.

## Problem Statement
Current output from `saymore_tsv_to_saymore_eaf.py` does not explicitly include media linkage in the EAF header.

Goal: add an optional CLI argument so users can define a media file when generating EAF.

## Confirmed Decisions
1. Add an optional argparse argument: `--media-file`.
2. Path handling should behave like Linux shell expectations:
   - Absolute if path starts with `/`.
   - Otherwise treat as relative.
3. Relative paths should be resolved from the current working directory at runtime.
4. If `--media-file` is provided and the file does not exist, fail fast with a clear error.
5. If `--media-file` is omitted, current behavior remains unchanged.
6. Also include relative media information when possible (target is `RELATIVE_MEDIA_URL`).
7. Do not normalize generated XML yet; first inspect raw PyMPI output.
8. Do not update README yet.

## PyMPI API Notes (from Elan docs)
Relevant API for planned implementation:
- `pympi.Elan.Eaf.add_linked_file(file_path, relpath=None, mimetype=None, time_origin=None, ex_from=None)`

Expected role in implementation:
- `file_path`: primary media path used in EAF media descriptor.
- `relpath`: relative media path where applicable.
- `mimetype`: left as default initially so PyMPI infers by extension.

## Open Questions (Deferred)
1. Should `MEDIA_URL` be forced to URI form (`file:///...`) if raw PyMPI output differs?
2. Should we add explicit `--media-mimetype` later for uncommon extensions?
3. Should relative path be `./filename` vs a longer relative path from output location?

## Proposed Implementation Plan (On Hold)
1. Extend argparse with `--media-file`.
2. Resolve and validate the media path.
3. Compute a relative path for `relpath` when possible.
4. Call `new_eaf.add_linked_file(...)` before writing output.
5. Generate output exactly as PyMPI emits it (no post-processing normalization yet).

## Test Strategy Prerequisite
Implementation should wait until a basic test framework is in place.

Minimum tests to add before feature work:
1. Baseline conversion test: no media arg, output behavior unchanged.
2. Media link happy path test: valid `--media-file` produces a media descriptor.
3. Missing file test: `--media-file` with non-existent path exits with error.
4. Relative path test: relative media input is resolved correctly from CWD.
5. Regression test: existing tier and annotation structure remains intact.

## Acceptance Criteria (Feature)
1. Script accepts `--media-file` without breaking existing positional args.
2. Missing media file with `--media-file` causes non-zero exit and clear error.
3. Generated EAF includes media descriptor fields from raw PyMPI behavior.
4. Existing behavior is unchanged when `--media-file` is not provided.

## Non-Goals
1. No README updates in this phase.
2. No XML normalization in this phase.
3. No broad refactor of conversion logic in this phase.

## Notes for Future Work
Use an attached/known-good EAF example as a fixture to compare media descriptor structure after initial implementation.
