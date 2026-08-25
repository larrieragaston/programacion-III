---
theme: bricks
title: Programación III - JS Contemporáneo
download: true
info: |
  JS Contemporáneo - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: javascript, es6, ecmascript, node, npm, INSPT, UTN
transition: slide-left
mdc: true
---

# JS Contemporáneo

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/javascript.svg" alt="JavaScript" class="h-16 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# Características de JavaScript

- **Interpretado**: no se compila a un binario antes de correr — un motor (V8, SpiderMonkey…) lo ejecuta directamente.
- **Multiparadigma**: imperativo, orientado a objetos, funcional — el funcional lo vimos a fondo en JS Funcional.
- **Tipado dinámico**: el tipo de una variable se determina en tiempo de ejecución, no hay que declararlo.
- **El único lenguaje que corre nativamente en el navegador** — y con Node.js, también en el servidor.

<div class="mt-6 text-sm italic opacity-80">

Multiparadigma y tipado dinámico no son casualidad — son parte de por qué JS es como es, que vemos a continuación.

</div>

---
layout: default
---

# El origen de JavaScript

<div class="flex gap-6 items-start mt-2">
<div class="flex-1">

- 1995 — Netscape necesita un lenguaje de scripting liviano para su navegador, para competir con los applets de Java de Sun Microsystems.
- **Brendan Eich** lo diseña en **10 días**, en mayo de 1995.
- Se lanza como **Mocha**, se renombra a **LiveScript**, y termina llamándose **JavaScript** — una decisión de marketing de último momento para subirse a la popularidad de Java, aunque los dos lenguajes no tienen relación técnica real.

<div class="mt-6 text-sm italic opacity-80">

Diseñado en una semana y media para un caso de uso chico (validar formularios en un `<form>`), terminó siendo el lenguaje más usado del mundo — varias de sus rarezas de sintaxis vienen de esa urgencia inicial.

</div>

</div>
<div class="shrink-0 text-center">
<img src="/people/brendan-eich.jpg" alt="Brendan Eich" class="w-36 rounded-lg shadow" />
<div class="mt-1 text-xs opacity-50">Brendan Eich, 2012</div>
</div>
</div>

---
layout: default
---

# Cronología de ECMAScript

<div class="relative mt-14 mx-2" style="height:100px">
<div class="absolute left-0 right-0 border-t-2 border-gray-300" style="top: 32px"></div>

<div class="absolute flex flex-col items-center text-center" style="left:2.0%; transform:translateX(-50%); width:44px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES1</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1.5 leading-tight">1997</div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:9.4%; transform:translateX(-50%); width:44px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES3</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1.5 leading-tight">1999</div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:16.8%; transform:translateX(-50%); width:44px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES5</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1.5 leading-tight">2009</div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:24.2%; transform:translateX(-50%); width:48px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none" style="color:#78350f">ES6</div></div>
<div class="w-3 h-3 rounded-full border-2 border-black mt-1.5" style="background:#facc15"></div>
<div class="text-[9px] opacity-60 mt-1.5 leading-tight">2015</div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:31.5%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2016</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:38.9%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2017</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:46.3%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2018</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:53.7%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2019</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:61.1%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2020</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:68.5%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2021</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:75.8%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2022</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:83.2%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2023</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:90.6%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2024</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

<div class="absolute flex flex-col items-center text-center" style="left:98.0%; transform:translateX(-50%); width:52px">
<div class="h-5 flex items-end justify-center"><div class="text-[9px] font-mono font-bold leading-none">ES2025</div></div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1.5" style="background:#22c55e"></div>
</div>

</div>

<div class="flex justify-center gap-5 mt-6 text-xs flex-wrap">
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#9ca3af"></span> ediciones tempranas</div>
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full border border-black" style="background:#facc15"></span> ES6 — el salto grande</div>
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#22c55e"></span> cadencia anual</div>
</div>

<div class="mt-3 text-xs italic opacity-70 text-center">

