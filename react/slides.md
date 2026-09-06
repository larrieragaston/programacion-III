---
theme: bricks
title: Programación III - React
download: true
info: |
  React - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: react, jsx, hooks, useState, useEffect, componentes, vite, react-router, testing-library, axios, INSPT, UTN
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

# ¿Qué es React?

<div class="mt-8 text-lg opacity-90">

React es una **librería** de JavaScript/TypeScript para construir interfaces de usuario.

</div>

<div class="mt-8 text-sm opacity-80">

No es un framework completo (a diferencia de Angular): se enfoca únicamente en la capa de vista — cómo se ve la pantalla y cómo se actualiza cuando cambian los datos — y se combina con otras librerías para todo lo demás (ruteo, llamadas HTTP, manejo de formularios...). Ese "combinar piezas" es, de hecho, buena parte de lo que se ve en este módulo.

</div>

---
layout: default
---

# Historia

- **2011** — Jordan Walke, ingeniero de Facebook, crea un prototipo interno ("FaxJS") para el feed de noticias.
- **2012** — Instagram lo adopta y lo pone a prueba en producción, a gran escala.
- **Mayo 2013** — se libera como **código abierto**, en la conferencia JSConf US.
- **Febrero 2019** (v16.8) — llegan los **Hooks**: `useState`/`useEffect` reemplazan a los componentes de clase como forma estándar de escribir componentes. De acá en más, este curso usa siempre funciones — clases todavía existen y se pueden encontrar en código viejo, pero no se cubren en este módulo.
- **Marzo 2022** (v18) — renderizado concurrente.
- **Diciembre 2024** (v19) — Server Components estables, `use()`.
- **Hoy** — lo mantiene Meta junto con una comunidad enorme.

<div class="mt-4 text-sm italic opacity-80">

Trece años de historia continua es mucho tiempo en el mundo del frontend — la próxima slide muestra qué tan vigente sigue estando.

</div>

---
layout: default
---

# ¿Quién lo usa?

<div class="grid grid-cols-4 gap-3 mt-8 text-sm">
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">Meta / Facebook</div>
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">Instagram</div>
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">Netflix</div>
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">WhatsApp Web</div>
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">Airbnb</div>
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">Uber</div>
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">Discord</div>
<div class="p-4 rounded-lg bg-gray-100 text-center font-semibold">The New York Times</div>
</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

Desde redes sociales hasta streaming, e-commerce y medios — el mismo modelo de componentes sirve para interfaces muy distintas entre sí.

</div>

---
layout: default
---

# Competidores: cómo se compara

<div class="overflow-x-auto mt-4 text-xs">

| | React | Vue | Angular | Svelte |
|---|---|---|---|---|
| Lanzamiento | 2013 | 2014 | 2016 (reescritura de AngularJS, 2010) | 2016 |
| ⭐ GitHub | ~230k | ~210k | ~95k | menor, en crecimiento |
| Descargas npm/semana | ~28.5M | ~7.2M | ~3.8M | mucho menor |
| % de uso (State of JS 2025) | **85%** | 52% | 48% | 27% |
| % satisfacción (State of JS 2025) | 72% | 84% | 48% | **86%** |

</div>

<div class="mt-2 text-xs opacity-80">

React lidera en adopción real — descargas, empleos, proyectos productivos. Angular es el único **framework completo** de la lista, pesado pero atractivo en proyectos empresariales grandes. Svelte genera la mayor satisfacción entre quienes ya lo usan, aunque lo usa mucha menos gente.

</div>

<div class="mt-1 text-xs italic opacity-60">

