---
theme: bricks
title: Programación III - JS Funcional
download: true
info: |
  JS Funcional - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: javascript, programación funcional, map, filter, reduce, INSPT, UTN
transition: slide-left
mdc: true
---

# JS Funcional

Programación III

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# Paradigmas de programación

<div class="grid grid-cols-2 gap-5 mt-6">
<div class="p-3 rounded-lg bg-blue-50 border border-blue-300">

<div class="text-center font-bold text-blue-900">Imperativos</div>
<div class="text-center text-xs opacity-70 mb-3">énfasis en la ejecución — cómo hacerlo, paso a paso</div>

<div class="grid grid-cols-3 gap-2 text-center text-xs">
<div class="p-2 bg-white rounded border border-gray-300">

**Estructurado**

<div class="mt-1 opacity-70">Basic, Pascal</div>
</div>
<div class="p-2 bg-white rounded border border-gray-300">

**Procedimental**

<img src="/logos/c.svg" class="h-5 mx-auto mt-1" alt="C" />
</div>
<div class="p-2 bg-white rounded border border-gray-300">

**Orientado a objetos**

<div class="flex justify-center gap-1 mt-1"><img src="/logos/cplusplus.svg" class="h-5" alt="C++" /><img src="/logos/python.svg" class="h-5" alt="Python" /></div>
<div class="mt-1 opacity-70">Java, C++, Python</div>
</div>
</div>
</div>

<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-400">

<div class="text-center font-bold text-yellow-900">Declarativos</div>
<div class="text-center text-xs opacity-70 mb-3">énfasis en la evaluación — qué se quiere obtener</div>

<div class="grid grid-cols-2 gap-2 text-center text-xs">
<div class="p-2 bg-white rounded border-2 border-yellow-400">

**Funcional**

<div class="flex justify-center gap-1 mt-1"><img src="/logos/haskell.svg" class="h-5" alt="Haskell" /><img src="/logos/clojure.svg" class="h-5" alt="Clojure" /><img src="/logos/javascript.svg" class="h-5" alt="JavaScript" /></div>
<div class="mt-1 opacity-70">Haskell, Clojure, JS*</div>
</div>
<div class="p-2 bg-white rounded border border-gray-300">

**Lógico**

<div class="mt-1 opacity-70">Prolog</div>
</div>
</div>
</div>
</div>

<div class="mt-4 text-xs italic opacity-70 text-center">

*JS no nace funcional — es multiparadigma, y permite ese estilo. Los lenguajes más usados hoy en día lo son: cada quien elige el estilo más adecuado para cada tarea.

</div>

---
layout: default
---

# Imperativo vs. declarativo

<div class="grid grid-cols-2 gap-6 mt-4 text-sm">
<div class="p-4 rounded-lg bg-gray-100">

**Imperativo** — cómo hacerlo, paso a paso

```js
const names = []
for (let i = 0; i < products.length; i++) {
  if (products[i].stock > 0) {
    names.push(products[i].name)
  }
}
```

</div>
<div class="p-4 rounded-lg bg-green-50 border border-green-200">

**Declarativo** — qué se quiere obtener

```js
const names = products
  .filter(p => p.stock > 0)
  .map(p => p.name)
```

</div>
</div>

<div class="mt-4 text-sm italic opacity-80">

La programación funcional es un estilo **declarativo**: se describe el resultado que se quiere, no la secuencia de pasos para construirlo.

</div>

---
layout: default
---

# ¿Qué es la programación funcional?

<div class="grid grid-cols-2 gap-8 mt-8 items-center">
<div class="text-sm">

- Evaluación de **funciones matemáticas**
- ~~Cambios de estado~~
- ~~Mutaciones de datos~~
- Se rige por **principios**, no por una secuencia de instrucciones

</div>
<div class="p-4 rounded-lg bg-gray-100 text-sm">

```js
const area = r => r ** 2 * Math.PI
```

</div>
</div>

<div class="mt-8 text-sm italic opacity-80">

Se define casi tanto por lo que **evita** (estado, mutación) como por lo que hace.

</div>

