# JS Funcional

## Paradigmas de programación

<div class="paradigm-tree">
<div class="paradigm-branch tone-blue">
<h4>Imperativos</h4>
<div class="paradigm-branch-sub">énfasis en la ejecución — cómo hacerlo, paso a paso</div>
<div class="paradigm-leaves">
<div class="paradigm-leaf">
<strong>Estructurado</strong>
<div>Basic, Pascal</div>
</div>
<div class="paradigm-leaf">
<strong>Procedimental</strong>
<div class="paradigm-leaf-imgs"><img src="/logos/c.svg" alt="C" /></div>
</div>
<div class="paradigm-leaf">
<strong>Orientado a objetos</strong>
<div class="paradigm-leaf-imgs"><img src="/logos/cplusplus.svg" alt="C++" /><img src="/logos/python.svg" alt="Python" /></div>
<div>Java, C++, Python</div>
</div>
</div>
</div>
<div class="paradigm-branch tone-yellow">
<h4>Declarativos</h4>
<div class="paradigm-branch-sub">énfasis en la evaluación — qué se quiere obtener</div>
<div class="paradigm-leaves">
<div class="paradigm-leaf highlight">
<strong>Funcional</strong>
<div class="paradigm-leaf-imgs"><img src="/logos/haskell.svg" alt="Haskell" /><img src="/logos/clojure.svg" alt="Clojure" /><img src="/logos/javascript.svg" alt="JS" /></div>
<div>Haskell, Clojure, JS*</div>
</div>
<div class="paradigm-leaf">
<strong>Lógico</strong>
<div>Prolog</div>
</div>
</div>
</div>
</div>

*JS no nace funcional — es multiparadigma, y permite ese estilo. Los lenguajes más usados hoy en día lo son: cada quien elige el estilo más adecuado para cada tarea.

### Imperativo vs. declarativo

<div class="card-grid card-grid-2">
<div class="info-card">
<h4>Imperativo — cómo hacerlo, paso a paso</h4>

```js
const names = []
for (let i = 0; i < products.length; i++) {
  if (products[i].stock > 0) {
    names.push(products[i].name)
  }
}
```
</div>
<div class="info-card tone-green">
<h4>Declarativo — qué se quiere obtener</h4>

```js
const names = products
  .filter(p => p.stock > 0)
  .map(p => p.name)
```
</div>
</div>

La programación funcional es un estilo **declarativo**: se describe el resultado que se quiere, no la secuencia de pasos para construirlo.

## ¿Qué es la programación funcional?

Se puede definir casi tanto por lo que **evita** como por lo que hace:

- Evaluación de **funciones matemáticas** — dado el mismo input, siempre el mismo output.
- ~~Cambios de estado~~
- ~~Mutaciones de datos~~
- Se rige por **principios**, no por una secuencia de instrucciones a ejecutar paso a paso.

```js
const area = r => r ** 2 * Math.PI
```

Este ejemplo ya muestra la idea completa: `area` no modifica nada externo, no depende de nada externo, y devuelve un valor calculado a partir de su entrada — igual que una función matemática en el sentido estricto. El resto del apunte desarrolla, uno por uno, los principios que hacen falta para escribir código así de manera consistente.

## Breve cronología

<div class="timeline-wrap">
<div class="timeline-line"></div>

<div class="timeline-node" style="left:2.0%">
<div class="timeline-label" style="color:#7c3aed">λ-calc</div>
<div class="timeline-dot" style="background:#7c3aed"></div>
<div class="timeline-year">1936</div>
</div>

<div class="timeline-node" style="left:13.6%">
<div class="timeline-label" style="color:#15803d">Lisp</div>
<div class="timeline-dot" style="background:#22c55e"></div>
<div class="timeline-year">1958</div>
</div>

<div class="timeline-node" style="left:21.0%">
<div class="timeline-label"><img src="/logos/c.svg" alt="C" /></div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">1972</div>
</div>

<div class="timeline-node" style="left:27.8%">
<div class="timeline-label" style="color:#15803d">ML</div>
<div class="timeline-dot" style="background:#22c55e"></div>
<div class="timeline-year">1973</div>
</div>

