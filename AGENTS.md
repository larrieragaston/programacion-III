# AGENTS.md

Instructions for any agent (Claude Code or otherwise) working in this repository. Read this before touching anything — it's the canonical, up-to-date reference for how this repo is built and maintained. `README.md` is the short human-facing version; `PLAN-UNIDAD-4.md` is the detailed content spec for the topics still being built; `.cursor/rules/pdf-to-slidev.mdc` is the step-by-step recipe for turning a source PDF into a new deck. This file is the one to keep updated as conventions evolve — if you change how something works, update the relevant section here in the same PR.

## What this repo is

Course material for **Programación III** at INSPT-UTN (Tecnicatura Superior en Informática Aplicada, Turno Noche, docente Prof. Ing. Gastón Larriera). Each topic is a standalone [Slidev](https://sli.dev/) presentation; most core topics also have a companion [VitePress](https://vitepress.dev/) site with a theory apunte and an exercise guide. Everything deploys automatically to GitHub Pages on push to `main` — **that means a push to `main` is a real publish to the site students use**, not a routine save point. See "Git workflow" below.

Live site: https://larrieragaston.github.io/programacion-III/

## Repo architecture

This is a monorepo of independent projects, not an npm workspace — each subfolder has its own `package.json`, `node_modules`, and is installed/run separately.

Two recurring patterns:

- **`<slug>/`** — a Slidev deck. Standalone project: `package.json` (`dev`/`build`/`export` scripts), `slides.md`, `global-top.vue` (fixed home icon back to the landing page, hidden during export — generic, identical across every deck, easy to forget when scaffolding a new one since its absence doesn't break the build), `public/` for images/logos, `pdfs/` (symlinked to `public/pdfs`) for generated PDFs.
- **`<slug>-docs/`** — a VitePress site: `docs/apunte.md`, `docs/ejercicios.md`, `docs/index.md` (hero landing), `docs/.vitepress/` (config + shared theme), `scripts/print-pdfs.mjs` (Playwright PDF export). Not every deck has one (`introduction/` and `fp-backus/` don't).

Root level: the landing page (`index.html`/`index.css`/`index.js`), `dev.sh` (local dev orchestration), `.github/workflows/deploy.yml` (CI), and this documentation.

### Current inventory

The landing page's own filter chips (Unidades / Próximamente / Extra / Deprecado) are the live source of truth for what exists — check `index.html` or the deployed site rather than trusting a stale list here. As of this writing:

- **Built (`data-category="unidad"`)**: Introducción (deck only), Cálculo λ, Clojure, Git & GitHub, JS Funcional, JS Contemporáneo, Asincronismo, TypeScript, React (deck + docs each, except Introducción).
- **Deprecated**: FP — John Backus (deck only, superseded by the Cálculo λ / Clojure / JS Funcional sequence).
- **Planned (`data-category="proximamente"`, placeholder cards already in the grid)**: Node + Express, MongoDB, Pruebas (Testing) — full spec for each in `PLAN-UNIDAD-4.md` section 5.
- **Optional/extra (`data-category="extra"`, placeholder cards already in the grid)**: Next.js, Tailwind CSS, NestJS, React Native con Expo — spec in `PLAN-UNIDAD-4.md` section 7.

## Local dev workflow

```bash
npm install                # root deps (concurrently)
cd <slug> && npm install   # per-deck deps, first time only — use `ulimit -n 10240` on macOS first
npm run dev                # root: starts index + every Slidev deck via dev.sh
npm run dev:no-export       # same, but skips the PDF re-export step on startup
```

`dev.sh` starts:
- The index page at `http://localhost:3030` (`npx serve`)
- Every Slidev deck on a **hardcoded** port — see the `MODULES`/`PORTS` arrays at the top of `dev.sh`. There is no auto-discovery here (despite what old docs used to imply): a new deck must be added to both arrays manually, in the same order, or it won't come up with `npm run dev`.

**`dev.sh` does not start `-docs/` sites.** Those are VitePress dev servers, started manually, one at a time, from their own folder:

```bash
cd <slug>-docs && npm install   # first time only — runs postinstall: playwright install chromium
npm run docs:dev
```

### Port table

| Slug | Slidev deck port | `-docs/` `docs:dev` port | `-docs/` `PRINT_PORT` |
|---|---|---|---|
| introduction | 3031 | — | — |
| lambda-calculus | 3032 | 5173 | 4173 |
| fp-backus | 3033 | — | — |
| clojure | 3034 | 5175 | 4174 |
| git-github | 3035 | 5177 | 4175 |
| js-funcional | 3036 | 5179 | 4176 |
| js-contemporaneo | 3037 | 5181 | 4177 |
| asincronismo | 3038 | 5183 | 4178 |
| typescript | 3039 | 5185 | 4179 |
| react | 3040 | 5187 | 4180 |

Asincronismo, TypeScript and React were built in parallel branches off `main` (not sequentially) — ports were pre-assigned per `PLAN-UNIDAD-4.md` section 6 so they wouldn't collide once merged. All three are now merged into `main`. Index page: `3030`. Next free deck port: `3041`. Next free `-docs/` pair: `5189` / `4181` (docs:dev increments by 2, PRINT_PORT by 1 — they drifted apart early on; always grep the actual `package.json`/`print-pdfs.mjs` files to confirm rather than trusting a table, this one included). `PLAN-UNIDAD-4.md` section 6 has the full reserved table through the rest of the core program.

### Regenerating PDFs

Every exported PDF (deck slides, apunte, ejercicios) is gitignored — a fresh clone has none, and every "Descargar" link on the landing will show as unavailable (grayed out, via the HEAD-request availability check in `index.js`) until you generate them:

```bash
cd <slug> && npm run export        # deck slides → pdfs/exports/<slug>-slides-export.pdf
cd <slug>-docs && npm run docs:pdf # builds the site + prints apunte/ejercicios, copies them into ../<slug>/pdfs/originales/
```

`npm run dev` (root) re-exports every deck's slides automatically on startup (`DISABLE_EXPORTS_ON_DEV=1` / `npm run dev:no-export` to skip). `docs:pdf` for the `-docs/` sites is always manual — nothing runs it for you locally.

## The landing page (`index.html` / `index.css` / `index.js`)

As of the redesign in PR #6, the landing is a **filterable card grid**, not a stacked list of sections. Structure:

```html
<nav class="filters">
  <button class="filter active" data-filter="todas">Todas (17)</button>
  <button class="filter" data-filter="unidad">Unidades</button>
  <button class="filter" data-filter="proximamente">Próximamente</button>
  <button class="filter" data-filter="extra">Extra</button>
  <button class="filter" data-filter="deprecado">Deprecado</button>
</nav>

<div class="grid">
  <!-- order is always fixed: Unidades → Próximamente → Extra → Deprecado -->
  <div class="card" data-category="unidad">
    <div class="card-title">JS Contemporáneo</div>
    <div class="card-desc">...</div>
    <div class="card-actions">
      <a class="view-link" href="./js-contemporaneo/" data-dev-port="3037">Presentación</a>
      <a class="view-link" href="./js-contemporaneo-docs/" data-dev-port="5181" data-dev-path="/">Material teórico</a>
      <div class="card-download-menu">
        <button class="card-download-menu-trigger" aria-expanded="false" aria-haspopup="true"
                aria-controls="menu-pdf-js-contemporaneo" id="menu-pdf-js-contemporaneo-btn">
          <span class="card-download-menu-label">Descargar</span>
          <svg class="card-download-dropdown-chevron">...</svg>
        </button>
        <div class="card-download-menu-panel" id="menu-pdf-js-contemporaneo" hidden>
          <a href="./js-contemporaneo/pdfs/exports/js-contemporaneo-slides-export.pdf" download target="_blank" rel="noopener noreferrer">Presentación (PDF)</a>
          <a href="./js-contemporaneo/pdfs/originales/js-contemporaneo-apunte.pdf" download target="_blank" rel="noopener noreferrer">Apunte teórico</a>
          <a href="./js-contemporaneo/pdfs/originales/js-contemporaneo-ejercicios.pdf" download target="_blank" rel="noopener noreferrer">Guía de ejercicios</a>
        </div>
      </div>
    </div>
  </div>
</div>
```

Key points:
- **One card per module**, not one card per resource. Every downloadable file (slides PDF, apunte, guía de ejercicios, ejercicios adicionales) lives in a single unified `.card-download-menu` dropdown per card — even a module with only one file still uses the dropdown pattern, for visual consistency.
- **`data-category`** drives both the fixed display order and the filter chips: `unidad` | `proximamente` | `extra` | `deprecado`.
- **`data-pending="true"`** marks a card as "not built yet" independent of category — both the plain `proximamente` cards and any `extra` card that isn't built yet carry it. The "Próximamente" filter chip matches on `data-pending`, not on `data-category`, so an unbuilt "Extra" topic shows under *both* the "Extra" filter (by category) and the "Próximamente" filter (by pending status) — see `index.js`'s filter click handler. When a topic is actually built, remove `data-pending` and its badge; it then only matches its category's filter.
- **Badges** (`.badge-proximamente`, `.badge-optional` for Extra, `.badge-deprecated`) only appear on non-`unidad` cards, top-left, as the card's first child. A card can carry two badges (Extra + Próximamente) side by side in a `.badge-row`.
- **`.card-deprecated`** adds `opacity: 0.5` to the whole card — every child element still functions (links, downloads), it just reads as visually dimmed. Don't mistake a dimmed deprecated-card link for a disabled one; check for the actual `is-disabled` class if in doubt.
- **`data-dev-port`/`data-dev-path`** on `.view-link` anchors: `index.js` rewrites these to `http://localhost:{port}{path}` when running on `localhost`, so the same markup works in dev and in production.
- **PDF availability**: `index.js` does a `HEAD` request against every download link on page load; a dead link gets `.is-disabled` and, if *every* link in a card's menu is dead, the whole trigger gets disabled and its label changes to "No disponible". This is why a fresh clone with no PDFs generated shows everything grayed out — it's not a bug, see "Regenerating PDFs" above.
- **Activating a placeholder card**: find the module's existing `data-category="proximamente"` (or `"extra"`) card, remove `data-pending` and its `<span class="badge">`, set `data-category="unidad"` if it was a core topic, and add the real `.card-actions` block copied from an already-activated card. Don't create a new card from scratch for a core/extra topic that already has a placeholder — it's already positioned correctly in the grid order.
- **Mobile**: `@media (max-width: 640px)` collapses the grid to 1 column — same breakpoint the rest of the site has always used.

The full original design spec (colors, spacing, interaction details) is in `landing-redesign/README.md` — useful historical context, but the implementation above is the actual current source of truth.

## Content conventions

From `PLAN-UNIDAD-4.md` section 4, applying to all new decks/docs:

- **Language split**: explanatory text (slides, apuntes, exercise statements) in **Spanish**. Code — variable/function/class names, keywords, in-code comments — in **English**. This is an explicit instructor requirement, not a style preference.
- **Slidev frontmatter template** (matches every existing deck):
  ```yaml
  ---
  theme: bricks
  title: Programación III - <Deck name>
  download: true
  info: |
    <Short description>
    INSPT - UTN
  author: Gastón Larriera
  keywords: <keywords>, INSPT, UTN
  transition: slide-left
  mdc: true
  ---
  ```
- **Folder slug**: lowercase, hyphenated, English (`js-funcional`, `git-github`, not `JS-Funcional` or `js_funcional`).
- **Narrative continuity**: each deck opens by explicitly referencing the previous one — this is a deliberate pedagogical thread (e.g. Clojure opens by referencing Cálculo Lambda, JS Funcional opens by referencing Clojure). Don't write a deck as if it's a standalone topic.
- **Core topics need both a deck and an apunte+ejercicios `-docs/` site.** Optional/extra topics (section 7 of the plan) don't, unless the instructor asks otherwise.

### `-docs/` site conventions

Every `<slug>-docs/` follows the same internal layout — use `git-github-docs/` as the exact template for a new one:

```
<slug>-docs/
├── package.json              # docs:dev/docs:build/docs:pdf/docs:preview scripts, own docs:dev port
├── utn-mark-logo.png         # copied as-is, used in the PDF header
├── docs/
│   ├── index.md              # hero landing, same pattern as clojure-docs/docs/index.md
│   ├── apunte.md
│   ├── ejercicios.md
│   ├── public/favicon.svg    # own icon per topic — see "known bug patterns" below (was accidentally copy-pasted identical across three sites at one point; don't reuse another topic's without changing it)
│   └── .vitepress/
│       ├── config.ts         # copy and change title/description/base/nav
│       └── theme/
│           ├── index.ts      # nearly identical across sites
│           └── custom.css    # **not byte-identical** across sites despite the intent — see below
└── scripts/
    └── print-pdfs.mjs        # copy, change PRINT_PORT and the cross-copy target paths
```

- **`custom.css` is meant to be shared but has drifted**: each site's copy has accumulated its own deck-specific classes (e.g. `.paradigm-tree` for js-funcional, `.lambda-lisp-clojure-compare-wrap` for lambda-calculus, `.branch-diagram-wrap` for git-github) on top of a common base. When fixing a bug in the shared parts (like the print `@media` block), **apply the fix to all 5 copies**, not just one — diff them first (`diff <(awk '/@media print/,/^}$/' a/custom.css) <(awk '/@media print/,/^}$/' b/custom.css)`) to find the identical anchor point in each file rather than assuming line numbers match.
- **`print-pdfs.mjs` copies its output to the sibling deck**, not to its own site: PDFs land in `<slug>/pdfs/originales/` (symlinked to `<slug>/public/pdfs/originales/`), so the Slidev build packages them and the landing's download links point at `./<slug>/pdfs/originales/...pdf`, never `./<slug>-docs/...`.
- **`apunte.md`**: denser than a slide — full explanations, not bullet points. **`ejercicios.md`**: progressive (simple → complex), one `##` heading per exercise, usually a numbered sub-list of steps within each.

## Known bug patterns (check for these before calling anything done)

These have all been hit for real in this repo. QA is not complete until you've checked both the live rendering **and** the actual exported PDF — several of these are invisible on screen and only show up in print.

- **Narrow-card code overflow**: a code block inside `.info-card`/a narrow grid column doesn't wrap. On screen there's a scrollbar (easy to miss); in the Playwright print render it clips silently with no visual cue at all. Fix: break long lines into multiple short lines inside the fenced code block.
- **`break-inside: avoid` full-page jump**: `custom.css`'s `@media print` sets `break-inside: avoid` on `.card-grid` (among others) so a card grid doesn't split across pages — but on a *large* grid (6+ cards) this can force the entire block to jump to the next PDF page, leaving the previous page mostly blank. Keep `card-grid` blocks to roughly ≤4-6 cards; split a bigger set into several smaller grids.
- **2+ digit `<ol>` markers clipped in print**: the same `@media print` block sets `padding: 0 !important` on `.vp-doc`/`.VPDoc` (to avoid double margins, since the page margin is handled by Playwright's print settings). That leaves list markers with only their own ~20px `padding-inline-start` to render in — enough for `1.`–`9.` but not for `10.`, `11.`, etc., which get cut off against the page's left edge. Already fixed (all 5 `custom.css` copies have `.vp-doc ol { padding-inline-start: 1.85em; }` inside `@media print`) — if you touch that block again, keep this rule or the bug comes back.
- **Forward/backward reference bugs after reordering**: prose like "ya visto" / "como vimos antes" / "más adelante" becomes factually wrong the moment a section moves earlier or later in the document. After any reorder, grep for `ya vist|más adelante|próxim.*slide|a continuaci` (or similar) in the touched file and check each hit is still true.
- **Heading-hierarchy orphaning in VitePress**: promoting/demoting a `##`/`###` heading changes the sidebar TOC nesting. Moving a `##` section away can leave its old sibling `###` subsections incorrectly nested under an unrelated `##` that happens to now precede them. Check the rendered sidebar after any structural move in an `apunte.md`.
- **Stale Slidev/Vite dev-server state**: after many sequential structural edits to `slides.md`, the dev server can keep serving stale content for a specific route even after a hard refresh. If a slide shows content that doesn't match the source file, kill and restart the Slidev process rather than trusting HMR.
- **`?print` query param** on a running Slidev deck renders the print/export layout in a normal browser tab — use it for fast iteration, but always confirm the *actual* exported PDF (`npm run export`) matches before confirming a deck done; print-mode rendering in a live browser and Playwright's headless print aren't always pixel-identical.
- **`npm install` on a new deck can pull a broken `markdown-exit`**: `unplugin-vue-markdown` depends on `markdown-exit` via a semver range, not a pin. A fresh `npm install` (any deck set up after roughly mid-2026) can resolve `markdown-exit@1.2.0`, whose stricter `Renderer.renderInline` throws `async rule detected, use renderInlineAsync()` the moment a slide has syntax-highlighted inline code (single backtick spans) — breaks the Overview page and, per-slide, sometimes the slide itself, with `slides.md` content that is otherwise completely valid Markdown. It looks exactly like a content bug (the error message points at your `.md` file) but isn't — every already-built deck's `node_modules` has the older `markdown-exit@1.0.0-beta.9`, which doesn't have this issue. Don't chase it by editing slide content. Fix: add `"overrides": { "markdown-exit": "1.0.0-beta.9" }` to the deck's `package.json` (see `asincronismo/package.json`) and re-run `npm install`. Confirm with `node -p "require('./node_modules/unplugin-vue-markdown/node_modules/markdown-exit/package.json').version"` — should print `1.0.0-beta.9`. If a future deck still breaks with this override in place, the fix may need a version bump instead; check whether newer `markdown-exit`/`unplugin-vue-markdown` releases have resolved the regression before assuming the pin is stale.

- **Scaffolding a new `-docs/` site by copying a sibling can leave its favicon un-swapped**: `js-contemporaneo-docs`, `asincronismo-docs`, and `typescript-docs` all shipped with byte-identical `favicon.svg` (verify with `md5`/`md5sum` across every `-docs/docs/public/favicon.svg`) — nobody customized it after copying the template. Not visible in normal review since the icon is small and each site otherwise looks distinct; fixed by giving each topic its own small `<rect>` + glyph/icon SVG (32x32 viewBox, `rx="6"` rounded background), following the pattern already used by `lambda-calculus-docs`/`clojure-docs`/`git-github-docs`/`js-funcional-docs`. Check this whenever a new `-docs/` site is scaffolded.

## Git workflow

- **Never `git push` to `main` without the instructor's explicit go-ahead.** `deploy.yml` publishes to the live GitHub Pages site on every push to `main` — a premature push ships unfinished or unreviewed material to real students.
- Local commits are fine and encouraged for checkpointing; the push (and PR merge) is a separate, deliberate step the user asks for explicitly.
- Work happens on feature branches (`feature/<topic>`, `docs/<topic>`, etc.), one branch per deck/topic/change, opened as a PR against `main`. After a merge, sync `main` (`git checkout main && git pull`) before branching again — don't assume the local `main` is current.
- Commit messages: Conventional-Commits-flavored (`feat(slug): ...`, `fix: ...`, `docs: ...`), in Spanish or English consistent with the surrounding history — check `git log --oneline` for the current tone before writing one.

## Reference documents

- **`PLAN-UNIDAD-4.md`** — the detailed spec for every topic still being built (objectives, suggested content, references, port reservations). Written to be picked up by a fresh agent with zero prior context — read it fully before starting a new deck.
- **`.cursor/rules/pdf-to-slidev.mdc`** — step-by-step workflow for turning a source PDF into a new Slidev deck (OCR extraction, folder scaffolding, `package.json` template, icon sourcing, updating the landing).
- **`landing-redesign/`** — the original design handoff (`README.md` spec + static `reference.html`) used to build the current landing page. Historical reference for *why* the landing looks the way it does; the actual implementation in `index.html`/`index.css`/`index.js` is the source of truth going forward.