---
layout: default
---

# Breve cronología

<div class="relative mt-16 mx-2">
<div class="absolute left-0 right-0 border-t-2 border-gray-300" style="top: 42px"></div>
<div class="relative flex justify-between items-start">

<div class="flex flex-col items-center text-center" style="width:52px">
<div class="text-[9px] font-mono font-bold leading-tight text-violet-700">λ-calc</div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#7c3aed"></div>
<div class="text-[9px] opacity-60 mt-1">1936</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<div class="text-[9px] font-mono font-bold leading-tight text-green-700">Lisp</div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#22c55e"></div>
<div class="text-[9px] opacity-60 mt-1">1958</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<img src="/logos/c.svg" class="h-4" alt="C" />
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1">1972</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<div class="text-[9px] font-mono font-bold leading-tight text-green-700">ML</div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#22c55e"></div>
<div class="text-[9px] opacity-60 mt-1">1973</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<div class="text-[9px] font-mono font-bold leading-tight text-green-700">Scheme</div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#22c55e"></div>
<div class="text-[9px] opacity-60 mt-1">1975</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<div class="text-[9px] font-mono font-bold leading-tight">Smalltalk</div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1">1980</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<img src="/logos/cplusplus.svg" class="h-4" alt="C++" />
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1">1983</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<img src="/logos/erlang.svg" class="h-4" alt="Erlang" />
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#22c55e"></div>
<div class="text-[9px] opacity-60 mt-1">1986</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<img src="/logos/haskell.svg" class="h-4" alt="Haskell" />
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#22c55e"></div>
<div class="text-[9px] opacity-60 mt-1">1990</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<img src="/logos/python.svg" class="h-4" alt="Python" />
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1">1991</div>
</div>

<div class="flex flex-col items-center text-center" style="width:56px">
<img src="/logos/javascript.svg" class="h-4" alt="JS" />
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#facc15"></div>
<div class="text-[9px] opacity-60 mt-1">JS nace<br>1995</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<div class="text-[9px] font-mono font-bold leading-tight">Java</div>
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#9ca3af"></div>
<div class="text-[9px] opacity-60 mt-1">1995</div>
</div>

<div class="flex flex-col items-center text-center" style="width:52px">
<img src="/logos/clojure.svg" class="h-4" alt="Clojure" />
<div class="w-3 h-3 rounded-full border-2 border-white mt-1" style="background:#22c55e"></div>
<div class="text-[9px] opacity-60 mt-1">2007</div>
</div>

<div class="flex flex-col items-center text-center" style="width:56px">
<img src="/logos/javascript.svg" class="h-4" alt="JS ES6" />
<div class="w-3 h-3 rounded-full border-2 border-black mt-1" style="background:#facc15"></div>
<div class="text-[9px] opacity-60 mt-1">ES6<br>2015</div>
</div>

</div>
</div>

<div class="flex justify-center gap-5 mt-6 text-xs flex-wrap">
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#7c3aed"></span> sistema formal, no un lenguaje</div>
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#22c55e"></span> linaje funcional</div>
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#9ca3af"></span> imperativo / POO</div>
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full border border-black" style="background:#facc15"></span> JS</div>
</div>

<div class="mt-3 text-xs italic opacity-70 text-center">

JS nace en 1995 — recién 20 años después, con **ES6 (2015)**, incorpora herramientas de estilo funcional: arrow functions, `const`, spread…

</div>

---
layout: default
---

# Mismo paradigma, tres lenguajes

<div class="grid grid-cols-3 gap-4 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100">

**Cálculo Lambda**

- El origen formal: todo es una función
- Sin estado, sin mutación — solo sustitución
- Notación: `λx. Add x 1`

</div>
<div class="p-4 rounded-lg bg-gray-100">

**Clojure**

- Funcional desde el diseño
- Inmutabilidad por defecto
- Sintaxis prefija: `(f x y)`

</div>
<div class="p-4 rounded-lg bg-gray-100">

**JavaScript**

- Multiparadigma (funcional, POO, imperativo)
- Mutable por defecto — la inmutabilidad se **elige**
- Sintaxis infija: `f(x, y)`

