---
name: create-agents-md
description: Create or update repository-level AGENTS.md instructions for Codex and other coding agents. Use when the user asks to add AGENTS.md, write repo instructions, document agent workflow, capture project conventions for Codex, or improve existing AGENTS.md guidance in a code repository.
---

# Create AGENTS.md

## Goal

Create a concise, accurate `AGENTS.md` that helps future coding agents work safely and effectively in the repository. Base the content on the actual repo, not generic best practices.

## Workflow

1. Locate the repository root:
   - Prefer the current working directory when it contains `.git`, package files, or obvious project structure.
   - If unsure, inspect parent directories and ask only when multiple plausible repositories exist.
2. Inspect existing guidance:
   - Read any existing `AGENTS.md`, `README*`, `CONTRIBUTING*`, `docs/`, `.github/`, tool configs, and package/build files.
   - Search for commands and conventions with `rg` or `rg --files` before slower tools.
   - Check `git status --short` before edits and preserve unrelated user changes.
3. Identify repository facts:
   - Primary language, frameworks, package managers, runtime versions, entry points, and major directories.
   - Install, build, test, lint, format, typecheck, dev server, and database/migration commands.
   - Naming, architecture, styling, test, review, localization, security, and deployment conventions that are evidenced by files.
4. Draft `AGENTS.md`:
   - Keep instructions actionable and repo-specific.
   - Include commands only when they are present or strongly implied by project files.
   - Mark uncertain commands or assumptions explicitly instead of presenting them as facts.
   - Avoid long explanations, duplicated README content, and generic agent advice.
5. Validate:
   - Re-read the final file for contradictions with the repo.
   - Run cheap verification when available, such as checking referenced scripts exist or package scripts parse.
   - Do not run expensive tests unless the user asked or the edit risk justifies it.

## Recommended Structure

Use this structure unless the repository clearly calls for another:

```markdown
# AGENTS.md

## Project Overview
- Briefly describe what this repository contains and the main runtime/framework.

## Key Commands
- `command`: purpose.
- Note prerequisites or environment files only when known.

## Repository Structure
- `path/`: role and ownership boundary.

## Coding Conventions
- Repo-specific style, naming, typing, component, API, or data rules.

## Testing And Validation
- Which tests/checks to run for common changes.
- Mention known limitations or slow checks.

## Agent Workflow Notes
- Safety notes for migrations, generated files, secrets, build artifacts, or user-owned changes.
```

## Content Rules

- Write in the repository's existing documentation language. If there is no clear precedent, use the user's language.
- Use English file names for `AGENTS.md` and technical identifiers exactly as they appear.
- Prefer bullets over prose blocks.
- Include paths and commands in backticks.
- Do not invent scripts, directories, or policies.
- Do not add tutorial content for tools the repo already assumes.
- Do not overwrite an existing `AGENTS.md` blindly; merge useful existing instructions and remove stale or contradictory content.
- If project facts cannot be determined, write a short "Unknown / Not Found" note only when that uncertainty matters for future agents.

## Useful Inspection Commands

Run only the commands needed for the repo:

```powershell
git status --short
rg --files
rg -n "npm run|pnpm|yarn|pytest|ruff|cargo|go test|mvn|gradle|bundle exec|composer|make "
```

For JavaScript or TypeScript projects, inspect `package.json` scripts directly. For Python, inspect `pyproject.toml`, `requirements*.txt`, `tox.ini`, `noxfile.py`, and `pytest.ini`. For monorepos, document workspace-level commands first, then package-specific exceptions.