<div class="timeline-node" style="left:34.7%">
<div class="timeline-label" style="color:#15803d">Scheme</div>
<div class="timeline-dot" style="background:#22c55e"></div>
<div class="timeline-year">1975</div>
</div>

<div class="timeline-node" style="left:41.6%">
<div class="timeline-label">Smalltalk</div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">1980</div>
</div>

<div class="timeline-node" style="left:48.4%">
<div class="timeline-label"><img src="/logos/cplusplus.svg" alt="C++" /></div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">1983</div>
</div>

<div class="timeline-node" style="left:55.3%">
<div class="timeline-label"><img src="/logos/erlang.svg" alt="Erlang" /></div>
<div class="timeline-dot" style="background:#22c55e"></div>
<div class="timeline-year">1986</div>
</div>

<div class="timeline-node" style="left:62.1%">
<div class="timeline-label"><img src="/logos/haskell.svg" alt="Haskell" /></div>
<div class="timeline-dot" style="background:#22c55e"></div>
<div class="timeline-year">1990</div>
</div>

<div class="timeline-node" style="left:69.0%">
<div class="timeline-label"><img src="/logos/python.svg" alt="Python" /></div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">1991</div>
</div>

<div class="timeline-node" style="left:75.8%">
<div class="timeline-label"><img src="/logos/javascript.svg" alt="JS" /></div>
<div class="timeline-dot" style="background:#facc15"></div>
<div class="timeline-year">JS nace<br>1995</div>
</div>

<div class="timeline-node" style="left:82.7%">
<div class="timeline-label">Java</div>
<div class="timeline-dot" style="background:#9ca3af"></div>
<div class="timeline-year">1995</div>
</div>

<div class="timeline-node" style="left:91.1%">
<div class="timeline-label"><img src="/logos/clojure.svg" alt="Clojure" /></div>
<div class="timeline-dot" style="background:#22c55e"></div>
<div class="timeline-year">2007</div>
</div>

<div class="timeline-node" style="left:98.0%">
<div class="timeline-label"><img src="/logos/javascript.svg" alt="JS ES6" /></div>
<div class="timeline-dot" style="background:#facc15;border-color:#111827"></div>
<div class="timeline-year">ES6<br>2015</div>
</div>

</div>

<div class="diagram-legend">
<span><span class="dot" style="background:#7c3aed"></span>sistema formal, no un lenguaje</span>
<span><span class="dot" style="background:#22c55e"></span>linaje funcional</span>
<span><span class="dot" style="background:#9ca3af"></span>imperativo / POO</span>
<span><span class="dot" style="background:#facc15"></span>JS</span>
</div>

JS nace en 1995 — recién 20 años después, con **ES6 (2015)**, incorpora herramientas de estilo funcional: arrow functions, `const`, spread… Notar además que el Cálculo Lambda, que sirve de base teórica a todo este tema, es anterior en casi 20 años al primer lenguaje de programación de la lista — es un sistema matemático, no una herramienta pensada para ejecutarse en una computadora.

## De Cálculo Lambda y Clojure a JavaScript

Ya vimos programación funcional dos veces: primero de forma formal, en **Cálculo Lambda** (Unidad 1) — funciones como único elemento del lenguaje, aplicación, sustitución. Después de forma práctica, en **Clojure** (Unidad 3) — un lenguaje diseñado desde cero para programar así: inmutabilidad por defecto, `map`/`filter`/`reduce` nativos, funciones de primera clase.

Ahora vemos el mismo paradigma en **JavaScript**. La pregunta que guía todo este apunte es siempre la misma: *"esto que ya sabemos hacer en Cálculo Lambda y en Clojure, ¿cómo se escribe en JS?"*

### Mismo paradigma, tres lenguajes

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>Cálculo Lambda</h4>

El origen formal: todo es una función. Sin estado, sin mutación — solo sustitución.

<div class="card-note">Notación: <code>λx. Add x 1</code></div>
</div>
<div class="info-card">
<h4>Clojure</h4>

Funcional desde el diseño. Inmutabilidad por defecto.

