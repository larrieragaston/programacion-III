# React

## El salto de paradigma más grande

Hasta acá vieron paradigmas imperativos y orientados a objetos (Java, C) y bases de datos relacionales, en los primeros dos años de la carrera. El salto más grande de esta unidad es el modelo **declarativo, basado en componentes** de React — y conecta directo con el eje funcional de todo el curso: un componente de React es, en esencia, **una función pura de `props`/`state` a JSX**. Mismos props y mismo state, mismo resultado visual — la misma idea de "función pura" de JS Funcional, aplicada a interfaces de usuario en vez de a transformaciones de datos.

De acá en adelante, todo el código de la unidad se escribe en **TypeScript**, recién visto en el tema anterior — empezando por los `props` tipados de cada componente.

## ¿Qué es React?

React es una **librería** de JavaScript/TypeScript para construir interfaces de usuario — no un framework completo (a diferencia de Angular): se enfoca en la capa de vista, y se combina con otras librerías según haga falta (ruteo, manejo de estado global, etc.).

Fue creada en **Facebook** por Jordan Walke, y liberada como código abierto en **2013**. Hoy la mantiene Meta junto con una comunidad enorme. Su modelo central — **la UI como función del estado** — se popularizó tanto que hoy influye en el diseño de otros frameworks (Vue, Svelte), aunque cada uno lo resuelva a su manera.

React no inventó los "componentes" — la idea ya existía en interfaces de escritorio hace décadas. Lo que sí instaló como estándar de la industria fue combinarlos con un modelo de datos unidireccional y un DOM virtual, que se explica en la siguiente sección.

## Por qué declarativo

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

Con manipulación directa del DOM (imperativo), cada cambio de estado obliga a escribir a mano los pasos para actualizar la pantalla — crear el elemento, asignarle sus propiedades, insertarlo en el lugar correcto. React invierte el problema: se describe la UI **en función del estado actual**, y React se encarga de calcular qué cambió y actualizar solo eso.

## El DOM virtual

El **DOM virtual** es una representación en memoria (un objeto JavaScript liviano) del DOM real del navegador. El flujo, cada vez que cambia el estado, es:

<div class="flow-row">
<div class="flow-box tone-brand">Cambia el estado</div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box">React arma un DOM virtual nuevo</div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box">Lo compara (<em>diff</em>) contra el anterior</div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-green">Aplica al DOM real solo lo mínimo necesario</div>
</div>

Manipular directamente el DOM real es costoso — trabajar primero en memoria y aplicar el mínimo cambio necesario (*reconciliation*) es la razón principal por la que React sigue siendo rápido incluso en interfaces grandes, con muchos componentes actualizándose seguido.

## JSX

### JSX: qué es realmente

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

JSX no es HTML ni un lenguaje nuevo — es **azúcar sintáctica** sobre `React.createElement`. Un compilador (Babel, o Vite por debajo) lo traduce a JavaScript plano antes de que llegue al navegador. Escribir JSX a mano es muchísimo más legible que anidar llamadas a `createElement` — pero el resultado final, una vez compilado, es exactamente el mismo código.

<div class="practice-box">
<p class="practice-label">Para pensar</p>

Un `<div className="card"><h3>{name}</h3></div>` con dos niveles de anidamiento se traduce a dos llamadas anidadas a `React.createElement`. ¿Cómo se vería, escrito a mano con `createElement`, un componente con tres niveles de anidamiento? No hace falta escribirlo completo — alcanza con notar cuánto más difícil es de leer que el JSX equivalente.
</div>

## Componentes

### Componentes funcionales + props tipados

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

Un componente es una función que recibe `props` (un objeto) y devuelve JSX. `{ name }: GreetingProps` desestructura el prop directamente en la firma — el mismo patrón de destructuring en parámetros ya visto en JS Contemporáneo, ahora con el tipo declarado con la `interface` recién vista en TypeScript.

### Composición de componentes

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

