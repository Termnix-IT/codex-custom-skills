# Implementation Rules

Use these rules after the design direction is clear and any required visual review in `SKILL.md` is complete. They are implementation constraints, not a replacement for inspecting the existing project.

## Preserve the Brief

- Do not introduce a new visual style during implementation unless the user approves it.
- Keep color, spacing, typography, component shape, density, and hierarchy aligned with the approved brief.
- If implementation constraints require a change, state the tradeoff and choose the smallest deviation. Re-present the affected visual proposal before implementing a material change to the approved structure or flow; minor refinements within the approved direction do not need another approval.

## Existing Systems

- Prefer existing components, tokens, utility classes, layout primitives, and interaction patterns.
- Do not add a new design system for a narrow change.
- Keep edits scoped to the requested surface unless shared components must change.
- Match the repository's framework, CSS strategy, state patterns, and asset pipeline.

## Layout

- Use stable dimensions for fixed-format UI such as toolbars, boards, grids, sidebars, tabs, counters, and cards.
- Avoid layout shifts when content changes.
- Ensure text does not overlap or overflow its parent.
- Use responsive constraints such as `minmax`, `clamp` only for dimensions, `aspect-ratio`, container queries, or explicit min/max widths where appropriate.
- Do not scale font size directly with viewport width.
- Do not put UI cards inside other UI cards.

## Typography

- Match type scale to context.
- Use compact headings inside tool panels, dashboards, sidebars, cards, and embedded app surfaces.
- Reserve hero-scale type for true hero sections.
- Keep letter spacing at `0` unless the existing design system explicitly uses another value.
- Ensure the longest expected labels fit in controls.

## Color

- Avoid one-note palettes dominated by one hue family.
- Use accent colors deliberately for hierarchy, status, or action.
- Maintain readable contrast across normal, hover, active, disabled, selected, focus, and error states.
- Avoid defaulting to heavy purple, dark blue, beige, brown, or orange themes unless requested or already established.

## Components

- Use icons for familiar tool actions when available.
- Use segmented controls for modes, toggles for binary settings, sliders or inputs for numeric settings, menus for option sets, and tabs for views.
- Keep buttons for clear commands.
- Build expected states: loading, empty, error, disabled, selected, active, hover, focus, and long-content states when relevant.
- Do not use visible in-app text to explain obvious UI mechanics or design choices.

## Websites

- Use visual assets when the page depends on product, place, object, person, game, or brand context.
- Do not default to generic gradient or SVG hero visuals when real or generated imagery would communicate better.
- For landing pages, ensure the first viewport clearly signals the brand, product, place, person, object, or literal offer.
- Ensure the next section is hinted in the first viewport on mobile and desktop.

## Embedded Web UI

- Do not assume full browser viewport behavior.
- Support app-like resizing and compact layouts.
- Respect fixed and minimum window sizes.
- Account for app chrome such as title bars, sidebars, status bars, native menus, and host-provided padding.
- Keep controls reachable and predictable.
- Check focus, hover, keyboard, scrolling, and modal behavior.
- Avoid oversized landing-page sections in desktop app surfaces.
- Prefer split panes, inspectors, toolbars, tables, lists, and panels when the surface is task-focused.

## Verification

- After frontend changes, run the project and verify the rendered UI with Browser or Playwright whenever possible.
- Check at least one desktop viewport and one narrow viewport for browser-based web apps.
- For embedded app UI, check the expected minimum window size and a larger resized state.
- Look for blank screens, console errors, missing assets, overlap, text overflow, layout jumps, and unusable controls.
- If verification cannot be run, state why and describe the residual visual risk.
