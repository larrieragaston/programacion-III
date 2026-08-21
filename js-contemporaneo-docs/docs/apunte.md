# JS Contemporáneo

## Características de JavaScript

- **Interpretado**: no se compila a un binario antes de correr — un motor (V8, SpiderMonkey…) lo ejecuta directamente.
- **Multiparadigma**: imperativo, orientado a objetos, funcional — el funcional lo vimos a fondo en JS Funcional.
- **Tipado dinámico**: el tipo de una variable se determina en tiempo de ejecución, no hay que declararlo.
- **El único lenguaje que corre nativamente en el navegador** — y con Node.js, también en el servidor.

Multiparadigma y tipado dinámico no son casualidad — son parte de por qué JS es como es, y eso tiene una explicación histórica bastante concreta.

## El origen de JavaScript

En 1995, Netscape necesitaba un lenguaje de scripting liviano para su navegador, para competir con los applets de Java de Sun Microsystems (una tecnología pesada, pensada para programas completos corriendo dentro de la página, no para pequeños scripts). **Brendan Eich** lo diseñó en **10 días**, en mayo de 1995.

El lenguaje se lanzó primero como **Mocha**, se renombró a **LiveScript**, y terminó llamándose **JavaScript** — una decisión de marketing de último momento para subirse a la popularidad de Java, aunque los dos lenguajes no tienen relación técnica real más allá de compartir parte de la sintaxis de llaves y punto y coma heredada de C.

Diseñado en una semana y media para un caso de uso chico (validar formularios en un `<form>` antes de enviarlos al servidor), terminó siendo el lenguaje más usado del mundo. Varias de sus rarezas de sintaxis y comportamiento — la coerción de tipos con `==`, el `this` dinámico de las funciones tradicionales, `var` con scope de función — vienen directamente de esa urgencia inicial: se priorizó tener *algo* funcionando rápido, no un diseño prolijo a largo plazo.

## Cronología de ECMAScript

**ECMAScript** es el nombre del estándar; **JavaScript** es la implementación más conocida de ese estándar (hay otras, como ActionScript de Flash). El estándar lo mantiene un comité llamado **TC39**.

<div class="timeline-wrap">
<div class="timeline-line"></div>

<div class="timeline-node" style="left:2.0%">
<div class="timeline-label">ES1</div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">1997</div>
</div>

<div class="timeline-node" style="left:9.4%">
<div class="timeline-label">ES3</div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">1999</div>
</div>

<div class="timeline-node" style="left:16.8%">
<div class="timeline-label">ES5</div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">2009</div>
</div>

<div class="timeline-node" style="left:24.2%">
<div class="timeline-label" style="color:#78350f">ES6</div>
<div class="timeline-dot" style="background:#facc15;border-color:#111827"></div>
<div class="timeline-year">2015</div>
</div>

<div class="timeline-node" style="left:31.5%">
<div class="timeline-label">ES2016</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:38.9%">
<div class="timeline-label">ES2017</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:46.3%">
<div class="timeline-label">ES2018</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:53.7%">
<div class="timeline-label">ES2019</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:61.1%">
<div class="timeline-label">ES2020</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:68.5%">
<div class="timeline-label">ES2021</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:75.8%">
<div class="timeline-label">ES2022</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:83.2%">
<div class="timeline-label">ES2023</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:90.6%">
<div class="timeline-label">ES2024</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

<div class="timeline-node" style="left:98.0%">
<div class="timeline-label">ES2025</div>
<div class="timeline-dot" style="background:#22c55e"></div>
</div>

</div>

<div class="diagram-legend">
<span><span class="dot" style="background:#9ca3af"></span>ediciones tempranas</span>
<span><span class="dot" style="background:#facc15;border:1px solid #111827"></span>ES6 — el salto grande</span>
<span><span class="dot" style="background:#22c55e"></span>cadencia anual</span>
</div>

Desde **ES6 (2015)**, TC39 saca una revisión **por año**, cada junio — por eso se nombran por año ("ES2016", "ES2020", "ES2024") en vez de por número secuencial ("ES7", "ES11"): el número de edición dejó de tener sentido cuando el ritmo pasó a ser anual y continuo. La última edición confirmada es **ES2025**; para cuando se lea este apunte, es probable que ya exista una ES2026.