Desde **ES6 (2015)**, el comité TC39 saca una revisión **por año**, cada junio — por eso se nombran por año (<code>ES2016</code>, <code>ES2020</code>, <code>ES2024</code>) en vez de por número secuencial (<code>ES7</code>, <code>ES11</code>). La última confirmada es **ES2025**; para cuando se dicte esta clase, es probable que ya exista una <code>ES2026</code>.

</div>

---
layout: default
---

# ES1 → ES6: los grandes saltos

<div class="grid grid-cols-2 gap-2 mt-3 text-xs">
<div class="p-2 rounded-lg bg-gray-100">

**ES1 — 1997**

Primera edición estandarizada. JS ya se podía escribir en un navegador, pero sin estándar formal todavía.
</div>
<div class="p-2 rounded-lg bg-gray-100">

**ES3 — 1999**

Expresiones regulares, `try`/`catch`, `switch`, `do...while`. La base "clásica" de JS durante más de una década.
</div>
<div class="p-2 rounded-lg bg-gray-100">

**ES5 — 2009**

`"use strict"`, `JSON` nativo, y las funciones de orden superior de arrays: `forEach`, `map`, `filter`, `reduce` (ya las vimos en la unidad anterior).
</div>
<div class="p-2 rounded-lg bg-yellow-50 border-2 border-yellow-400">

**ES6 / ES2015 — 2015**

El salto grande: `let`/`const`, arrow functions, clases, módulos, Promesas, template literals, destructuring… la base de todo el JS que se escribe hoy.
</div>
</div>

<div class="mt-2 text-xs italic opacity-80 text-center">

Después de ES6 no hubo otro salto de esa magnitud — desde 2016, cada año suma funcionalidades puntuales sobre esa misma base, sin cambiar la sintaxis de fondo.

</div>

---
layout: center
---

# Cadencia anual (2016 en adelante)

---
layout: default
---

# Lo más relevante, año a año

<div class="grid grid-cols-5 gap-1.5 mt-3 text-[11px] leading-snug">
<div class="p-1.5 rounded-lg bg-gray-100">

**2016**

`2 ** 10` en vez de `Math.pow(2, 10)`
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2017**

`async`/`await` — se ve en Asincronismo
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2018**

Spread/rest en objetos — ya visto en JS Funcional
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2019**

`Array.prototype.flat()` — se ve más adelante en este deck
</div>
<div class="p-1.5 rounded-lg bg-yellow-50 border border-yellow-300">

**2020**

`BigInt`, `?.`, `??` — se ven más adelante
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2021**

`replaceAll()`, `Promise.any()`
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2022**

Campos de clase `#privado`, `Array.at()`, top-level `await`
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2023**

Copias inmutables: `toSorted()`, `toReversed()`, `with()`
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2024**

`Object.groupBy()`, `Promise.withResolvers()`
</div>
<div class="p-1.5 rounded-lg bg-gray-100">

**2025**

Helpers de iteradores, métodos de `Set`
</div>
</div>

<div class="mt-3 text-xs italic opacity-80 text-center">

Desde ES6, casi todo lo nuevo cabe en una oración. La última edición confirmada es <strong>ES2025</strong>; TC39 publica una revisión cada junio.

</div>

---
layout: center
---

# El salto grande: ES6 (2015)

---
layout: default
---

# Declarar variables: `let` vs `var`

```js
var name = 'Ada'
let name = 'Ada'    // mismo resultado, distinto comportamiento
```

<v-click>

- `var` tiene **scope de función** (o global) — ignora los bloques (`if`, `for`, `{}`).
- `let` tiene **scope de bloque** — solo existe dentro del `{}` donde se declaró.
- `var` sufre *hoisting* "raro": la declaración se sube al principio de la función, pero queda `undefined` hasta la línea donde se asigna. `let` también se sube, pero queda en una zona inaccesible (*temporal dead zone*) hasta esa línea — usarla antes tira error, no `undefined`.
- Redeclarar la misma variable con `var` no tira error. Con `let`, sí.

</v-click>

<v-click>

<div class="mt-4 text-sm italic opacity-80">

Hoy `var` prácticamente no se usa en código nuevo — quedó por compatibilidad con proyectos viejos.

</div>

</v-click>

---
layout: default
---

# `const` y sus límites

