---
theme: bricks
title: Programación III - Next.js
download: true
info: |
  Next.js - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: nextjs, react, ssr, ssg, isr, app router, server components, server actions, vercel, INSPT, UTN
transition: slide-left
mdc: true
---

# Next.js

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/nextjs.svg" alt="Next.js" class="h-14 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# ¿Qué es Next.js?

- Un **framework** construido sobre React — no lo reemplaza, le agrega lo que React por sí solo no resuelve: ruteo, renderizado en el servidor, optimización de imágenes y fuentes, empaquetado.
- Mismo modelo mental de componentes — props, estado, hooks — si ya conocés React, no hay un lenguaje nuevo que aprender, sí una forma distinta de organizar el proyecto.
- Desarrollado y mantenido por **Vercel**, la empresa que también lo despliega como servicio — los dos crecieron juntos.

<div class="flex gap-10 justify-center mt-6 items-center">
<img src="/logos/react.svg" alt="React" class="h-12 opacity-80" />
<div class="text-2xl opacity-40">+</div>
<img src="/logos/vercel.svg" alt="Vercel" class="h-10 opacity-80" />
</div>

---
layout: default
---

# Historia breve

- **2016** — Vercel (en ese momento, "ZEIT") libera Next.js: ruteo por archivos y renderizado en el servidor, sobre React, sin configurar nada a mano.
- **2020** (v9.3) — se suma generación estática (SSG) como primera clase, no solo SSR.
- **2022** (v13) — llega el **App Router**: Server Components por defecto, carpeta `app/` en paralelo a la vieja `pages/`.
- **2023** (v13.4) — el App Router se vuelve estable y recomendado para proyectos nuevos.
- **Hoy** (v16) — Server Actions estables, cacheo más fino, es el framework de React más usado para proyectos nuevos con necesidad de SEO o renderizado en servidor.

<div class="mt-3 text-sm italic opacity-80 text-center">

Este apunte usa el **App Router** (carpeta `app/`) en todos los ejemplos — es la forma recomendada desde 2023, la vieja carpeta `pages/` sigue andando pero no se cubre acá.

</div>

---
layout: center
---

# Empezar un proyecto

---
layout: default
---

# `create-next-app`

```bash
npx create-next-app@latest mi-tienda
```

<div class="text-sm opacity-80 mb-1">

Pregunta, interactivamente: TypeScript (sí, por defecto), ESLint, Tailwind CSS, carpeta `src/`, App Router (sí, por defecto), alias de imports. Se puede saltear todo con flags:

</div>

```bash
npx create-next-app@latest mi-tienda --typescript --tailwind --eslint --app
```

<div class="mt-2 text-sm opacity-80">

Deja un proyecto corriendo (`npm run dev`) con una página de bienvenida — listo para borrar y empezar.

</div>

<div class="mt-1 text-xs opacity-60">