### ES1 → ES6: los grandes saltos

<div class="card-grid card-grid-2">
<div class="info-card">
<h4>ES1 — 1997</h4>

Primera edición estandarizada. JS ya se podía escribir en un navegador, pero sin estándar formal todavía — cada navegador implementaba su propia variante.
</div>
<div class="info-card">
<h4>ES3 — 1999</h4>

Expresiones regulares, `try`/`catch`, `switch`, `do...while`. La base "clásica" de JS durante más de una década (ES4 se abandonó por desacuerdos en el comité).
</div>
<div class="info-card">
<h4>ES5 — 2009</h4>

`"use strict"`, `JSON` nativo, y las funciones de orden superior de arrays: `forEach`, `map`, `filter`, `reduce` (ya las vimos a fondo en la unidad anterior, JS Funcional).
</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
<h4>ES6 / ES2015 — 2015</h4>

El salto grande: `let`/`const`, arrow functions, clases, módulos, Promesas, template literals, destructuring… la base de todo el JS que se escribe hoy. El resto de este apunte es, en gran parte, un recorrido por lo que trajo esta edición.
</div>
</div>

Después de ES6 no hubo otro salto de esa magnitud — desde 2016, cada año suma funcionalidades puntuales sobre esa misma base: mejores formas de trabajar con arrays, objetos y errores, y azúcar sintáctica para casos que ya eran posibles pero incómodos de escribir. La sección siguiente recorre, año a año, lo más destacado de cada edición hasta hoy.

## Cadencia anual (2016 en adelante)

Algunos de estos ítems se cubren en detalle en decks propios de la unidad para no duplicar contenido; acá quedan mencionados en su contexto histórico, con snippets cortos para los más autocontenidos.

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>2016</h4>

Operador de exponenciación: `2 ** 10` (en vez de `Math.pow(2, 10)`).
</div>
<div class="info-card">
<h4>2017</h4>

`async`/`await` — se ve en detalle en la próxima unidad (Asincronismo).
</div>
<div class="info-card">
<h4>2018</h4>

Spread y rest en objetos literales: `{ ...product, price: 15000 }` — ya visto en JS Funcional.
</div>
</div>

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>2019</h4>

`Array.prototype.flat()` — se ve más adelante en este mismo apunte.
</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
<h4>2020</h4>

`BigInt`, encadenamiento opcional `?.`, coalescencia de nulos `??` — las dos últimas, más adelante en este apunte.
</div>
<div class="info-card">
<h4>2021</h4>

`String.prototype.replaceAll()`, `Promise.any()`, y asignación lógica (`??=`, `||=`, `&&=`):

```js
config.timeout
  ??= 5000
```
</div>
</div>

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>2022</h4>

Campos de clase privados (`#saldo`), `Array.prototype.at()`, y `await` de nivel superior (sin envolverlo en una función `async`).
</div>
<div class="info-card">
<h4>2023</h4>

Versiones no-mutantes de los clásicos de array: `toSorted()`, `toReversed()`, `with()` — el equivalente inmutable de `sort()`, `reverse()` y `arr[i] = x`:

```js
numbers.toSorted(
  (a, b) => a - b
)
```
</div>
<div class="info-card">
<h4>2024</h4>

`Object.groupBy()` — agrupa los elementos de un array según una función, sin `reduce` manual:

```js
Object.groupBy(
  products,
  p => p.category
)
```
</div>
</div>

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>2025</h4>

Helpers de iteradores (`.map`/`.filter`/`.take` sobre iterators) y métodos de conjuntos en `Set` (`union`, `intersection`, `difference`).
</div>
</div>

## El salto grande: ES6 (2015)

### Declarar variables: `let` vs. `var`

```js
var name = 'Ada'
let name = 'Ada'    // mismo resultado, distinto comportamiento
```

- `var` tiene **scope de función** (o global) — ignora los bloques (`if`, `for`, `{}` sueltos).
- `let` tiene **scope de bloque** — solo existe dentro del `{}` donde se declaró.
- `var` sufre *hoisting* "raro": la declaración se sube al principio de la función, pero queda `undefined` hasta la línea donde se asigna. `let` también se sube, pero queda en una zona inaccesible (*temporal dead zone*) hasta esa línea — usarla antes tira error, no `undefined`.
- Redeclarar la misma variable con `var` en el mismo scope no tira error. Con `let`, sí.

