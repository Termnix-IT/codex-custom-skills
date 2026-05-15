# AGENTS.md

## Language

- Respond to the user in Japanese by default.
- Keep code, commands, file paths, API names, JSON keys, and other technical identifiers in their original English form.

## Repository Purpose

- This repository stores custom Codex Skills for public GitHub sharing.
- Keep each skill self-contained under `skills/<skill-name>/`.
- The required entrypoint for every skill is `SKILL.md`.

## Skill Authoring

- Use English directory names for skills, scripts, modules, and executable files.
- Prefer Japanese file names for reference documents, notes, manuals, and reports.
- Keep `SKILL.md` concise and action-oriented.
- Put optional helpers next to the skill:
  - `scripts/` for executable helpers.
  - `assets/` for reusable static files.
  - `references/` for supporting documents.

## Editing Guidelines

- Avoid adding dependencies unless a skill genuinely needs them.
- Do not commit local secrets, tokens, generated caches, or machine-specific config.
- Preserve user-authored skill text unless explicitly asked to rewrite it.
