---
theme: bricks
title: Programación III - Tailwind CSS
download: true
info: |
  Tailwind CSS - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: tailwind, css, utility-first, oxide, vite, responsive, dark mode, INSPT, UTN
transition: slide-left
mdc: true
---

# Tailwind CSS

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/tailwindcss.svg" alt="Tailwind CSS" class="h-14 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# ¿Qué es Tailwind CSS?

- Un framework **utility-first**: en vez de escribir una clase propia por componente (`.card`, `.btn-primary`) y definir su CSS aparte, se componen clases chiquitas y ya hechas (`flex`, `p-4`, `text-center`) directo en el HTML/JSX.
- Cada clase hace **una sola cosa** y mapea casi directo a una propiedad CSS — `pt-4` es `padding-top`, `text-sm` es `font-size`. Se aprenden rápido porque son predecibles.
- No es un set de componentes visuales (como Bootstrap) — no trae un "botón" con estilo propio. Da las piezas; el diseño final lo arma quien lo usa.

<div class="flex gap-10 justify-center mt-6 items-center">
<img src="/logos/tailwindcss.svg" alt="Tailwind CSS" class="h-12 opacity-80" />
</div>

---
layout: default
---

# Historia breve

- **2017** — Adam Wathan lo libera como proyecto open source, después de usar la idea internamente en sus propios proyectos.
- **2019** — Just-In-Time (JIT) engine experimental: genera solo el CSS de las clases que realmente se usan, al vuelo.
- **2021** (v3) — JIT pasa a ser el motor por defecto, variantes arbitrarias (`[&:nth-child(3)]`), *dark mode* de primera clase.
- **2025** (v4) — reescritura completa del motor (**Oxide**, en Rust): builds incrementales hasta 100x más rápidos, y la configuración pasa de un archivo JS a directivas dentro del propio CSS.
- **Hoy** — v4 es la versión recomendada para proyectos nuevos; este apunte usa esa versión en todos los ejemplos.

---
layout: center
---

# Empezar un proyecto

---
layout: default
---

# Instalar con Vite

```bash
npm install tailwindcss @tailwindcss/vite
```

```ts
// vite.config.ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],
})
```

```css
/* src/index.css */
@import "tailwindcss";
```

<div class="mt-1 text-sm opacity-80">

Tres pasos y listo — sin PostCSS ni `autoprefixer` que configurar a mano, el plugin de Vite se encarga de todo el pipeline.

</div>

<div class="mt-1 text-xs opacity-60">

