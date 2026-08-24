---
theme: bricks
title: Programación III - React
download: true
info: |
  React - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: react, jsx, hooks, useState, useEffect, componentes, INSPT, UTN
transition: slide-left
mdc: true
---

# React

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/react.svg" alt="React" class="h-16 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# El salto de paradigma más grande

- Vieron paradigmas imperativos/OO (Java, C) y bases relacionales en los primeros dos años. El salto más grande de esta unidad es el modelo **declarativo, basado en componentes** — y conecta directo con el eje funcional de todo el curso.
- Un componente de React es, en esencia, **una función pura de `props`/`state` a JSX**: mismos props/state → mismo resultado visual. La idea de "función pura" de JS Funcional vuelve, aplicada a interfaces de usuario.
- De acá en adelante, todo el código de la unidad se escribe en **TypeScript** — recién visto — empezando por los `props` tipados de cada componente.

<div class="mt-6 text-sm italic opacity-80">

Retomando: en JS Funcional, una función pura devolvía siempre el mismo resultado para los mismos argumentos. React aplica exactamente esa idea a la pantalla — un componente "devuelve" la UI que corresponde a su estado actual.

</div>

---
layout: default
---

# ¿Qué es React?

- Una **librería** de JavaScript/TypeScript para construir interfaces de usuario — no un framework completo (a diferencia de Angular): se enfoca en la capa de vista, y se combina con otras librerías para ruteo, manejo de estado global, etc.
- Creada en **Facebook** por Jordan Walke, liberada como código abierto en **2013**. Hoy la mantiene Meta junto con una comunidad enorme.
- Su modelo — **UI como función del estado** — se popularizó tanto que hoy influye en el diseño de otros frameworks (Vue, Svelte) aunque cada uno lo resuelva a su manera.

<div class="mt-6 text-sm italic opacity-80">

React no inventó los "componentes" (la idea ya existía en UI de escritorio hace décadas) — lo que sí instaló como estándar de la industria fue combinarlos con un modelo de datos unidireccional y un DOM virtual, que se ve a continuación.

</div>

---
layout: default
---

# Por qué declarativo

```js
// Imperativo: hay que describir CÓMO llegar al resultado, paso a paso
const li = document.createElement('li')
li.textContent = 'Mouse'
li.classList.add('product-item')
document.querySelector('ul').appendChild(li)
```

```jsx
// Declarativo: se describe QUÉ se quiere ver, no los pasos para lograrlo
<ul>
  <li className="product-item">Mouse</li>
</ul>
```

<div class="mt-4 text-sm opacity-80">

Con manipulación directa del DOM (imperativo), cada cambio de estado obliga a escribir a mano los pasos para actualizar la pantalla. React invierte el problema: se describe la UI **en función del estado actual**, y React se encarga de calcular qué cambió y actualizar solo eso.

</div>

---
layout: default
---

# El DOM virtual

- El **DOM virtual** es una representación en memoria (un objeto JS liviano) del DOM real del navegador.
- Cuando el estado cambia, React arma un DOM virtual nuevo y lo compara (*diff*) contra el anterior — sin tocar el DOM real todavía.
- Recién después aplica al DOM real **solo los cambios mínimos necesarios** (*reconciliation*), en vez de volver a dibujar toda la pantalla.

<div class="flex justify-center gap-4 mt-6 text-xs">
<div class="p-3 rounded-lg border-2 border-blue-400 bg-blue-50 text-center w-40">Cambia el estado</div>
<div class="p-3 rounded-lg border-2 border-yellow-400 bg-yellow-50 text-center w-40">React calcula el diff</div>
<div class="p-3 rounded-lg border-2 border-green-400 bg-green-50 text-center w-40">Se actualiza solo lo necesario</div>
</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

Manipular directamente el DOM real es costoso — trabajar primero en memoria y aplicar el mínimo cambio necesario es la razón principal por la que React es rápido incluso con interfaces grandes.