</div>
</div>

<div class="mt-4 text-xs">

```text
(λx. Add x 1) aplicada a cada elemento de la lista
```

```clojure
(map inc [1 2 3 4])  ;; => (2 3 4 5)
```

```js
[1, 2, 3, 4].map(x => x + 1)  // => [2, 3, 4, 5]
```

</div>

<div class="mt-2 text-xs italic opacity-80">

Los conceptos siguen siendo válidos — en JS nada obliga a usarlos.

</div>

---
layout: center
---

# El porqué y el origen

---
layout: default
---

# Surgimientos

<div class="text-sm mt-4">

- **Alonzo Church** — 1936 — Cálculo Lambda
- **John McCarthy** — 1958 — Lisp

</div>

<div class="flex flex-wrap gap-6 items-center justify-center mt-10">
<div class="text-4xl font-serif">λ</div>
<img src="/logos/haskell.svg" class="h-8" alt="Haskell" />
<img src="/logos/erlang.svg" class="h-8" alt="Erlang" />
<img src="/logos/clojure.svg" class="h-8" alt="Clojure" />
<img src="/logos/scala.svg" class="h-8" alt="Scala" />
<img src="/logos/fsharp.svg" class="h-8" alt="F#" />
<div class="text-sm font-mono font-bold px-2 py-1 rounded bg-gray-100">ML</div>
</div>

<div class="mt-8 text-sm italic opacity-80 text-center">

De Church y McCarthy en adelante, la idea se repite en distintos lenguajes — cada uno la adapta a su época y su comunidad.

</div>

---
layout: default
---

# ¿Por qué surgió la programación funcional?

El código se **lee** muchas más veces de las que se **escribe**.

<div class="mt-4 text-sm">

| | Lectura | Escritura |
|---|---|---|
| Tiempo original | 80% | 20% |
| Si se reduce a la mitad el tiempo de **escritura** | 80% | 10% |
| Si se reduce a la mitad el tiempo de **lectura** | 40% | 20% |
| **Reducción total del proyecto** | **-40%** | **-10%** |

</div>

<div class="mt-4 text-sm italic opacity-80">

Optimizar para que el código sea más fácil de **leer** reduce el costo total mucho más que optimizar para escribirlo rápido. Las funciones puras — sin estado oculto, sin efectos secundarios — son más fáciles de leer, porque no hay nada escondido que rastrear. Por eso importan.

</div>

---
layout: center
---

# De lo imperativo a lo funcional: un ejemplo

---
layout: default
---

# El problema: evitar un doble clic

```html
<button id="btn" onclick="billTheUser(some, sales, data)">Cobrar</button>
```

```js
function billTheUser(some, sales, data) {
  window.alert('Cobrando...')
  // acá se cobra de verdad
}
```

<div class="mt-4 text-sm opacity-80">

Si alguien hace doble clic, se cobra dos veces. ¿Cómo lo evitamos?

</div>

---
layout: default
---

# Intentos con estado mutable

<div class="grid grid-cols-3 gap-3 mt-6 text-xs">
<div class="p-3 rounded-lg bg-red-50 border border-red-200">

**Flag global**

```js
let clicked = false

function billTheUser(...) {
  if (!clicked) {
    clicked = true
    // cobrar
  }
}
```

</div>
<div class="p-3 rounded-lg bg-red-50 border border-red-200">

**Deshabilitar el botón**

```js
function billTheUser(...) {
  document
    .getElementById('btn')
    .disabled = true
  // cobrar
}
```

</div>
<div class="p-3 rounded-lg bg-red-50 border border-red-200">

**Redefinir el handler**

```js
function billTheUser(...) {
  billTheUser = function () {}
  // cobrar
}
```

</div>
</div>

<div class="mt-6 text-sm italic opacity-80">

Funcionan, pero cada uno depende de **estado mutable compartido** — una variable global, el DOM, o la propia función reasignada — frágil y difícil de razonar.

</div>

---
layout: default
---

# La solución: encapsular el estado