Hoy `var` prácticamente no se usa en código nuevo — quedó por compatibilidad con proyectos viejos. La convención moderna es `const` por defecto, y `let` solo cuando la variable realmente necesita reasignarse.

### `const` y sus límites

```js
const PI = 3.14159
PI = 3    // ❌ TypeError: Assignment to constant variable.
```

`const` evita **reasignar** la variable — no significa que el valor sea inmutable:

```js
const product = { name: 'Mouse', price: 18000 }
product.price = 15000    // ✅ funciona — el objeto se puede mutar
product = {}               // ❌ TypeError — esto sí es una reasignación
```

Mismo tema que se vio en inmutabilidad (Unidad JS Funcional): `const` protege la variable, no el valor. Para eso hace falta `Object.freeze` o construir copias nuevas (spread), no alcanza con `const`.

### Scope de bloque

```js
if (true) {
  var a = 1
  let b = 2
}

console.log(a)   // => 1  (var "se escapó" del if)
console.log(b)   // ❌ ReferenceError: b is not defined
```

`var` solo respeta los límites de una **función** — a un `if`, un `for` o un `{}` suelto los atraviesa sin problema. `let` y `const` respetan cualquier bloque `{}`, que es el comportamiento que casi siempre se espera y evita bugs sutiles (por ejemplo, closures dentro de un `for` que capturan la variable equivocada — un problema clásico de `var` que `let` resuelve solo).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí un `for` clásico (`for (var i = 0; ...)`) que guarde 3 funciones en un array, cada una debería imprimir su propio `i` al ejecutarse. Ejecutalas y observá qué imprime cada una. Repetí el mismo `for` cambiando `var` por `let` y compará el resultado — investigá por qué cambia.
</div>

### Arrow functions

```js
// ES5
const double = function (x) {
  return x * 2
}

// ES6
const double = (x) => {
  return x * 2
}
```

Misma función, sintaxis más corta. Con una sola expresión en el cuerpo, se pueden omitir `return` y las llaves:

```js
const double = x => x * 2               // un solo parámetro: paréntesis opcionales
const add = (a, b) => a + b              // varios parámetros: paréntesis obligatorios
const greet = () => 'Hola!'               // sin parámetros: paréntesis obligatorios
```

La diferencia real entre una arrow function y una función tradicional no es solo lo corta que queda — está en cómo cada una maneja `this`.

### Arrow functions y el `this` léxico

```js
function Person(name) {
  this.name = name
  setTimeout(function () {
    console.log(this.name)   // undefined — "this" acá NO es el Person
  }, 100)
}
```

```js
function Person(name) {
  this.name = name
  setTimeout(() => {
    console.log(this.name)   // "Ada" — la arrow "hereda" el this de Person
  }, 100)
}
```

Una función tradicional define su propio `this` **según quién la invoca** — en este ejemplo, quien invoca el callback es `setTimeout`, no el objeto `Person`, así que `this` dentro de esa función no apunta a la instancia. Una arrow function no tiene `this` propio: usa el del contexto donde fue **escrita** (el `this` de `Person`, en este caso), no el de quien la llama. Esa es la diferencia real entre las dos sintaxis.

Por esta misma razón, una arrow function **no se puede usar como constructor** (`new`) ni tiene su propio `arguments` — depende enteramente del contexto que la rodea.

<div class="card-grid card-grid-2">
<div class="info-card">
<h4>Función tradicional</h4>

Tiene su propio `this` (depende de quién la invoca), se puede usar como constructor, tiene `arguments`.

<div class="card-note">Métodos de objeto, constructores</div>
</div>
<div class="info-card tone-green">
<h4>Arrow function</h4>

No tiene `this` propio — usa el del contexto donde se definió. No se puede usar como constructor. Sintaxis más corta.

<div class="card-note">Callbacks, funciones cortas, closures</div>
</div>
</div>

No una reemplaza a la otra — se elige según el comportamiento que hace falta, no solo por preferencia estética.

### Template literals