<div class="card-note">Sintaxis prefija: <code>(f x y)</code></div>
</div>
<div class="info-card">
<h4>JavaScript</h4>

Multiparadigma (funcional, POO, imperativo). Mutable por defecto — la inmutabilidad se **elige**.

<div class="card-note">Sintaxis infija: <code>f(x, y)</code></div>
</div>
</div>

```clojure
;; Clojure
(map inc [1 2 3 4])  ;; => (2 3 4 5)
```

```js
// JavaScript
;[1, 2, 3, 4].map(x => x + 1)  // => [2, 3, 4, 5]
```

Los conceptos que aprendimos con Cálculo Lambda y Clojure siguen siendo válidos en JS — lo que cambia es que acá nada obliga a usarlos. Programar "funcional" en JavaScript es una elección de estilo y disciplina, no una imposición del lenguaje.

## Los orígenes

<div class="card-grid card-grid-2">
<div class="info-card">
<h4>λ Cálculo Lambda</h4>

<div class="card-note">Alonzo Church — 1936</div>

Sistema formal para expresar cómputo usando solo funciones — la base matemática de todo lo que sigue. Es anterior a la existencia de las computadoras: no es un lenguaje de programación, es lógica pura.
</div>
<div class="info-card">
<h4>Lisp</h4>

<div class="card-note">John McCarthy — 1958</div>

El primer lenguaje con funciones de primera clase — trata el código mismo como datos (listas). Sigue en uso hoy, casi 70 años después.
</div>
<div class="info-card">
<h4>ML</h4>

<div class="card-note">Robin Milner — 1973</div>

Primer lenguaje con inferencia de tipos automática (el tipo se deduce solo, sin anotarlo) — influencia directa en Haskell, OCaml y F#.
</div>
<div class="info-card">
<h4>Scheme</h4>

<div class="card-note">Guy Steele y Gerald Sussman — 1975</div>

Dialecto minimalista de Lisp que formaliza el *closure* léxico — el mismo mecanismo que vamos a usar más adelante en JS.
</div>
</div>

## La familia funcional moderna

<div class="card-grid card-grid-3">
<div class="info-card" style="text-align:center">
<img src="/logos/erlang.svg" alt="Erlang" style="height:1.5rem;margin:0 auto 0.4rem" />
<h4>Erlang</h4>

<div class="card-note">Joe Armstrong (Ericsson) — 1986</div>

Concurrencia y tolerancia a fallos, pensado para centrales telefónicas.
</div>
<div class="info-card" style="text-align:center">
<img src="/logos/haskell.svg" alt="Haskell" style="height:1.5rem;margin:0 auto 0.4rem" />
<h4>Haskell</h4>

<div class="card-note">Comité (Simon Peyton Jones y otros) — 1990</div>

Puramente funcional, con evaluación perezosa por defecto.
</div>
<div class="info-card" style="text-align:center">
<img src="/logos/scala.svg" alt="Scala" style="height:1.5rem;margin:0 auto 0.4rem" />
<h4>Scala</h4>

<div class="card-note">Martin Odersky — 2003</div>

Funcional y orientado a objetos, corre sobre la JVM.
</div>
<div class="info-card" style="text-align:center">
<img src="/logos/fsharp.svg" alt="F#" style="height:1.5rem;margin:0 auto 0.4rem" />
<h4>F#</h4>

<div class="card-note">Don Syme (Microsoft Research) — 2005</div>

Un ML moderno para la plataforma .NET.
</div>
<div class="info-card" style="text-align:center">
<img src="/logos/clojure.svg" alt="Clojure" style="height:1.5rem;margin:0 auto 0.4rem" />
<h4>Clojure</h4>

<div class="card-note">Rich Hickey — 2007</div>

Un Lisp moderno sobre la JVM, con inmutabilidad persistente.
</div>
<div class="info-card" style="text-align:center">
<img src="/logos/elixir.svg" alt="Elixir" style="height:1.5rem;margin:0 auto 0.4rem" />
<h4>Elixir</h4>

<div class="card-note">José Valim — 2011</div>

Sintaxis moderna sobre la BEAM, la máquina virtual de Erlang.
</div>
</div>