```js
const billTheUser = (clicked => {
  return (some, sales, data) => {
    if (!clicked) {
      clicked = true
      // cobrar
    }
  }
})(false)
```

<div class="mt-4 text-sm opacity-80">

El flag <code>clicked</code> ya no es global ni vive en el DOM — vive **encerrado** dentro de la función, inaccesible desde afuera. Esto se llama *closure*, y vamos a entender exactamente cómo funciona en la próxima sección.

</div>

---
layout: default
---

# ¿Por qué JS?

<v-click>

- Es el único lenguaje que corre nativamente en el navegador
- Con Node.js corre también en el servidor — mismo lenguaje en todo el stack (esto vamos a usarlo en el resto de la unidad: React, Node + Express)
- Ecosistema enorme: npm es el gestor de paquetes más grande que existe
- Ya trae varias herramientas de estilo funcional incorporadas — por ejemplo `map`, `filter` y `reduce` sobre arrays, pero son solo algunos ejemplos entre varias

</v-click>

<v-click>

<div class="mt-6 text-sm italic opacity-80">

No es un lenguaje puramente funcional como Haskell — es un lenguaje imperativo/orientado a objetos al que **se le puede programar de forma funcional**, con disciplina.

</div>

</v-click>

---
layout: default
---

# Las 7 características de la programación funcional

<div class="grid grid-cols-2 gap-x-8 gap-y-3 mt-6 text-sm">
<div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-800 text-white text-xs flex items-center justify-center shrink-0">1</span> Programas como funciones</div>
<div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-800 text-white text-xs flex items-center justify-center shrink-0">2</span> Funciones puras</div>
<div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-800 text-white text-xs flex items-center justify-center shrink-0">3</span> Datos inmutables</div>
<div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-800 text-white text-xs flex items-center justify-center shrink-0">4</span> Funciones de primera clase</div>
<div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-800 text-white text-xs flex items-center justify-center shrink-0">5</span> Funciones de orden superior</div>
<div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-800 text-white text-xs flex items-center justify-center shrink-0">6</span> Composición de funciones</div>
<div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-800 text-white text-xs flex items-center justify-center shrink-0">7</span> Recursividad</div>
</div>

<div class="mt-6 text-sm italic opacity-80">

Esta es la hoja de ruta del resto de la clase — un concepto a la vez, siempre con el mismo ejemplo de fondo.

</div>

---
layout: default
---

# 1. Programas como funciones

- **Estructura de un programa**: una lista de definiciones de funciones.
- **Ejecución de un programa**: aplicar esas funciones a sus argumentos — según las reglas que ya vimos en Cálculo Lambda.

```clojure
(defn prom [v] (/ (reduce + v) (count v)))
(prom [1 3 5 7])   ;; => 4
```

```js
const prom = v => v.reduce((x, y) => x + y) / v.length
prom([1, 3, 5, 7])   // => 4
```

---
layout: center
---

# Funciones de primera clase y de orden superior

---
layout: default
---

# Funciones de primera clase

Un lenguaje tiene **funciones de primera clase** cuando trata a las funciones como a cualquier otro valor: se pueden asignar, guardar en una estructura, pasar y comparar. Es una propiedad **del lenguaje**.

```js
const greet = function (name) {
  return `Hola, ${name}!`
}

const operations = { greet, shout: (name) => greet(name).toUpperCase() }
const callbacks = [greet, operations.shout]
```

<v-click>

<div class="mt-3 text-sm opacity-80">

En **Cálculo Lambda** esto no es una elección de diseño — es lo único que existe. Una abstracción **es** una función, y nombrarla es simplemente asociarle un nombre:

</div>

```text
greet ≡ λname. "Hola, " ++ name
```

</v-click>

<v-click>

<div class="mt-2 text-sm opacity-80">

En **Clojure**, la misma idea:

</div>

```clojure
(def greet (fn [name] (str "Hola, " name)))
```

</v-click>

---
layout: default
---

# Funciones de orden superior

Una **función de orden superior** (HOF) recibe otra función como argumento, o devuelve una función. Es una propiedad **de esa función** — posible solo porque el lenguaje tiene funciones de primera clase.