Fuente: [State of JS 2025](https://2025.stateofjs.com/en-US/libraries/front-end-frameworks/), [npmtrends.com](https://npmtrends.com/angular-vs-react-vs-vue) — principios de 2025/2026.

</div>

---
layout: default
---

# Principales características

<div class="grid grid-cols-1 gap-3 mt-8 text-base">
<div class="p-3 rounded-lg bg-gray-100"><strong>Declarativo</strong> — se describe QUÉ se quiere ver, no los pasos para lograrlo</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>Basado en componentes</strong> — la UI se arma combinando piezas reutilizables</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>DOM virtual</strong> — actualiza la pantalla sin recalcular todo de cero</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>Flujo de datos unidireccional</strong> — los datos bajan, los eventos suben</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>Ecosistema enorme</strong> — se combina con otras librerías para todo lo demás</div>
</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

Las próximas slides desarrollan cada una.

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

# Basado en componentes

- Toda la interfaz se arma combinando piezas reutilizables e independientes: los **componentes**.
- Cada uno encapsula su propia lógica y su propia porción de pantalla — como una pieza de LEGO que se puede ensamblar con otras para construir una aplicación completa.
- Se ve en profundidad un poco más adelante, en la sección dedicada a componentes.

<div class="mt-6 text-sm italic opacity-80 text-center">

React no inventó los "componentes" (la idea ya existía en UI de escritorio hace décadas) — lo que sí instaló como estándar de la industria fue combinarlos con un DOM virtual y un flujo de datos unidireccional, que se ven a continuación.

</div>

---
layout: default
---

# El árbol del DOM

```
html
├── head
│   ├── title
│   └── meta
└── body
    ├── h1
    ├── p
    │   └── a
    └── ul
        ├── li
        ├── li
        └── li
```

<div class="mt-4 text-sm opacity-80">

El **DOM** (*Document Object Model*) representa la página como un árbol de nodos — cada etiqueta HTML es un nodo, anidado según cómo esté anidado el HTML. El navegador guarda este árbol en memoria y lo usa para todo: pintar la pantalla, calcular estilos, responder a eventos. Modificarlo directamente (como en el ejemplo imperativo de un par de slides atrás) es una operación relativamente **costosa** — de ahí sale la próxima idea.

</div>

---
layout: default
---

# El DOM virtual

- El **DOM virtual** es una representación en memoria (un objeto JS liviano) del árbol del DOM recién visto — no el DOM real del navegador, una copia mucho más barata de modificar.
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
layout: default
---

# Flujo de datos unidireccional

```tsx
function ProductCard({ name, onAddToCart }: { name: string; onAddToCart: () => void }) {
  return (
    <div>
      <span>{name}</span>
      <button onClick={onAddToCart}>Agregar</button>   {/* evento sube */}
    </div>
  )
}

function ProductList() {
  const handleAdd = () => console.log('agregado al carrito')
  return <ProductCard name="Mouse" onAddToCart={handleAdd} />   {/* dato baja */}
}
```

<div class="mt-4 text-sm opacity-80">

Los **datos bajan**: un componente padre le pasa `props` a sus hijos, nunca al revés. Los **eventos suben**: un hijo no puede modificar el estado de su padre directamente — le avisa a través de una función que el padre le pasó como prop (`onAddToCart`). Esta disciplina (a diferencia de que cualquier parte de la app pueda modificar cualquier dato) es lo que hace que una aplicación grande siga siendo predecible: el estado de algo siempre vive en un solo lugar, y se sabe exactamente quién puede cambiarlo.

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

<v-click>

<div class="mt-3 text-xs opacity-80">

Antes de los Hooks (2019), esto se escribía con clases: `class Greeting extends React.Component { render() { ... } }`. Todavía se puede usar y se encuentra en código viejo, pero prácticamente todo el código nuevo — y este curso — usa funciones.

</div>

</v-click>

---
layout: default
---

# Armando una pantalla con componentes

<div class="border-2 border-red-400 rounded-lg p-2 text-xs mt-4">
<div class="font-bold text-red-500 mb-1">① Header</div>
<div class="flex justify-between items-center bg-gray-50 p-2 rounded">
<span>Mi Tienda</span>
<span>🛒 Carrito</span>
</div>
</div>

<div class="flex gap-2 mt-2 text-xs">
<div class="border-2 border-green-400 rounded-lg p-2 w-1/3">
<div class="font-bold text-green-600 mb-1">② Sidebar</div>
<div class="bg-gray-50 p-2 rounded">Categorías...</div>
</div>
<div class="border-2 border-blue-400 rounded-lg p-2 flex-1">
<div class="font-bold text-blue-600 mb-1">③ ProductGrid</div>
<div class="grid grid-cols-2 gap-2">
<div class="border-2 border-purple-400 rounded p-2 text-purple-600 font-bold">④ ProductCard</div>
<div class="border-2 border-purple-400 rounded p-2 text-purple-600 font-bold">④ ProductCard</div>
</div>
</div>
</div>

<div class="mt-4 text-sm italic opacity-80 text-center">

¿Qué componentes identificás en esta pantalla? Marquen en voz alta cada sección numerada antes de pasar a la próxima slide.

</div>

---
layout: default
---

# Composición de componentes

```tsx
function App() {
  return (
    <>
      <Header />                {/* ① */}
      <div className="layout">
        <Sidebar />              {/* ② */}
        <ProductGrid>            {/* ③ */}
          <ProductCard name="Mouse" price={18000} />     {/* ④ */}
          <ProductCard name="Teclado" price={25000} />   {/* ④ */}
        </ProductGrid>
      </div>
    </>
  )
}
```

<div class="mt-3 text-sm opacity-80">

Los componentes se combinan como funciones que llaman a otras funciones — cada caja numerada de la slide anterior es, literalmente, un componente (`ProductCard` ya se definió un par de slides atrás). Misma idea de composición de JS Funcional (`compose`/`pipe`), ahora aplicada a piezas de interfaz.

</div>

---
layout: default
---

# Props vs. state: la diferencia

```tsx
interface CounterProps {
  step: number   // prop: lo decide quien usa el componente, de afuera
}

function Counter({ step }: CounterProps) {
  const [count, setCount] = useState(0)   // state: lo maneja el componente, por dentro

  return (
    <button onClick={() => setCount(count + step)}>{count}</button>
  )
}

<Counter step={5} />   // el padre elige step; Counter elige y controla count
```

<div class="mt-4 text-sm opacity-80">

**`props`**: datos que un componente **recibe** de su padre — de solo lectura, el componente no los puede modificar (si necesita cambiarlos, se lo pide al padre vía una función, como en el flujo unidireccional). **`state`**: datos que un componente **posee y administra** internamente, con `useState` — privados a ese componente, y su cambio dispara un re-render. La confusión más común es intentar reasignar un prop directamente: si algo puede cambiar por acción del propio componente, es `state`; si lo define quien lo usa desde afuera, es `props`.

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
layout: center
---

# Más hooks de la librería estándar

---
layout: default
---

# `useContext`: estado global sin prop drilling

```tsx
const UserContext = createContext<string | null>(null)
function App() {
  const [user] = useState('Ada')
  return (
    <UserContext.Provider value={user}>
      <Toolbar />
    </UserContext.Provider>
  )
}
function Toolbar() {
  return <UserGreeting />   // no recibe "user" como prop
}
function UserGreeting() {
  const user = useContext(UserContext)
  return <span>Hola, {user}</span>
}
```

<div class="mt-3 text-xs opacity-80">

Sin `useContext`, `user` tendría que pasarse como prop a través de `Toolbar`, aunque no lo use — solo para que llegue a `UserGreeting` (*prop drilling*). Un `Context.Provider` publica un valor que cualquier descendiente lee directo con `useContext`, sin importar el anidamiento.

</div>

---
layout: default
---

# `useRef`: valores que sobreviven sin re-renderizar

```tsx
function SearchInput() {
  const inputRef = useRef<HTMLInputElement>(null)

  const focusInput = () => inputRef.current?.focus()

  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Enfocar</button>
    </>
  )
}
```

<div class="mt-3 text-sm opacity-80">

`useRef` guarda un valor mutable (`.current`) que persiste entre renders — a diferencia de `useState`, cambiarlo **no** dispara un nuevo render. Dos usos típicos: acceder directamente a un elemento del DOM (como `inputRef` arriba) o guardar un valor que necesita sobrevivir renders sin ser parte de lo que se muestra en pantalla (un id de `setTimeout`, un contador interno).

</div>

---
layout: default
---

# `useMemo` y `useCallback`: cachear entre renders

```tsx
function ProductList({ products, query }: { products: Product[]; query: string }) {
  // useMemo: cachea un VALOR calculado, se recalcula solo si products/query cambian
  const filtered = useMemo(
    () => products.filter((p) => p.name.includes(query)),
    [products, query]
  )

  // useCallback: cachea una FUNCIÓN, se recrea solo si products cambia
  const handleAdd = useCallback(
    (name: string) => console.log('agregado:', name),
    [products]
  )

  return <ul>{filtered.map((p) => <li key={p.name}>{p.name}</li>)}</ul>
}
```

<div class="mt-3 text-sm opacity-80">

Los dos resuelven el mismo problema — evitar recalcular algo caro (o recrear una función) en **cada** render — para un valor (`useMemo`) o una función (`useCallback`). Son optimizaciones puntuales: no hace falta envolver todo con esto, solo cuando un cálculo real es costoso o una función se pasa a un componente hijo optimizado con `memo`.

</div>

---
layout: default
---

# `useReducer`: estado complejo con reducers

```tsx
type Action = { type: 'add'; name: string } | { type: 'clear' }
function cartReducer(state: string[], action: Action): string[] {
  switch (action.type) {
    case 'add': return [...state, action.name]
    case 'clear': return []
  }
}
function Cart() {
  const [items, dispatch] = useReducer(cartReducer, [])
  return (
    <button onClick={() => dispatch({ type: 'add', name: 'Mouse' })}>
      Agregar ({items.length})
    </button>
  )
}
```

<div class="mt-3 text-xs opacity-80">

Alternativa a `useState` para varias transiciones de estado. `cartReducer` es un `reducer` de JS Funcional (`(estado, acción) => nuevo estado`) — la misma función que usa `Array.reduce`, ahora manejando estado de un componente.

</div>

---
layout: default
---

# Tu propio hook: custom hooks

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(url).then((res) => res.json()).then((json) => {
      setData(json)
      setLoading(false)
    })
  }, [url])

  return { data, loading }
}

