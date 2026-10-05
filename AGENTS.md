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

## Skillの採用・廃止

- 現役Skillは`skills/<skill-name>/`に置く。外部Skillを採用する場合は、出典、採用コミット、ローカルでの変更点をSkill内の`採用元.md`に記録し、配布元のlicense / noticeを保持する。
- Skillを置き換えるときは、旧版を`archive/skills/<skill-name>/`へ保管する。本文と補助ファイルを保持し、`廃止理由.md`に廃止日、理由、置き換え先、採用判断の根拠と制約、復元方法を記録する。利用中の版がリポジトリ版と異なる場合は、その版も区別して保管する。
- アーカイブ内の`SKILL.md`は`旧手順.md`へ改名する。アーカイブはインストール対象から外し、現役Skillの一覧と参照を更新する。
- 同名のアーカイブがある場合は、日付付きのサブフォルダへ保存し、過去の記録を上書きしない。