```js
const name = 'Ada'
const age = 29

// ES5
const greeting = 'Hola, ' + name + '. Tenés ' + age + ' años.'

// ES6: comillas invertidas (backticks) + interpolación con ${...}
const greetingEs6 = `Hola, ${name}. Tenés ${age} años.`
```

También permiten strings multilínea sin necesitar `\n`:

```js
const message = `Línea 1
Línea 2
Línea 3`
```

Dentro de las llaves de la interpolación va cualquier expresión válida de JS, no solo una variable — `` `${price * 1.21}` `` funciona igual que `${name}`.

### Parámetros por defecto

```js
// ES5: el patrón manual
function greet(name) {
  name = name || 'invitado'
  return `Hola, ${name}!`
}

// ES6: valor por defecto en la propia firma
function greet(name = 'invitado') {
  return `Hola, ${name}!`
}

greet()          // => "Hola, invitado!"
greet('Ada')      // => "Hola, Ada!"
```

El valor por defecto se usa solo cuando el argumento es `undefined` — pasar `null` explícitamente no lo activa (a diferencia del patrón `name || 'invitado'` de ES5, que también se activaba con cualquier valor "falsy": `0`, `''`, `false`).

### Rest y spread en funciones

```js
// rest: junta el resto de los argumentos en un array
function sum(first, ...rest) {
  return rest.reduce((total, n) => total + n, first)
}
sum(1, 2, 3, 4)   // => 10

// spread: "desparrama" un array como argumentos individuales
const numbers = [1, 2, 3, 4]
sum(...numbers)   // equivalente a sum(1, 2, 3, 4)
```

Mismos tres puntos (`...`), significado opuesto según el lugar: **rest** agrupa (en una definición de función), **spread** desparrama (en una llamada o dentro de un literal de array/objeto — como ya se vio en copias inmutables, `[...arr, x]` y `{ ...obj, k: v }`).

### Destructuring de arrays

```js
const colors = ['rojo', 'verde', 'azul']

// asignación al declarar
const [first, second] = colors
// first => "rojo", second => "verde"

// ignorar valores con una coma vacía
const [, , third] = colors   // third => "azul"

// intercambiar variables sin una auxiliar
let a = 1, b = 2
;[a, b] = [b, a]   // a => 2, b => 1

// valores por defecto + resto con spread
const [primary = 'negro', ...others] = colors
```

### Destructuring de objetos

```js
const product = { name: 'Mouse', price: 18000, stock: 5 }

// básica: los nombres deben coincidir con las claves
const { name, price } = product

// renombrar al desestructurar
const { name: productName } = product

// valor por defecto si la clave no existe
const { discount = 0 } = product
```

Al desestructurar objetos **sin** declarar (reasignando variables ya existentes), los paréntesis son obligatorios — si no, el motor interpreta `{ ... }` como el inicio de un bloque de código, no de un objeto:

```js
let name, price
;({ name, price } = product)   // sin los ( ) es un error de sintaxis
```

### Destructuring en parámetros de función

```js
// sin destructuring
function describe(product) {
  return `${product.name} — $${product.price}`
}

// con destructuring directo en la firma
function describe({ name, price }) {
  return `${name} — $${price}`
}

// con valor por defecto
function describe({ name, price = 0 }) {
  return `${name} — $${price}`
}
```

Muy común en componentes de React (`function Card({ title, image })`) — se va a ver en detalle más adelante en la unidad.

<div class="practice-box">
<p class="practice-label">Practicá</p>

A partir de `const person = { name: 'Ada', age: 29, address: { city: 'Londres' } }`, escribí una desestructuración que extraiga `name` y renombre `age` a `edad`, con un valor por defecto de `0` para una propiedad `country` que no existe. Después escribí una función `describePerson` que reciba un objeto así desestructurado directamente en su firma.
</div>

## Arrays: lo esencial

Estos métodos son parte de la sintaxis moderna del lenguaje — a diferencia de `map`/`filter`/`reduce` (ya vistos a fondo en la unidad anterior desde una mirada funcional), acá el eje es simplemente conocer la API disponible y, sobre todo, saber cuáles mutan el array original y cuáles no.

### Crear y modificar un array