→ [nextjs.org/docs/app/getting-started/installation](https://nextjs.org/docs/app/getting-started/installation)

</div>

---
layout: default
---

# Estructura del proyecto

```
mi-tienda/
├── app/
│   ├── layout.tsx     # layout raíz — obligatorio
│   ├── page.tsx       # la ruta "/"
│   └── globals.css
├── public/             # archivos estáticos, sin procesar
├── next.config.ts
└── package.json
```

<div class="mt-2 text-sm opacity-80">

Todo lo que importa para rutear vive adentro de `app/` — cada carpeta es, potencialmente, un segmento de URL. `public/` es exactamente lo mismo que ya conocés de cualquier proyecto web: archivos servidos tal cual, por su nombre.

</div>

---
layout: center
---

# Ruteo por archivos

---
layout: default
---

# Páginas: carpetas son rutas

```ts
app/page.tsx              →  /
app/about/page.tsx        →  /about
app/products/page.tsx     →  /products
```

```tsx
// app/products/page.tsx
export default function ProductsPage() {
  return <h1>Catálogo</h1>
}
```

<div class="mt-2 text-sm opacity-80">

Solo un archivo `page.tsx` convierte una carpeta en una ruta navegable — una carpeta sin `page.tsx` adentro no es una URL, puede existir solo para agrupar o para guardar componentes auxiliares.

</div>

---
layout: default
---

# Layouts compartidos

```tsx
// app/layout.tsx — obligatorio, envuelve TODA la app
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
```

<div class="mt-2 text-sm opacity-80">

Un `layout.tsx` envuelve su carpeta y todas las sub-rutas — se puede anidar (un layout en `app/products/` agrega un menú lateral solo a esa sección) y **no vuelve a renderizarse** al navegar entre páginas que comparten el mismo layout, a diferencia de recargar la página entera.

</div>

---
layout: default
---

# Rutas dinámicas

```
app/products/[id]/page.tsx   →  /products/1, /products/2, ...
```

```tsx
// app/products/[id]/page.tsx
export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  return <h1>Producto {id}</h1>
}
```

<div class="mt-1 text-xs opacity-80">

Los corchetes (`[id]`) marcan un segmento dinámico — `params` llega como una `Promise` (hay que esperarla con `await`), algo propio del App Router que no existía en la forma vieja de rutear.

</div>

---
layout: default
---

# `loading`, `error` y `not-found`

```
app/products/[id]/
├── page.tsx
├── loading.tsx    # se muestra mientras carga la página
├── error.tsx      # atrapa un error de esta ruta
└── not-found.tsx  # se muestra si se llama a notFound()
```

```tsx
import { notFound } from 'next/navigation'

const product = await getProduct(id)
if (!product) notFound()
```

<div class="mt-2 text-sm opacity-80">

Convenciones de archivo, no componentes que haya que importar a mano — Next.js los detecta por nombre y los usa automáticamente para esa carpeta y sus sub-rutas.

</div>

---
layout: default
---

# Navegación con `<Link>`

```tsx
import Link from 'next/link'

export default function ProductsPage() {
  return (
    <Link href="/products/1">Ver producto</Link>
  )
}
```

<div class="mt-3 text-sm opacity-80">

Un `<a>` común recarga toda la página; `<Link>` navega sin recargar — descarga el código de la ruta de destino por adelantado (*prefetch*), mientras el link está visible en pantalla, para que el clic se sienta instantáneo.

</div>

---
layout: center
---

# Server y Client Components

---
layout: default
---

# Server Component, por defecto

```tsx
// Server Component — se ejecuta en el servidor, nunca llega al navegador
async function ProductsPage() {
  const products = await getProducts()   // fetch directo, sin useEffect
  return <ul>{products.map((p) => <li key={p.id}>{p.name}</li>)}</ul>
}
```

<div class="mt-3 text-sm opacity-80">

Sin marcar nada, **todo componente adentro de `app/` corre en el servidor** — su código JavaScript ni siquiera se manda al navegador. Puede ser `async` y usar `await` directamente, sin `useEffect` ni estado de carga manual.

</div>

---
layout: default
---

# `'use client'`: cuándo hace falta

```tsx
'use client'

import { useState } from 'react'

export default function AddToCartButton() {
  const [added, setAdded] = useState(false)
  return <button onClick={() => setAdded(true)}>Agregar</button>
}
```

<div class="mt-2 text-sm opacity-80">

Hace falta en cualquier componente que use **hooks de estado** (`useState`, `useEffect`) o **eventos del navegador** (`onClick`, `onChange`) — ahí sí, su código se manda al cliente para poder reaccionar. La directiva va al principio del archivo, antes de cualquier import.

</div>

---
layout: default
---

# Componer Server y Client

```tsx
// Server Component (sin 'use client')
export default async function ProductPage({ params }) {
  const { id } = await params
  const product = await getProduct(id)   // esto NO podría ir en un Client Component
  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton />  {/* acá sí, un Client Component chico */}
    </div>
  )
}
```

<div class="mt-2 text-sm opacity-80">

La práctica recomendada: la página entera es Server Component (rápida, sin JS de más), y solo el pedacito interactivo (un botón, un formulario) es `'use client'` — no al revés. Marcar toda una página como cliente manda mucho más JavaScript del necesario.

</div>

---
layout: center
---

# Obtener datos

---
layout: default
---

# Fetch en un Server Component

```tsx
async function getProducts() {
  const res = await fetch('https://api.ejemplo.com/products')
  return res.json()
}

export default async function ProductsPage() {
  const products = await getProducts()
  return <ul>{products.map((p) => <li key={p.id}>{p.name}</li>)}</ul>
}
```

<div class="mt-2 text-sm opacity-80">

El `fetch` corre en el servidor, antes de mandar el HTML — la persona que abre la página recibe el contenido ya armado, no una pantalla vacía que se llena después con JavaScript.

</div>

---
layout: default
---

# SSG, SSR e ISR

<div class="overflow-x-auto mt-2 text-sm">

| | Cuándo se genera | `fetch` |
|---|---|---|
| **SSG** (estático) | Una vez, al hacer build | `cache: 'force-cache'` (default) |
| **SSR** (en cada visita) | En cada request | `cache: 'no-store'` |
| **ISR** (estático + se refresca) | Al build, y de nuevo cada *N* segundos | `next: { revalidate: 60 }` |

</div>

```ts
fetch(url, { next: { revalidate: 60 } })   // ISR: se refresca cada 60s
```

<div class="mt-2 text-sm opacity-80">

No es una decisión global del proyecto — se elige **por cada fetch**, pasándole una opción de cacheo. Una misma página puede combinar datos estáticos con datos que se revalidan seguido.

</div>

<div class="mt-1 text-xs opacity-60">

→ [nextjs.org/docs/app/getting-started/fetching-data](https://nextjs.org/docs/app/getting-started/fetching-data)

</div>

---
layout: default
---

# `generateStaticParams`

```tsx
// app/products/[id]/page.tsx
export async function generateStaticParams() {
  const products = await getProducts()
  return products.map((p) => ({ id: p.id }))
}
```

<div class="mt-3 text-sm opacity-80">

Para que una ruta dinámica (`[id]`) sea estática (SSG), Next.js necesita saber de antemano **qué** valores de `id` existen — esta función le devuelve la lista completa, y arma una página estática por cada uno, en el build.

</div>

---
layout: center
---

# Mutaciones

---
layout: default
---

# Route Handlers

```ts
// app/api/products/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const products = await getProducts()
  return NextResponse.json(products)
}
```

<div class="mt-3 text-sm opacity-80">

Un archivo `route.ts` adentro de `app/api/` expone un endpoint HTTP real — `GET`/`POST`/`PUT`/`DELETE` son funciones exportadas con ese nombre exacto. Útil cuando algo externo (una app mobile, otro servicio) necesita consumir estos datos como JSON.

</div>

---
layout: default
---

# Server Actions: mutar sin API

<div class="grid grid-cols-2 gap-3 text-sm">
<div>

```tsx
// app/products/actions.ts
'use server'

export async function createProduct(
  formData: FormData
) {
  const name = formData.get('name') as string
  await db.products.create({ name })
}
```

</div>
<div>

```tsx
import { createProduct } from './actions'

export default function NewProductPage() {
  return (
    <form action={createProduct}>
      <input name="name" />
      <button type="submit">Crear</button>
    </form>
  )
}
```

</div>
</div>

<div class="mt-2 text-xs opacity-80">

`'use server'` marca una función para correr en el servidor — un `<form>` la puede usar directo en su `action`, sin escribir un endpoint ni un `fetch` manual del lado del cliente. Funciona incluso con JavaScript deshabilitado.

</div>

<div class="mt-1 text-xs opacity-60">

→ [nextjs.org/docs/app/getting-started/updating-data](https://nextjs.org/docs/app/getting-started/updating-data)

</div>

---
layout: center
---

# Optimizaciones automáticas

---
layout: default
---

# `next/image`

```tsx
import Image from 'next/image'

<Image src="/mouse.png" alt="Mouse" width={300} height={300} />
```

<div class="grid grid-cols-2 gap-3 mt-3 text-sm">
<div class="p-3 rounded-lg bg-gray-100"><strong>Sin pedirlo</strong><br/>Lazy loading, formato moderno (WebP/AVIF) si el navegador lo soporta, tamaño ajustado al dispositivo.</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>Evita</strong><br/>El salto de layout (<em>layout shift</em>) mientras la imagen carga — reserva el espacio de antemano.</div>
</div>

---
layout: default
---

# `next/font`

```tsx
import { Geist } from 'next/font/google'

const geist = Geist({ subsets: ['latin'] })

export default function RootLayout({ children }) {
  return <html className={geist.className}>...</html>
}
```

<div class="mt-3 text-sm opacity-80">

La fuente se descarga **en el build**, no en cada visita — queda alojada junto al resto de los archivos estáticos. Sin pedidos extra a Google Fonts en el navegador de cada persona, mejor privacidad y una carga más rápida.

</div>

---
layout: default
---

# Metadata API

```tsx
// app/products/[id]/page.tsx
export async function generateMetadata({ params }) {
  const { id } = await params
  const product = await getProduct(id)
  return { title: product.name, description: `Comprá ${product.name}` }
}
```

<div class="mt-3 text-sm opacity-80">

Exportar `metadata` (fijo) o `generateMetadata` (calculado) desde cualquier `page.tsx`/`layout.tsx` arma automáticamente el `<title>` y las etiquetas `<meta>` de esa página — sin tocar `<head>` a mano.

</div>

---
layout: center
---

# Cierre

---
layout: default
---

# ¿Cuándo conviene Next.js?

<div class="grid grid-cols-2 gap-4 mt-4 text-sm">
<div class="p-4 rounded-lg bg-green-50 border-2 border-green-300">

**Conviene**

Sitios donde el SEO importa (contenido que debe indexar Google), páginas que se benefician de cargar rápido con el contenido ya armado, o que combinan partes estáticas con partes dinámicas.
</div>
<div class="p-4 rounded-lg bg-yellow-50 border-2 border-yellow-300">

**Una SPA alcanza**

Un panel interno, una app detrás de login donde nadie necesita indexarla, o un prototipo chico donde la complejidad extra no se justifica todavía.
</div>
</div>

<div class="mt-4 text-sm italic opacity-80 text-center">

No reemplaza a una SPA de React en todos los casos — agrega una herramienta más, para un problema específico (SEO y carga inicial).

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-6 mt-2 text-xs">
<div>

**Ruteo**

| Forma | Para qué |
|---|---|
| `app/x/page.tsx` | Ruta `/x` |
| `app/layout.tsx` | Layout compartido, obligatorio en la raíz |
| `app/x/[id]/page.tsx` | Ruta dinámica |
| `loading.tsx` / `error.tsx` | Estados por convención de archivo |
| `<Link href="...">` | Navegación sin recargar |

</div>
<div>

**Datos y componentes**

| Forma | Para qué |
|---|---|
| Componente `async` | Server Component con fetch directo |
| `'use client'` | Habilita hooks/eventos del navegador |
| `next: { revalidate: N }` | ISR, cada N segundos |
| `generateStaticParams` | Pre-generar rutas dinámicas |
| `'use server'` | Server Action, para mutar desde un form |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [nextjs.org/docs](https://nextjs.org/docs) — documentación oficial
- [nextjs.org/docs/app/getting-started/installation](https://nextjs.org/docs/app/getting-started/installation) — instalación y `create-next-app`
- [nextjs.org/docs/app/getting-started/server-and-client-components](https://nextjs.org/docs/app/getting-started/server-and-client-components) — Server vs. Client Components, en profundidad
- [nextjs.org/docs/app/getting-started/fetching-data](https://nextjs.org/docs/app/getting-started/fetching-data) — fetch, cache y estrategias de rendering
- [nextjs.org/docs/app/getting-started/updating-data](https://nextjs.org/docs/app/getting-started/updating-data) — Server Actions
- [nextjs.org/docs/app/api-reference/file-conventions](https://nextjs.org/docs/app/api-reference/file-conventions) — todas las convenciones de archivo del App Router
- [nextjs.org/docs/app/api-reference/components/image](https://nextjs.org/docs/app/api-reference/components/image) · [.../font](https://nextjs.org/docs/app/api-reference/components/font)
- [nextjs.org/learn](https://nextjs.org/learn) — curso interactivo oficial, gratuito

</div>
