/**
 * Genera PDF desde el HTML ya construido por VitePress.
 * Cabecera institucional y numeración solo en el PDF (Playwright header/footer), no en el HTML.
 * Requiere: vitepress build docs (o npm run docs:pdf).
 */
import fs from 'node:fs'
import http from 'node:http'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import handler from 'serve-handler'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const dist = path.join(__dirname, '../docs/.vitepress/dist')
const outDir = path.join(__dirname, '../docs/public/pdfs')
const repoRoot = path.join(__dirname, '../..')
/** Mismas rutas que enlaza index.html en la raíz del repo (y copia en public para Slidev). */
const lambdaCalculusPdfDestDirs = [
  path.join(repoRoot, 'lambda-calculus/pdfs/originales'),
  path.join(repoRoot, 'lambda-calculus/public/pdfs/originales'),
]
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

function listDirSafe(dir) {
  try {
    return fs.readdirSync(dir)
  } catch {
    return []
  }
}

function hasChromiumHeadlessShell(cacheRoot) {
  if (!cacheRoot || !fs.existsSync(cacheRoot)) return false
  for (const name of listDirSafe(cacheRoot)) {
    if (!name.startsWith('chromium_headless_shell-')) continue
    const shellRoot = path.join(cacheRoot, name)
    for (const plat of listDirSafe(shellRoot)) {
      const exeDir = path.join(shellRoot, plat)
      let st
      try {
        st = fs.statSync(exeDir)
      } catch {
        continue
      }
      if (!st.isDirectory()) continue
      for (const f of listDirSafe(exeDir))
        if (f === 'chrome-headless-shell' || f === 'chrome-headless-shell.exe') return true
    }
  }
  return false
}

function userPlaywrightBrowsersCandidates() {
  const home = os.homedir()
  return [
    path.join(home, 'Library/Caches/ms-playwright'),
    path.join(home, '.cache', 'ms-playwright'),
    process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'ms-playwright') : null,
  ].filter(Boolean)
}

function findUserPlaywrightBrowsersPath() {
  for (const c of userPlaywrightBrowsersCandidates()) {
    if (hasChromiumHeadlessShell(c)) return c
  }
  return null
}

/** Caché del agente: a veces trae headless shell x64 y en Apple Silicon Playwright busca arm64. */
function shouldIgnorePlaywrightBrowsersPath(p) {
  return Boolean(p && p.includes('cursor-sandbox-cache'))
}

/**
 * Ajusta PLAYWRIGHT_BROWSERS_PATH si el actual es incompleto o incompatible (p. ej. sandbox del IDE).
 */
function resolvePlaywrightBrowsersPath() {
  const current = process.env.PLAYWRIGHT_BROWSERS_PATH
  const userCache = findUserPlaywrightBrowsersPath()

  if (shouldIgnorePlaywrightBrowsersPath(current) && userCache) {
    process.env.PLAYWRIGHT_BROWSERS_PATH = userCache
    console.error('Playwright: caché del IDE omitido; usando', userCache)
    return
  }

  if (current && hasChromiumHeadlessShell(current)) return

  if (userCache) {
    process.env.PLAYWRIGHT_BROWSERS_PATH = userCache
    console.error('Playwright: usando navegadores en', userCache)
  }
}

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

function copyPdfToLambdaCalculus(pdfPath, pdfName) {
  for (const dir of lambdaCalculusPdfDestDirs) {
    fs.mkdirSync(dir, { recursive: true })
    fs.copyFileSync(pdfPath, path.join(dir, pdfName))
  }
}

if (!fs.existsSync(path.join(dist, 'index.html'))) {
  console.error('No build output in', dist, '— run: vitepress build docs')
  process.exit(1)
}

fs.mkdirSync(outDir, { recursive: true })

resolvePlaywrightBrowsersPath()
const { chromium } = await import('playwright')

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
  await page.goto(url, { waitUntil: 'networkidle', timeout: 90_000 })
  await page.waitForSelector('.vp-doc', { state: 'visible', timeout: 30_000 })
  await page.emulateMedia({ media: 'print' })
  const outPath = path.join(outDir, pdfName)
  await page.pdf({
    path: outPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: pdfHeaderTemplate(docTitle),
    footerTemplate: pdfFooterTemplate,
    margin: { top: '108px', bottom: '52px', left: '14mm', right: '14mm' },
    tagged: true,
  })
  copyPdfToLambdaCalculus(outPath, pdfName)
}

await browser.close()
server.close()
console.error('PDFs en docs/public/pdfs/ y copiados a lambda-calculus/.../pdfs/originales/')
