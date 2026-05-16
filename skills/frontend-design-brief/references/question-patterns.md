# Question Patterns

Ask 1-3 questions at a time. Prefer concrete choices over open-ended prompts. Use design labels to make options easier to evaluate, but always explain what the label means in the current context.

## Image-Based Design

- "This reference reads as `minimal SaaS`: restrained borders, neutral surfaces, and clear hierarchy. Should the implementation follow that direction?"
- "The image has a `command center UI` feel with dense panels and status-heavy layout. Do you want that density preserved?"
- "The visual direction looks closer to `cyberpunk` than a standard dashboard. Should that be the full redesign direction, or only an accent?"
- "This looks like `futuristic restrained`: technical and modern without heavy neon. Is that the right balance?"
- "The image uses large imagery and strong type like an `editorial` layout. Should the page become more narrative, or stay app-like?"
- "The surface treatment resembles `glassmorphism`. Should I keep translucent panels, or convert them into solid cards for readability?"

## Small Scope

Use when changing one component, one section, one visual rule, or a narrow UI issue.

- "Should this header visually merge with the navbar, or read as a separate app bar?"
- "Should the left side include an icon, or stay text-first?"
- "Should this button become the primary visual anchor, or stay consistent with the existing button system?"
- "Do you want only spacing adjusted, or also color and typography?"
- "Should this card become flatter with subtle borders, or more elevated with stronger shadow?"
- "Should the change match the current style exactly, or introduce a small new accent?"

## Medium Scope

Use when changing related components, shared layout, design system alignment, or one feature area.

- "Should I start from shared components like header, sidebar, cards, and buttons before touching page-specific sections?"
- "Should the existing information density be preserved, or should the layout become more spacious?"
- "Should list and detail views share the same visual rules?"
- "Is this meant to align with the current design system, or introduce a new direction for this feature area?"
- "Should the common shell change first, or should only the content area be redesigned?"
- "Should filters, tables, and empty states be handled together so the workflow feels consistent?"

## Large Scope

Use for page-wide or app-wide redesign.

- "Should the whole product shift toward `minimal SaaS`, `command center UI`, `cyberpunk`, `luxury`, or another style?"
- "Should the current navigation and screen structure remain, or can the layout be redesigned?"
- "Is the priority daily usability, visual impact, brand expression, or conversion?"
- "Should the redesign be conservative, moderate, or dramatic?"
- "Should this feel more like a website, a dashboard, or a desktop application?"
- "Do you want to keep existing user flows and only change presentation, or revisit information architecture too?"

## Embedded Web UI

Use for Electron, Tauri, WebView, VS Code webviews, and similar app surfaces.

- "Is this UI meant to feel like a desktop app rather than a website?"
- "What minimum window size should the design support?"
- "Should the layout prioritize compact controls and split panes?"
- "Are title bars, sidebars, status bars, or native menus part of the visible surface?"
- "Should modals behave like lightweight app dialogs, or full-page flows?"
- "Should keyboard and focus behavior be treated as primary interactions?"

## When The User Says To Decide

If the user asks Codex to decide, make one conservative recommendation and confirm only if the change is broad or visually opinionated.

- "I recommend `calm productivity`: compact, readable, and durable for repeated use. I will proceed with that unless you want a more expressive direction."
- "For this Electron surface, I recommend `native-like desktop UI` with split panes and compact controls rather than landing-page composition."
- "For this landing page, I recommend `product showcase` so the actual product is visible in the first viewport."