De Church y McCarthy en adelante, la idea se repite en distintos lenguajes — cada uno la adapta a su época y su comunidad.

## ¿Por qué surgió la programación funcional?

El código se **lee** muchas más veces de las que se **escribe**. Esa asimetría es uno de los argumentos centrales detrás de la programación funcional:

<div class="card-grid" style="grid-template-columns: 1fr;">
<div class="info-card">

| | Lectura | Escritura |
|---|---|---|
| Tiempo original | 80% | 20% |
| Si se reduce a la mitad el tiempo de **escritura** | 80% | 10% |
| Si se reduce a la mitad el tiempo de **lectura** | 40% | 20% |
| **Reducción total del proyecto** | **-40%** | **-10%** |

</div>
</div>

Optimizar para que el código sea más fácil de **leer** reduce el costo total de un proyecto mucho más que optimizar para escribirlo rápido. Las funciones puras — sin estado oculto, sin efectos secundarios — son más fáciles de leer, porque no hay nada escondido que rastrear: alcanza con mirar los parámetros y el `return`. Por eso importan.

## De lo imperativo a lo funcional: un ejemplo

Un caso real y chico ayuda a ver la diferencia en la práctica: evitar que un botón dispare una acción dos veces si alguien hace doble clic.

```html
<button id="btn" onclick="billTheUser(some, sales, data)">Cobrar</button>
```

```js
function billTheUser(some, sales, data) {
  window.alert('Cobrando...')
  // acá se cobra de verdad
}
```

La primera reacción suele ser resolverlo con **estado mutable compartido** — una variable global, el propio DOM, o la función reasignándose a sí misma:

```js
// Flag global
let clicked = false
function billTheUser(...) {
  if (!clicked) {
    clicked = true
    // cobrar
  }
}

// Deshabilitar el botón
function billTheUser(...) {
  document
    .getElementById('btn')
    .disabled = true
  // cobrar
}

// Redefinir el handler
function billTheUser(...) {
  billTheUser = function () {}
  // cobrar
}
```

Los tres funcionan, pero cada uno depende de algo mutable y externo a la función — frágil y difícil de razonar cuando el código crece. La alternativa funcional **encapsula** el estado en vez de compartirlo:

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

El flag `clicked` ya no es global ni vive en el DOM — vive **encerrado** dentro de la función, inaccesible desde afuera. Esto se llama *closure*, y se explica en detalle en la sección de funciones de orden superior, un poco más abajo.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Elegí otro problema típico de UI que hoy resolverías con una variable global (por ejemplo, contar cuántas veces se abrió un modal, o recordar si un formulario ya se envió) y reescribilo usando el mismo patrón de closure que `billTheUser`.
</div>

## ¿Por qué JS?

- Es el único lenguaje que corre nativamente en el navegador.
- Con Node.js corre también en el servidor — mismo lenguaje en todo el stack (esto se aprovecha en el resto de la unidad: React, Node + Express).
- Tiene el ecosistema de paquetes (npm) más grande que existe.
- Ya trae varias herramientas de estilo funcional incorporadas — por ejemplo `map`, `filter` y `reduce` sobre arrays, pero son solo algunos ejemplos entre varias (`some`, `every`, `find`, `flatMap`, entre otras).

JavaScript no es un lenguaje puramente funcional como Haskell — es un lenguaje imperativo/orientado a objetos al que **se le puede programar de forma funcional**, con disciplina.

## Las 7 características de la programación funcional

Esta es la hoja de ruta del resto del apunte — un concepto a la vez, siempre con el mismo ejemplo de fondo:

1. Programas como funciones
2. Funciones puras
3. Datos inmutables
4. Funciones de primera clase
5. Funciones de orden superior
6. Composición de funciones
7. Recursividad

### 1. Programas como funciones

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

## Funciones de primera clase y de orden superior

### Funciones de primera clase

Un lenguaje tiene **funciones de primera clase** cuando trata a las funciones como a cualquier otro valor: se pueden asignar a una variable, guardar en un array o un objeto, pasar como argumento y devolver. Es una propiedad **del lenguaje**.