```js
const cart = ['teclado', 'mouse']

cart.push('monitor')       // agrega al final     => ['teclado','mouse','monitor']
cart.unshift('funda')      // agrega al principio => ['funda', ...]

cart.pop()                 // quita el último y lo devuelve
cart.shift()                // quita el primero y lo devuelve

cart.splice(1, 0, 'pad')   // en el índice 1, borra 0 y agrega 'pad'
cart.splice(1, 1)          // en el índice 1, borra 1 elemento
```

Todos estos métodos **mutan** el array original — algo a tener en cuenta después de todo lo que se vio sobre inmutabilidad en la unidad anterior.

### Derivar sin mutar vs. mutar

<div class="card-grid card-grid-2">
<div class="info-card tone-green">
<h4>No mutan — devuelven un array nuevo</h4>

```js
cart.slice(0, 2)      // sub-array
cart.concat(['pad'])  // concatena
cart.flat()            // aplana
```
</div>
<div class="info-card tone-red">
<h4>Mutan — devuelven el mismo array</h4>

```js
cart.sort()
cart.reverse()
cart.fill('x', 0, 2)
```
</div>
</div>

Antes de usar cualquier método de array, vale la pena chequear en [MDN](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array) si muta o no — no siempre es intuitivo por el nombre (`slice` no muta, `splice` sí, y se confunden fácil).

### `sort` y su gotcha con números

```js
const numbers = [10, 2, 33, 4]
numbers.sort()
// => [10, 2, 33, 4]  ¡mal ordenado!
```

Por defecto, `sort` convierte cada elemento a **string** y ordena alfabéticamente — por eso `"10"` queda antes que `"2"`. La solución es pasarle una función comparadora:

```js
numbers.sort((a, b) => a - b)
// => [2, 4, 10, 33]  — negativo: a va antes; positivo: b va antes
```

La misma idea sirve para criterios más complejos, como ordenar objetos por más de un campo:

```js
const people = [
  { name: 'Beto', age: 30 },
  { name: 'Ana', age: 25 },
  { name: 'Ana', age: 40 },
]
people.sort((p1, p2) => p1.name.localeCompare(p2.name) || p2.age - p1.age)
// ordena por nombre asc, y a igual nombre, por edad desc
```

### Buscar en un array

```js
const cart = ['teclado', 'mouse', 'monitor']

cart.includes('mouse')     // => true  (¿está el valor?)
cart.indexOf('monitor')    // => 2     (¿en qué posición?)
cart.indexOf('webcam')     // => -1    (no está)
```

Para arrays de objetos, `includes`/`indexOf` no sirven (comparan por referencia, no por contenido) — para eso están `find` y `findIndex`, que reciben un predicado igual que `filter`:

```js
const products = [{ id: 1, name: 'Mouse' }, { id: 2, name: 'Teclado' }]

products.find(p => p.id === 2)        // => { id: 2, name: 'Teclado' }
products.findIndex(p => p.id === 2)   // => 1
```

<div class="practice-box">
<p class="practice-label">Practicá</p>

Con `const cart = ['teclado', 'mouse']`, escribí paso a paso: agregá `'monitor'` al final, agregá `'funda'` al principio, y después ordená el array alfabéticamente con `sort` — sin pasarle ninguna función comparadora, para confirmar que con strings sí funciona bien por defecto (a diferencia del caso de los números).
</div>

### Recorrer y comprobar: `forEach`, `some`, `every`

```js
const cart = ['teclado', 'mouse', 'monitor']

cart.forEach(item => console.log(item))
// ejecuta la función por cada item, no devuelve nada (undefined)
```

A diferencia de `map` — visto a fondo en JS Funcional — `forEach` no arma un array nuevo: es la versión "impura" del recorrido, pensada para cuando el objetivo es un efecto (loggear, guardar en una base de datos, actualizar el DOM) y no transformar datos. Si en algún punto se termina usando `forEach` para construir un array nuevo empujando valores a mano, casi siempre conviene un `map` o un `filter` en su lugar.

`some` y `every` reciben un predicado, igual que `filter` y `find`, pero en vez de un array o un elemento devuelven un `boolean`:

```js
const prices = [800, 1200, 450]

prices.some(p => p > 1000)    // => true   (¿alguno cumple la condición?)
prices.every(p => p > 1000)   // => false  (¿todos cumplen la condición?)
```

### Crear y combinar arrays

