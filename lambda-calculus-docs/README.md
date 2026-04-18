# Cálculo λ — sitio de documentación (VitePress)

Sitio estático con **apunte teórico**, **guía de ejercicios** y **ejercicios adicionales** para Programación III (INSPT · UTN). Se publica junto al resto del material del curso en GitHub Pages (mismo repositorio que las presentaciones Slidev).

## Qué incluye este proyecto

| Contenido | Archivo |
|-----------|---------|
| Apunte teórico | `docs/apunte.md` |
| Guía de ejercicios (enunciados + enlaces a intérpretes) | `docs/ejercicios.md` |
| Ejercicios adicionales | `docs/ejercicios-adicionales.md` |
| Página de inicio (hero + enlaces) | `docs/index.md` |
| Tema y estilos | `docs/.vitepress/theme/` (`index.ts`, `custom.css`) |
| Configuración VitePress | `docs/.vitepress/config.ts` |
| PDFs generados (no versionados) | `docs/public/pdfs/*.pdf` y copia en `../lambda-calculus/public/pdfs/originales/` |

Esos PDF están en `.gitignore`; se regeneran con `npm run docs:pdf` (Playwright). En CI se generan antes del build de Slidev.

## Requisitos

- Node.js ≥ 18
- Tras `npm install`, el `postinstall` ejecuta `playwright install chromium`. Si falla el PDF, probar: `npm run docs:install-browsers`.

## Comandos

```bash
npm install                    # primera vez; instala Chromium para Playwright
npm run docs:dev               # desarrollo: http://localhost:5173
npm run docs:build             # solo build → docs/.vitepress/dist
npm run docs:pdf               # build + exportar PDFs (Playwright)
npm run docs:preview           # previsualizar el build estático
```

## Base URL (`/` vs ruta en GitHub Pages)

En `docs/.vitepress/config.ts`, `base` se resuelve así:

- **Local (sin `CI`):** `base: '/'` — rutas como `/apunte/`, `/pdfs/...` funcionan en `localhost:5173`.
- **CI (`CI=true`):** `base: '/programacion-III/lambda-calculus-docs/'` para GitHub Pages del repo `programacion-III` (`https://usuario.github.io/programacion-III/`).
- **Override manual:** `VP_BASE=/foo/ npm run docs:dev` (o el mismo prefijo en build).

`vite.publicDir` apunta a `docs/public` (PDFs y estáticos).

## Integración con la landing del repo raíz

En el `index.html` de la raíz del monorepo, la **Unidad 1 — Cálculo Lambda** tiene dos entradas:

1. **Presentación** → carpeta Slidev `lambda-calculus/` (puerto de dev distinto).
2. **Material teórico** → este sitio: `./lambda-calculus-docs/` con `data-dev-port="5173"` y `data-dev-path="/"` para que en localhost abra la raíz del VitePress.

Convención: los `<a>` con `data-dev-port` y opcionalmente `data-dev-path` los ajusta el script inline del `index.html` cuando el host es `localhost` / `127.0.0.1`.

## Proceso: de PDFs originales a Markdown

1. Colocar los PDF fuente en una carpeta de trabajo (p. ej. `source-pdfs/` o la ruta que uses).
2. Desde la **raíz del repo** (donde está `pdf_to_md.py`), extraer texto a Markdown según el script (dependencias Python: ver comentarios en `pdf_to_md.py` y `requirements-docs.txt` si existe).
3. Post-procesar con **`scripts/restructure_docs.py`**: limpia cabeceras repetidas, CC, títulos, y puede separar la guía de ejercicios en `ejercicios.md`.
4. **Revisión manual:** el OCR/extracción siempre exige corrección (fórmulas, código, listas).

Rutas útiles:

- `../../pdf_to_md.py` (raíz del monorepo)
- `scripts/restructure_docs.py` (esta carpeta)

## Proceso: HTML “limpio” vs PDF con membrete

- **Navegación web:** no se incrusta el bloque institucional grande en el Markdown (se quitó el `div.doc-print-header` de las páginas). El título del documento es el encabezado `#` normal.
- **PDF:** la cabecera (UTN · INSPT · materia · título del documento · docente) y el pie con **número de página** se generan en **`scripts/print-pdfs.mjs`** con Playwright (`displayHeaderFooter`, `headerTemplate`, `footerTemplate`). Así el PDF no arrastra la UI de VitePress (“Menu”, “On this page”, sidebar, etc.) si además el CSS de impresión oculta el cromo.

Para ocultar nav, sidebar, aside y pies de página al imprimir, ver **`docs/.vitepress/theme/custom.css`** (`@media print`).

Páginas largas usan en frontmatter `aside: false` para no mostrar el índice lateral “En esta página” en pantalla.

## Añadir o renombrar un PDF exportado

En `scripts/print-pdfs.mjs`, el array `pages` lista cada ruta de salida del build (`*.html`), el nombre del archivo PDF y el **título que aparece en la cabecera del PDF**. Tras cambiar rutas o páginas nuevas, hay que tener el `.md` correspondiente en `docs/` y que VitePress genere el `.html` en el build.

## Convenciones de navegación (sitio)

- Título del sitio y marca superior: **Cálculo λ** (`title` en `config.ts`).
- Enlace “Apunte” renombrado a **Apunte teórico** en nav y sidebar.
- No se enlazan los PDF desde el menú lateral (los PDF son artefacto de descarga o uso offline; se generan en `public/pdfs/`).

## Cómo replicar este esquema para otro tema (otra unidad)

1. Copiar la carpeta `lambda-calculus-docs/` con otro nombre (p. ej. `otro-tema-docs/`) o crear un esqueleto equivalente: `docs/`, `docs/.vitepress/config.ts`, `theme`, `public/`.
2. Ajustar `title`, `description`, `sidebar`, `nav` y los `.md`.
3. Ajustar `base` en CI si la carpeta de despliegue en Pages cambia (misma lógica `CI` / `VP_BASE`).
4. Duplicar y adaptar `scripts/print-pdfs.mjs` (lista `pages` y títulos de cabecera).
5. Añadir una tarjeta en el `index.html` raíz con el puerto de dev del VitePress de ese paquete y el `href` correcto.
6. Documentar en el `README.md` del repo raíz el nuevo subproyecto (opcional pero recomendable).

## Documentación relacionada

- Repo raíz: [README.md](../README.md) — visión general del monorepo, Slidev, y sección resumida de este sitio.
- Presentaciones desde PDF: regla de Cursor `.cursor/rules/pdf-to-slidev.mdc` (flujo Slidev, no VitePress).

## Licencia y uso

Material educativo para INSPT — UTN.