```js
const PI = 3.14159
PI = 3    // ❌ TypeError: Assignment to constant variable.
```

<v-click>

`const` evita **reasignar** la variable — no significa que el valor sea inmutable:

```js
const product = { name: 'Mouse', price: 18000 }
product.price = 15000    // ✅ funciona — el objeto se puede mutar
product = {}              // ❌ TypeError — esto sí es una reasignación
```

</v-click>

<v-click>

<div class="mt-4 text-sm opacity-80">

Mismo tema que vimos en inmutabilidad: `const` protege la variable, no el valor. Para eso hace falta `Object.freeze` o construir copias nuevas (spread), no alcanza con `const`.

</div>

</v-click>

---
layout: default
---

# Scope de bloque

```js
if (true) {
  var a = 1
  let b = 2
}

console.log(a)   // => 1  (var "se escapó" del if)
console.log(b)   // ❌ ReferenceError: b is not defined
```

<div class="mt-4 text-sm opacity-80">

`var` solo respeta los límites de una **función** — a un `if`, un `for` o un `{}` suelto los atraviesa sin problema. `let` y `const` respetan cualquier bloque `{}`, que es el comportamiento que casi siempre se espera.

</div>

<v-click>

```js
function scopeDeFuncion() {
  var c = 3
}
console.log(c)   // ❌ ReferenceError — acá sí respeta el límite de función
```

</v-click>

---
layout: default
---

# Arrow functions: sintaxis

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

<div class="mt-4 text-sm opacity-80">

Misma función, sintaxis más corta. La diferencia real no es solo estética — se ve en la próxima slide con <code>this</code>.

</div>

---
layout: default
---

# Arrow functions: variantes

```js
// una sola expresión: se puede omitir "return" y las llaves
const double = x => x * 2

// un solo parámetro: los paréntesis son opcionales
const double = x => x * 2
const doubleExplicit = (x) => x * 2   // también válido

// sin parámetros: los paréntesis son obligatorios
const greet = () => 'Hola!'

// varios parámetros: los paréntesis son obligatorios
const add = (a, b) => a + b
```

<div class="mt-4 text-sm opacity-80">

Todas estas formas conviven — cuál usar es una cuestión de estilo del equipo, no una regla del lenguaje.

</div>

---
layout: default
---

# Arrow functions y el `this` léxico

```js
function Person(name) {
  this.name = name
  setTimeout(function () {
    console.log(this.name)   // undefined — "this" acá NO es el Person
  }, 100)
}
```

<v-click>

```js
function Person(name) {
  this.name = name
  setTimeout(() => {
    console.log(this.name)   // "Ada" — la arrow "hereda" el this de Person
  }, 100)
}
```

</v-click>

<v-click>

<div class="mt-4 text-sm opacity-80">

Una función tradicional define su propio `this` **según quién la invoca** (`setTimeout`, en este caso — y ahí `this` no es el objeto). Una arrow function no tiene `this` propio: usa el del contexto donde fue **escrita**, no el de quien la llama. Esa es la diferencia real entre las dos sintaxis, no solo lo corta que queda el código.

</div>

</v-click>

---
layout: default
---

# Funciones tradicionales vs. arrow

<div class="grid grid-cols-2 gap-6 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100">

**Función tradicional**

- Tiene su propio `this` (depende de quién la invoca)
- Se puede usar como constructor (`new`)
- Tiene `arguments`

<div class="mt-2 text-xs opacity-70">Métodos de objeto, constructores</div>
</div>
<div class="p-4 rounded-lg bg-yellow-50 border border-yellow-300">

**Arrow function**

- No tiene `this` propio — usa el del contexto donde se definió
- No se puede usar como constructor
- Sintaxis más corta

<div class="mt-2 text-xs opacity-70">Callbacks, funciones cortas, closures</div>
</div>
</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

No una reemplaza a la otra — se elige según el comportamiento que hace falta.

</div>

---
layout: default
---

# Template literals

```js
const name = 'Ada'
const age = 29

// ES5
const greeting = 'Hola, ' + name + '. Tenés ' + age + ' años.'

// ES6: comillas invertidas (backticks) + interpolación con ${}
const greetingEs6 = `Hola, ${name}. Tenés ${age} años.`
```

