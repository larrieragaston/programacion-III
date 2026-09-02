---
theme: bricks
title: Programación III - TypeScript
download: true
info: |
  TypeScript - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: typescript, tipado estático, interfaces, genéricos, INSPT, UTN
transition: slide-left
mdc: true
---

# TypeScript

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/typescript.svg" alt="TypeScript" class="h-16 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# ¿Qué es TypeScript?

<div class="text-sm opacity-80 mb-3">

TypeScript es un **superset** de JavaScript: todo código JS válido es también código TS válido. Agrega anotaciones de tipo que un compilador (`tsc`) chequea — y después **borra por completo** al generar el JavaScript final, sin dejar rastro en runtime. Por eso "tipado **estático**": los tipos se verifican en tiempo de **compilación**, no de ejecución.

</div>

<div class="grid grid-cols-2 gap-4 text-xs">
<div>

**JavaScript**

```js
function applyDiscount(price, rate) {
  return price - price * rate
}

applyDiscount(1000, '10%')
// => NaN, recién se nota en runtime
```

</div>
<div>

**TypeScript**

```ts
function applyDiscount(
  price: number,
  rate: number
): number {
  return price - price * rate
}

applyDiscount(1000, '10%')
// ❌ error de compilación
```

</div>
</div>

<div class="mt-3 text-xs italic opacity-80 text-center">

Mismo bug, mismo lugar — la diferencia es CUÁNDO se detecta: en TS, mientras se escribe el código; en JS, cuando un usuario real llega a ejecutar esa línea.

</div>

---
layout: default
---

# Tipos básicos

```ts
let productName: string = 'Mouse'
let price: number = 18000
let inStock: boolean = true

inStock = 'sí'   // ❌ Type 'string' is not assignable to type 'boolean'

let ids: number[] = [1, 2, 3]          // array de numbers
let names: Array<string> = ['Mouse']    // misma idea, sintaxis genérica

let point: [number, number] = [10, 20]   // tupla: largo y tipos fijos
```

<div class="mt-3 text-sm opacity-80">

`number[]` y `Array<number>` son exactamente lo mismo, dos formas de escribir el mismo tipo. La segunda forma ya es una pista de lo que viene más adelante: los **genéricos**. En JS puro, la línea de `inStock = 'sí'` no tira ningún error — el valor simplemente cambia de tipo en silencio, y cualquier código que esperaba un `boolean` ahí puede romperse más adelante, sin aviso.

</div>

---
layout: default
---

# Inferencia de tipos

```ts
let productName = 'Mouse'   // TS infiere: string
let price = 18000            // TS infiere: number

price = '18000'               // ❌ Type 'string' is not assignable to type 'number'
```

<div class="mt-4 text-sm opacity-80">

No hace falta anotar **todo** — si TypeScript puede deducir el tipo a partir del valor inicial, alcanza con eso. Las anotaciones explícitas (`: string`, `: number`) importan sobre todo en las firmas de funciones, donde no hay un valor inicial del que inferir — como en `applyDiscount`, un par de slides atrás.

</div>

---
layout: default
---

# Tipar funciones

```ts
function applyDiscount(price: number, rate: number = 0.1): number {
  return price - price * rate
}

function logStockWarning(product: string, remaining?: number): void {
  console.warn(remaining ? `${product}: quedan ${remaining}` : `${product}: sin stock`)
}

applyDiscount(1000)              // usa el rate por defecto: 0.1
logStockWarning('Mouse')          // remaining es opcional, se puede omitir
```

<div class="mt-4 text-sm opacity-80">

Parámetros y retorno se anotan igual que las variables. `rate: number = 0.1` es un parámetro **con valor por defecto**; `remaining?: number` es **opcional** — se puede omitir al llamar la función. `void` indica que la función no devuelve nada útil, como `logStockWarning`, que solo tiene un efecto (un `console.warn`). En JS puro, llamar a `logStockWarning('Mouse', '5')` con un string en vez de un número no tira ningún error — acá sí, apenas se escribe la línea.

</div>

---
layout: default
---

# `any` vs. `unknown`