```js
Array.from({ length: 3 }, (_, i) => i * 2)   // => [0, 2, 4]
Array.from('abc')                              // => ['a', 'b', 'c']

Array.isArray(cart)     // => true
Array.isArray('cart')   // => false
```

`Array.from` construye un array a partir de algo iterable o "array-like" (un string, un `Set`, el resultado de `document.querySelectorAll`), con una función mapeadora opcional como segundo argumento. `Array.isArray` es la forma correcta de chequear si algo es un array — `typeof` no sirve, porque `typeof []` da `'object'`.

Para copiar o combinar arrays sin mutar, spread como literal:

```js
const copy = [...cart]                // copia superficial
const merged = [...cart, 'funda']     // combina agregando un elemento

const nested = [[1, 2], [3, [4, 5]]]
nested.flatMap(x => x)   // como map + flat(1) en un solo paso => [1, 2, 3, [4, 5]]
```

<div class="practice-box">
<p class="practice-label">Practicá</p>

Con `const prices = [1200, 800, 1500, 950]`, usá `every` para chequear si todos los precios superan los `500`, y `some` para chequear si alguno supera los `1400`. Después escribí la misma lógica con un `for` tradicional y compará: ¿cuál versión comunica mejor la intención?
</div>

## Optional chaining `?.`

```js
const user = { profile: { address: { city: 'Buenos Aires' } } }

// antes de ES2020: había que chequear cada nivel
const city = user
  && user.profile
  && user.profile.address
  && user.profile.address.city

// con optional chaining
const city = user?.profile?.address?.city
```

Si algún eslabón de la cadena es `null` o `undefined`, la expresión completa devuelve `undefined` en vez de tirar `TypeError`. También funciona llamando métodos que podrían no existir:

```js
user.profile.onSave?.()   // llama a onSave solo si existe
```

## Nullish coalescing `??`

```js
function getDiscount(rate) {
  return rate ?? 0.1   // usa 0.1 solo si rate es null o undefined
}

getDiscount(0)      // => 0     — ¡0 es un valor válido, se respeta!
getDiscount(null)   // => 0.1
```

| Valor de `rate` | `rate \|\| 0.1` | `rate ?? 0.1` |
|---|---|---|
| `0` | `0.1` ⚠️ | `0` ✅ |
| `''` | `0.1` ⚠️ | `''` ✅ |
| `false` | `0.1` ⚠️ | `false` ✅ |
| `null` / `undefined` | `0.1` | `0.1` |

`||` reemplaza **cualquier** valor "falsy" (`0`, `''`, `false`, `NaN`...). `??` solo reemplaza `null`/`undefined` — por eso es la opción correcta para valores por defecto que legítimamente pueden ser `0`, string vacío o `false`.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Con `const config = { timeout: 0, retries: null }`, escribí `const finalTimeout = config.timeout ?? 5000` y `const finalTimeoutMal = config.timeout || 5000`, comparalos, y explicá con tus palabras por qué dan resultados distintos. Repetí con `config.retries`.
</div>

## `==` vs. `===`

```js
0 == '0'      // => true   — compara con coerción de tipos
0 === '0'     // => false  — compara tipo y valor, sin convertir nada

null == undefined     // => true
null === undefined    // => false

'' == false    // => true   — ambos "falsy", coercionan igual
```

`==` convierte los operandos a un tipo común antes de comparar — las reglas de esa conversión no siempre son intuitivas (son parte de las rarezas heredadas del diseño apurado del lenguaje, mencionadas al principio de este apunte). La convención moderna es usar **siempre `===`** (y `!==`), salvo el caso puntual de comparar contra `null`/`undefined` a la vez, donde `== null` es un atajo aceptado por muchos equipos.

## Módulos y ecosistema

### Módulos: ES Modules vs. CommonJS

<div class="card-grid card-grid-2">
<div class="info-card">
<h4>CommonJS — el original de Node</h4>

```js
// math.js
function add(a, b) { return a + b }
module.exports = { add }

// app.js
const { add } = require('./math')
```
</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
<h4>ES Modules — estándar del lenguaje (ES6)</h4>

```js
// math.js
export function add(a, b) {
  return a + b
}

// app.js
import { add } from './math.js'
```
</div>
</div>