```js
const greet = function (name) {
  return `Hola, ${name}!`
}

const operations = {
  greet,
  shout: (name) => greet(name).toUpperCase(),
}

const callbacks = [greet, operations.shout]
```

En **Cálculo Lambda** esto no es una elección de diseño — es lo único que existe: no hay otra cosa *que* funciones. Una abstracción **es** una función, y nombrarla es simplemente asociarle un nombre:

```text
greet ≡ λname. "Hola, " ++ name
```

En **Clojure**, la misma idea, con la misma sintaxis de siempre:

```clojure
(def greet (fn [name] (str "Hola, " name)))
```

### Funciones de orden superior

Una **función de orden superior** (*higher-order function*, HOF) es una función puntual que recibe otra función como argumento, o devuelve una función. A diferencia de "primera clase", que es una propiedad del lenguaje, esta es una propiedad **de esa función en particular** — y solo es posible porque el lenguaje ya tiene funciones de primera clase. Son conceptos relacionados pero distintos: uno es la condición habilitante, el otro es lo que se construye con ella.

```js
// recibe una función como argumento
function repeat(n, action) {
  for (let i = 0; i < n; i++) action(i)
}
repeat(3, i => console.log(`Vuelta ${i}`))
```

Ya usamos varias HOFs sin nombrarlas: cada vez que le pasamos una función a `map`, `filter` o un `addEventListener`, esa función que recibe es de orden superior.

Una HOF también puede **devolver** una función nueva — una **fábrica de funciones**:

```js
function multiplier(factor) {
  return number => number * factor
}
const double = multiplier(2)
double(5) // => 10
```

Cada llamada a `multiplier` crea una función nueva que "recuerda" el valor de `factor` que tenía en ese momento. Esto se llama *closure* (clausura) — la función devuelta mantiene acceso al entorno donde fue creada, aunque `multiplier` ya haya terminado de ejecutarse. Es exactamente el mecanismo que resolvió el problema del doble clic unas secciones atrás: el flag `clicked` quedaba "recordado" dentro de la función devuelta.

En Cálculo Lambda, una función de orden superior que aplica otra función dos veces:

```text
twice ≡ λf.λx. f (f x)
```

Y en Clojure:

```clojure
(defn twice [f] (fn [x] (f (f x))))
```

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una función `logAndRun(fn)` que devuelva una nueva función: al llamarla, primero imprime `"Ejecutando..."` por consola y después ejecuta `fn` con los argumentos recibidos, devolviendo su resultado. Probala envolviendo alguna función simple, como una que sume dos números.
</div>

## Pureza e inmutabilidad

### Funciones puras vs. impuras

<div class="card-grid card-grid-2">
<div class="info-card tone-red">
<h4>Impura</h4>

```js
let total = 0

function addToTotal(price) {
  total += price   // side effect
  return total
}
```

Depende de estado externo y lo modifica.
</div>
<div class="info-card tone-green">
<h4>Pura</h4>

```js
function add(a, b) {
  return a + b
}
```

Mismo input, mismo output, siempre. Sin efectos secundarios.
</div>
</div>

Una función pura es fácil de testear, de leer y de reutilizar — su resultado no depende de "cuándo" ni "cuántas veces" se la llame, ni de qué pasó antes en el programa.

<div class="practice-box">
<p class="practice-label">Practicá</p>

De las siguientes funciones, identificá cuáles son puras y cuáles no, y reescribí las impuras como puras: `function addTax(price) { return price * 1.21 }`, `function logAndDouble(x) { console.log(x); return x * 2 }`, `function getRandomDiscount() { return Math.random() * 0.3 }`.
</div>

### Transparencia referencial

Una expresión es **referencialmente transparente** si se puede reemplazar por su resultado sin cambiar el comportamiento del programa.

```js
function double(x) {
  return x * 2
}

const a = double(5) + double(5)
const b = 10 + 10   // reemplazando double(5) por su resultado

// a === b siempre, porque double es pura
```

Este es el mismo principio detrás de la **beta-reducción** en Cálculo Lambda: `(λx. Add x x) 5` se puede sustituir directamente por `Add 5 5` — funciona precisamente porque no hay estado escondido. Con una función impura esto no vale: `addToTotal(100) + addToTotal(100)` no es lo mismo que calcular una vez y duplicar, porque cada llamada cambia `total`.