```js
// recibe una función como argumento
function repeat(n, action) {
  for (let i = 0; i < n; i++) action(i)
}
repeat(3, i => console.log(`Vuelta ${i}`))
```

<div class="mt-4 text-sm opacity-80">

Ya usamos varias sin nombrarlas: cada vez que le pasamos una función a <code>map</code>, <code>filter</code> o un <code>addEventListener</code>, esa función que recibe es de orden superior.

</div>

---
layout: default
---

# Fábrica de funciones

Una HOF también puede **devolver** una función nueva:

```js
function multiplier(factor) {
  return number => number * factor
}
const double = multiplier(2)
double(5) // => 10
```

<div class="mt-3 text-sm opacity-80">

`multiplier` es una **fábrica de funciones**: cada llamada crea una función nueva que "recuerda" `factor` — esto es un *closure*, lo mismo que resolvió el problema del doble clic hace unos slides: el flag <code>clicked</code> quedaba "recordado" dentro de la función devuelta.

</div>

<v-click>

<div class="mt-3 text-sm opacity-80">

En Cálculo Lambda, una función que aplica otra dos veces:

</div>

```text
twice ≡ λf.λx. f (f x)
```

```clojure
(defn twice [f] (fn [x] (f (f x))))
```

</v-click>

---
layout: center
---

# Pureza e inmutabilidad

---
layout: default
---

# Funciones puras vs. impuras

<div class="grid grid-cols-2 gap-6 mt-4">
<div class="p-4 rounded-lg bg-red-50 border border-red-200">

**Impura**

```js
let total = 0

function addToTotal(price) {
  total += price   // side effect
  return total
}
```

Depende de estado externo y lo modifica.

</div>
<div class="p-4 rounded-lg bg-green-50 border border-green-200">

**Pura**

```js
function add(a, b) {
  return a + b
}
```

Mismo input, mismo output, siempre. Sin efectos secundarios.

</div>
</div>

<v-click>

<div class="mt-4 text-sm opacity-80">

Una función pura es fácil de testear, de leer y de reutilizar — no depende de "cuándo" ni "cuántas veces" se llame.

</div>

</v-click>

---
layout: default
---

# Transparencia referencial

Una expresión es "referencialmente transparente" si se puede reemplazar por su resultado sin cambiar el comportamiento del programa.

```js
function double(x) {
  return x * 2
}

const a = double(5) + double(5)
const b = 10 + 10   // reemplazando double(5) por su resultado

// a === b siempre — porque double es pura
```

<v-click>

<div class="mt-4 text-sm opacity-80">

Con una función impura esto no vale: `addToTotal(100) + addToTotal(100)` no es lo mismo que calcular una vez y duplicar, porque cada llamada cambia `total`.

</div>

</v-click>

<v-click>

<div class="mt-2 text-sm italic opacity-80">

Este es el mismo principio detrás de la **beta-reducción** en Cálculo Lambda: `(λx. Add x x) 5` se puede sustituir directamente por `Add 5 5` — funciona porque no hay estado escondido.

</div>

</v-click>

---
layout: default
---

# Inmutabilidad

A diferencia de Clojure, en JS los arrays y objetos son **mutables por defecto**. Mutarlos "por las dudas" es peligroso.

```js
function addItem(cart, item) {
  cart.push(item)   // ⚠️ muta el array recibido
  return cart
}

const cart = ['teclado']
const newCart = addItem(cart, 'mouse')
// cart también cambió — quien lo llamó no se enteró
```

<v-click>

```js
function addItem(cart, item) {
  return [...cart, item]   // copia + agrega, sin mutar el original
}
```

</v-click>

---
layout: default
---

# Copias inmutables

```js
// Arrays: spread
const original = [1, 2, 3]
const copy = [...original, 4]        // [1, 2, 3, 4] — original intacto

// Objetos: spread
const product = { name: 'Mouse', price: 18000 }
const onSale = { ...product, price: 15000 }   // objeto nuevo

// Object.freeze: bloquea mutaciones en runtime (shallow)
const config = Object.freeze({ currency: 'ARS' })
config.currency = 'USD'   // falla en silencio (o TypeError en modo estricto)
```

