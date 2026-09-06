# Programación III - Material

Course material for **Programación III** at [INSPT - UTN](https://www.inspt.utn.edu.ar/) (Tecnicatura Superior en Informática Aplicada, Turno Noche).
Each topic is a [Slidev](https://sli.dev/) presentation, most paired with a [VitePress](https://vitepress.dev/) site (apunte teórico + guía de ejercicios), both exportable to PDF.

**Live site:** https://larrieragaston.github.io/programacion-III/

## Author

**Gastón A. Larriera**
gaston.larriera@inspt.utn.edu.ar

## For agents / contributors

**Read [`AGENTS.md`](AGENTS.md) first.** It has the full picture: repo architecture, dev workflow, the landing page's card-grid structure, content conventions, known bug patterns, and the git workflow this repo expects. This README stays intentionally short and human-facing; `AGENTS.md` is the deep reference, and [`PLAN-UNIDAD-4.md`](PLAN-UNIDAD-4.md) has the detailed content spec for the topics still being built.

## What's here

The landing page (`index.html`) is a filterable card grid — **Unidades** (built), **Próximamente** (planned, not built yet), **Extra** (optional/advanced, outside the core program), **Deprecado** (superseded). That grid is the source of truth for what currently exists; broadly:

- **Built**: Introducción, Cálculo λ, Clojure, Git & GitHub, JS Funcional, JS Contemporáneo, Asincronismo, TypeScript, React.
- **Deprecated**: FP — John Backus (superseded by the Cálculo λ / Clojure / JS Funcional sequence).
- **Planned**: Node + Express, MongoDB, Pruebas (Testing) — see [`PLAN-UNIDAD-4.md`](PLAN-UNIDAD-4.md) for the full spec of each.
- **Optional / extra**: Next.js, Tailwind CSS, NestJS, React Native con Expo.

## Prerequisites

- [Node.js](https://nodejs.org/) >= 18
- npm (comes with Node.js)
- On macOS, raise the open-file limit before installing a new deck's dependencies: `ulimit -n 10240`

For the PDF/OCR migration utilities (optional, only needed to convert old source PDFs into new decks):
- [Tesseract](https://github.com/tesseract-ocr/tesseract) with Spanish language data, [Poppler](https://poppler.freedesktop.org/) (`pdftoppm`, `pdftotext`)
- Python 3 with the packages in [`requirements-docs.txt`](requirements-docs.txt)

## Quick start

```bash
# Install root dependencies (first time only)
npm install

# Install a presentation's own dependencies (first time, per folder)
cd introduction && npm install && cd ..

# Start the index page + every Slidev deck
npm run dev
```

This runs `dev.sh`, which starts:
- **Index** at `http://localhost:3030`
- **Each Slidev deck** on its own fixed port (`3031`, `3032`, ... — see the `MODULES`/`PORTS` arrays in `dev.sh`)

Links on the index page detect `localhost` and rewrite themselves to the right dev port automatically (`index.js`).

`dev.sh` does **not** start the VitePress (`-docs/`) sites — those are run manually, one at a time, from their own folder:

```bash
cd git-github-docs && npm install   # first time only (runs postinstall: playwright install chromium)
npm run docs:dev                    # http://localhost:5177
```

See `AGENTS.md` for the full port table across every `-docs/` site.

### Regenerating PDFs

Exported PDFs (deck slides and `-docs/` apuntes/ejercicios) are gitignored and not committed — clone a fresh copy of this repo and every "Descargar" link on the landing will be broken until you generate them:

```bash
# Slides PDF for one deck
cd git-github && npm run export

# Apunte + ejercicios PDF for one -docs/ site (also copies them into the sibling deck's pdfs/originales/)
cd git-github-docs && npm run docs:pdf
```

`npm run dev` (root) does this automatically for every Slidev deck on startup unless you run `npm run dev:no-export` — but `-docs/` sites still need `docs:pdf` run manually.

## Adding new content

Two documents cover this in detail — read both before starting:

1. **[`.cursor/rules/pdf-to-slidev.mdc`](.cursor/rules/pdf-to-slidev.mdc)** — step-by-step recipe for creating a new Slidev deck (folder layout, `package.json` template, `slides.md` conventions, icons, updating `index.html`/`dev.sh`).
2. **[`PLAN-UNIDAD-4.md`](PLAN-UNIDAD-4.md)** — the content spec for every topic still pending in the core program (objectives, suggested content, references), plus the exact `<slug>-docs/` folder structure and port table.

Short version: each topic is a `<slug>/` (Slidev) + `<slug>-docs/` (VitePress) pair, built one at a time, tested locally, then wired into the landing page grid by activating its existing "Próximamente" placeholder card (see `AGENTS.md`).

## Project structure

```
programacion-III/
├── AGENTS.md                   # Full repo conventions — read this first
├── PLAN-UNIDAD-4.md            # Content spec for topics still being built
├── README.md
├── .github/workflows/deploy.yml  # Builds every deck + docs site, deploys to GitHub Pages
├── .cursor/rules/pdf-to-slidev.mdc  # Step-by-step: new deck from a source PDF
├── index.html / index.css / index.js  # Landing page: filterable card grid
├── dev.sh                      # Starts the index + every Slidev deck (hardcoded MODULES/PORTS arrays)
├── landing-redesign/           # Design handoff used to build the current landing (historical reference)
├── introduction/                    # Slidev only (no -docs/ site)
├── lambda-calculus/  + lambda-calculus-docs/   # Slidev + VitePress pair
├── clojure/           + clojure-docs/
├── git-github/        + git-github-docs/
├── js-funcional/      + js-funcional-docs/
├── js-contemporaneo/  + js-contemporaneo-docs/
├── asincronismo/      + asincronismo-docs/
├── typescript/        + typescript-docs/
├── react/              + react-docs/
└── fp-backus/                   # Slidev only — deprecated, kept for reference
```

Every `<slug>-docs/` follows the same internal layout (`docs/apunte.md`, `docs/ejercicios.md`, `docs/.vitepress/`, `scripts/print-pdfs.mjs`) — see `AGENTS.md` for the exact tree.

## Deploy

Automatic via GitHub Actions (`.github/workflows/deploy.yml`) on every push to `main`. The workflow:

1. Copies the landing page files (`index.html`, `index.css`, `index.js`, favicon, logo) into `_site/`.
2. Builds `lambda-calculus-docs` and `clojure-docs` (own hardcoded steps), then loops over every other folder whose `package.json` mentions `"vitepress"` and builds it the same way — `docs:build` + `scripts/print-pdfs.mjs` + copy `dist` into `_site/<folder>/`. **A new `<slug>-docs/` site does not need a workflow change** as long as it follows the established pattern.
3. Loops over every folder whose `package.json` mentions `"slidev"`, exports its PDF, builds it, and copies the result into `_site/<folder>/`. Same auto-discovery — **no workflow change needed** for a new deck either.
4. Uploads `_site` to GitHub Pages.

Published URLs:
- **Index:** https://larrieragaston.github.io/programacion-III/
- **Deck:** `https://larrieragaston.github.io/programacion-III/{slug}/`
- **Docs site:** `https://larrieragaston.github.io/programacion-III/{slug}-docs/`

**Never push to `main` without the instructor's explicit go-ahead** — every push publishes immediately to the live site students use. Local commits are fine; the push is a separate, deliberate step. See `AGENTS.md`.

### GitHub repository name

The repo must stay named **`programacion-III`** — every deck's `slidev build --base /programacion-III/<slug>/` and every VitePress `base` config hardcode that first path segment. Renaming the repo means updating every one of those.

## Tech stack

- [Slidev](https://sli.dev/) — Markdown to interactive slides (`theme: bricks`)
- [VitePress](https://vitepress.dev/) — apuntes teóricos y guías de ejercicios
- [Playwright](https://playwright.dev/) — PDF export (slides and VitePress pages alike)
- [GitHub Actions](https://docs.github.com/en/actions) + [GitHub Pages](https://pages.github.com/) — CI/CD and hosting
- Tesseract OCR + Poppler — one-off utilities for migrating old source PDFs into new decks

## License

This material is for educational use at INSPT - UTN.