</div>

---
layout: center
---

# JSX

---
layout: default
---

# JSX: qué es realmente

```jsx
const nav = (
  <ul id="nav">
    <li>Inicio</li>
  </ul>
)
```

```js
// Lo mismo, compilado por Babel — esto es lo que corre en el navegador
const nav = React.createElement(
  'ul',
  { id: 'nav' },
  React.createElement('li', null, 'Inicio')
)
```

<div class="mt-4 text-sm opacity-80">

JSX no es HTML ni un lenguaje nuevo — es **azúcar sintáctica** sobre `React.createElement`. Un compilador (Babel, o Vite por debajo) lo traduce a JavaScript plano antes de que llegue al navegador. Escribir JSX a mano es mucho más legible que anidar llamadas a `createElement`, pero el resultado final es exactamente el mismo código.

</div>

---
layout: center
---

# Componentes

---
layout: default
---

# Componentes funcionales + props tipados

```tsx
interface GreetingProps {
  name: string
}

function Greeting({ name }: GreetingProps) {
  return <h1>Hola, {name}!</h1>
}

// Uso
<Greeting name="Ada" />
```

<div class="mt-4 text-sm opacity-80">

Un componente es una función que recibe `props` (un objeto) y devuelve JSX. `{ name }: GreetingProps` desestructura el prop directamente en la firma — el mismo patrón de destructuring en parámetros ya visto en JS Contemporáneo, ahora con el tipo declarado con la `interface` recién vista en TypeScript.

</div>

---
layout: default
---

# Composición de componentes

```tsx
interface ProductCardProps {
  name: string
  price: number
}

function ProductCard({ name, price }: ProductCardProps) {
  return (
    <div className="card">
      <h3>{name}</h3>
      <p>${price}</p>
    </div>
  )
}

function ProductList() {
  return (
    <div>
      <ProductCard name="Mouse" price={18000} />
      <ProductCard name="Teclado" price={25000} />
    </div>
  )
}
```

<div class="mt-4 text-sm opacity-80">

Los componentes se combinan como funciones que llaman a otras funciones — `ProductList` compone varios `ProductCard`. Es la misma idea de composición de JS Funcional (`compose`/`pipe`), aplicada a piezas de interfaz en vez de transformaciones de datos.

</div>

---
layout: center
---

# Estado: `useState`

---
layout: default
---

# `useState`

```tsx
import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  )
}
```

<div class="mt-4 text-sm opacity-80">

`useState(0)` declara una variable de estado (`count`, arranca en `0`) y su función para actualizarla (`setCount`). Llamar a `setCount` no solo cambia el valor — le avisa a React que tiene que volver a renderizar el componente con el nuevo estado.

</div>

---
layout: default
---

# Por qué no se puede mutar el estado

```tsx
const [items, setItems] = useState(['Mouse', 'Teclado'])

// ❌ mutar directamente no dispara un nuevo render
items.push('Monitor')

// ✅ crear un array nuevo, con spread — React lo detecta y re-renderiza
setItems([...items, 'Monitor'])
```

<div class="mt-4 text-sm opacity-80">

Mismo tema que en JS Funcional: React detecta cambios comparando **referencias**, no el contenido interno del objeto. Si se muta el array original, la referencia sigue siendo la misma — React no se entera de nada y la pantalla no se actualiza. Por eso el estado siempre se actualiza creando una copia nueva (spread, como en el ejemplo), nunca mutando el valor anterior.

</div>

---
layout: center
---

# Renderizado condicional y de listas

---
layout: default
---

# Renderizado condicional

```tsx
interface Props {
  isLoggedIn: boolean
}

function Greeting({ isLoggedIn }: Props) {
  if (isLoggedIn) {
    return <h1>Bienvenida de nuevo!</h1>
  }
  return <h1>Por favor, iniciá sesión.</h1>
}

// Alternativa compacta, con operador ternario
function Badge({ isLoggedIn }: Props) {
  return <span>{isLoggedIn ? 'Conectado' : 'Desconectado'}</span>
}
```

