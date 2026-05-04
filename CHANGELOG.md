# Changelog

## Unreleased

### Added
- Added GPT Researcher project workspace mode with persistent project state:
  - project metadata
  - topic queue
  - checkpoints
  - sources
  - artifacts
  - memory entries
  - markdown export
- Added source-based GPT Researcher entrypoints via `python -m gpt_researcher` and backward-compatible top-level `cli.py`
- Added focused regression tests for:
  - project workspace sync
  - GPT Researcher agent project mode
  - CLI project mode
  - output sanitization
- Added lightweight GitHub Actions focused test workflow for safe validation on pushes and pull requests

### Changed
- Clarified repository scope in `README.md` to explain the dual structure:
  - `gptr` local-first workspace CLI
  - `gpt_researcher` fork with persisted project mode
- Expanded `.gitignore` for generated local outputs from real research runs and test flows

### Fixed
- Fixed final report leakage of internal `<think>...</think>` reasoning blocks by sanitizing user-visible report output

### Validated
- Real local end-to-end test completed on the topic:
  - protein thermostability prediction
- Focused regression suite passed after the sanitizer fix