CommonJS es específico de Node; ES Modules es parte del lenguaje y también corre en el navegador (`<script type="module">`). Node soporta los dos — cuál se usa depende de la configuración del proyecto (`"type": "module"` en `package.json`, o extensión `.mjs`). Los proyectos nuevos suelen preferir ES Modules por ser el estándar, pero es común encontrar código CommonJS en proyectos Node más viejos o en muchas librerías.

### Node.js y npm

- **Node.js**: el motor V8 de Chrome, empaquetado para correr JavaScript fuera del navegador — así JS se convierte en un lenguaje de servidor, no solo de scripting en el browser.
- **npm**: el gestor de paquetes que viene con Node — instala, versiona y comparte librerías (es el registro de paquetes más grande que existe, en cualquier lenguaje).
- **`package.json`**: describe un proyecto — nombre, versión, dependencias, scripts ejecutables.
- **`node_modules/`**: la carpeta donde npm instala las dependencias — ya se vivió instalando Slidev y VitePress para el material de esta materia.

```bash
node -v                  # ver la versión de Node instalada, ej. v22.14.0
npm -v                   # ver la versión de npm instalada

npm init -y             # crea un package.json
npm install express       # instala una dependencia y la agrega al package.json
npm run <script>          # corre un script definido en package.json
```

Vale la pena correr `node -v` al menos una vez y confirmar la versión instalada — no todos los motores soportan todavía las features más nuevas de la cronología vista al principio de este apunte. Por ejemplo, los métodos `toSorted()`/`with()` de 2023 recién funcionan desde Node 20 en adelante.

## Cheat sheet

<div class="card-grid card-grid-2">
<div>

**Sintaxis ES6+**

| Feature | Ejemplo |
|---|---|
| Variables | `let`, `const` (no `var`) |
| Arrow function | `(a, b) => a + b` |
| Template literal | `` `Hola ${name}` `` |
| Destructuring | `const { a, b } = obj` |
| Spread / rest | `[...arr]`, `function f(...args)` |
| Módulos | `export`/`import { x } from './f.js'` |

</div>
<div>

**Operadores nuevos**

| Operador | Qué hace |
|---|---|
| `?.` | Encadenamiento opcional |
| `??` | Valor por defecto (solo null/undefined) |
| `**` | Exponenciación |
| `===` | Igualdad estricta (preferida sobre `==`) |
| `??=` `\|\|=` `&&=` | Asignación lógica (ES2021) |

</div>
</div>

<div class="card-grid card-grid-2">
<div>

**Arrays — métodos más usados**

| Método | Qué hace |
|---|---|
| `map` `filter` `reduce` | Transformar (JS Funcional) |
| `find` `findIndex` | Buscar por predicado |
| `some` `every` | ¿Alguno / todos cumplen? |
| `forEach` | Recorrer con un efecto |
| `push` `pop` `splice` | Mutan el array |
| `slice` `concat` `flat` | No mutan — copia nueva |

</div>
<div>

**Node y npm**

| Comando | Qué hace |
|---|---|
| `node -v` / `npm -v` | Ver versiones instaladas |
| `npm init -y` | Crea un `package.json` |
| `npm install <pkg>` | Instala una dependencia |
| `npm run <script>` | Corre un script del proyecto |
| `require()` / `import` | CommonJS / ES Modules |

</div>
</div>

## Referencias y recursos

- [es.javascript.info](https://es.javascript.info/) — tutorial moderno de JS, completo y en español
- [developer.mozilla.org — JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript) — referencia oficial del lenguaje
- [developer.mozilla.org — Array](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array) — referencia completa de métodos de arrays
- [TC39 proposals](https://github.com/tc39/proposals) — el proceso real de evolución del lenguaje, para quien quiera ver qué viene después
- [node.js](https://nodejs.org/es) — documentación oficial de Node.js

## Cierre

El objetivo de este tema es tener el vocabulario sintáctico moderno resuelto — `let`/`const`, arrow functions, destructuring, spread/rest, módulos — para poder concentrarse en los conceptos nuevos del resto de la unidad (asincronismo, TypeScript, React, Node + Express) sin tropezar todavía con la sintaxis. Todo el código que se escriba de acá en adelante en la materia asume este apunte como base.
