---
name: frontend-design-brief
description: Use when Codex needs to clarify, evaluate, or preserve frontend design direction before implementing or modifying browser-based or embedded web UIs, including websites, web apps, Electron, Tauri, WebView-based desktop apps, VS Code webviews, dashboards, local tools, and other HTML/CSS/JS-rendered interfaces. Trigger when the user provides generated images, screenshots, existing UI, asks for design changes, asks to redesign part or all of a frontend, or wants implementation rules that keep visual design consistent.
---

# Frontend Design Brief

Use this skill to turn vague frontend design intent into an explicit design brief before implementation, then keep the implementation aligned with that brief.

This skill owns design clarification and brief creation. When implementation begins, use this brief alongside `frontend-skill` for visual composition, imagery, hierarchy, and motion.

## Core Rule

Before non-trivial frontend design work, clarify the design direction. Ask 1-3 focused questions only when an unresolved choice materially affects the result and cannot be inferred from the request or existing UI. A clear written direction removes the need for clarification questions; new screens and substantial layout or navigation changes still follow the visual review below.

## Workflow

1. Identify the design source: generated image, screenshot, existing UI, written direction, or requested redesign.
2. If images are provided, analyze them before proposing a direction.
3. If modifying existing UI, determine the intended scope: small, medium, or large.
4. Ask scope-appropriate questions only when needed.
5. Produce a concise design brief.
6. For new screens or substantial layout or navigation changes, present a visual wireframe and obtain approval before implementing the proposed UI.
7. During implementation, preserve the approved visual direction and brief.
8. After frontend changes, verify the rendered UI with Browser or Playwright whenever the project can be run locally.

## Visual Review Before Implementation

- Use this review for new screens and substantial changes to layout, information hierarchy, or navigation. Skip it for typo fixes, small spacing or color adjustments, behavior fixes that preserve the screen structure, and work within an already approved design. An explicit instruction to implement without prior review takes precedence. Asking Codex to choose a design alone does not waive this review.
- Build the smallest visual proposal that makes the decision concrete: normally one representative screen at the intended viewport size, with key content, controls, and the main action. Include another size or state only when it changes the layout or flow being reviewed. Do not design every screen in advance.
- Show an actual viewable wireframe using a local HTML preview, rendered image, or another available visual tool. Use realistic labels and content lengths. If color, typography, or atmosphere is central to the request, add a styled mockup. Explain what the preview demonstrates and which details are provisional; a text brief or file path alone does not satisfy visual review.
- Creating the preview is authorized preparatory work. Keep it limited to communicating the proposal; defer production UI integration, behavior, and data connections until approval. Keep the brief in chat rather than creating a new Markdown document by default.
- Present the preview with a short explanation of the main layout decisions and ask whether to implement it or revise it. Wait for the user's answer before implementing that proposal. While waiting, continue only work that does not depend on the visual choice. Silence or elapsed time is not approval. If a visual preview cannot be shown, explain the limitation and agree on a review method before dependent implementation.
- Reuse a supplied mockup or wireframe when the user has explicitly approved it for implementation and it covers the affected layout and flow. After approval, proceed through implementation and verification without repeated checks for minor refinements. Return for visual review only when a material deviation changes the approved structure or flow.

## Image-Based Direction

When the user provides or references an image from `gpt-image-2.0`, Codex app image generation, screenshots, mockups, or other visual references:

- Analyze layout, composition, color, typography, spacing, surface treatment, visual density, component shape, imagery, and mood.
- Name the apparent design styles with established design vocabulary.
- Ask how closely to follow those styles only when the user's intent is unclear.
- Do not treat image analysis as approval; reuse an explicitly approved implementation reference under the visual review rule.

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
- Proposed or approved design direction, clearly distinguished
- Visual vocabulary
- Layout rules
- Component rules
- Color and typography direction
- Constraints
- Verification plan
