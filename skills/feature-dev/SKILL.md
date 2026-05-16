---
name: feature-dev
description: Structured feature development workflow for Codex. Use when the user asks to implement a feature, develop a non-trivial change, compare designs before implementation, clarify requirements before coding, or proceed with feature-dev. Guides discovery, codebase exploration, clarification, design comparison, implementation, review, and summary while following applicable AGENTS.md instructions.
---

# Feature Development

Use this skill to handle new features and medium-or-larger changes with exploration and design before implementation.

This skill defines the workflow for discovery, design, implementation, review, and summary. It does not replace applicable `AGENTS.md`, repository instructions, user instructions, or tool-specific rules.

## When To Use

Use this skill when the task involves:

- Adding a new feature.
- Extending existing code while checking impact.
- Understanding the codebase and comparing designs before implementation.
- Separating post-implementation review into clear review concerns.

For small fixes or obvious single-file changes, skip this skill and use the normal workflow.

## Core Principles

- Understand first. Do not implement before finding the relevant existing patterns.
- Remove ambiguity. Ask about important gaps before coding.
- Compare options when the implementation is non-trivial.
- Follow the existing codebase conventions.
- Review the result by separate concerns after implementation.
- Do not start broad implementation without explicit user approval.

## Recommended Architecture

```text
Orchestrator (this skill)
  - Phase 1: Discovery
  - Phase 2: Codebase Exploration
    - Use agents/explorer.md perspective when useful
  - Phase 3: Clarifying Questions
  - Phase 4: Architecture Design
    - Use agents/architect.md perspective for design comparison
  - Phase 5: Implementation
  - Phase 6: Quality Review
    - Use agents/reviewer.md perspective for review
  - Phase 7: Summary
```

Use sub-agents according to the applicable `AGENTS.md` Sub-Agent Delegation policy. This skill defines the feature-development workflow and does not prevent sub-agent use.

## Workflow

### Phase 1: Discovery

Extract the following from the request:

- What to build.
- What problem it solves.
- What is out of scope.
- Known constraints.

If the feature request is ambiguous, ask the smallest useful set of questions. If the request is clear enough, skip questions.

Create a concise task list. Use `update_plan` when available and useful; otherwise summarize the plan briefly in the conversation.

### Phase 2: Codebase Exploration

Understand the relevant code. According to the applicable `AGENTS.md` Sub-Agent Delegation policy, delegate exploration with the `agents/explorer.md` perspective when the work can be split safely. If not delegating, apply the same perspective locally.

Exploration themes:

- Similar features.
- Relevant architecture and abstraction boundaries.
- Extension points across UI, API, data, and tests.

For each exploration pass, collect:

- 5-10 important files.
- Main call flows.
- Existing naming, responsibility boundaries, error handling, and test patterns.
- Risks when changing the code.

After receiving exploration results, read the important files yourself before making implementation decisions.

### Phase 3: Clarifying Questions

Compare the exploration results with the initial request and identify unresolved decisions.

Check for:

- Edge cases.
- Error handling.
- Consistency with existing behavior.
- Backward compatibility.
- Performance requirements.
- UI or API behavior.
- Scope boundaries.

Group questions together. Do not skip this phase when important uncertainty remains.

If the user says to decide, state your recommended assumption and proceed on that basis.

### Phase 4: Architecture Design

For medium-or-larger changes, compare at least two options using the `agents/architect.md` perspective:

- Minimal-change option.
- Balanced option.

For broad or high-impact features, optionally include an extensibility-focused option.

Each comparison must include:

- Files to create or modify.
- Fit with existing code.
- Complexity.
- Testability.
- Future extensibility.

Finish with one recommended option and concrete reasons.

### Phase 5: Implementation

Start implementation after explicit approval when the change is broad or the design needed user confirmation.

Implementation rules:

- Re-read important files before editing them.
- Preserve existing responsibility boundaries.
- Implement broad changes in stages.
- Add or update relevant tests and validation.
- Share concise progress updates.

According to the applicable `AGENTS.md` Sub-Agent Delegation policy, use `worker` sub-agents when the work can be split by write scope. Assign clear ownership and tell workers not to revert changes made by others.

### Phase 6: Quality Review

After implementation, review using the `agents/reviewer.md` perspective. According to the applicable `AGENTS.md` Sub-Agent Delegation policy, delegate review when the scope can be split safely.

Review concerns:

- Bugs, missing behavior, and regressions.
- Simplicity, duplication, and responsibility boundaries.
- Project conventions, tests, and operational concerns.

Prioritize important findings and avoid low-value noise.

When findings exist, summarize:

- What is wrong.
- Where it is.
- Whether it should be fixed before finishing.

### Phase 7: Summary

Report:

- What was implemented.
- Important decisions.
- Changed files.
- Validation performed.
- Remaining risks or follow-up candidates.

## Sub-Agent Perspectives

- Exploration: [agents/explorer.md](agents/explorer.md)
- Design comparison: [agents/architect.md](agents/architect.md)
- Review: [agents/reviewer.md](agents/reviewer.md)

When delegating, provide only the necessary context and a clear output format. Do not pre-load the sub-agent with your conclusion unless the task requires it.

## Output Style

- Respond to the user in the language required by the active instructions.
- Keep design comparisons concise.
- Do not begin implementation while important requirements remain unresolved.
- Keep final summaries short and high-density.