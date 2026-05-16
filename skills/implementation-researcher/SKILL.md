---
name: implementation-researcher
description: Use before implementing non-trivial code changes to research and compare standard libraries, built-in APIs, framework features, existing dependencies, new libraries, and self-build risks, including whether existing implemented code should be simplified or replaced before refactoring. Trigger for new features, existing feature changes, refactors, existing implementation improvement, library additions, architecture or design changes, API or CLI design, data storage, security-sensitive work, file processing, state management, and other implementation planning where Codex should investigate options before coding.
---

# Implementation Researcher

Use this skill before deciding the feature shape, requirements, design, dependency strategy, or implementation approach for non-trivial work. The goal is to prevent avoidable custom work, unnecessary dependencies, designs that conflict with the existing project, and missed opportunities to simplify already implemented code with standard or existing capabilities.

During the research phase, do not write implementation code. Read, compare, and propose an implementation plan first. Small read-only commands and checks are allowed when they clarify the plan.

## Research Modes

Use **Lite Research** for small, low-risk changes:

- Typo fixes, README edits, small UI adjustments, and simple changes that clearly follow an existing local pattern.
- Confirm the relevant file, nearby pattern, and whether the change touches any high-risk area.
- Keep the result brief, but still include a recommendation and reason.

Use **Full Research** for non-trivial or risky changes:

- New features, library additions, architecture or design changes, security-related work, data storage, API design, CLI design, image processing, file processing, authentication, encryption, state management, concurrency, migrations, or network behavior.
- Compare standard, framework, existing dependency, new dependency, and custom implementation options.
- Explicitly call out self-build risks and open questions before proposing implementation.

Default to Full Research when the mode is unclear.

## Existing Implementation Review

Use this skill before refactoring or improving an existing implementation. First understand what the current code does, why it may have been written that way, and what tests or callers protect the behavior.

Compare the current implementation against:

- Standard library or built-in APIs that could replace custom code.
- Framework features that make the current code simpler, safer, or more idiomatic.
- Existing dependencies already available in the project.
- Well-known libraries that would reduce meaningful complexity.
- Common design patterns that better fit the current requirement and project architecture.

Do not recommend rewriting working code only because another approach exists. Recommend replacement only when it improves correctness, security, maintainability, performance, or future change cost enough to justify migration risk.

## Sub-Agent Use

The main agent owns the final recommendation, implementation plan, architecture decisions, dependency decisions, and security judgment.

For Full Research, consider explorer sub-agents only for bounded read-only research such as:

- Finding existing implementation patterns, shared utilities, related tests, or prior design choices.
- Checking current dependency usage and framework capabilities.
- Comparing localized code conventions across independent subsystems.

Do not delegate the final recommendation or security-sensitive judgment entirely to a sub-agent. Do not use worker sub-agents during this research phase because this skill should not write implementation code.

## Required Project Inspection

Before recommending an approach, inspect the existing project shape and relevant files. Check for these files when present:

- `README`, `AGENTS.md`, and local documentation.
- Dependency and build manifests: `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Dockerfile`, `compose.yaml`, and related lockfiles.
- Source structure, framework entrypoints, existing feature patterns, shared utilities, tests, and configuration.

Prefer project conventions over generic advice. If an existing dependency or framework feature satisfies the requirement, prefer it over adding a new dependency.

## Comparison Checklist

Evaluate each relevant option:

- **Standard Library / Built-in API**: Is there a safe built-in API that satisfies the requirement with acceptable maintainability?
- **Framework Feature**: Does the framework already provide a supported pattern or extension point?
- **Existing Dependency**: Can an installed dependency solve this without expanding the dependency graph?
- **New Library**: Is the added dependency justified by complexity, correctness, security, maintenance, and project fit?
- **Custom Implementation**: Is the scope small enough to build and maintain locally without hidden risk?

Do not recommend a new library because it seems convenient. Tie the recommendation to the current requirement and the project's conventions.

## High-Risk Self-Build Areas

Explicitly check for self-build risk when the change touches:

- Security, authentication, authorization, permissions, cryptography, password storage, secrets, or input validation.
- Date/time handling, time zones, localization, parsing, serialization, or file formats.
- Concurrency, background jobs, retries, network communication, rate limits, or distributed behavior.
- Database migrations, transactions, schema evolution, data retention, logging, monitoring, or auditability.

For these areas, prefer proven standard APIs, framework features, or established libraries unless the custom implementation is clearly narrow and low risk.

## Output Format

When this skill is used, respond in this format unless the user asks for a different structure:

1. **Requirement Summary**
2. **Existing Project Context**
3. **Candidate Approaches**
   - Standard Library / Built-in API
   - Framework Feature
   - Existing Dependency
   - New Library
   - Custom Implementation
4. **Self-Build Risk**
5. **Recommended Approach**
6. **Reason**
7. **Implementation Plan**
8. **Assumptions / Open Questions**

Keep the result compact and decision-oriented. The output may be short for Lite Research, but it must include the recommended approach, reason, and implementation plan before coding begins.

## References

- For short usage examples and an `AGENTS.md` rule snippet, see `references/usage-and-agents.md`.
