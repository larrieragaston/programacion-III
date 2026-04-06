import { defineConfig } from 'vitepress'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

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

export default defineConfig({
  lang: 'es-AR',
  title: 'Cálculo λ',
  description:
    'Material teórico y prácticas: λ-cálculo, guías de ejercicios e intérpretes. Programación III — INSPT.',
  base,
  vite: {
    publicDir: path.resolve(__dirname, '../public'),
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