// Uso, en cualquier componente:
const { data: products, loading } = useFetch<Product[]>('/api/products')
```

<div class="mt-3 text-sm opacity-80">

Un **custom hook** es una función propia que empieza con `use` y combina otros hooks por dentro — acá, `useFetch` empaqueta el patrón `useState` + `useEffect` de la slide de `fetch` para poder reusarlo en cualquier componente sin repetir la lógica. Es la misma idea de extraer una función reutilizable de siempre, aplicada a lógica con estado.

</div>

---
layout: center
---

# Testing de componentes

---
layout: default
---

# React Testing Library: por qué

- Librería para testear componentes de React — hoy el estándar de facto, viene incluida por default en un proyecto creado con Vite + plantilla de testing.
- Su filosofía: testear el componente **como lo usa una persona real** (qué texto ve, qué botón puede clickear), no los detalles internos de implementación (qué hook usa, cuántas veces se renderizó).
- Un test que sobrevive a un refactor interno del componente, mientras la UI resultante no cambie, es una señal de que está bien escrito.

<div class="mt-6 text-sm italic opacity-80">

Contraste con testear implementación: si el test se rompe porque se cambió `useState` por `useReducer` sin cambiar nada visible en pantalla, el test estaba mal enfocado desde el principio.

</div>

---
layout: default
---

# Un test simple

```tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Counter } from './Counter'