Los componentes se combinan como funciones que llaman a otras funciones — `ProductList` compone varios `ProductCard`. Es la misma idea de composición de JS Funcional (`compose`/`pipe`), aplicada a piezas de interfaz en vez de a transformaciones de datos puras.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una `interface UserCardProps { name: string; role: 'alumno' | 'profesor' }` (reutilizando el literal type visto en TypeScript) y un componente `UserCard` que muestre el nombre y, condicionalmente, un ícono o texto distinto según el `role`. Componé un `UserList` que renderice tres `UserCard` con datos distintos.
</div>

## Estado: `useState`

### `useState`

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

`useState(0)` declara una variable de estado (`count`, arranca en `0`) y su función para actualizarla (`setCount`). Llamar a `setCount` no solo cambia el valor — le avisa a React que tiene que volver a renderizar el componente con el nuevo estado. `useState` es un **hook**: una función especial de React que solo se puede llamar en el nivel superior de un componente (no dentro de un `if` o un `for`), y que engancha el componente al sistema de estado y re-render de React.

### Por qué no se puede mutar el estado

```tsx
const [items, setItems] = useState(['Mouse', 'Teclado'])

// ❌ mutar directamente no dispara un nuevo render
items.push('Monitor')

// ✅ crear un array nuevo, con spread — React lo detecta y re-renderiza
setItems([...items, 'Monitor'])
```

Mismo tema que en JS Funcional: React detecta cambios comparando **referencias**, no el contenido interno del objeto. Si se muta el array original, la referencia sigue siendo la misma — React no se entera de nada y la pantalla no se actualiza. Por eso el estado siempre se actualiza creando una copia nueva (spread, como en el ejemplo, o un `map`/`filter` que ya devuelven un array nuevo), nunca mutando el valor anterior.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí un componente `Cart` con `useState<string[]>([])` para una lista de productos en un carrito. Agregá un botón "Agregar Mouse" que use spread para agregar `'Mouse'` al array, y otro botón "Vaciar" que reemplace el estado por un array vacío. Mostrá la cantidad de ítems con `{items.length}`.
</div>

## Renderizado condicional y de listas

### Renderizado condicional

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

JSX es JavaScript — así que "renderizado condicional" es, literalmente, usar `if`/`else` o el operador ternario para decidir qué JSX devolver. Nada nuevo que aprender más allá de lo que ya sabían.

### Listas: `map` de nuevo

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

Otra conexión directa con JS Funcional: renderizar una lista es `map`-ear un array de datos a un array de elementos JSX. La única pieza nueva es `key`.

### `key`: por qué hace falta

```tsx
products.map((p) => <li key={p.name}>{p.name}</li>)
```

`key` le da a React una identidad estable por elemento de la lista — así, cuando la lista cambia (se agrega, se quita o se reordena un ítem), React puede saber **cuál** elemento del DOM corresponde a cuál dato, en vez de volver a crear todos desde cero. Tiene que ser única entre elementos hermanos y, idealmente, estable entre renders — un `id` real de los datos, no el índice del array como primera opción (el índice cambia si la lista se reordena, lo que puede causar bugs sutiles de estado mezclado entre ítems).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Con el catálogo de `Product[]` ya usado, renderizá la lista completa con `map` y `key={p.name}`. Después agregá un `useState<boolean>` que alterne entre mostrar todos los productos o solo los que tienen `price > 20000` (renderizado condicional combinado con `filter`, ya visto en JS Funcional).
</div>

## Formularios controlados

### Input controlado

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

Un input **controlado** tiene su valor manejado por el estado de React (`value={query}`), no por el DOM directamente — cada tecla dispara `onChange`, que actualiza el estado, que a su vez actualiza el `value` mostrado. React queda como la única fuente de verdad del valor del campo, en vez de tener que leerlo del DOM cuando haga falta (que es como se hacía antes, con `document.querySelector(...).value`).

### Formulario con varios campos y filtro

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

Todo lo visto hasta acá combinado: estado (`query`), `filter` de JS Funcional, y renderizado de lista con `key`. Este patrón — estado que dispara un filtro que dispara un re-render — es la base de casi cualquier UI interactiva.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Extendé `ProductFilter` con un segundo input numérico para un precio máximo (`useState<number>`), y combiná ambos filtros (`query` y precio máximo) en el mismo `filter`. Los dos inputs deben ser controlados.
</div>

## Efectos: `useEffect`

### `useEffect`: para qué sirve

