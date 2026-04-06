/**
 * Genera PDF desde el HTML ya construido por VitePress.
 * Cabecera institucional y numeración solo en el PDF (Playwright header/footer), no en el HTML.
 * Requiere: vitepress build docs (o npm run docs:pdf).
 */
import fs from 'node:fs'
import http from 'node:http'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { chromium } from 'playwright'
import handler from 'serve-handler'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const dist = path.join(__dirname, '../docs/.vitepress/dist')
const outDir = path.join(__dirname, '../docs/public/pdfs')
const base =
  process.env.VP_BASE !== undefined && process.env.VP_BASE !== ''
    ? process.env.VP_BASE
    : process.env.CI === 'true'
      ? '/programacion-III-material/lambda-calculus-docs/'
      : '/'

/** [html, pdfFilename, título en cabecera del PDF] */
const pages = [
  ['apunte.html', 'calculo-lambda-apunte.pdf', 'Apunte teórico — Cálculo λ'],
  ['ejercicios.html', 'calculo-lambda-ejercicios.pdf', 'Guía de ejercicios — Cálculo λ'],
  [
    'ejercicios-adicionales.html',
    'calculo-lambda-ejercicios-adicionales.pdf',
    'Ejercicios adicionales — Cálculo λ',
  ],
]

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function pdfHeaderTemplate(docTitle) {
  const t = escapeHtml(docTitle)
  return `<div style="width:100%;box-sizing:border-box;padding:6px 48px 8px;font-size:8px;color:#0f172a;border-bottom:1px solid #cbd5e1;font-family:system-ui,sans-serif;">
  <div style="font-weight:700;letter-spacing:0.04em;text-transform:uppercase;">Universidad Tecnológica Nacional · INSPT</div>
  <div style="margin-top:2px;">Programación III · Ciclo lectivo 2026</div>
  <div style="margin-top:5px;font-size:10px;font-weight:700;">${t}</div>
  <div style="margin-top:3px;font-size:8px;">Prof. Gastón A. Larriera</div>
</div>`
}

const pdfFooterTemplate = `<div style="width:100%;box-sizing:border-box;padding:4px 48px 0;font-size:9px;color:#64748b;text-align:center;font-family:system-ui,sans-serif;">
  <span class="pageNumber"></span> / <span class="totalPages"></span>
</div>`

if (!fs.existsSync(path.join(dist, 'index.html'))) {
  console.error('No build output in', dist, '— run: vitepress build docs')
  process.exit(1)
}

fs.mkdirSync(outDir, { recursive: true })

const server = http.createServer((req, res) =>
  handler(req, res, { public: dist }),
)

await new Promise((resolve, reject) => {
  server.listen(4173, '127.0.0.1', (err) => (err ? reject(err) : resolve()))
})

const browser = await chromium.launch()
const page = await browser.newPage()

for (const [html, pdfName, docTitle] of pages) {
  const url = `http://127.0.0.1:4173${base}${html}`
  console.error('PDF ←', url)
  await page.goto(url, { waitUntil: 'networkidle' })
  await page.emulateMedia({ media: 'print' })
  await page.pdf({
    path: path.join(outDir, pdfName),
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: pdfHeaderTemplate(docTitle),
    footerTemplate: pdfFooterTemplate,
    margin: { top: '108px', bottom: '52px', left: '14mm', right: '14mm' },
  })
}

await browser.close()
server.close()
console.error('PDFs written to docs/public/pdfs/')