<v-click>

<div class="mt-4 text-sm italic opacity-80">

`Object.freeze` es superficial: si un valor interno es otro objeto, ese sí se puede seguir mutando.

</div>

</v-click>

---
layout: center
---

# Transformando colecciones

---
layout: default
---

# El caso: catálogo de una tienda online

Vamos a usar el mismo tipo de datos en todos los ejemplos que siguen:

```js
const products = [
  { name: 'Teclado mecánico', price: 45000, category: 'accesorios', stock: 12 },
  { name: 'Monitor 27"',      price: 210000, category: 'monitores',  stock: 3  },
  { name: 'Mouse inalámbrico', price: 18000, category: 'accesorios', stock: 0  },
  { name: 'Notebook 15"',     price: 950000, category: 'notebooks',  stock: 5  },
]
```

---
layout: default
---

# `map`

Transforma cada elemento y devuelve un array **nuevo**, del mismo largo.

```js
const names = products.map(p => p.name)
// => ['Teclado mecánico', 'Monitor 27"', 'Mouse inalámbrico', 'Notebook 15"']

const withDiscount = products.map(p => ({ ...p, price: p.price * 0.9 }))
// mismo largo, cada objeto es una copia con price actualizado
```

<v-click>

<div class="mt-4 text-sm opacity-80">

`(map (fn [p] (:name p)) products)` en Clojure — y en el fondo, aplicar `λp. (name p)` a cada elemento de la lista.

</div>

</v-click>

---
layout: default
---

# `filter`

Se queda con los elementos que cumplen una condición — el array resultante puede ser más chico.

```js
const inStock = products.filter(p => p.stock > 0)
// se descarta el Mouse inalámbrico (stock: 0)

const accessories = products.filter(p => p.category === 'accesorios')
```

<v-click>

<div class="mt-4 text-sm opacity-80">

`(filter (fn [p] (pos? (:stock p))) products)` en Clojure — la condición es un predicado `λp. stock(p) > 0`, igual que en Cálculo Lambda.

</div>

</v-click>

---
layout: default
---

# `reduce`

Combina todos los elementos en un único valor, arrastrando un **acumulador**.

```js
const totalValue = products.reduce(
  (accumulator, p) => accumulator + p.price * p.stock,
  0,   // valor inicial del acumulador
)
// suma price * stock de cada producto
```

<v-click>

```js
// también sirve para construir estructuras nuevas, no solo números
const byCategory = products.reduce((groups, p) => {
  const key = p.category
  return { ...groups, [key]: [...(groups[key] ?? []), p.name] }
}, {})
```

</v-click>

<v-click>

<div class="mt-2 text-sm opacity-80">

`(reduce + 0 (map ...))` en Clojure — el acumulador es explícito en ambos, algo que en Cálculo Lambda se modela con recursión pura (sin `reduce` nativo).

</div>

</v-click>

---
layout: default
---

# Encadenando: un pipeline real

`map`, `filter` y `reduce` devuelven arrays (o valores) nuevos — se pueden encadenar.

```js
// valor total del stock de accesorios disponibles
const accessoriesValue = products
  .filter(p => p.category === 'accesorios')
  .filter(p => p.stock > 0)
  .reduce((total, p) => total + p.price * p.stock, 0)

// => 540000  (solo el teclado: el mouse tiene stock 0)
```

<v-click>

<div class="mt-4 text-sm opacity-80">

Cada paso es una función pura sobre el resultado del paso anterior — se lee de arriba a abajo como una receta.

</div>

</v-click>

---
layout: center
---

# Composición

---
layout: default
---

# `compose` / `pipe` caseros

Componer es construir una función nueva encadenando otras más chicas — sin librería, se puede escribir a mano.

```js
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x)
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x)

const discount10 = price => price * 0.9
const addTax = price => price * 1.21
const round = price => Math.round(price)

const finalPrice = pipe(discount10, addTax, round)
finalPrice(45000)   // => descuento, después impuesto, después redondeo
```

