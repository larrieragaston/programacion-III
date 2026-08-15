# JS Funcional

## Paradigmas de programación

<div class="branch-diagram-wrap">
<svg viewBox="0 0 760 250" class="branch-diagram" role="img" aria-label="Árbol de paradigmas: imperativos (procedimental, orientado a objetos) y declarativos (funcional, lógica)">
  <rect x="290" y="6" width="180" height="34" rx="8" fill="#e5e7eb" stroke="#111827" stroke-width="1.5" />
  <text x="380" y="28" text-anchor="middle" style="font-family:monospace;font-size:15px;fill:#111827">Paradigmas</text>

  <line x1="380" y1="40" x2="380" y2="58" stroke="#9ca3af" stroke-width="2" />
  <line x1="150" y1="58" x2="610" y2="58" stroke="#9ca3af" stroke-width="2" />
  <line x1="150" y1="58" x2="150" y2="76" stroke="#9ca3af" stroke-width="2" />
  <line x1="610" y1="58" x2="610" y2="76" stroke="#9ca3af" stroke-width="2" />

  <rect x="60" y="76" width="180" height="34" rx="8" fill="#dbeafe" stroke="#3b82f6" stroke-width="1.5" />
  <text x="150" y="98" text-anchor="middle" style="font-family:monospace;font-size:14px;fill:#1e3a8a">Imperativos</text>
  <text x="150" y="122" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">énfasis en la ejecución</text>

  <rect x="520" y="76" width="180" height="34" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" />
  <text x="610" y="98" text-anchor="middle" style="font-family:monospace;font-size:14px;fill:#78350f">Declarativos</text>
  <text x="610" y="122" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">énfasis en la evaluación</text>

  <line x1="150" y1="132" x2="150" y2="150" stroke="#9ca3af" stroke-width="2" />
  <line x1="75" y1="150" x2="225" y2="150" stroke="#9ca3af" stroke-width="2" />
  <line x1="75" y1="150" x2="75" y2="166" stroke="#9ca3af" stroke-width="2" />
  <line x1="225" y1="150" x2="225" y2="166" stroke="#9ca3af" stroke-width="2" />

  <rect x="20" y="166" width="110" height="30" rx="6" fill="#f3f4f6" stroke="#9ca3af" />
  <text x="75" y="186" text-anchor="middle" style="font-family:monospace;font-size:12px;fill:#374151">Procedimental</text>
  <text x="75" y="212" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">Pascal, C</text>

  <rect x="170" y="166" width="110" height="30" rx="6" fill="#f3f4f6" stroke="#9ca3af" />
  <text x="225" y="186" text-anchor="middle" style="font-family:monospace;font-size:12px;fill:#374151">Orientado a objetos</text>
  <text x="225" y="212" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">Java, Smalltalk</text>

  <line x1="610" y1="132" x2="610" y2="150" stroke="#9ca3af" stroke-width="2" />
  <line x1="535" y1="150" x2="685" y2="150" stroke="#9ca3af" stroke-width="2" />
  <line x1="535" y1="150" x2="535" y2="166" stroke="#9ca3af" stroke-width="2" />
  <line x1="685" y1="150" x2="685" y2="166" stroke="#9ca3af" stroke-width="2" />

  <rect x="480" y="166" width="110" height="30" rx="6" fill="#facc15" stroke="#111827" stroke-width="1.5" />
  <text x="535" y="186" text-anchor="middle" style="font-family:monospace;font-size:12px;font-weight:bold;fill:#111827">Funcional</text>
  <text x="535" y="212" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">Haskell, Clojure, JS*</text>

  <rect x="630" y="166" width="110" height="30" rx="6" fill="#f3f4f6" stroke="#9ca3af" />
  <text x="685" y="186" text-anchor="middle" style="font-family:monospace;font-size:12px;fill:#374151">Lógica</text>
  <text x="685" y="212" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">Prolog</text>
</svg>
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

### Breve cronología

