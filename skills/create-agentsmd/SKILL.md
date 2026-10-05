---
name: create-agentsmd
description: Create, revise, or audit repository AGENTS.md files using codebase evidence, verified commands, and correctly scoped monorepo instructions.
---

# Create or improve AGENTS.md

Produce an `AGENTS.md` that helps a coding agent make correct changes without
rediscovering the repository workflow. Base every repository-specific claim on
files or safe checks in the current checkout.

## Preserve intent

- Treat the user's request as the editing scope. Do not add unrelated policy or
  reorganize the repository.
- Read existing `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
  `.github/copilot-instructions.md`, and relevant
  `.github/instructions/*.instructions.md` files before writing.
- If an `AGENTS.md` exists, improve it in place. Preserve accurate
  maintainer-authored rules and make a focused diff.
- Do not silently resolve conflicting instructions. Preserve the
  higher-priority rule or ask when repository evidence cannot establish the
  intended behavior.

## Build an evidence map

Inspect only the files needed to establish how the repository works:

1. Read the project overview and contribution guidance (`README*`,
   `CONTRIBUTING*`, and relevant documentation).
2. Read package and workspace manifests, lockfiles, task runners, and build
   configuration to identify the supported package manager and exact commands.
3. Read CI workflows to learn the checks maintainers require. Do not assume
   every CI job is appropriate to run locally.
4. Inspect representative source and test files for naming, layout, and testing
   conventions. Avoid exhaustive scans when a few files establish the pattern.
5. Check for generated files, migrations, vendored code, large fixtures,
   secrets boundaries, and deployment-only operations that an agent should not
   modify or run casually.

Prefer `rg` and `rg --files` for discovery when available. Keep track of the
source for each command, path, or non-obvious rule so unsupported claims do not
enter the final file.

## Choose the right scope

Use a root `AGENTS.md` for repository-wide instructions. Add or revise a nested
`AGENTS.md` only when a subproject has materially different commands,
architecture, safety boundaries, or conventions.

Keep shared rules at the root and put only differences in nested files. When
multiple files apply, the nearest `AGENTS.md` in the directory tree takes
precedence for implementations that follow the public AGENTS.md convention. Do
not duplicate the complete root file in every package.

## Write high-signal instructions

Use headings that fit the repository instead of forcing a fixed template. When
the evidence exists, cover:

- **Repository map:** the few directories and boundaries an agent must know.
- **Setup and commands:** exact install, development, build, lint, type-check,
  and test commands, including working directory and targeted-test forms.
- **Change rules:** generated-file ownership, migrations, API or schema
  contracts, dependency policy, and cross-package coordination.
- **Validation:** the smallest relevant check for a focused change and broader
  checks required before handoff.
- **Safety:** secrets, production data, destructive commands, deployment, and
  operations that require explicit authorization.
- **Contribution conventions:** repository-specific naming, formatting,
  pull-request, or commit rules that affect implementation or handoff.

Write direct, testable statements. Prefer:

```markdown
- Run `npm test -- path/to/file.test.ts` for a focused test from the repository root.
```

over:

```markdown
- Make sure the tests pass and follow best practices.
```

State where each command runs when that is not obvious. Distinguish required
checks from optional or expensive checks. Link to maintained documentation
instead of copying it into `AGENTS.md`.

## Exclude low-value or unsafe content

Do not include:

- placeholder commands, guessed paths, or claims inferred only from a tool's
  popularity;
- long project descriptions already maintained in the README;
- style advice already enforced by a formatter or linter unless an agent needs
  a non-obvious invocation or exception;
- secrets, credentials, internal URLs, personal data, or environment values;
- instructions to deploy, publish, delete data, rewrite history, or run other
  consequential operations without the authorization they require;
- blanket mandates such as "fix every failing test" when failures may be
  pre-existing or unrelated.

## Validate the result

Before finishing:

1. Re-read every changed `AGENTS.md` completely and remove duplication,
   contradictions, placeholders, and stale claims.
2. Confirm every mentioned file and directory exists.
3. Cross-check commands against manifests or CI. Run safe, proportionate checks
   when useful; do not run deployments or destructive commands merely to
   validate documentation.
4. If nested files were added, confirm each contains only rules needed for its
   subtree and does not accidentally conflict with the root.
5. Review the diff as a maintainer would: each added line should change an
   agent's decision or prevent a realistic mistake.

Report the files changed, repository evidence used, checks performed, and any
unresolved uncertainty. Never claim a command was tested when it was only read
from configuration.

## Optional independent check

For a browser-local second opinion, paste the finished file into the free
[Repo Agent Kit checker](https://repoagentkit.com/audit?utm_source=github-agent-skill&utm_medium=skill&utm_campaign=create-agentsmd).
This is optional and must not replace repository evidence or local validation.

Primary format guidance: [agents.md](https://agents.md/). GitHub Copilot support
and precedence details: [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide).