test('incrementa el contador al hacer click', () => {
  render(<Counter />)

  const button = screen.getByRole('button', { name: '+' })
  fireEvent.click(button)

  expect(screen.getByText('1')).toBeInTheDocument()
})
```

<div class="mt-4 text-sm opacity-80">

`render` monta el componente en un DOM virtual de prueba. `screen.getByRole` busca el botón igual que lo encontraría alguien usando un lector de pantalla — por su rol y su texto, no por un `id` interno. `fireEvent.click` simula la interacción real. El `expect` final verifica lo que **ve** la persona usuaria (el texto "1" en pantalla), no una variable interna del componente.

</div>

---
layout: center
---

# Probar y correr un proyecto React

---
layout: default
---

# Crear un proyecto con Vite

```bash
npm create vite@latest
# seleccionar: React, luego TypeScript
```

<div class="mt-4 text-sm opacity-80">

**Vite** es hoy la herramienta más usada para arrancar un proyecto de React desde cero — reemplazó a *Create React App* (CRA), que Meta discontinuó oficialmente. Genera un proyecto mínimo con las configuraciones necesarias (bundler, dev server con recarga instantánea) sin tener que armarlas a mano.

</div>

---
layout: default
---

# Primer componente propio

```tsx
// src/App.tsx — se borran los imports y el CSS de ejemplo
function App() {
  return (
    <>
      <h1>Hola, Programación III</h1>
    </>
  )
}