<div class="branch-diagram-wrap">
<svg viewBox="0 0 780 200" class="branch-diagram" role="img" aria-label="Cronología de lenguajes, con los de linaje funcional destacados">
  <line x1="30" y1="100" x2="750" y2="100" stroke="#9ca3af" stroke-width="2" />

  <circle cx="60" cy="100" r="6" fill="#22c55e" />
  <text x="60" y="80" text-anchor="middle" style="font-family:monospace;font-size:11px;font-weight:bold;fill:#15803d">Lisp</text>
  <text x="60" y="122" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">1958</text>

  <circle cx="200" cy="100" r="6" fill="#9ca3af" />
  <text x="200" y="132" text-anchor="middle" style="font-family:monospace;font-size:11px;fill:#374151">C</text>
  <text x="200" y="148" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">1972</text>

  <circle cx="270" cy="100" r="6" fill="#22c55e" />
  <text x="270" y="80" text-anchor="middle" style="font-family:monospace;font-size:11px;font-weight:bold;fill:#15803d">ML</text>
  <text x="270" y="122" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">1973</text>

  <circle cx="340" cy="100" r="6" fill="#22c55e" />
  <text x="340" y="132" text-anchor="middle" style="font-family:monospace;font-size:11px;font-weight:bold;fill:#15803d">Scheme</text>
  <text x="340" y="148" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">1975</text>

  <circle cx="420" cy="100" r="6" fill="#9ca3af" />
  <text x="420" y="80" text-anchor="middle" style="font-family:monospace;font-size:11px;fill:#374151">C++</text>
  <text x="420" y="122" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">1983</text>

  <circle cx="490" cy="100" r="6" fill="#22c55e" />
  <text x="490" y="132" text-anchor="middle" style="font-family:monospace;font-size:11px;font-weight:bold;fill:#15803d">Haskell</text>
  <text x="490" y="148" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">1990</text>

  <circle cx="570" cy="100" r="6" fill="#9ca3af" />
  <text x="570" y="80" text-anchor="middle" style="font-family:monospace;font-size:11px;fill:#374151">Java</text>
  <text x="570" y="122" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">1995</text>

  <circle cx="660" cy="100" r="6" fill="#22c55e" />
  <text x="660" y="132" text-anchor="middle" style="font-family:monospace;font-size:11px;font-weight:bold;fill:#15803d">Clojure</text>
  <text x="660" y="148" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">2007</text>

  <circle cx="730" cy="100" r="6" fill="#facc15" stroke="#111827" />
  <text x="700" y="80" text-anchor="middle" style="font-family:monospace;font-size:11px;font-weight:bold;fill:#78350f">JS (ES6)</text>
  <text x="730" y="122" text-anchor="middle" style="font-family:sans-serif;font-size:10px;fill:#6b7280">2015</text>
</svg>
</div>
<div class="diagram-legend">
<span><span class="dot" style="background:#22c55e"></span>linaje funcional</span>
<span><span class="dot" style="background:#9ca3af"></span>imperativo / POO</span>
<span><span class="dot" style="background:#facc15"></span>JS gana arrow functions, <code>const</code>, spread…</span>
</div>

## De Cálculo Lambda y Clojure a JavaScript

Ya vimos programación funcional dos veces: primero de forma formal, en **Cálculo Lambda** (Unidad 1) — funciones como único elemento del lenguaje, aplicación, sustitución. Después de forma práctica, en **Clojure** (Unidad 3) — un lenguaje diseñado desde cero para programar así: inmutabilidad por defecto, `map`/`filter`/`reduce` nativos, funciones de primera clase.

Ahora vemos el mismo paradigma en **JavaScript**. La pregunta que guía todo este apunte es siempre la misma: *"esto que ya sabemos hacer en Cálculo Lambda y en Clojure, ¿cómo se escribe en JS?"*

### Mismo paradigma, tres lenguajes

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>Cálculo Lambda</h4>

