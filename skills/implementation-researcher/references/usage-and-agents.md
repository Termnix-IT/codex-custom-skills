# Usage Examples And AGENTS.md Snippet

## Short Usage Examples

Use this skill before adding a dependency:

> Use `implementation-researcher` before adding CSV export. Check whether the project already has a CSV or table utility, compare built-in APIs and lightweight libraries, then propose an implementation plan.

Use this skill before changing design or state management:

> Use `implementation-researcher` before refactoring settings persistence. Inspect the existing storage pattern, compare framework storage helpers, current dependencies, and custom code risks, then recommend an approach.

Use this skill before high-risk implementation work:

> Use `implementation-researcher` before implementing password reset. Research framework auth features, existing dependencies, token storage, validation, and security risks before proposing the plan.


Use this skill before improving existing custom code:

> Use `implementation-researcher` before refactoring the custom date parser. Check whether standard date APIs, framework utilities, existing dependencies, or a well-known parsing library can replace it safely, then recommend whether to keep, simplify, or replace the current implementation.

## AGENTS.md Snippet

```markdown
## Pre-Implementation Design

- Before deciding the feature shape, requirements, design, dependency strategy, or implementation approach for non-trivial work, use the `implementation-researcher` skill.
- Use it to compare built-in APIs, framework features, existing dependencies, new libraries, and custom implementation risks before coding.
- For Full Research, use explorer sub-agents only for bounded read-only research such as finding existing patterns, dependency usage, related tests, or framework capabilities.
- The main agent owns the final recommendation, implementation plan, architecture decisions, dependency decisions, and security judgment.
- Skip or keep this lightweight for typo fixes, documentation-only edits, and obvious changes that follow an existing local pattern.
```