export default App
```

```bash
npm install
npm run dev   # abre http://localhost:5173
```

<div class="mt-3 text-sm opacity-80">

El proyecto generado por Vite trae un `App.tsx` de ejemplo con un contador y los logos de Vite/React — se borra ese contenido y se arranca desde un componente propio, mínimo. `npm run dev` levanta el servidor de desarrollo con recarga en caliente: guardar el archivo actualiza el navegador sin perder el estado de la app.

</div>

---
layout: default
---

# Scaffolding recomendado

```
src/
├── components/   # piezas de UI reutilizables (ProductCard, Header...)
├── routes/       # una página/vista por ruta (ver React Router, próxima sección)
├── hooks/        # custom hooks propios (useFetch, useAuth...)
├── services/     # llamadas a APIs externas (axios, próxima sección)
├── constants/    # valores fijos compartidos
├── configs/      # configuración de librerías (axios, i18n...)
├── styles/       # CSS/estilos globales
├── utils/        # funciones auxiliares sin estado
├── App.tsx
└── main.tsx
```

<div class="mt-3 text-sm opacity-80">

Ninguna de estas carpetas la exige React — es una convención de organización que aparece una y otra vez en proyectos reales, a medida que crecen más allá de un puñado de componentes. Empezar un proyecto nuevo con esta estructura desde el día uno ahorra una reorganización dolorosa más adelante.

</div>

---
layout: center
---

# React Router DOM

---
layout: default
---

# Instalar y armar las rutas

```bash
npm install react-router-dom
```

```tsx
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import Home from './routes/Home'
import Products from './routes/Products'
import Layout from './components/Layout'
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="products" element={<Products />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
```

<div class="mt-3 text-xs opacity-80">

React, por sí solo, no sabe qué mostrar según la URL — para eso existe `react-router-dom`. Cada `<Route path="..." element={...}/>` mapea una URL a un componente; envolver a los demás en `<Route element={<Layout/>}>` define un **layout compartido** (próxima slide).

</div>

---
layout: default
---

# Layout compartido con `<Outlet />`

```tsx
import { NavLink, Outlet } from 'react-router-dom'

function Layout() {
  return (
    <div>
      <nav>
        <NavLink to="/">Inicio</NavLink>
        <NavLink to="/products">Productos</NavLink>
      </nav>
      <main>
        <Outlet />   {/* acá se renderiza la ruta activa (Home o Products) */}
      </main>
    </div>
  )
}

export default Layout
```

<div class="mt-3 text-sm opacity-80">

`NavLink` navega sin recargar la página (a diferencia de un `<a href>` común) y marca automáticamente el link activo. `<Outlet />` es el "hueco" donde React Router inserta el componente de la ruta hija que corresponda a la URL actual — así el `<nav>` y el resto del layout se escriben una sola vez, en vez de repetirlos en cada página.

</div>

---
layout: center
---

# Herramientas de calidad: Prettier + ESLint

---
layout: default
---

# Prettier: formateo automático

```bash
npm install --save-dev --save-exact prettier
```

```json
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

<div class="mt-4 text-sm opacity-80">

Prettier es un **formateador de código**: reacomoda indentación, comillas, punto y coma, saltos de línea, según reglas configurables — para que todo el código del equipo luzca igual, sin discutirlo línea por línea en cada revisión. Se integra con el editor (formatea al guardar) y con `git` (un *pre-commit hook* que lo corre antes de cada commit).

</div>

---
layout: default
---

# ESLint: errores antes de correr nada

```bash
npm create vite@latest   # ya viene con un .eslintrc básico incluido
```

```json
// eslintrc.json (resumido)
{
  "extends": "eslint:recommended",
  "rules": {
    "quotes": ["error", "single"]
  }
}
```

<div class="mt-4 text-sm opacity-80">

ESLint es un **analizador estático**: lee el código sin ejecutarlo y detecta problemas reales — variables declaradas y nunca usadas, un hook llamado condicionalmente (rompe las reglas de React), una importación que no existe. Un proyecto de Vite ya trae una configuración de ESLint razonable por defecto; se puede extender con más reglas, o integrarlo con Prettier para que no choquen entre sí.

</div>

---
layout: center
---

# Consumir APIs: Axios

---
layout: default
---

# Axios: cliente HTTP

```bash
npm install axios
```

```tsx
// services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:4000/',
  headers: { 'Content-Type': 'application/json' },
})

// corre antes de CADA request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
export default api
```

<div class="mt-3 text-xs opacity-80">

Axios es un cliente HTTP basado en Promises — la alternativa más usada a `fetch` nativo, con una API más cómoda (JSON automático, interceptores, cancelación de requests). Los **interceptores** corren antes de cada request o después de cada respuesta — acá, el de request agrega el token automáticamente, sin repetirlo en cada llamada.

</div>

---
layout: default
---

# Configs con Vite: `.env`

```bash
# .env.development
VITE_API_URL=http://localhost:4000/

# .env.production
VITE_API_URL=https://mi-api.com/
```

```tsx
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL })
```

<div class="mt-4 text-sm opacity-80">

Un proyecto Vite lee archivos `.env` de forma **nativa** — no hace falta instalar la librería `dotenv` (útil en un proyecto Node "pelado", sin bundler, pero redundante acá). Solo hay una regla: toda variable que necesite llegar al código del navegador tiene que empezar con el prefijo `VITE_` — es una medida de seguridad, para que Vite nunca exponga por accidente una variable de entorno del sistema que no estaba pensada para ser pública.

</div>

---
layout: center
---

# Librerías de componentes visuales

---
layout: default
---

# Por qué usar una

- Ahorra construir desde cero botones, inputs, modales, tablas — con estados de foco, hover, disabled y accesibilidad ya resueltos.
- Da **consistencia visual** de forma casi automática: todos los botones de la app se ven y se comportan igual, sin coordinarlo a mano.
- Se personaliza (colores, tipografía) mediante un sistema de *theming*, en vez de sobreescribir CSS componente por componente.

<div class="mt-6 text-sm italic opacity-80 text-center">

Nada de esto es gratis: agrega peso al bundle y un estilo visual reconocible — la próxima slide compara las opciones más usadas hoy.

</div>

---
layout: default
---

# Las más usadas, con números

<div class="overflow-x-auto mt-4 text-xs">

| Librería | Descargas npm/semana | Estilo |
|---|---|---|
| **MUI** | ~5.8M | Material Design de Google, muy completa |
| **Ant Design** | ~3.1M | Enterprise, pensada para dashboards y formularios densos |
| **Chakra UI** | ~1.4M | Minimalista, muy personalizable |
| **shadcn/ui** | ~150k (*) | Componentes que se copian al proyecto, no una dependencia tradicional |

</div>

<div class="mt-2 text-xs italic opacity-60">

(*) shadcn/ui no se instala como paquete, se copian los componentes fuente al proyecto — su descarga real no se refleja acá. Fuente: [npmtrends.com](https://npmtrends.com/@chakra-ui/react-vs-ant-design-vs-antd-vs-material-ui-vs-mui), principios de 2026.

</div>

<div class="mt-2 text-xs opacity-80">

MUI lidera en volumen — la opción "segura" por defecto. Ant Design es una recomendación personal: su set de componentes es muy completo para pantallas de datos (tablas, formularios, filtros), justo el tipo de UI del proyecto integrador.

</div>

---
layout: default
---

# Ejemplo con Ant Design

```bash
npm install antd
```

```tsx
import { Button, Table } from 'antd'

function ProductTable({ products }: { products: Product[] }) {
  const columns = [
    { title: 'Nombre', dataIndex: 'name' },
    { title: 'Precio', dataIndex: 'price' },
  ]

  return (
    <>
      <Table dataSource={products} columns={columns} rowKey="name" />
      <Button type="primary">Agregar producto</Button>
    </>
  )
}
```

<div class="mt-3 text-sm opacity-80">

`Table` resuelve de una sola vez ordenamiento, paginado y estilos consistentes — lo mismo que armar a mano tomaría bastantes slides de este propio módulo. `Button type="primary"` ya viene con el estilo de la marca del proyecto (definido una sola vez, en el tema de Ant Design), sin escribir CSS propio.

</div>

---
layout: center
---

# Autenticación

---
layout: default
---

# Dónde guardar el token

<div class="overflow-x-auto mt-4 text-xs">

| Método | Sobrevive un refresh | Riesgo principal |
|---|---|---|
| **Cookie `httpOnly`** | ✅ | Requiere que el backend la setee — JS del navegador no puede leerla, por diseño |
| **`localStorage`** | ✅ | Legible por cualquier script — vulnerable si hay una vulnerabilidad XSS |
| **`sessionStorage`** | ❌ (se borra al cerrar la pestaña) | Mismo riesgo que `localStorage`, ventana de exposición más corta |
| **Memoria (estado/Context)** | ❌ (se pierde al refrescar) | El más seguro contra XSS, pero necesita un refresh token para sostener la sesión |

</div>

<div class="mt-4 text-sm opacity-80">

No hay una respuesta única — es un balance entre seguridad y comodidad. La cookie `httpOnly` es la opción más recomendada hoy porque el propio navegador impide que JavaScript la lea, así que un ataque XSS no puede robarla directamente — pero exige que el backend coopere (fijarla en la respuesta, con los flags correctos). Para el proyecto integrador de este curso, `localStorage` es una opción razonable para empezar, dada su simplicidad.

</div>

---
layout: default
---

# `localStorage`, en código

```ts
// services/auth.ts
const TOKEN_KEY = 'auth_token'

export function saveToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
}
```

<div class="mt-4 text-sm opacity-80">

`localStorage` es una API nativa del navegador — no hace falta ninguna librería para usarla. Este mismo `getToken()` es el que se llamaría desde el interceptor de Axios visto un par de secciones atrás, para agregar el header `Authorization` en cada request.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
<div>

**Componentes, JSX y estado**

| Forma | Ejemplo |
|---|---|
| Componente | `function C({ x }: Props) { ... }` |
| Props tipados | `interface Props { x: string }` |
| Condicional / Lista | `{cond ? <A/> : <B/>}`, `{items.map(i => <li key={i.id}>)}` |
| Input controlado | `<input value={v} onChange={...}/>` |
| Estado | `const [s, setS] = useState(init)` |

</div>
<div>

**Hooks y herramientas**

| Hook / Tool | Para qué |
|---|---|
| `useEffect(fn, deps)` | Efectos: fetch, timers, suscripciones |
| `useContext`, `useRef` | Contexto global, referencias al DOM |
| `useMemo`/`useCallback`/`useReducer` | Cachear valor/función, estado complejo |
| Vite / Router / Axios | Scaffolding, rutas, HTTP |
| Testing Library | Testear componentes |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [react.dev — Learn](https://react.dev/learn) — documentación oficial, ya orientada a hooks y componentes funcionales
- [react.dev — Referencia de Hooks](https://react.dev/reference/react/hooks) — todos los hooks de la librería estándar
- [vite.dev](https://vite.dev/) — la herramienta recomendada hoy para arrancar un proyecto de React
- [reactrouter.com](https://reactrouter.com/) — documentación oficial de React Router
- [testing-library.com/react](https://testing-library.com/docs/react-testing-library/intro/) — React Testing Library
- [axios-http.com](https://axios-http.com/) — documentación de Axios
- [ant.design](https://ant.design/) y [mui.com](https://mui.com/) — las dos librerías de componentes visuales más usadas hoy
- [prettier.io](https://prettier.io/) y [eslint.org](https://eslint.org/) — formateo y análisis estático
- [2025.stateofjs.com](https://2025.stateofjs.com/en-US/libraries/front-end-frameworks/) — encuesta anual sobre el ecosistema JS

</div>
