# Programacion III - Material

Course slides for Programacion III at [INSPT - UTN](https://www.inspt.utn.edu.ar/).  
Built with [Slidev](https://sli.dev/) — a markdown-based presentation tool for developers.

## Author

**Gaston A. Larriera**  
gaston.larriera@inspt.utn.edu.ar

## About

This repository contains all the class presentations for Programacion III (Functional Programming / Full Stack JS).  
Each presentation is a standalone [Slidev](https://sli.dev/) project inside its own folder, managed as a monorepo.

Presentations are automatically deployed to GitHub Pages on every push to `main`.

**Live site:** https://larrieragaston.github.io/programacion-III/

## Presentations

| # | Folder | Topic |
|---|--------|-------|
| 1 | `introduction/` | Course overview, grading policy, contact info |

## Prerequisites

- [Node.js](https://nodejs.org/) >= 18
- npm (comes with Node.js)

For the OCR utility (optional):
- [Tesseract](https://github.com/tesseract-ocr/tesseract) with Spanish language data
- Python 3 with `pytesseract` and `pdf2image`

## Quick start

```bash
# Install root dependencies (first time only)
npm install

# Install presentation dependencies (first time, for each folder)
cd introduction && npm install && cd ..

# Start everything: index page + all presentations
npm run dev
```

This launches:
- **Index** at `http://localhost:3030` with links to all presentations
- **Each presentation** on sequential ports starting from `3031`

Links on the index page automatically detect localhost and point to the correct dev port.

### Cálculo λ — material escrito (VitePress)

The folder [`lambda-calculus-docs/`](lambda-calculus-docs/) is a [VitePress](https://vitepress.dev/) site: **Apunte**, **Guía de ejercicios** (`ejercicios.md`), and **Ejercicios adicionales**. Local dev uses VitePress `base` `/` so URLs like `http://localhost:5173/pdfs/...` work; GitHub Actions sets `CI=true` so production builds use `/programacion-III/lambda-calculus-docs/` (override with `VP_BASE=...` if the site root changes). The Pages workflow builds this site, runs PDF export, and copies `dist` to `_site/lambda-calculus-docs/`; the same export refreshes the PDF linked from the main index under `lambda-calculus/pdfs/originales/`.

```bash
cd lambda-calculus-docs && npm install   # runs postinstall: playwright install chromium
npm run docs:install-browsers            # if docs:pdf fails with “Executable doesn't exist”
npm run docs:dev                         # http://localhost:5173
npm run docs:build                       # static site only → docs/.vitepress/dist
npm run docs:pdf                         # build + export PDFs (Playwright print of the built HTML)
```

Serve the repo root (e.g. `npx serve . -l 3030`) and open the cards for Unidad 1; they point to port `5173` with `data-dev-path` (see root `index.html`). Run `npm run docs:pdf` after clone if you need working PDF links under `docs/public/pdfs/` (those files are gitignored).

**Migrating from PDF again:** use [`pdf_to_md.py`](pdf_to_md.py) against `lambda-calculus-docs/source-pdfs/`, then run [`lambda-calculus-docs/scripts/restructure_docs.py`](lambda-calculus-docs/scripts/restructure_docs.py) to strip headers/CC text, promote section titles, and split the **guía de ejercicios** into `ejercicios.md`. Edit the Markdown by hand afterward.

**PDF export** matches the site: `docs:pdf` builds the site and prints `apunte.html`, `ejercicios.html`, and `ejercicios-adicionales.html` to `docs/public/pdfs/*.pdf` via Playwright (not `md-to-pdf`).

## Adding a new presentation

1. Create the folder:

```bash
mkdir my-new-topic
cd my-new-topic
```

2. Create `package.json` (replace `my-new-topic` with your folder name):

```json
{
  "name": "programacion-III-my-new-topic",
  "private": true,
  "scripts": {
    "dev": "slidev",
    "build": "slidev build --base /programacion-III/my-new-topic/",
    "export": "slidev export"
  },
  "dependencies": {
    "@slidev/cli": "^52.14.1",
    "@slidev/theme-default": "^0.25.0"
  }
}
```

3. Create `slides.md` with the slide content (see `introduction/slides.md` as a reference).

4. Install dependencies:

```bash
npm install
```

5. Add a link in the root `index.html` following the existing pattern:

```html
<li>
  <a href="./my-new-topic/" data-dev-port="3032">
    <div class="card-number">2</div>
    <div class="card-content">
      <strong>My new topic</strong>
      <span>Brief description of the content</span>
    </div>
  </a>
</li>
```

The `data-dev-port` should be the next sequential port (`3032`, `3033`, ...).  
The port is assigned automatically by `dev.sh` in alphabetical folder order.

6. Push to `main` — deploy is automatic.

## Project structure

```
programacion-III/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions: builds all presentations and deploys to Pages
├── .gitignore                  # Ignores node_modules, dist, .slidev
├── index.html                  # Landing page with links to all presentations
├── package.json                # Root package with dev script
├── package-lock.json
├── dev.sh                      # Auto-discovers and starts all Slidev servers + index
├── ocr_extract.py              # Utility: extracts text from PDF slides via OCR (Tesseract)
├── README.md
└── introduction/               # Each presentation is a self-contained Slidev project
    ├── package.json            #   Build config with --base path for GitHub Pages
    ├── package-lock.json
    ├── slides.md               #   Slide content in Markdown
    └── public/                 #   Static assets (images, etc.)
```

### File descriptions

| File | Purpose |
|------|---------|
| `deploy.yml` | CI/CD workflow that builds every Slidev project and deploys the result to GitHub Pages |
| `index.html` | Landing page shown at the root URL; lists all presentations with links |
| `dev.sh` | Shell script that finds all Slidev folders and starts them concurrently with the index server |
| `ocr_extract.py` | Python script to extract text from image-based PDFs using Tesseract OCR; useful for migrating old slides |
| `slides.md` | Markdown file with all the slides for a presentation; uses Slidev syntax |

## Deploy

Automatic via GitHub Actions on every push to `main`.

The workflow:
1. Copies the site index (`index.html`, `index.css`, `index.js`, assets) into `_site/`
2. Builds **lambda-calculus-docs** (VitePress), runs **Playwright** (`scripts/print-pdfs.mjs`) to regenerate the three PDF en `lambda-calculus/public/pdfs/originales/`, and copies the VitePress `dist` to `_site/lambda-calculus-docs/`
3. Finds every subfolder with Slidev in `package.json`, runs `npm run export` (PDF diapositivas) and `npm run build`, copies each `dist` into `_site/{folder}/` (el build de `lambda-calculus` incluye los PDF del paso 2 vía `public/`)
4. Uploads `_site` to GitHub Pages

Published URLs:
- **Index:** https://larrieragaston.github.io/programacion-III/
- **Presentations:** `https://larrieragaston.github.io/programacion-III/{folder-name}/`

### GitHub repository name

The repository on GitHub should be named **`programacion-III`** (misma forma en la URL de Pages: `/programacion-III/`). El `slidev build --base` debe coincidir con ese primer segmento. Si renombrás o forkeás el repo, actualizá cada `--base` en los `*/package.json` y volvé a desplegar.

Tras renombrar en GitHub, los clones viejos suelen seguir funcionando por redirección; podés actualizar el remoto con `git remote set-url origin https://github.com/<usuario>/programacion-III.git`.

## Useful commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start index + all presentations (from root) |
| `cd {folder} && npm run dev` | Start a single presentation |
| `cd {folder} && npm run build` | Generate static SPA in `dist/` |
| `cd {folder} && npm run export` | Export to PDF |

## Tech stack

- [Slidev](https://sli.dev/) — Markdown to interactive slides
- [GitHub Actions](https://docs.github.com/en/actions) — CI/CD
- [GitHub Pages](https://pages.github.com/) — Hosting
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) — PDF text extraction (utility)

## License

This material is for educational use at INSPT - UTN.