<v-click>

```js
// multilínea, sin necesitar \n
const message = `Línea 1
Línea 2
Línea 3`
```

</v-click>

<v-click>

<div class="mt-4 text-sm opacity-80">

Dentro de las llaves de la interpolación va cualquier expresión válida de JS, no solo una variable — `` `${price * 1.21}` `` funciona igual.

</div>

</v-click>

---
layout: default
---

# Parámetros por defecto

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

<div class="mt-4 text-sm opacity-80">

El valor por defecto se usa solo cuando el argumento es <code>undefined</code> — pasar <code>null</code> explícitamente no lo activa.

</div>

---
layout: default
---

# Rest y spread en funciones

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

<div class="mt-4 text-sm opacity-80">

Mismos tres puntos (<code>...</code>), significado opuesto según el lugar: **rest** agrupa (en una definición), **spread** desparrama (en una llamada o un literal).

</div>

---
layout: default
---

# Destructuring de arrays

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

---
layout: default
---

# Destructuring de objetos

```js
const product = { name: 'Mouse', price: 18000, stock: 5 }

// básica: los nombres deben coincidir con las claves
const { name, price } = product

// renombrar al desestructurar
const { name: productName } = product

// valor por defecto si la clave no existe
const { discount = 0 } = product
```

<v-click>

<div class="mt-4 text-sm opacity-80">

Al desestructurar objetos <strong>sin</strong> declarar (reasignando variables ya existentes), los paréntesis son obligatorios:

</div>

```js
let name, price
;({ name, price } = product)   // sin los ( ) es un error de sintaxis
```

</v-click>

---
layout: default
---

# Destructuring en parámetros de función

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

<div class="mt-4 text-sm opacity-80">

Muy común en componentes de React (`function Card({ title, image })`) — ya lo vamos a ver en el resto de la unidad.

</div>

---
layout: center
---

# Arrays: lo esencial

---
layout: default
---

# Crear y modificar un array

```js
const cart = ['teclado', 'mouse']

cart.push('monitor')       // agrega al final    => ['teclado','mouse','monitor']
cart.unshift('funda')      // agrega al principio => ['funda',...]

cart.pop()                 // quita el último y lo devuelve
cart.shift()                // quita el primero y lo devuelve

cart.splice(1, 0, 'pad')   // en el índice 1, borra 0 y agrega 'pad'
cart.splice(1, 1)          // en el índice 1, borra 1 elemento
```

<div class="mt-4 text-sm italic opacity-80">

Todos estos métodos **mutan** el array original — algo a tener en cuenta después de todo lo que vimos sobre inmutabilidad.

</div>

---
layout: default
---

# Derivar sin mutar vs. mutar

<div class="grid grid-cols-2 gap-6 mt-6 text-sm">
<div class="p-4 rounded-lg bg-green-50 border border-green-200">

**No mutan — devuelven un array nuevo**

```js
cart.slice(0, 2)     // sub-array
cart.concat(['pad'])  // unión
cart.flat()            // aplana anidados
```
</div>
<div class="p-4 rounded-lg bg-red-50 border border-red-200">

**Mutan — devuelven el mismo array**

```js
cart.sort()
cart.reverse()
cart.fill('x', 0, 2)
```
</div>
</div>

<div class="mt-6 text-sm italic opacity-80">

Antes de usar cualquier método de array, vale la pena chequear en <a href="https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array" target="_blank" rel="noopener">MDN</a> si muta o no — no es intuitivo por el nombre.

</div>

---
layout: default
---

# `sort` y su gotcha con números

```js
const numbers = [10, 2, 33, 4]
numbers.sort()
// => [10, 2, 33, 4]  ¡mal ordenado!
```

<div class="mt-4 text-sm opacity-80">

Por defecto, <code>sort</code> convierte cada elemento a **string** y ordena alfabéticamente — por eso <code>"10"</code> queda antes que <code>"2"</code>. La solución es pasarle una función comparadora:

</div>

<v-click>

```js
numbers.sort((a, b) => a - b)
// => [2, 4, 10, 33]  — negativo: a va antes; positivo: b va antes
```