### Inmutabilidad

A diferencia de Clojure, en JavaScript los arrays y objetos son **mutables por defecto**. Mutarlos "por las dudas" es una fuente común de bugs difíciles de rastrear:

```js
function addItem(cart, item) {
  cart.push(item)   // ⚠️ muta el array recibido
  return cart
}

const cart = ['teclado']
const newCart = addItem(cart, 'mouse')
// cart también cambió — quien lo llamó no se enteró
```

La alternativa inmutable: en vez de modificar la estructura recibida, se construye una copia nueva con el cambio aplicado.

```js
function addItem(cart, item) {
  return [...cart, item]   // copia + agrega, sin mutar el original
}
```

### Copias inmutables

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

`Object.freeze` es superficial (*shallow*): si un valor interno es a su vez otro objeto, ese objeto interno se puede seguir mutando sin problema. Y `const` tampoco alcanza por sí solo — evita **reasignar** la variable, no evita mutar el valor que contiene.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Tomá la función `addItem` mutable de más arriba y escribí un test manual: guardá el array original en una variable aparte antes de llamarla, llamala, y confirmá con `console.log` que el original cambió. Repetí el mismo test con la versión inmutable y confirmá que esta vez no cambió.
</div>

## Transformando colecciones

### El caso: catálogo de una tienda online

Los ejemplos que siguen usan siempre el mismo tipo de datos:

```js
const products = [
  { name: 'Teclado mecánico', price: 45000, category: 'accesorios', stock: 12 },
  { name: 'Monitor 27"',      price: 210000, category: 'monitores',  stock: 3  },
  { name: 'Mouse inalámbrico', price: 18000, category: 'accesorios', stock: 0  },
  { name: 'Notebook 15"',     price: 950000, category: 'notebooks',  stock: 5  },
]
```

### `map`

Transforma cada elemento y devuelve un array **nuevo**, del mismo largo que el original.

```js
const names = products.map(p => p.name)
// => ['Teclado mecánico', 'Monitor 27"', 'Mouse inalámbrico', 'Notebook 15"']

const withDiscount = products.map(p => ({ ...p, price: p.price * 0.9 }))
// mismo largo; cada objeto es una copia con price actualizado
```

Equivalente a `(map (fn [p] (:name p)) products)` en Clojure — y, en el fondo, a aplicar `λp. (name p)` a cada elemento de la lista.

<div class="practice-box">
<p class="practice-label">Practicá</p>

A partir de <code>products</code>, generá un array <code>pricesWithTax</code> con el precio de cada producto incrementado un 21%, sin modificar el catálogo original.
</div>

### `filter`

Se queda con los elementos que cumplen una condición — el array resultante puede ser más chico que el original (o del mismo tamaño, o vacío).

```js
const inStock = products.filter(p => p.stock > 0)
// se descarta el Mouse inalámbrico (stock: 0)

const accessories = products.filter(p => p.category === 'accesorios')
```

Equivalente a `(filter (fn [p] (pos? (:stock p))) products)` en Clojure — la condición es un predicado, `λp. Gt (stock p) 0`, igual que en Cálculo Lambda.

### `reduce`

Combina todos los elementos en un único valor, arrastrando un **acumulador** paso a paso.

```js
const totalValue = products.reduce(
  (accumulator, p) => accumulator + p.price * p.stock,
  0,   // valor inicial del acumulador
)
// suma price * stock de cada producto
```

`reduce` no está limitado a sumar números — sirve para construir cualquier estructura nueva a partir de un array:

```js
const byCategory = products.reduce((groups, p) => {
  const key = p.category
  return { ...groups, [key]: [...(groups[key] ?? []), p.name] }
}, {})
// => { accesorios: [...], monitores: [...], notebooks: [...] }
```

Equivalente a `(reduce + 0 (map ...))` en Clojure — el acumulador es explícito en ambos casos, algo que en Cálculo Lambda puro se modela con recursión (no existe un `reduce` nativo).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Usando <code>reduce</code>, calculá <code>mostExpensiveProduct</code>: el producto con el <code>price</code> más alto del catálogo, sin ordenar el array primero.
</div>

