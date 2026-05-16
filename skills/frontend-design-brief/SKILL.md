---
name: frontend-design-brief
description: Use when Codex needs to clarify, evaluate, or preserve frontend design direction before implementing or modifying browser-based or embedded web UIs, including websites, web apps, Electron, Tauri, WebView-based desktop apps, VS Code webviews, dashboards, local tools, and other HTML/CSS/JS-rendered interfaces. Trigger when the user provides generated images, screenshots, existing UI, asks for design changes, asks to redesign part or all of a frontend, or wants implementation rules that keep visual design consistent.
---

# Frontend Design Brief

Use this skill to turn vague frontend design intent into an explicit design brief before implementation, then keep the implementation aligned with that brief.

This skill owns design clarification and brief creation. When implementation begins, use this brief alongside `frontend-skill` for visual composition, imagery, hierarchy, and motion.

## Core Rule

Before non-trivial frontend design work, clarify the design direction. If the user gives a clear instruction, proceed without unnecessary questions. If the direction is vague, image-derived, or broad enough to affect multiple UI decisions, ask 1-3 focused questions before implementing.

## Workflow

1. Identify the design source: generated image, screenshot, existing UI, written direction, or requested redesign.
2. If images are provided, analyze them before proposing a direction.
3. If modifying existing UI, determine the intended scope: small, medium, or large.
4. Ask scope-appropriate questions only when needed.
5. Produce a concise design brief.
6. During implementation, preserve the approved brief.
7. After frontend changes, verify the rendered UI with Browser or Playwright whenever the project can be run locally.

## Image-Based Direction

When the user provides or references an image from `gpt-image-2.0`, Codex app image generation, screenshots, mockups, or other visual references:

- Analyze layout, composition, color, typography, spacing, surface treatment, visual density, component shape, imagery, and mood.
- Name the apparent design styles with established design vocabulary.
- Ask whether the user wants the frontend to follow those styles.
- Do not treat image analysis as approval.

Read `references/design-vocabulary.md` when style labels or design terminology would help.

## Existing UI Modification

When modifying an existing UI, ask what scope the user intends unless already clear.

Classify scope:

- Small: one component, one section, one visual rule, or a narrow UI issue.
- Medium: multiple related components, shared layout, design system alignment, or one feature area.
- Large: whole-page redesign, app-wide direction change, brand-level visual change, or major style shift.

Read `references/question-patterns.md` for scope-specific questions.

## Embedded Web UI

For Electron, Tauri, WebView, VS Code webviews, and similar embedded web UI:

- Treat the UI as an app surface, not a marketing page.
- Respect fixed, minimum, and resizable window constraints.
- Account for title bars, sidebars, status bars, native menus, and app chrome.
- Prefer dense, durable, repeat-use interfaces over oversized landing-page composition.
- Check resize behavior, scroll regions, focus states, and modal positioning.

## Implementation Rules

During implementation:

- Follow the approved design brief.
- Prefer existing project design patterns, components, tokens, and layout primitives.
- Avoid unrelated redesigns.
- Keep typography, spacing, color, component shape, density, and hierarchy coherent.
- Prevent text overflow, layout shifts, and incoherent overlap.
- Use visual assets when the experience needs product, place, object, game, or visual identity context.
- Verify rendered output after frontend changes when possible.

Read `references/implementation-rules.md` before substantial implementation work.

## Design Brief Output

After clarification, produce a short design brief with:

- Scope
- Target surface
- Approved design direction
- Visual vocabulary
- Layout rules
- Component rules
- Color and typography direction
- Constraints
- Verification plan