→ [tailwindcss.com/docs/installation/using-vite](https://tailwindcss.com/docs/installation/using-vite)

</div>

---
layout: default
---

# Sin archivo de configuración

```css
/* src/index.css */
@import "tailwindcss";

@theme {
  --color-brand: #7c3aed;
  --font-sans: "Inter", sans-serif;
  --breakpoint-3xl: 1920px;
}
```

<div class="mt-2 text-sm opacity-80">

Hasta la versión 3, personalizar colores, fuentes o breakpoints significaba editar un `tailwind.config.js` en JavaScript. Desde v4 se hace directo en CSS, con `@theme` — cada token se convierte en una variable CSS nativa (`var(--color-brand)`), disponible también fuera de las clases de Tailwind.

</div>

---
layout: center
---

# Utility-first, en la práctica

---
layout: default
---

# Clases vs. CSS a mano

<div class="grid grid-cols-2 gap-4 text-sm">
<div>

**CSS tradicional**

```css
.card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,.1);
}
```

```html
<div class="card">...</div>
```

</div>
<div>

**Tailwind**

```html
<div class="p-6 rounded-lg bg-white shadow">
  ...
</div>
```

</div>
</div>

<div class="mt-3 text-sm opacity-80">

Mismo resultado, pero sin saltar entre un archivo `.css` y el marcado — y sin la decisión extra de cómo nombrar `.card`. El costo: el HTML se llena de clases.

</div>

---
layout: default
---

# Spacing y layout

```html
<div class="flex items-center justify-between gap-4 p-4">
  <div class="grid grid-cols-3 gap-2 w-full">
    <div class="h-20 bg-slate-200"></div>
  </div>
</div>
```

<div class="mt-2 text-sm opacity-80">

`flex`/`grid` activan esos modelos de layout; `gap-4`, `p-4`, `m-2` usan una escala numérica consistente (no píxeles sueltos) donde cada paso es `0.25rem` — `p-4` = `1rem`, `p-8` = `2rem`. `w-full`, `h-20`, `items-center`, `justify-between` cubren el resto de Flexbox/Grid.

</div>

<div class="mt-1 text-xs opacity-60">

→ [tailwindcss.com/docs/padding](https://tailwindcss.com/docs/padding) · [tailwindcss.com/docs/flex](https://tailwindcss.com/docs/flex)

</div>

---
layout: default
---

# Colores y tipografía

```html
<p class="text-indigo-600 bg-indigo-50 font-semibold text-lg leading-tight">
  Texto con color y tipografía
</p>
```

<div class="mt-2 text-sm opacity-80">

Cada color viene en una escala de **11 tonos** (`50` el más claro, `950` el más oscuro) — `bg-indigo-50` es un fondo pastel, `text-indigo-600` un texto saturado. `font-*` controla el peso (`font-bold`), `text-*` el tamaño (`text-lg`), `leading-*` el interlineado.

</div>

<div class="mt-1 text-xs opacity-60">

→ [tailwindcss.com/docs/colors](https://tailwindcss.com/docs/colors)

</div>

---
layout: default
---

# Estados: hover, focus y más

```html
<button
  class="bg-indigo-600 hover:bg-indigo-700 focus:ring-2
         focus:ring-indigo-300 active:scale-95
         disabled:opacity-50 transition"
>
  Guardar
</button>
```

<div class="mt-3 text-sm opacity-80">

Cualquier clase puede llevar un prefijo de estado: `hover:`, `focus:`, `active:`, `disabled:`, `first:`, `last:` — se combinan libremente (`hover:focus:bg-...` no hace falta, pero `md:hover:bg-...` sí es válido). `transition` suaviza el cambio entre estados.

</div>

---
layout: default
---

# Responsive: mobile-first

```html
<div class="text-sm md:text-base lg:text-lg grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  ...
</div>
```

<div class="mt-3 text-sm opacity-80">

Sin prefijo, la clase aplica **siempre** (el caso base, pensado para mobile). Un prefijo como `md:` la aplica desde ese ancho de pantalla **hacia arriba** — no es "solo en md", es "en md y más grande". Breakpoints por defecto: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px).

</div>

---
layout: default
---

# Dark mode

```css
/* src/index.css — opcional, para controlarlo con una clase */
@custom-variant dark (&:where(.dark, .dark *));
```

```html
<div class="bg-white text-slate-900 dark:bg-slate-900 dark:text-white">
  Se adapta solo
</div>
```

<div class="mt-2 text-sm opacity-80">

Por defecto, `dark:` sigue la preferencia del sistema operativo (`prefers-color-scheme`). Para que un botón en la propia página controle el tema (en vez del SO), se redefine la variante `dark` para que mire una clase `.dark` en un ancestro — ahí alcanza con alternar esa clase por JavaScript.

</div>

---
layout: default
---

# Valores arbitrarios

```html
<div class="w-[32px] bg-[#1da1f2] grid grid-cols-[1fr_2fr] top-[117px]">
  ...
</div>
```

<div class="mt-3 text-sm opacity-80">

Para ese caso puntual que no está en la escala — un color de marca exacto, un ancho específico — los corchetes aceptan **cualquier valor CSS válido**, sin salir del archivo. Usarlo seguido es señal de que probablemente conviene agregar ese valor al `@theme` en vez de repetirlo suelto.

</div>

---
layout: center
---

# Evitar la repetición

---
layout: default
---

# Componentes, no `@apply`

```tsx
function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700">
      {children}
    </button>
  )
}
```

<div class="mt-2 text-sm opacity-80">

`@apply` existe (agrupa clases de Tailwind dentro de una clase CSS propia, `.btn { @apply px-4 py-2 ...; }`) pero reintroduce el problema que Tailwind evita: un nombre que mantener y un archivo CSS que volver a mirar. En un proyecto con componentes (React, Vue), la forma recomendada es extraer un **componente** que agrupe las clases — ahí sí se reutilizan, junto con el marcado y el comportamiento.

</div>

<div class="mt-1 text-xs opacity-60">

→ [tailwindcss.com/docs/styling-with-utility-classes#managing-duplication](https://tailwindcss.com/docs/styling-with-utility-classes)

</div>

---
layout: default
---

# Clases condicionales

```tsx
function Alert({ variant }: { variant: 'error' | 'success' }) {
  return (
    <div
      className={[
        'p-4 rounded border',
        variant === 'error'
          ? 'bg-red-50 border-red-300 text-red-700'
          : 'bg-green-50 border-green-300 text-green-700',
      ].join(' ')}
    >
      {variant === 'error' ? 'Algo salió mal' : 'Listo'}
    </div>
  )
}
```

<div class="mt-2 text-sm opacity-80">

Como las clases son strings, elegir un set u otro según una condición es JavaScript común — un ternario, un `.join(' ')`, o una librería chica como `clsx` cuando hay muchas combinaciones, sin que Tailwind tenga que saber nada de eso.

</div>

---
layout: center
---

# Funciones extra

---
layout: default
---

# Container queries

```html
<div class="@container">
  <div class="flex flex-col @sm:flex-row gap-4">
    ...
  </div>
</div>
```

<div class="mt-3 text-sm opacity-80">

`md:`/`lg:` responden al ancho de la **ventana**. `@container` marca un elemento como referencia, y `@sm:`/`@md:` dentro de él responden al ancho de **ese contenedor** — útil para un componente (una card en una sidebar angosta) que debe verse distinto según dónde se lo use, no según el tamaño de la pantalla entera.

</div>

<div class="mt-1 text-xs opacity-60">

→ [tailwindcss.com/docs/responsive-design#container-queries](https://tailwindcss.com/docs/responsive-design)

</div>

---
layout: default
---

# Plugins oficiales

```bash
npm install @tailwindcss/forms @tailwindcss/typography
```

```css
@import "tailwindcss";
@plugin "@tailwindcss/forms";
@plugin "@tailwindcss/typography";
```

<div class="mt-2 text-sm opacity-80">

**`forms`** resetea inputs/selects/checkboxes a un estilo consistente entre navegadores, para no pelear contra el estilo nativo de cada uno. **`typography`** agrega la clase `prose`, pensada para bloques de texto largo (un artículo, un render de Markdown) donde escribir `text-*`/`leading-*` a mano en cada etiqueta sería tedioso.

</div>

---
layout: default
---

# Herramientas del editor

- **Extensión oficial de VS Code** (*Tailwind CSS IntelliSense*): autocompletar de clases, preview del color al lado de cada una, y errores si se escribe una clase que no existe.
- **`prettier-plugin-tailwindcss`**: ordena automáticamente las clases de cada elemento en un orden consistente (layout → spacing → tipografía → color) al guardar — elimina la discusión de en qué orden escribirlas.

<div class="mt-3 text-xs opacity-60">

→ [marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)

</div>

---
layout: center
---

# Cierre

---
layout: default
---

# ¿Cuándo conviene Tailwind?

<div class="grid grid-cols-2 gap-6 mt-2">
<div class="p-4 rounded-lg border-2 border-green-300 bg-green-50">

**Conviene**

Proyectos con componentes (React, Vue) donde el estilo vive junto al marcado, equipos que quieren un sistema de diseño consistente sin inventar nombres de clases, o cuando iterar rápido visualmente importa más que tener un CSS "prolijo" por separado.

</div>
<div class="p-4 rounded-lg border-2 border-yellow-300 bg-yellow-50">

**Pensarlo dos veces**

HTML server-rendered sin componentes, donde las clases se repiten sin forma fácil de extraerlas; o un equipo que ya tiene un sistema de diseño propio maduro en CSS puro.

</div>
</div>

<div class="mt-3 text-sm italic opacity-80 text-center">

No reemplaza saber CSS — ayuda a escribir menos, no a no entenderlo.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
<div>

**Layout y spacing**

| Clase | Para qué |
|---|---|
| `flex` / `grid` | Modelo de layout |
| `p-4` / `m-2` / `gap-4` | Padding, margin, espacio entre hijos |
| `w-full` / `h-20` | Ancho/alto |
| `items-center` / `justify-between` | Alineación |
| `grid-cols-3` | Columnas de grid |

</div>
<div>

**Variantes**

| Prefijo | Para qué |
|---|---|
| `hover:` / `focus:` / `disabled:` | Estados |
| `sm:` / `md:` / `lg:` | Responsive (viewport) |
| `@sm:` (con `@container`) | Responsive (contenedor) |
| `dark:` | Dark mode |
| `[...]` | Valor arbitrario |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [tailwindcss.com/docs](https://tailwindcss.com/docs) — documentación oficial
- [tailwindcss.com/docs/installation/using-vite](https://tailwindcss.com/docs/installation/using-vite) — instalación con Vite
- [tailwindcss.com/docs/theme](https://tailwindcss.com/docs/theme) — `@theme`, tokens de diseño en CSS
- [tailwindcss.com/docs/colors](https://tailwindcss.com/docs/colors) — paleta completa de colores
- [tailwindcss.com/docs/responsive-design](https://tailwindcss.com/docs/responsive-design) — breakpoints y container queries
- [tailwindcss.com/docs/dark-mode](https://tailwindcss.com/docs/dark-mode) — las dos formas de armar dark mode
- [tailwindcss.com/docs/styling-with-utility-classes](https://tailwindcss.com/docs/styling-with-utility-classes) — filosofía utility-first, en profundidad
- [tailwindcss.com/plugins](https://tailwindcss.com/plugins) — `forms`, `typography` y el resto de los plugins oficiales
- [play.tailwindcss.com](https://play.tailwindcss.com) — playground oficial, sin instalar nada
- [marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss) — extensión de VS Code

</div>