### Encadenando: un pipeline real

`map`, `filter` y `reduce` devuelven arrays (o valores) nuevos, así que se pueden encadenar uno después de otro:

```js
// valor total del stock de accesorios disponibles
const accessoriesValue = products
  .filter(p => p.category === 'accesorios')
  .filter(p => p.stock > 0)
  .reduce((total, p) => total + p.price * p.stock, 0)

// => 540000  (solo el teclado: el mouse tiene stock 0)
```

Cada paso es una función pura que trabaja sobre el resultado del paso anterior — la cadena se lee de arriba a abajo como una receta, sin variables intermedias mutables.

## Composición

### `compose` / `pipe` caseros

Componer funciones es construir una función nueva encadenando otras más chicas. No hace falta ninguna librería — se puede escribir a mano en pocas líneas:

```js
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x)
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x)

const discount10 = price => price * 0.9
const addTax = price => price * 1.21
const round = price => Math.round(price)

const finalPrice = pipe(discount10, addTax, round)
finalPrice(45000)   // descuento, después impuesto, después redondeo
```

<div class="flow-row">
<div class="flow-box tone-brand"><code>45000</code></div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-brand"><code>discount10</code></div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-brand"><code>addTax</code></div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-green"><code>round</code></div>
</div>

`pipe` va de izquierda a derecha; `compose` va de derecha a izquierda — es el `(comp f g)` de Clojure, y formalmente `λf.λg.λx. f (g x)` de Cálculo Lambda. Notar que `finalPrice` nunca menciona su argumento — eso se llama estilo **point-free** (o *tacit programming*).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí las funciones puras <code>applyDiscount(rate)</code> (que devuelve una función que aplica ese descuento a un precio), <code>addTax(price)</code> y <code>roundPrice(price)</code>, y usá <code>pipe</code> para construir un <code>finalPrice</code> propio que aplique un 15% de descuento, después impuesto, y después redondeo.
</div>

## Currying y aplicación parcial

### Currying

Currificar es convertir una función de varios argumentos en una cadena de funciones de un solo argumento — el mismo currying visto en la Unidad 1 (Cálculo Lambda).

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

Es exactamente `λa.λb. Add a b` de Cálculo Lambda, escrito con la sintaxis de arrow functions de JavaScript. Aplicar un argumento a la vez es la razón por la que en Cálculo Lambda una función "de dos argumentos" en realidad no existe — siempre es una función de un argumento que devuelve otra función.

### Currying con más argumentos

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

### Currying genérico

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

`curry` acepta la función tal como está y devuelve una versión que se puede invocar de a un argumento por vez, de a varios, o con todos juntos — con el mismo resultado.

### Aplicación parcial

"Fijar" algunos argumentos de una función y dejar el resto pendientes, sin tener que currificar todo a mano:

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

JavaScript también trae esto nativo: `fn.bind(null, ...fixedArgs)` hace lo mismo que el `partial` casero de arriba. Es la misma idea que aplicar un solo argumento a una función currificada en Cálculo Lambda: `(λa.λb. Sub a b) 1` deja pendiente `λb. Sub 1 b`.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Currificá a mano <code>applyDiscount(rate, price)</code> como <code>applyDiscountCurried = rate => price => ...</code>, y a partir de esa versión creá <code>applyBlackFridayDiscount</code> (30% fijo) y <code>applyClearanceDiscount</code> (50% fijo) sin repetir la lógica del descuento. Repetí el mismo resultado partiendo de la versión sin currificar, usando <code>fn.bind(null, ...)</code>.
</div>

## Recursividad en JS

Repaso — ya la vimos en Clojure con `recur`. La idea es la misma: una función que se llama a sí misma, con un caso base que detiene la recursión.

```js
function factorial(n) {
  if (n <= 1) return 1          // caso base
  return n * factorial(n - 1)   // caso recursivo
}
factorial(5)   // => 120

function sum(numbers) {
  if (numbers.length === 0) return 0
  const [first, ...rest] = numbers
  return first + sum(rest)
}
sum([1, 2, 3, 4])   // => 10
```