El origen formal: todo es una función. Sin estado, sin mutación — solo sustitución.

<div class="card-note">Notación: <code>λx. x + 1</code></div>
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

### ¿Por qué JS?

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

// devuelve una función nueva
function multiplier(factor) {
  return number => number * factor
}
const double = multiplier(2)
double(5) // => 10
```

`multiplier` es una **fábrica de funciones**: cada llamada crea una función nueva que "recuerda" el valor de `factor` que tenía en ese momento. Esto se llama *closure* (clausura) — la función devuelta mantiene acceso al entorno donde fue creada, aunque `multiplier` ya haya terminado de ejecutarse.

En Cálculo Lambda, una función de orden superior que aplica otra función dos veces:

```text
twice ≡ λf.λx. f (f x)
```

Y en Clojure:

```clojure
(defn twice [f] (fn [x] (f (f x))))
```

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

Este es el mismo principio detrás de la **beta-reducción** en Cálculo Lambda: `(λx. x + x) 5` se puede sustituir directamente por `5 + 5` — funciona precisamente porque no hay estado escondido. Con una función impura esto no vale: `addToTotal(100) + addToTotal(100)` no es lo mismo que calcular una vez y duplicar, porque cada llamada cambia `total`.

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

## `map`, `filter`, `reduce`

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

### `filter`

Se queda con los elementos que cumplen una condición — el array resultante puede ser más chico que el original (o del mismo tamaño, o vacío).

```js
const inStock = products.filter(p => p.stock > 0)
// se descarta el Mouse inalámbrico (stock: 0)

const accessories = products.filter(p => p.category === 'accesorios')
```

Equivalente a `(filter (fn [p] (pos? (:stock p))) products)` en Clojure — la condición es un predicado, `λp. stock(p) > 0`, igual que en Cálculo Lambda.

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

`pipe` va de izquierda a derecha; `compose` va de derecha a izquierda — es el `(comp f g)` de Clojure, y formalmente `λf. λg. λx. f (g x)` de Cálculo Lambda. Notar que `finalPrice` nunca menciona su argumento — eso se llama estilo **point-free** (o *tacit programming*).

## Currying y aplicación parcial

### Currying

Currificar es convertir una función de varios argumentos en una cadena de funciones de un solo argumento — el mismo currying visto en la Unidad 1 (Cálculo Lambda).

```js
// sin currificar
function add(a, b) {
  return a + b
}
add(2, 3)   // => 5

// currificada
const addCurried = a => b => a + b
addCurried(2)(3)   // => 5

const add2 = addCurried(2)   // función parcialmente aplicada, "espera" b
add2(3)                      // => 5
add2(10)                     // => 12
```

Es exactamente `λa. λb. a + b` de Cálculo Lambda, escrito con la sintaxis de arrow functions de JavaScript. Aplicar un argumento a la vez es la razón por la que en Cálculo Lambda una función "de dos argumentos" en realidad no existe — siempre es una función de un argumento que devuelve otra función.

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

JavaScript también trae esto nativo: `fn.bind(null, ...fixedArgs)` hace lo mismo que el `partial` casero de arriba. Es la misma idea que aplicar un solo argumento a una función currificada en Cálculo Lambda: `(λa. λb. a - b) 0.3` deja pendiente `λb. 0.3 - b`.

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

## Esto ya lo sabías

| Cálculo Lambda | Clojure | JavaScript |
|---|---|---|
| `λx. x + 1` | `(map inc coll)` | `coll.map(x => x + 1)` |
| predicado `λx. par(x)` | `(filter even? coll)` | `coll.filter(x => x % 2 === 0)` |
| recursión (combinador Y) | `(reduce + coll)` | `coll.reduce((a, b) => a + b, 0)` |
| `λf. λg. λx. f (g x)` | `(comp f g)` | `compose(f, g)` (casero, o de una librería) |
| `(λa. λb. a - b) 1` | `(partial f a)` | `partial(f, a)` o `f.bind(null, a)` |
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