```ts
// llega como respuesta de una API — en JS puro, esto es "cualquier cosa"
function parseProduct(json: any) {
  return json.name.toUpperCase()   // ✅ compila — TS no chequea nada sobre "any"
}
parseProduct({ precio: 100 })       // explota en runtime: json.name es undefined

function parseProductSafe(json: unknown) {
  if (typeof json === 'object' && json !== null && 'name' in json) {
    return (json as { name: string }).name.toUpperCase()   // ✅ ya lo comprobamos
  }
  throw new Error('JSON inválido: no tiene name')
}
```

<div class="mt-4 text-sm opacity-80">

`any` **apaga el chequeo de tipos** por completo — es escribir JS dentro de TS, y anula el motivo por el que se eligió TypeScript. `unknown` es la alternativa segura: acepta cualquier valor igual (útil para datos externos como una respuesta HTTP), pero obliga a comprobar la forma real (*narrowing*, próxima slide) antes de operar con él. `as { name: string }` es una **type assertion**: el "casteo" de TypeScript — le dice al compilador "confiá en que esto tiene esta forma", sin volver a chequearlo. A diferencia de un cast en Java/C#, no convierte nada en runtime: es pura información para el compilador, se borra al compilar — si te equivocás, el error aparece después, en runtime. Por eso hay que usarlo solo después de haber comprobado algo de verdad, como con el `if` de arriba.

</div>

---
layout: default
---

# Union types y narrowing

```ts
function formatProductId(id: string | number): string {
  if (typeof id === 'number') {
    return id.toString().padStart(6, '0')
  }
  return id.toUpperCase()
}

formatProductId(42)      // => "000042"
formatProductId('mou1')  // => "MOU1"
```

<div class="mt-4 text-sm opacity-80">

`string | number` es un **union type**: el valor puede ser cualquiera de los dos. Dentro del `if`, TypeScript **angosta** (*narrows*) el tipo automáticamente según el chequeo (`typeof`) — dentro de esa rama, `id` ya es tratado como `number`, sin necesitar ninguna conversión manual. El `'name' in json` de la slide anterior es otra forma de narrowing: comprueba si existe una propiedad, en vez del tipo primitivo.

</div>

---
layout: default
---

# `?.`, `??` y `!`: trabajar con valores ausentes

```ts
function getStock(product?: Product): number {
  return product?.stock ?? 0
}

getStock(undefined)                              // => 0
getStock({ name: 'Mouse', price: 1, stock: 5 })    // => 5

const trusted = product!.stock   // "confiá en mí, esto no es null/undefined"
```

<div class="mt-3 text-sm opacity-80">

**`?.`** (*optional chaining*): si lo de la izquierda es `null`/`undefined`, corta ahí y devuelve `undefined`, en vez de explotar. **`??`** (*nullish coalescing*): da un valor por defecto **solo** si lo de la izquierda es `null`/`undefined` — a diferencia de `||`, que también reemplazaría `0`, `''` o `false` (un error común: `stock ?? 0` mantiene un stock de `0` real, `stock || 0` lo pisaría por las dudas).

</div>

<v-click>

<div class="mt-2 text-xs opacity-80">

**`!`** (*non-null assertion*) apaga el chequeo puntual: le decís al compilador que confíe en que ahí nunca va a haber `null`/`undefined`. Si te equivocás, explota en runtime exactamente igual que sin TypeScript — usarlo con cuidado, solo cuando estás realmente seguro.

</div>

</v-click>

---
layout: default
---

# Literal types

```ts
type ProductCategory = 'electronics' | 'clothing' | 'books'

function shippingDays(category: ProductCategory): number {
  return category === 'books' ? 2 : 5
}

shippingDays('electronics')   // ✅
shippingDays('food')          // ❌ Type '"food"' is not assignable...
```

<div class="mt-4 text-sm opacity-80">

Un **literal type** no es "un string cualquiera" — es exactamente ese valor, o uno de un conjunto cerrado de valores. Es una forma de modelar, con el propio sistema de tipos, un conjunto fijo de opciones válidas (una alternativa más liviana a un `enum`, que se ve más adelante, cuando alcanza con comparar strings).