<div class="flex flex-wrap items-center justify-center gap-2 mt-6 text-xs">
<div class="px-3 py-2 rounded-lg bg-blue-50 border border-blue-200 font-mono">45000</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-blue-50 border border-blue-200 font-mono">discount10</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-blue-50 border border-blue-200 font-mono">addTax</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-green-50 border border-green-200 font-mono">round</div>
</div>

<div class="text-center mt-2 text-xs opacity-70">

`pipe` va de izquierda a derecha; `compose` va de derecha a izquierda — es `(comp f g)` de Clojure, y formalmente `λf.λg.λx. f (g x)` de Cálculo Lambda. Notar que `finalPrice` nunca menciona su argumento — eso se llama estilo **point-free**.

</div>

---
layout: center
---

# Currying y aplicación parcial

---
layout: default
---

# Currying

Convertir una función de varios argumentos en una cadena de funciones de un solo argumento — el mismo currying de la Unidad 1 (cálculo λ).

```js
// sin currificar
function add(a, b) {
  return a + b
}
add(2, 3)   // => 5

// currificada — exactamente una cadena de funciones de un solo argumento
const addCurried = a => b => a + b
addCurried(2)(3)   // => 5

const add2 = addCurried(2)   // función parcialmente aplicada, "espera" b
add2(3)                      // => 5
add2(10)                     // => 12
```

<v-click>

<div class="mt-4 text-sm opacity-80">

Es exactamente `λa.λb. Add a b` de Cálculo Lambda, escrito con la sintaxis de arrow functions de JS.

</div>

</v-click>

---
layout: default
---

# Currying con más argumentos

Con más argumentos, el patrón es el mismo: una función devuelve otra función, que devuelve otra, hasta que no queda ningún argumento pendiente.

```js
function sum3(a, b, c) {
  return a + b + c
}

// currificada a mano, sin ningún helper — exactamente una cadena de tres funciones
const sum3Curried = a => b => c => a + b + c
sum3Curried(1)(2)(3)   // => 6

const sum3WithFirstTwo = sum3Curried(1)(2)   // "espera" el tercer argumento
sum3WithFirstTwo(3)                          // => 6
sum3WithFirstTwo(10)                         // => 13
```

---
layout: default
---

# Currying genérico

Currificar a mano función por función funciona, pero no escala. Una función `curry` genérica lo hace por nosotros:

```js
function curry(fn) {
  return function curried(...args) {
    return args.length >= fn.length
      ? fn(...args)
      : (...more) => curried(...args, ...more)
  }
}

const addThree = curry((a, b, c) => a + b + c)
addThree(1)(2)(3)   // => 6
addThree(1, 2)(3)   // => 6
addThree(1, 2, 3)   // => 6
```

<div class="mt-3 text-sm opacity-80">

`curry` acepta la función tal como está y devuelve una versión que se puede invocar de a un argumento por vez, de a varios, o con todos juntos — con el mismo resultado.

</div>

---
layout: default
---

# Aplicación parcial

"Fijar" algunos argumentos de una función y dejar el resto pendientes, sin currificar a mano todo.

```js
function partial(fn, ...fixedArgs) {
  return (...remainingArgs) => fn(...fixedArgs, ...remainingArgs)
}

function applyDiscount(rate, price) {
  return price * (1 - rate)
}

const applyBlackFridayDiscount = partial(applyDiscount, 0.3)
applyBlackFridayDiscount(45000)   // => 31500
```

<v-click>

<div class="mt-4 text-sm opacity-80">

JS también trae esto nativo: <code>fn.bind(null, ...fixedArgs)</code> hace lo mismo que nuestro <code>partial</code>. Es la misma idea que aplicar un solo argumento a una función curried en Cálculo Lambda: `(λa.λb. Sub a b) 1` deja pendiente `λb. Sub 1 b`.

</div>

</v-click>

---
layout: center
---

# Recursividad

---
layout: default
---

# Recursividad en JS