<div class="mt-4 text-sm opacity-80">

JSX es JavaScript — así que "renderizado condicional" es, literalmente, usar `if`/`else` o el operador ternario para decidir qué JSX devolver. Nada nuevo que aprender más allá de lo que ya sabían.

</div>

---
layout: default
---

# Listas: `map` de nuevo

```tsx
interface Product {
  name: string
  price: number
}

function ProductList({ products }: { products: Product[] }) {
  return (
    <ul>
      {products.map((p) => (
        <li key={p.name}>{p.name} — ${p.price}</li>
      ))}
    </ul>
  )
}
```

<div class="mt-4 text-sm opacity-80">

Otra conexión directa con JS Funcional: renderizar una lista es `map`-ear un array de datos a un array de elementos JSX. La única pieza nueva es `key`, en la próxima slide.

</div>

---
layout: default
---

# `key`: por qué hace falta

```tsx
products.map((p) => <li key={p.name}>{p.name}</li>)
```

<div class="mt-4 text-sm opacity-80">

`key` le da a React una identidad estable por elemento de la lista — así, cuando la lista cambia (se agrega, se quita o se reordena un ítem), React puede saber **cuál** elemento del DOM corresponde a cuál dato, en vez de volver a crear todos desde cero. Tiene que ser única entre hermanos y, idealmente, estable entre renders (un `id` real de los datos — el índice del array es un último recurso, no la primera opción, porque cambia si la lista se reordena).

</div>

---
layout: center
---

# Formularios controlados

---
layout: default
---

# Input controlado

```tsx
import { useState } from 'react'

function SearchBox() {
  const [query, setQuery] = useState('')

  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="Buscar producto..."
    />
  )
}
```

<div class="mt-4 text-sm opacity-80">

Un input **controlado** tiene su valor manejado por el estado de React (`value={query}`), no por el DOM directamente — cada tecla dispara `onChange`, que actualiza el estado, que a su vez actualiza el `value` mostrado. React queda como la única fuente de verdad del valor del campo, en vez de tener que leerlo del DOM cuando haga falta.

</div>

---
layout: default
---

# Formulario con varios campos y filtro

```tsx
function ProductFilter({ products }: { products: Product[] }) {
  const [query, setQuery] = useState('')

  const filtered = products.filter((p) =>
    p.name.toLowerCase().includes(query.toLowerCase())
  )

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <ul>
        {filtered.map((p) => <li key={p.name}>{p.name}</li>)}
      </ul>
    </div>
  )
}
```

<div class="mt-4 text-sm opacity-80">

Todo lo visto hasta acá combinado: estado (`query`), `filter` de JS Funcional, y renderizado de lista con `key`. Este patrón — estado que dispara un filtro que dispara un re-render — es la base de casi cualquier UI interactiva.

</div>

---
layout: center
---

# Efectos: `useEffect`

---
layout: default
---

# `useEffect`: para qué sirve

- Sirve para manejar **efectos secundarios**: código que interactúa con algo fuera del componente — pedidos de red, timers, suscripciones — la misma idea de "efecto" vista como opuesto a "pureza" en JS Funcional.
- Recibe una función y, opcionalmente, un array de **dependencias**.
- Cuándo corre, según las dependencias:

<div class="grid grid-cols-3 gap-4 mt-4 text-sm">
<div class="p-3 rounded-lg bg-gray-100 text-center">

**Sin array**

Corre después de **cada** render.
</div>
<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-300 text-center">

**`[]`**

Corre **una sola vez**, después del primer render.
</div>
<div class="p-3 rounded-lg bg-gray-100 text-center">

**`[a, b]`**

Corre en el primer render y de nuevo cada vez que `a` o `b` cambian.
</div>
</div>