```js
const people = [
  { name: 'Beto', age: 30 },
  { name: 'Ana', age: 25 },
  { name: 'Ana', age: 40 },
]
people.sort((p1, p2) => p1.name.localeCompare(p2.name) || p2.age - p1.age)
// ordena por nombre asc, y a igual nombre, por edad desc
```

</v-click>

---
layout: default
---

# Buscar en un array

```js
const cart = ['teclado', 'mouse', 'monitor']

cart.includes('mouse')     // => true  (¿está el valor?)
cart.indexOf('monitor')    // => 2     (¿en qué posición?)
cart.indexOf('webcam')     // => -1    (no está)
```

<div class="mt-4 text-sm opacity-80">

Para arrays de objetos, <code>includes</code>/<code>indexOf</code> no sirven (comparan por referencia) — para eso están <code>find</code> y <code>findIndex</code>, que reciben un predicado como <code>filter</code>:

</div>

<v-click>

```js
const products = [{ id: 1, name: 'Mouse' }, { id: 2, name: 'Teclado' }]

products.find(p => p.id === 2)        // => { id: 2, name: 'Teclado' }
products.findIndex(p => p.id === 2)   // => 1
```

</v-click>

---
layout: default
---

# Recorrer y comprobar: `forEach`, `some`, `every`

```js
const cart = ['teclado', 'mouse', 'monitor']

cart.forEach(item => console.log(item))
// ejecuta la función por cada item, no devuelve nada (undefined)
```

<div class="mt-4 text-sm opacity-80">

A diferencia de <code>map</code> — que ya vimos en JS Funcional — <code>forEach</code> no arma un array nuevo: es la versión "impura" del recorrido, para cuando el objetivo es un efecto (loggear, guardar) y no transformar datos.

</div>

<v-click>

```js
const prices = [800, 1200, 450]

prices.some(p => p > 1000)    // => true   (¿alguno cumple?)
prices.every(p => p > 1000)   // => false  (¿todos cumplen?)
```

<div class="mt-2 text-sm opacity-80">

Reciben un predicado, igual que <code>filter</code> y <code>find</code> — pero devuelven un <code>boolean</code> en vez de un array o un elemento.

</div>

</v-click>

---
layout: default
---

# Crear y combinar arrays

```js
Array.from({ length: 3 }, (_, i) => i * 2)   // => [0, 2, 4]
Array.from('abc')                              // => ['a', 'b', 'c']

Array.isArray(cart)     // => true
Array.isArray('cart')   // => false
```

<div class="mt-4 text-sm opacity-80">

Para copiar o combinar arrays sin mutar, spread como literal:

</div>

<v-click>

```js
const copy = [...cart]                // copia superficial
const merged = [...cart, 'funda']     // combina agregando un elemento

const nested = [[1, 2], [3, [4, 5]]]
nested.flatMap(x => x)   // como map + flat(1) en un solo paso
```

</v-click>

---
layout: default
---

# Optional chaining `?.`

```js
const user = { profile: { address: { city: 'Buenos Aires' } } }

// antes de ES2020: había que chequear cada nivel
const city = user && user.profile && user.profile.address && user.profile.address.city

// con optional chaining
const city = user?.profile?.address?.city
```

<div class="mt-4 text-sm opacity-80">

Si algún eslabón de la cadena es <code>null</code> o <code>undefined</code>, la expresión completa devuelve <code>undefined</code> en vez de tirar <code>TypeError</code>. También funciona llamando métodos que podrían no existir:

</div>

<v-click>

```js
user.profile.onSave?.()   // llama a onSave solo si existe
```

</v-click>

---
layout: default
---

# Nullish coalescing `??`

```js
function getDiscount(rate) {
  return rate ?? 0.1   // usa 0.1 solo si rate es null o undefined
}

getDiscount(0)      // => 0     — ¡0 es un valor válido, se respeta!
getDiscount(null)   // => 0.1
```

<div class="mt-2 text-xs">

