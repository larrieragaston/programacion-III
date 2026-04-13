import fs from 'node:fs'
import { defineConfig } from 'vitepress'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import type { Plugin } from 'vite'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

const faviconSvgPath = path.resolve(__dirname, '../public/favicon.svg')

/** Chrome pide /favicon.ico aunque exista link rel=icon; redirigimos al SVG en dev. */
function faviconIcoRedirectToSvg(): Plugin {
  return {
    name: 'lambda-docs-favicon-ico',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const pathname = req.url?.split('?')[0] ?? ''
        if (pathname === '/favicon.ico') {
          res.statusCode = 307
          res.setHeader('Location', '/favicon.svg')
          res.end()
          return
        }
        next()
      })
    },
  }
}

/**
 * GitHub Actions sets CI=true → use path for GitHub Pages.
 * Local dev (no CI): base "/" so /pdfs/... and /apunte work at localhost:5173.
 * Override anytime: VP_BASE=/foo/ vitepress dev docs
 */
const base =
  process.env.VP_BASE !== undefined && process.env.VP_BASE !== ''
    ? process.env.VP_BASE
    : process.env.CI === 'true'
      ? '/programacion-III-material/lambda-calculus-docs/'
      : '/'

/** Índice del repo (README). Override: P3_MATERIAL_HOME=https://... */
const p3MaterialHome =
  process.env.P3_MATERIAL_HOME ||
  (process.env.CI === 'true'
    ? 'https://larrieragaston.github.io/programacion-III/'
    : 'http://localhost:3030/')

const faviconHref = `${base}favicon.svg`
const faviconSvgRaw = fs.readFileSync(faviconSvgPath, 'utf8')
const faviconDataUri =
  'data:image/svg+xml,' + encodeURIComponent(faviconSvgRaw.trim())

/** Navbar: índice P3 con icono de casa (el texto del nav se renderiza con v-html). */
const p3NavItemText = `<span class="nav-p3-home"><svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg><span>Programación III</span></span>`

export default defineConfig({
  lang: 'es-AR',
  title: 'Cálculo λ',
  description:
    'Material teórico y prácticas: λ-cálculo, guías de ejercicios e intérpretes. Programación III — INSPT.',
  base,
  head: [
    ['link', { rel: 'icon', href: faviconDataUri, type: 'image/svg+xml' }],
    ['link', { rel: 'icon', href: faviconHref, type: 'image/svg+xml', sizes: 'any' }],
  ],
  vite: {
    publicDir: path.resolve(__dirname, '../public'),
    plugins: [faviconIcoRedirectToSvg()],
  },
  markdown: {
    math: true,
  },
  themeConfig: {
    nav: [
      { text: 'Inicio', link: '/' },
      { text: 'Apunte teórico', link: '/apunte' },
      { text: 'Guía de ejercicios', link: '/ejercicios' },
      { text: 'Ejercicios adicionales', link: '/ejercicios-adicionales' },
      {
        text: p3NavItemText,
        link: p3MaterialHome,
        target: '_self',
        rel: 'noopener noreferrer',
        noIcon: true,
      },
    ],
    sidebar: [
      {
        text: 'Unidad 1',
        items: [
          { text: 'Inicio', link: '/' },
          { text: 'Apunte teórico', link: '/apunte' },
          { text: 'Guía de ejercicios', link: '/ejercicios' },
          { text: 'Ejercicios adicionales', link: '/ejercicios-adicionales' },
        ],
      },
    ],
    socialLinks: [],
    footer: {
      message: 'Programación III — INSPT',
    },
  },
})