</div>

---
layout: center
---

# Modelar objetos: `interface` y `type`

---
layout: default
---

# `interface`

```ts
interface Product {
  name: string
  price: number
  stock: number
  discount?: number   // propiedad opcional
}

function describe(product: Product): string {
  return `${product.name} — $${product.price}`
}

const mouse: Product = { name: 'Mouse', price: 18000, stock: 5 }
```

<div class="mt-4 text-sm opacity-80">

`interface` define la **forma** de un objeto: qué propiedades tiene y de qué tipo es cada una. Cualquier objeto que "encaje" en esa forma es válido — no hace falta declarar explícitamente que `mouse` "implementa" `Product`, alcanza con que tenga las propiedades correctas (*structural typing*, distinto del *nominal typing* de Java/C#, donde sí hay que declarar la relación explícitamente).

</div>

<v-click>

<div class="mt-2 text-xs opacity-80">

En JS puro, este typo no lo detecta nadie hasta que alguien ejecute `describe(mouse)` y el resultado salga mal:

```js
const mouse = { name: 'Mouse', pryce: 18000, stock: 5 }   // "pryce", nadie avisa
```

</div>

</v-click>

---
layout: default
---

# Extender interfaces

```ts
interface Product {
  name: string
  price: number
}

interface DigitalProduct extends Product {
  downloadUrl: string
  sizeInMb: number
}

const ebook: DigitalProduct = {
  name: 'Curso de TS',
  price: 5000,
  downloadUrl: '/files/curso-ts.pdf',
  sizeInMb: 12,
}
```

<div class="mt-4 text-sm opacity-80">

`extends` combina interfaces — `DigitalProduct` tiene las propiedades propias más todas las de `Product`. Útil para modelar variantes de un mismo concepto sin repetir campos comunes.

</div>

---
layout: default
---

# `readonly`: inmutabilidad con tipos

```ts
interface Product {
  readonly id: number
  name: string
  price: number
}

function renameProduct(product: Product, name: string) {
  product.id = 999       // ❌ Cannot assign to 'id' because it is a read-only property
  product.name = name     // ✅ esto sí se puede
}

const ids: readonly number[] = [1, 2, 3]
ids.push(4)   // ❌ Property 'push' does not exist on type 'readonly number[]'
```

<div class="mt-4 text-sm opacity-80">

La misma idea de no mutar que vieron en JS Funcional con `map`/`filter` (crear algo nuevo en vez de modificar lo existente) — ahora reforzada por el compilador. `readonly` no cambia nada en el JavaScript final (se borra al compilar, como todo tipo), pero avisa **en tiempo de compilación** si el propio código intenta reasignar una propiedad o mutar un array que se declaró como si no debiera cambiar.

</div>

---
layout: default
---

# `as const`: ¿y las constantes?

```ts
const config = { role: 'admin', level: 1 }
config.role = 'user'          // ✅ compila — el objeto no es readonly, solo la variable

const frozen = { role: 'admin', level: 1 } as const
frozen.role = 'user'          // ❌ Cannot assign to 'role' because it is a read-only property

let role = 'admin'            // tipo: string
let fixedRole = 'admin' as const   // tipo: 'admin' (literal, no se ensancha)
```

<div class="mt-3 text-sm opacity-80">

`const` (de JS) solo evita **reasignar la variable** — el objeto que contiene se puede seguir mutando por dentro, como `config.role` arriba. `as const` (de TS) es la pieza que faltaba: es el mismo `as` que ya vieron para castear (`any vs. unknown`), aplicado no a un tipo propio sino a la palabra `const` — le pide al compilador tratar el valor como su versión más específica posible: todas las propiedades pasan a ser `readonly` de forma recursiva, y los strings/numbers quedan fijados como su valor literal en vez de ensancharse a `string`/`number`. Es la forma de lograr, con un objeto, algo parecido a lo que `const` ya hacía con un primitivo.

</div>

---
layout: default
---

# `type`

```ts
type Product = {
  name: string
  price: number
}

type ID = string | number                          // alias para un union type
type Handler = (event: string) => void               // tipo de una función
type ProductOrId = Product | ID                       // combinación de otros tipos
```

<div class="mt-4 text-sm opacity-80">

`type` es más general que `interface`: además de objetos, puede nombrar unions, tipos primitivos, tipos de función y combinaciones entre todos ellos. `interface` solo describe objetos — y tiene un comportamiento particular que vale la pena conocer antes de elegir entre uno y otro.

</div>

---
layout: default
---

# Ojo con las interfaces: se fusionan

```ts
interface Product { name: string }
// en otro archivo del mismo proyecto, sin saber que ya existía...
interface Product { price: number }
// TS no avisa nada — combina ambas declaraciones en una sola
const mouse: Product = { name: 'Mouse', price: 18000 }   // ✅ compila
```

<div class="mt-2 text-xs opacity-80">

Esto se llama ***declaration merging***: dos `interface` con el **mismo nombre** no chocan, TS las combina sola. Es una función real y deliberada (extender un tipo de una librería que no controlás) — pero en un proyecto grande, si dos módulos usan el mismo nombre **sin querer**, la fusión es silenciosa, y el error puede aparecer mucho después, lejos de la causa real.

</div>

<v-click>

<div class="mt-2 text-xs opacity-80">

```ts
type Product = { name: string }
type Product = { price: number }   // ❌ Error: Duplicate identifier 'Product'.
```

`type` es más estricto acá: el mismo nombre dos veces es directamente un error de compilación. Por eso, en equipos grandes, hay quienes prefieren `type` para que un choque de nombres accidental se note enseguida, en vez de fusionarse en silencio.

</div>

</v-click>

---
layout: default
---

# `interface` vs. `type`: cuál usar

<div class="grid grid-cols-2 gap-6 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100">

**`interface`**

- Pensada para la forma de objetos y clases.
- Se puede extender (`extends`) y **fusiona** declaraciones repetidas del mismo nombre (a propósito o no).
- Mensajes de error algo más legibles en objetos complejos.

<div class="mt-2 text-xs opacity-70">Preferirla para modelar entidades: props de componentes, modelos de datos.</div>
</div>
<div class="p-4 rounded-lg bg-yellow-50 border border-yellow-300">

**`type`**

- Sirve para *cualquier* tipo: objetos, unions, primitivos, funciones.
- **No** se puede reabrir/fusionar después de declarado — nombre repetido es error.

<div class="mt-2 text-xs opacity-70">Preferirlo para unions, tipos de función, o cuando un choque de nombres debe fallar fuerte.</div>
</div>
</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

En la práctica se mezclan todo el tiempo en un mismo proyecto — la regla general es "objetos con <code>interface</code>, todo lo demás con <code>type</code>", pero no es una ley estricta.

</div>

---
layout: default
---

# `enum`

```ts
enum UserRole {
  Student = 'student',
  Teacher = 'teacher',
  Admin = 'admin',
}

function greetUser(role: UserRole) {
  if (role === UserRole.Admin) console.log('Bienvenido, administrador')
}

greetUser(UserRole.Teacher)
```

<div class="mt-4 text-sm opacity-80">

Un `enum` agrupa un conjunto fijo de valores con nombre. Cumple un propósito parecido al de los literal types (`ProductCategory`, unas slides atrás) — la diferencia es que un `enum` existe también en el JavaScript compilado (genera código real), mientras que los literal types desaparecen por completo al compilar. Para casos simples, muchos equipos hoy prefieren un union de literal types por ser más liviano; `enum` sigue siendo útil cuando el conjunto de valores necesita existir también como objeto en runtime.

</div>

---
layout: center
---

# Genéricos

---
layout: default
---

# ¿Qué es un genérico?

```ts
function identity<T>(value: T): T {
  return value
}

identity<number>(42)        // T = number  → devuelve 42
identity<string>('hola')    // T = string  → devuelve 'hola'

identity<number>('hola')    // ❌ Argument of type 'string' is not assignable to parameter of type 'number'
```

<div class="mt-3 text-sm opacity-80">

Un **genérico** es un tipo que recibe otro tipo como parámetro — igual que un parámetro común, pero en vez de un valor se pasa un tipo. `<T>` declara esa "variable de tipo": se completa en cada llamada (`T = number`, `T = string`, ...), y TypeScript chequea que el argumento realmente coincida con lo que se pidió. Sin nombrarlo, ya lo venían usando: `Array<T>` y `Promise<T>` son genéricos — vuelven en la próxima slide.

</div>

---
layout: default
---

# Genéricos en objetos: `interface<T>`

```ts
interface ApiResponse<T> {
  data: T
  status: number
}

const productResponse: ApiResponse<Product> = {
  data: { name: 'Mouse', price: 18000, stock: 5 },
  status: 200,
}

const listResponse: ApiResponse<Product[]> = {
  data: [{ name: 'Mouse', price: 18000, stock: 5 }],
  status: 200,
}
```

<div class="mt-3 text-sm opacity-80">

La misma idea aplicada a un objeto en vez de a una función: `ApiResponse<T>` es una plantilla, no un tipo cerrado — `data` va a tener la forma de lo que sea `T` en cada uso. `ApiResponse<Product>` y `ApiResponse<Product[]>` son dos tipos distintos, generados a partir de la misma interfaz genérica, sin escribirla dos veces.

</div>

---
layout: default
---

# Ya los venían usando: `Array<T>` y `Promise<T>`

```ts
let ids: number[]        // "array de numbers"
let ids: Array<number>   // mismo tipo — azúcar sintáctico de lo mismo

async function fetchProduct(id: number): Promise<Product> {
  const res = await fetch(`/api/products/${id}`)
  return res.json()
}

const mouse = await fetchProduct(1)
mouse.price   // TS sabe que es number, sin castear nada a mano
```

<div class="mt-3 text-sm opacity-80">

Mismo patrón que `identity<T>` y `ApiResponse<T>`: una plantilla (`Array<T>`, `Promise<T>`) con un tipo concreto adentro. `Array<number>` es "un array donde `T = number`"; `Promise<Product>` es "una promesa que, cuando se resuelve, entrega un `Product`" — el genérico que vieron en Asincronismo, ahora con nombre y sabiendo por qué funciona así.

</div>

---
layout: default
---

# Por qué hace falta un genérico propio

```ts
// opción 1: una función por cada tipo — funciona, pero no escala
function firstElementNumber(list: number[]): number | undefined { return list[0] }
// firstElementString, firstElementProduct... una más por cada tipo nuevo
// opción 2: unificarlas con "any" — escala, pero se pierde el tipo
function firstElementAny(list: any[]) {
  return list[0]
}

const p = firstElementAny([{ name: 'Mouse', price: 18000 }])
p.priec   // typo — y TS no dice nada, porque "any" no chequea nada
```

<div class="mt-2 text-xs opacity-80">

Escribir una función por tipo funciona, pero obliga a duplicar la misma lógica cada vez. Unificarlas con `any[]` evita la duplicación, pero devuelve `any` — se pierde el tipo, y un typo como `p.priec` compila igual. Hace falta una sola función que mantenga el tipo específico de cada llamada: ahí entra un genérico propio.

</div>

---
layout: default
---

# Escribir un genérico propio

```ts
function firstElement<T>(list: T[]): T | undefined {
  return list[0]
}

const products: Product[] = [
  { name: 'Mouse', price: 18000, stock: 5 },
  { name: 'Teclado', price: 25000, stock: 3 },
]

const p = firstElement(products)   // tipo: Product | undefined
p?.priec   // ❌ TS avisa: Property 'priec' does not exist — ahora sí

firstElement([1, 2, 3])        // tipo: number | undefined
firstElement(['a', 'b'])       // tipo: string | undefined
```

<div class="mt-3 text-sm opacity-80">

`<T>` declara un **parámetro de tipo**: una variable que representa "el tipo que sea, decidido en cada llamada". La misma función funciona para arrays de cualquier tipo, y TypeScript infiere `T` automáticamente a partir del argumento — sin escribir la función una vez por tipo ni resignar el chequeo con `any`, como en la slide anterior.

</div>

---
layout: default
---

# Utility types: transformar tipos existentes

```ts
interface Product {
  name: string
  price: number
  stock: number
}

type ProductPreview = Pick<Product, 'name' | 'price'>   // solo esas dos props
type ProductUpdate = Partial<Product>                     // todas las props, opcionales
type ProductWithoutStock = Omit<Product, 'stock'>         // todas menos esa
type ProductCatalog = Record<string, Product>             // diccionario: clave → Product
function updateProduct(id: number, changes: ProductUpdate) { /* ... */ }
updateProduct(1, { price: 15000 })   // ✅ no hace falta pasar el objeto completo
```

<div class="mt-2 text-xs opacity-80">

`Pick`, `Partial`, `Omit` y `Record` son **genéricos ya incluidos** en TS: toman un tipo y devuelven una versión transformada. Útiles para tipar un `PATCH` HTTP o un diccionario — van a volver a aparecer en React y Node.

</div>

---
layout: center
---

# Probar y correr TypeScript

---
layout: default
---

# La forma más rápida: el Playground

<div class="mt-2 text-sm opacity-80">

No hace falta instalar nada para probar los ejemplos de esta clase: en <a href="https://www.typescriptlang.org/play">typescriptlang.org/play</a> se escribe TypeScript en el navegador y se ve todo en vivo.

</div>

<div class="mt-4 grid grid-cols-1 gap-2 text-sm">
<div class="p-2 rounded bg-gray-100">Panel izquierdo: el código TypeScript que vas escribiendo</div>
<div class="p-2 rounded bg-gray-100">Panel derecho: el JavaScript que genera — para ver qué "le hace" el compilador</div>
<div class="p-2 rounded bg-gray-100">Los errores de tipos aparecen subrayados en rojo ahí mismo, sin compilar nada a mano</div>
</div>

<div class="mt-4 text-sm italic opacity-80">

Todavía no vimos cómo armar un proyecto de Node — para ir probando código TypeScript por su cuenta, esta es la forma más simple.

</div>

---
layout: default
---

# Instalar y correr TypeScript en tu máquina

```bash
npm install -g typescript ts-node   # instalación global — sin armar un proyecto

tsc archivo.ts          # compila un archivo suelto → archivo.js
node archivo.js           # => 900

ts-node archivo.ts       # compila y ejecuta en un solo paso, sin generar el .js
```

<div class="mt-4 text-sm opacity-80">

No hace falta un proyecto de Node (con `package.json`, carpetas `src/`, etc.) para esto: alcanza con instalar TypeScript de forma global y correrlo sobre un único archivo suelto. Cuando más adelante armen un proyecto real — con React, por ejemplo — van a instalar TypeScript como dependencia **de ese proyecto** en vez de global, y ahí sí van a ver un `package.json`, un `tsconfig.json` y una estructura de carpetas armados en serio.

</div>

---
layout: default
---

# `tsconfig.json`

```bash
npx tsc --init   # genera un tsconfig.json con valores por defecto comentados
```

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
```

<div class="mt-3 text-sm opacity-80">

Apenas armen un proyecto real (por ejemplo, con React) va a aparecer uno de estos junto al `package.json`. `tsconfig.json` le dice al compilador (`tsc`) qué archivos compilar y con qué reglas. `target` fija a qué versión de JS se transpila; `outDir`/`rootDir` separan fuente y salida; `esModuleInterop` permite mezclar `import`/`export` con paquetes viejos de CommonJS sin fricción.

</div>

---
layout: default
---

# `tsconfig.json`: opciones que importan

```json
{
  "compilerOptions": {
    "strict": true,
    "lib": ["ES2022", "DOM"],
    "sourceMap": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

<div class="mt-3 text-xs opacity-80">

`strict: true` en realidad activa **varios** flags a la vez — entre ellos `noImplicitAny` (obliga a tipar en vez de inferir `any` en silencio) y `strictNullChecks` (`null`/`undefined` dejan de aceptarse en cualquier lado, hay que declararlos explícitamente: de ahí sale la necesidad de `?.`/`??` de unas slides atrás). `lib` importa cuando el código usa APIs del navegador (`document`, `fetch`) — sin `"DOM"` ahí, TS ni sabe que existen. `sourceMap` permite debuggear el `.ts` original en el navegador/editor, no el `.js` compilado. `skipLibCheck` acelera la compilación salteando el chequeo de tipos de las librerías instaladas. `include`/`exclude` acotan qué carpetas mira el compilador — **muy recomendado**, sobre todo `strict`, en cualquier proyecto nuevo.

</div>

---
layout: default
---

# Cómo leer un error de compilación

```ts
applyDiscount(1000, '10%')
```

```
archivo.ts:5:21 - error TS2345: Argument of type 'string' is not
assignable to parameter of type 'number'.

5 applyDiscount(1000, '10%')
                      ~~~~~~
```

<div class="mt-3 text-xs opacity-80">

**`archivo:línea:columna`** — dónde está el problema. **`TS2345`** — el código del error (googleable: buscar "TS2345" lleva directo a la explicación). El mensaje describe qué esperaba TS y qué recibió. El **`~~~~~~`** señala la expresión exacta que lo disparó — no toda la línea.

</div>

<div class="mt-3 grid grid-cols-1 gap-1 text-xs">
<div class="p-2 rounded bg-gray-100"><code>TS2322</code> — un valor no es asignable a ese tipo (lo más común)</div>
<div class="p-2 rounded bg-gray-100"><code>TS2339</code> — esa propiedad no existe en el tipo (típico de un typo)</div>
<div class="p-2 rounded bg-gray-100"><code>TS2345</code> — un argumento no coincide con el parámetro esperado</div>
<div class="p-2 rounded bg-gray-100"><code>TS18048</code> / <code>TS2532</code> — el valor puede ser <code>undefined</code>, hay que comprobarlo antes</div>
</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-1 text-xs">
<div>

**Tipos**

| Forma | Ejemplo |
|---|---|
| Primitivos | `string`, `number`, `boolean` |
| Array / Tupla | `number[]`, `[number, number]` |
| Union | `string \| number` |
| Literal | `'electronics' \| 'books'` |
| Función | `(a: number) => string` |
| Ausencia / inmutable | `?.`, `??`, `!`, `readonly`, `as const` |

</div>
<div>

**Modelado y genéricos**

| Forma | Ejemplo |
|---|---|
| Objeto | `interface Product { name: string }` |
| Alias | `type ID = string \| number` |
| Extender | `interface B extends A {}` |
| Genérico | `Array<T>`, `Promise<T>` |
| Genérico propio | `function f<T>(x: T): T` |
| Utility types | `Partial<T>`, `Pick<T,K>`, `Omit<T,K>` |
| Config | `tsconfig.json` + `tsc` / `ts-node` |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2">

- [typescriptlang.org — Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — documentación oficial, completa y bien organizada
- [typescriptlang.org — Playground](https://www.typescriptlang.org/play) — probar TS en el navegador, sin instalar nada, útil para demos en vivo
- [typescriptlang.org — TSConfig Reference](https://www.typescriptlang.org/tsconfig) — todas las opciones de `tsconfig.json`, explicadas una por una
- [typescriptlang.org — Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html) — referencia de `Partial`, `Pick`, `Omit`, `Record` y el resto
- [totaltypescript.com](https://www.totaltypescript.com/) — artículos y ejercicios gratuitos de nivel intermedio/avanzado, de Matt Pocock
- [freeCodeCamp — Learn TypeScript](https://www.freecodecamp.org/news/learn-typescript-beginners-guide/) — curso introductorio gratuito, con proyecto práctico
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) — convenciones reales de un equipo grande, útil para ver cómo se usa TS "en serio"
- [type-challenges](https://github.com/type-challenges/type-challenges) — ejercicios de la comunidad para practicar el sistema de tipos, de básico a muy avanzado
- [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped) — el repositorio de tipos (`@types/...`) para librerías JS que no traen los suyos

</div>