| Valor de `rate` | `rate \|\| 0.1` | `rate ?? 0.1` |
|---|---|---|
| `0` | `0.1` ⚠️ | `0` ✅ |
| `''` | `0.1` ⚠️ | `''` ✅ |
| `false` | `0.1` ⚠️ | `false` ✅ |
| `null` / `undefined` | `0.1` | `0.1` |

</div>

<div class="mt-2 text-xs italic opacity-80">

<code>||</code> reemplaza **cualquier** valor "falsy" (<code>0</code>, <code>''</code>, <code>false</code>...). <code>??</code> solo reemplaza <code>null</code>/<code>undefined</code> — por eso es la opción correcta para valores por defecto.

</div>

---
layout: default
---

# `==` vs `===`

```js
0 == '0'      // => true   — compara con coerción de tipos
0 === '0'     // => false  — compara tipo y valor, sin convertir nada

null == undefined     // => true
null === undefined    // => false

'' == false    // => true   — ambos "falsy", coercionan igual
```

<div class="mt-4 text-sm opacity-80">

<code>==</code> convierte los operandos a un tipo común antes de comparar — las reglas de esa conversión no siempre son intuitivas. La convención moderna es usar <strong>siempre <code>===</code></strong> (y <code>!==</code>), salvo el caso puntual de comparar contra <code>null</code>/<code>undefined</code> a la vez, donde <code>== null</code> es un atajo aceptado.

</div>

---
layout: center
---

# Módulos y ecosistema

---
layout: default
---

# Módulos: ES Modules vs. CommonJS

<div class="grid grid-cols-2 gap-6 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100">

**CommonJS** — el original de Node

```js
// math.js
function add(a, b) { return a + b }
module.exports = { add }

// app.js
const { add } = require('./math')
```
</div>
<div class="p-4 rounded-lg bg-yellow-50 border border-yellow-300">

**ES Modules** — estándar del lenguaje (ES6)

```js
// math.js
export function add(a, b) { return a + b }

// app.js
import { add } from './math.js'
```
</div>
</div>

<div class="mt-6 text-sm italic opacity-80">

CommonJS es específico de Node; ES Modules es parte del lenguaje y también corre en el navegador (<code>&lt;script type="module"&gt;</code>). Node soporta los dos — cuál se usa depende de la configuración del proyecto (<code>"type": "module"</code> en <code>package.json</code>, o extensión <code>.mjs</code>).

</div>

---
layout: default
---

# Node.js y npm

<img src="/logos/node.svg" alt="Node.js" class="abs-tr mt-32 mr-20 h-16 opacity-90" />

<div class="max-w-2xl">

- **Node.js**: el motor V8 de Chrome, empaquetado para correr JavaScript fuera del navegador — así JS se convierte en un lenguaje de servidor.
- **npm**: el gestor de paquetes que viene con Node — instala, versiona y comparte librerías.
- **`package.json`**: describe un proyecto (nombre, dependencias, scripts).
- **`node_modules/`**: donde npm instala las dependencias.

</div>

<div class="mt-3 text-sm opacity-80">

```bash
node -v                  # ver la versión instalada, ej. v22.14.0
npm -v                   # ver la versión de npm
npm init -y              # crea un package.json
npm install express      # instala una dependencia
npm run <script>         # corre un script del proyecto
```

</div>

<div class="mt-1 text-xs italic opacity-80">

Vale la pena correr <code>node -v</code> al menos una vez — no todos los motores soportan aún las features más nuevas de la cronología vista al principio del deck.

</div>

---
layout: default
---

# Cheat sheet: sintaxis y operadores

<div class="grid grid-cols-2 gap-8 mt-4 text-xs">
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

---
layout: default
---

# Cheat sheet: arrays y herramientas

<div class="grid grid-cols-2 gap-8 mt-4 text-xs">
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

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2">

- [es.javascript.info](https://es.javascript.info/) — tutorial moderno de JS, completo y en español
- [developer.mozilla.org — JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript) — referencia oficial del lenguaje
- [developer.mozilla.org — Array](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array) — referencia completa de métodos de arrays
- [TC39 proposals](https://github.com/tc39/proposals) — el proceso real de evolución del lenguaje, para quien quiera ver qué viene después
- [node.js](https://nodejs.org/es) — documentación oficial de Node.js

</div>