---
layout: default
---

# `useEffect` + `fetch`

```tsx
function ProductList() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadProducts() {
      const res = await fetch('/api/products')
      setProducts(await res.json())
      setLoading(false)
    }
    loadProducts()
  }, [])   // [] — solo al montar el componente

  if (loading) return <p>Cargando...</p>
  return <ul>{products.map((p) => <li key={p.name}>{p.name}</li>)}</ul>
}
```

<div class="mt-4 text-sm opacity-80">

El mismo `async`/`await` de Asincronismo, ahora disparado desde `useEffect` con dependencias `[]` — "buscá los productos una vez, apenas se monta el componente". El estado `loading` maneja el intermedio entre "todavía no llegó la respuesta" y "ya se puede mostrar algo" — un patrón que va a reaparecer todo el tiempo al conectar con una API real (Node + Express, más adelante en la unidad).

</div>

---
layout: default
---

# Qué sigue después de estos dos hooks

- `useState` y `useEffect` alcanzan para la gran mayoría de los componentes de este curso — son, con diferencia, los dos hooks más usados en cualquier proyecto real de React.
- Existen más hooks en la librería estándar para casos puntuales — no se cubren en profundidad acá, pero vale saber que existen para cuando aparezca la necesidad concreta:

<div class="grid grid-cols-2 gap-4 mt-4 text-xs">
<div class="p-3 rounded-lg bg-gray-100">

**`useContext`** — compartir estado entre componentes lejanos en el árbol, sin pasar props manualmente en cada nivel.
</div>
<div class="p-3 rounded-lg bg-gray-100">

**`useRef`** — guardar un valor mutable que sobrevive entre renders sin disparar uno nuevo (o acceder directamente a un elemento del DOM).
</div>
<div class="p-3 rounded-lg bg-gray-100">

**`useMemo` / `useCallback`** — cachear un valor o una función entre renders, para optimizar performance en casos puntuales.
</div>
<div class="p-3 rounded-lg bg-gray-100">

**`useReducer`** — alternativa a `useState` para estado más complejo, con la misma lógica de un `reducer` ya visto en JS Funcional.
</div>
</div>

<div class="mt-4 text-sm italic opacity-80 text-center">

También se puede escribir un <strong>custom hook</strong> propio (una función que empieza con <code>use</code> y combina otros hooks) para reutilizar lógica entre componentes — otra herramienta para más adelante.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-4 text-xs">
<div>

**Componentes y JSX**

| Forma | Ejemplo |
|---|---|
| Componente | `function C({ x }: Props) { return <div/> }` |
| Props tipados | `interface Props { x: string }` |
| Condicional | `{cond ? <A/> : <B/>}` |
| Lista | `{items.map(i => <li key={i.id}>...)}` |
| Input controlado | `<input value={v} onChange={...}/>` |

</div>
<div>

**Hooks**

| Hook | Para qué |
|---|---|
| `useState(init)` | Estado local del componente |
| `useEffect(fn, deps)` | Efectos: fetch, timers, suscripciones |
| `deps: []` | Efecto corre una sola vez |
| `deps: [a, b]` | Efecto corre si cambian `a`/`b` |
| `useContext`, `useRef`, `useMemo`... | Casos puntuales, para explorar después |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2">

- [react.dev — Learn](https://react.dev/learn) — documentación oficial, ya orientada a hooks y componentes funcionales
- [react.dev — Keeping Components Pure](https://react.dev/learn/keeping-components-pure) — conecta directo con el eje funcional del curso
- [react.dev — Referencia de Hooks](https://react.dev/reference/react/hooks) — todos los hooks de la librería estándar, incluidos los mencionados brevemente en este deck
- [vite.dev](https://vite.dev/) — la herramienta recomendada hoy para arrancar un proyecto de React desde cero (`npm create vite@latest`)

</div>