Repaso — ya la vimos en Clojure con `recur`. La idea es la misma: una función que se llama a sí misma con un caso base.

```js
function factorial(n) {
  if (n <= 1) return 1          // caso base
  return n * factorial(n - 1)   // caso recursivo
}
factorial(5)   // => 120
```

<v-click>

<div class="mt-4 text-sm opacity-80">

**A diferencia de Clojure**: `recur` garantiza *tail call optimization* (no crece el stack).
JavaScript **no garantiza TCO** — una recursión muy profunda puede agotar el stack.
Para esos casos conviene iterar (o usar `reduce`).

</div>

</v-click>

<v-click>

<div class="mt-2 text-xs italic opacity-70">

En Cálculo Lambda puro ni siquiera hay `function factorial() {...}` — una función no puede nombrarse a sí misma. La recursión se logra con el **combinador Y** (Unidad 1).

</div>

</v-click>

---
layout: default
---

# El combinador Y (repaso)

`fact` se llama a sí misma **por su nombre** — un lujo que Cálculo Lambda puro no tiene. El combinador Y logra el mismo efecto sin nombrar nada:

```js
const Y = f => f(x => Y(f)(x))

const fact = Y(f => n => (n === 0 ? 1 : n * f(n - 1)))
fact(5)   // => 120
```

<div class="mt-3 text-sm opacity-80">

`Y` recibe una función anónima y le "presta" la forma de llamarse a sí misma — así es como Cálculo Lambda resuelve la recursión sin `function factorial()` ni `recur`.

</div>

---
layout: default
---

# Esto ya lo sabías

<div class="text-xs mt-4">

| Cálculo Lambda | Clojure | JavaScript |
|---|---|---|
| `λx. Add x 1` | `(map inc coll)` | `coll.map(x => x + 1)` |
| — (predicado `λx. par(x)`) | `(filter even? coll)` | `coll.filter(x => x % 2 === 0)` |
| recursión (Y-combinador) | `(reduce + coll)` | `coll.reduce((a, b) => a + b, 0)` |
| `λf.λg.λx. f (g x)` | `(comp f g)` | `compose(f, g)` (casero, o de una librería) |
| `(λa.λb. Sub a b) 1` | `(partial f a)` | `partial(f, a)` o `f.bind(null, a)` |
| solo vía combinador Y | `recur` | función que se llama a sí misma (sin TCO garantizado) |
| sustitución, sin estado | inmutabilidad por defecto | inmutabilidad **a elección** (spread, `Object.freeze`) |

</div>

<v-click>

<div class="mt-3 text-sm italic opacity-80">

El paradigma no cambió — cambió el lenguaje, y con él, cuánto hay que disciplinarse.

</div>

</v-click>

---
layout: default
---

# JS Funcional — cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-sm">
<div>

**Orden superior**

| Método | Qué hace |
|---|---|
| `arr.map(fn)` | Transforma cada elemento |
| `arr.filter(fn)` | Se queda con los que cumplen |
| `arr.reduce(fn, init)` | Combina todo en un valor |
| `fn.bind(null, ...args)` | Aplicación parcial nativa |

</div>
<div>

**Inmutabilidad**

| Sintaxis | Qué hace |
|---|---|
| `[...arr, x]` | Copia + agrega (array) |
| `{ ...obj, k: v }` | Copia + actualiza (objeto) |
| `Object.freeze(obj)` | Bloquea mutaciones (shallow) |
| `const` | Evita reasignar la variable (no congela el valor) |

</div>
</div>

---
layout: default
---

# Referencias y recursos

- [developer.mozilla.org — Array](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array) — referencia completa de métodos de arrays
- [Mostly Adequate Guide to FP](https://mostly-adequate.gitbook.io/mostly-adequate-guide/) — apunte gratuito de programación funcional en JS (en inglés)
- [Functional-Light JS](https://github.com/getify/Functional-Light-JS) — libro gratuito de Kyle Simpson sobre FP práctica en JS
- Kereki, F. — *Mastering JavaScript Functional Programming*
- Mantyla, D. — *Functional Programming in JavaScript*
