# Handoff: Landing Page Redesign (Programación III)

## Overview
Redesign of the course landing page at the repo root (`index.html` / `index.css` / `index.js`). Same purpose as today's page — link to each unit's Slidev presentation and VitePress theory docs — reorganized as a filterable card grid instead of a stacked list of sections.

## About the Design Files
`reference.html` in this folder is a **design reference built in plain HTML/CSS**, not production code to copy as-is. The task is to recreate this layout inside the existing repo's environment: it's a static site (no framework, no build step for the root page — see `index.html`/`index.css`/`index.js` and `dev.sh`), so the natural implementation is to update those same three files directly, keeping the existing dev-port auto-detection logic in `index.js` (`data-dev-port` / `data-dev-path` attribute handling) and the existing PDF-availability check (HEAD request that disables dead download links).

## Fidelity
**High-fidelity.** Colors, spacing, and typography below are final values, taken directly from the current `index.css` (not invented) plus new values for the added dropdown/badge states. Recreate pixel-perfectly.

## Screens / Views
Single screen: the landing page.

### Header
- Full-width bar, `padding: 1.8rem 2.5rem`, `background: linear-gradient(135deg, #1e3a5f, #2563eb)`, text white.
- Left: INSPT logo (`logo-inspt.png`, provided in this folder), `height: 52px`.
- Center (flex:1, text-align center): `<h1>Programación III</h1>` at `1.8rem/700`, subtitle "Turno Noche" at `0.95rem` opacity 0.85, small line "Material de clase · Ciclo Lectivo 2026" at `0.8rem` opacity 0.65.
- Right: 3 stacked pill links — Campus Virtual, Mail al docente, Web INSPT — `rgba(255,255,255,.15)` background, `1px solid rgba(255,255,255,.3)` border, `border-radius:.4rem`, `font-size:.75rem/500`.

### Filter chips
Row under the header, `padding: 26px 36px 0`, `gap: 10px`. Pills `padding: 8px 16px`, `border-radius: 20px`, `font-size: 12.5px/600`.
- Active chip: `background:#2563eb`, `color:white`.
- Inactive chip: `border:1px solid #e2e8f0`, `color:#334155`.
- Chips: "Todas (N)", "Unidades", "Próximamente", "Extra", "Deprecado". Filtering is visual only in the reference — wire up actual show/hide by category in implementation.

### Card grid
`padding: 22px 36px 32px`, `display:grid`, `grid-template-columns: repeat(3, 1fr)`, `gap:16px`. Responsive: collapse to 1 column under ~640px (same breakpoint as current `index.css`).

**Card ordering is fixed and always in this order:** Unidades (regular units) → Próximamente (future units) → Extra (optional/supplementary topics) → Deprecado (deprecated units, always last).

Each card: white background, `1px solid #e2e8f0` border, `border-radius:.75rem`, `padding:18px`, `display:flex; flex-direction:column; gap:12px`.
- **No unit numbers on cards** (deliberately removed from the previous iteration).
- Optional badge (top-left, only for Próximamente/Extra/Deprecado): `font-size:9.5px/700`, uppercase, `letter-spacing:.03em`, `padding:3px 7px`, `border-radius:5px`, `border:1px solid`.
  - Próximamente: `background:#f1f5f9`, `color:#64748b`, `border-color:#e2e8f0`.
  - Extra: `background:#eff6ff`, `color:#2563eb`, `border-color:#93c5fd`.
  - Deprecated: `background:#fef2f2`, `color:#dc2626`, `border-color:#fca5a5`. Deprecated cards additionally get `opacity:.5` on the whole card.
- Title: `font-size:14.5px/700`.
- Description: `font-size:11.5px`, `line-height:1.4`, `color:#64748b`.
- Actions row (`margin-top:auto` to pin to card bottom):
  - One pill per **viewable** resource (e.g. "Presentación", "Material teórico") — these link to the Slidev/VitePress site to view online. Style: `background:#eff6ff`, `border:1px solid #bfdbfe`, `color:#1d4ed8`, `border-radius:8px`, `padding:6px 10px`, `font-size:11px/600`.
  - One **"Descargar ▾" dropdown trigger**, same pill style, replacing the old one-link-per-file approach. Clicking opens a panel listing every downloadable file for that unit (slides PDF, apunte, guía de ejercicios, ejercicios adicionales, etc — however many apply). Panel: `position:absolute; top:calc(100% + 6px); left:0`, `min-width:12rem`, `padding:.35rem`, `background:white`, `border:1px solid #e2e8f0`, `border-radius:.65rem`, `box-shadow:0 4px 6px -1px rgba(0,0,0,.08),0 10px 20px -4px rgba(0,0,0,.12)`. Panel links: `padding:.5rem .65rem`, `border-radius:.45rem`, `font-size:.78rem/500`, `color:#1e293b`, hover `background:#eff6ff; color:#1d4ed8`.
  - Cards with no resources yet (Próximamente placeholders) show no action pills.

## Interactions & Behavior
- **Download dropdown**: click trigger toggles its panel; click outside or Escape closes it; only one panel open at a time. This exact behavior already exists in the current `index.js` for `.card-download-menu` — reuse/adapt it rather than rewriting, and keep the existing HEAD-request availability check (disable + "No disponible" for missing PDFs).
- **Filter chips**: clicking a chip should filter the grid to that category (Unidades / Próximamente / Extra / Deprecado) or show all; not implemented in the static reference.
- **Dev-port redirection**: keep the existing `index.js` logic that rewrites links to `http://localhost:{port}` on localhost, driven by `data-dev-port` / `data-dev-path` attributes on each card's main link.
- Hover states: card border can pick up `#2563eb` on hover (as in the current design) to signal interactivity.

## State Management
- No client-side data fetching beyond the existing PDF-availability HEAD checks.
- Filter state: which chip is active (single-select, default "Todas").

## Design Tokens
- Colors: background `#f8fafc`, text `#1e293b`, muted text `#64748b`, borders `#e2e8f0`, accent blue `#2563eb` / `#1d4ed8` (text), accent bg `#eff6ff`, accent border `#bfdbfe`, header gradient `#1e3a5f → #2563eb`, deprecated red `#dc2626` / bg `#fef2f2` / border `#fca5a5`, neutral badge `#64748b` / bg `#f1f5f9`.
- Font: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif` (unchanged from current site).
- Border radius: chips `20px`, cards `.75rem` (12px), buttons/pills `8px`, dropdown panel `.65rem` (~10px).
- Card grid gap: `16px`. Grid: 3 columns desktop, 1 column mobile.

## Content
The 4 real units today are: Introducción, Cálculo Lambda, Clojure, Git & GitHub — each with its actual title/description/resources as currently listed in `index.html`. "Próximamente" and "Extra" cards in the reference are placeholders; replace with real upcoming/supplementary topics as they're defined (8 more units are planned per the course owner).

## Assets
- `logo-inspt.png` — INSPT/UTN logo, copied from the repo root, included in this folder.
- No other new imagery; icons are inline SVG (chevron for dropdown) — keep as inline SVG, don't rasterize.

## Files
- `reference.html` (this folder) — static HTML/CSS reference implementation of the design, plus a minimal JS snippet showing the dropdown toggle pattern.
- Full option exploration (3 initial directions + iterations) lives in the project's `Landing Page Options.dc.html`, option id `3a`, if more context or the earlier discarded directions are useful.
- Target files to modify in the actual repo: `index.html`, `index.css`, `index.js`.