**A diferencia de Clojure**: `recur` garantiza *tail call optimization* (TCO) — no crece el stack sin importar cuántas veces se repita. **JavaScript no garantiza TCO** en ningún motor mayor (V8, el que usan Chrome y Node, no lo implementa) — una recursión muy profunda puede tirar `RangeError: Maximum call stack size exceeded`. Para esos casos, en JS se prefiere iterar, o usar `reduce`.

En Cálculo Lambda puro la situación es todavía más radical: ni siquiera existe algo como `function factorial() { ... }` — una función anónima no puede nombrarse a sí misma dentro de su propia definición. La recursión se logra igual, pero con un combinador (el **combinador Y**, visto en la Unidad 1), que es precisamente el mecanismo que le permite a una función "verse a sí misma" sin tener nombre.

### El combinador Y (repaso)

`factorial` se llama a sí misma **por su nombre** — un lujo que Cálculo Lambda puro no tiene. El combinador Y logra el mismo efecto sin nombrar nada:

```js
const Y = f => f(x => Y(f)(x))

const fact = Y(f => n => (n === 0 ? 1 : n * f(n - 1)))
fact(5)   // => 120
```

`Y` recibe una función anónima y le "presta" la forma de llamarse a sí misma — así es como Cálculo Lambda resuelve la recursión sin `function factorial()` ni `recur`.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una función recursiva <code>sumStock(products)</code> que sume el <code>stock</code> de todos los productos del catálogo sin usar <code>reduce</code> ni ningún bucle. Probala con un array de más de 10.000 elementos generado en un <code>for</code> simple — si aparece <code>RangeError: Maximum call stack size exceeded</code>, anotá aproximadamente a partir de qué tamaño ocurre en tu entorno, y reescribí la misma función con <code>reduce</code> para comparar.
</div>

## Esto ya lo sabías

| Cálculo Lambda | Clojure | JavaScript |
|---|---|---|
| `λx. Add x 1` | `(map inc coll)` | `coll.map(x => x + 1)` |
| predicado `λx. Par x` | `(filter even? coll)` | `coll.filter(x => x % 2 === 0)` |
| recursión (combinador Y) | `(reduce + coll)` | `coll.reduce((a, b) => a + b, 0)` |
| `λf. λg. λx. f (g x)` | `(comp f g)` | `compose(f, g)` (casero, o de una librería) |
| `(λa. λb. Sub a b) 1` | `(partial f a)` | `partial(f, a)` o `f.bind(null, a)` |
| solo vía combinador Y | `recur` | función que se llama a sí misma (sin TCO garantizado) |
| sustitución, sin estado | inmutabilidad por defecto | inmutabilidad **a elección** (spread, `Object.freeze`) |

El paradigma no cambió a lo largo de la unidad — cambió el lenguaje, y con él, cuánto hay que disciplinarse para seguir escribiendo funcional.

## Cheat sheet

<div class="card-grid card-grid-2">
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

## Referencias y recursos

- [developer.mozilla.org — Array](https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array) — referencia completa de métodos de arrays
- [Mostly Adequate Guide to FP](https://mostly-adequate.gitbook.io/mostly-adequate-guide/) — apunte gratuito de programación funcional en JS (en inglés)
- [Functional-Light JS](https://github.com/getify/Functional-Light-JS) — libro gratuito de Kyle Simpson sobre FP práctica en JS
- Kereki, F. — *Mastering JavaScript Functional Programming*
- Mantyla, D. — *Functional Programming in JavaScript*

## Cierre

El objetivo de este tema es que `map`, `filter`, `reduce`, la inmutabilidad y las funciones puras dejen de sentirse como "la forma rara de escribir JS" y pasen a ser la forma por defecto de resolver un problema — el mismo criterio que ya se usaba en Clojure, aplicado con la sintaxis de JavaScript. A partir de acá, ese mismo estilo aparece una y otra vez en el resto de la unidad: en los componentes de React, en los handlers de Node + Express, y en las transformaciones de datos de MongoDB.
