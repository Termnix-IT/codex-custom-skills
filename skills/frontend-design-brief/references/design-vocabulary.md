# Design Vocabulary

Use these terms to label visual direction clearly. Do not force a style label when it does not fit. When asking the user, explain the practical effect of the label in plain language.

## Minimal SaaS

Clean, restrained, product-focused UI with clear hierarchy, neutral backgrounds, subtle borders, and functional spacing.

Best for dashboards, settings, B2B tools, admin apps, onboarding flows, and product surfaces that should feel reliable.

Avoid when the user wants strong visual identity, spectacle, or expressive art direction.

## Utility UI

Dense, task-focused interface with compact controls, predictable navigation, and low decoration.

Best for internal tools, editors, monitoring screens, local tools, and desktop app surfaces.

Avoid for marketing pages or brand-first experiences.

## Native-Like Desktop UI

Embedded web UI that feels close to a desktop application, with compact controls, stable panels, menus, split panes, clear focus states, and keyboard-friendly behavior.

Best for Electron, Tauri, VS Code webviews, WebView apps, and local productivity tools.

## Command Center UI

High-information dashboard style with panels, metrics, status indicators, logs, maps, timelines, and operational controls.

Best for monitoring, security, incident response, analytics, infrastructure, and admin interfaces.

Avoid when the user needs calm reading, long-form content, or a low-density consumer interface.

## Dashboard UI

Structured data surface with charts, tables, filters, cards, and summaries.

Best for business intelligence, operations, admin panels, and reporting.

Distinguish from `command center UI`: dashboard UI can be calmer and less operational.

## Editorial

Magazine-like layout with strong typography, large imagery, deliberate whitespace, and narrative content flow.

Best for portfolios, articles, case studies, brand pages, and product storytelling.

Avoid for dense operational tools.

## Marketing Landing

Conversion-oriented page structure with a strong first viewport, offer-led messaging, social proof, feature sections, and clear calls to action.

Best for SaaS websites, product launches, waitlists, and service pages.

Avoid inside embedded desktop app surfaces unless the screen is explicitly promotional.

## Product Showcase

Visual-first product presentation that highlights the actual product, object, interface, or venue.

Best for product pages, portfolios, object-focused pages, and branded websites.

Use real or generated imagery when the user needs to inspect the thing being presented.

## Glassmorphism

Translucent surfaces, blur, layered depth, soft highlights, and low-contrast overlays.

Use sparingly. Verify contrast, readability, performance, and accessibility.

Avoid in dense tools where blur and transparency reduce scanability.

## Neumorphism

Soft extruded surfaces created by subtle inner and outer shadows.

Use only for narrow, decorative interfaces. It often creates weak contrast and unclear affordances.

## Cyberpunk

Dark, high-contrast, neon-accented, futuristic visual language with synthetic lighting, sharp contrast, and dramatic atmosphere.

Use only when the user explicitly wants a strong stylized direction, or when it is confirmed as an accent rather than a full redesign.

## Futuristic Restrained

Modern, technical, and slightly sci-fi without heavy neon or dramatic theming.

Best when the user wants advanced or AI-related tone while preserving professional usability.

## Brutalist

Raw, blocky, high-contrast, grid-forward, intentionally rough or unconventional layout.

Best for expressive sites and creative portfolios.

Avoid as a default for productivity tools.

## Luxury

Elegant spacing, restrained palette, high-quality imagery, refined typography, and subtle interaction.

Best for premium products, hospitality, fashion, portfolios, and high-end services.

Avoid when speed, density, or frequent operational use matters more than presentation.

## Playful

Colorful, rounded, expressive, animated, and approachable interface.

Best for games, kids products, creative tools, casual apps, and friendly onboarding.

Avoid for serious operational tools unless the brand requires it.

## Calm Productivity

Quiet, durable, low-distraction UI with balanced spacing, clear affordances, and restrained color.

Best for writing tools, planning apps, knowledge bases, and daily-use software.

## Data-Dense

Compact information layout with tables, filters, summaries, badges, and narrow spacing.

Best for expert workflows where users compare many records quickly.

Pair with strong alignment, predictable row heights, and careful overflow handling.

## Spatial Canvas

Large open workspace with zoom, pan, nodes, boards, or freeform arrangement.

Best for diagrams, whiteboards, maps, node editors, visual planning, and design tools.

Requires stable controls, minimaps or orientation aids when complexity grows, and careful empty-state design.

## Split-Pane Tool

App layout built from resizable or fixed panes, such as sidebar, editor, inspector, preview, and console.

Best for developer tools, editors, local utilities, and desktop-style interfaces.

## Content-First

Design that prioritizes reading flow, hierarchy, and legibility over controls or decoration.

Best for documentation, manuals, articles, notes, and study materials.

## Game UI

Expressive, stateful, animated interface designed around gameplay, score, inventory, controls, and feedback loops.

Use domain-appropriate assets and interaction feedback. Do not treat game UI like a generic SaaS dashboard.