`useEffect` sirve para manejar **efectos secundarios**: código que interactúa con algo fuera del componente — pedidos de red, timers, suscripciones. La misma idea de "efecto" que se vio como opuesto de "pureza" en JS Funcional. Recibe una función y, opcionalmente, un array de **dependencias**, que determina cuándo corre:

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>Sin array</h4>

Corre después de <strong>cada</strong> render.
</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
<h4><code>[]</code></h4>

Corre <strong>una sola vez</strong>, después del primer render.
</div>
<div class="info-card">
<h4><code>[a, b]</code></h4>

Corre en el primer render y de nuevo cada vez que <code>a</code> o <code>b</code> cambian.
</div>
</div>

### `useEffect` + `fetch`: conectando con Asincronismo

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

El mismo `async`/`await` de Asincronismo, ahora disparado desde `useEffect` con dependencias `[]` — "buscá los productos una vez, apenas se monta el componente". El estado `loading` maneja el intermedio entre "todavía no llegó la respuesta" y "ya se puede mostrar algo" — un patrón que va a reaparecer todo el tiempo al conectar con una API real (Node + Express, más adelante en la unidad).

Una nota importante: `useEffect` no puede recibir directamente una función `async` (React espera que la función de efecto devuelva nada o una función de limpieza, no una Promise) — por eso el patrón habitual es declarar una función `async` **adentro** del efecto y llamarla enseguida, como en el ejemplo.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí un componente `UserGreeting` que use `useEffect` con `[]` para simular una carga (con un `setTimeout` de un segundo envuelto en una Promise, como en Asincronismo) que resuelva con un nombre de usuario. Mientras carga, mostrá `"Cargando..."`; cuando termine, mostrá `"Hola, {nombre}!"`.
</div>

## Qué sigue después de estos dos hooks

`useState` y `useEffect` alcanzan para la gran mayoría de los componentes de este curso — son, con diferencia, los dos hooks más usados en cualquier proyecto real de React. Existen más hooks en la librería estándar para casos puntuales, que no se cubren en profundidad en este apunte pero vale saber que existen:

<div class="card-grid card-grid-2">
<div class="info-card">
<h4><code>useContext</code></h4>

Compartir estado entre componentes lejanos en el árbol, sin pasar props manualmente en cada nivel intermedio.
</div>
<div class="info-card">
<h4><code>useRef</code></h4>

Guardar un valor mutable que sobrevive entre renders sin disparar uno nuevo, o acceder directamente a un elemento del DOM.
</div>
<div class="info-card">
<h4><code>useMemo</code> / <code>useCallback</code></h4>

Cachear un valor o una función entre renders, para optimizar performance en casos puntuales donde un recálculo es costoso.
</div>
<div class="info-card">
<h4><code>useReducer</code></h4>

Alternativa a <code>useState</code> para estado más complejo, con la misma lógica de un <code>reducer</code> ya visto en JS Funcional.
</div>
</div>

También se puede escribir un **custom hook** propio (una función que empieza con `use` y combina otros hooks) para reutilizar lógica de estado/efectos entre varios componentes — otra herramienta para cuando aparezca la necesidad real, típicamente en el proyecto integrador.

## Cheat sheet

<div class="card-grid card-grid-2">
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

## Referencias y recursos

- [react.dev — Learn](https://react.dev/learn) — documentación oficial, ya orientada a hooks y componentes funcionales
- [react.dev — Keeping Components Pure](https://react.dev/learn/keeping-components-pure) — conecta directo con el eje funcional del curso
- [react.dev — Referencia de Hooks](https://react.dev/reference/react/hooks) — todos los hooks de la librería estándar, incluidos los mencionados brevemente en este apunte
- [vite.dev](https://vite.dev/) — la herramienta recomendada hoy para arrancar un proyecto de React desde cero (`npm create vite@latest`)

## Cierre

El objetivo de este tema es entender el modelo mental de React (UI como función del estado) y manejar con soltura componentes, props tipados, `useState` y `useEffect` — la base de cualquier interfaz interactiva. El resto de la unidad (Node + Express, MongoDB) construye el backend que un componente como `ProductList` va a terminar consumiendo con `fetch`, cerrando el circuito completo de una aplicación full-stack.
