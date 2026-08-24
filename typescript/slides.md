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

# El pivot de la unidad

- Todo lo anterior — JS Funcional, JS Contemporáneo, Asincronismo — fue **JavaScript puro**.
- De acá en adelante — React, Node + Express, MongoDB — el código de este curso se presenta en **TypeScript**.
- Ya usaron algo parecido a un genérico sin llamarlo así: `Promise<T>`, de Asincronismo. Vuelve a aparecer hoy, ahora explicado.

<div class="mt-6 text-sm italic opacity-80">

No es un lenguaje nuevo — es JavaScript con una capa extra encima. La pregunta de hoy es qué problema resuelve esa capa.

</div>

---
layout: default
---

# El problema que resuelve

```js
// JavaScript — esto compila y corre sin quejarse
function applyDiscount(price, rate) {
  return price - price * rate
}

applyDiscount(1000, 0.1)     // => 900, como se esperaba
applyDiscount(1000, '10%')   // => NaN — el error aparece recién en producción
```

<v-click>

<div class="mt-4 text-sm opacity-80">

JavaScript es dinámico: no hay que declarar tipos, lo cual da flexibilidad — pero errores tontos como pasar un string donde se esperaba un número recién se descubren **en tiempo de ejecución**, muchas veces lejos de donde ocurrió el error real.

</div>

</v-click>

---
layout: default
---

# TypeScript: JS + una capa de tipos

```ts
function applyDiscount(price: number, rate: number): number {
  return price - price * rate
}

applyDiscount(1000, 0.1)     // ✅ compila
applyDiscount(1000, '10%')   // ❌ error de compilación, antes de correr nada
// Argument of type 'string' is not assignable to parameter of type 'number'.
```

<div class="mt-4 text-sm opacity-80">

TypeScript es un **superset** de JavaScript: todo código JS válido es también código TS válido. Agrega anotaciones de tipo que el compilador (`tsc`) chequea — y después **borra por completo** al generar el JavaScript final. En runtime no queda ni rastro de TypeScript.

</div>

<v-click>

<div class="mt-2 text-sm italic opacity-80">

Por eso "tipado estático": los tipos se verifican en tiempo de **compilación**, no en tiempo de ejecución — el objetivo es adelantar el error al momento de escribir el código, no descubrirlo con un usuario real en producción.

</div>

</v-click>

---
layout: default
---

# Tipos básicos

```ts
let name: string = 'Ada'
let age: number = 29
let isActive: boolean = true

let ids: number[] = [1, 2, 3]        // array de numbers
let names: Array<string> = ['Ada']    // misma idea, sintaxis genérica

let point: [number, number] = [10, 20]   // tupla: largo y tipos fijos
```

<div class="mt-4 text-sm opacity-80">

`number[]` y `Array<number>` son exactamente lo mismo, dos formas de escribir el mismo tipo. La segunda forma ya es una pista de lo que viene más adelante: los **genéricos**.

</div>

---
layout: default
---

# Inferencia de tipos

```ts
let name = 'Ada'        // TS infiere: string
let age = 29             // TS infiere: number

name = 42                 // ❌ Type 'number' is not assignable to type 'string'
```

<div class="mt-4 text-sm opacity-80">

No hace falta anotar **todo** — si TypeScript puede deducir el tipo a partir del valor inicial, alcanza con eso. Las anotaciones explícitas (`: string`, `: number`) importan sobre todo en las firmas de funciones, donde no hay un valor inicial del que inferir.

</div>

---
layout: default
---

# Tipar funciones

```ts
function greet(name: string, greeting: string = 'Hola'): string {
  return `${greeting}, ${name}!`
}

function logError(message: string, code?: number): void {
  console.error(code ? `[${code}] ${message}` : message)
}

const double = (x: number): number => x * 2
```

<div class="mt-4 text-sm opacity-80">

Parámetros y retorno se anotan igual que las variables. `code?: number` marca un parámetro **opcional** — se puede omitir al llamar la función. `void` indica que la función no devuelve nada útil (como `logError`, que solo tiene un efecto).

</div>

---
layout: default
---

# `any` vs. `unknown`

```ts
let a: any = 'hola'
a.toUpperCase()   // ✅ compila — TS no chequea nada sobre "any"
a()                  // ✅ compila también — y explota en runtime

let b: unknown = 'hola'
b.toUpperCase()   // ❌ error de compilación: hay que angostar el tipo primero

if (typeof b === 'string') {
  b.toUpperCase()   // ✅ ahora sí — TS sabe que acá b es un string
}
```

<div class="mt-4 text-sm opacity-80">

`any` **apaga el chequeo de tipos** por completo para esa variable — es escribir JS dentro de TS, y anula el motivo por el que se eligió TypeScript. `unknown` es la alternativa segura: acepta cualquier valor igual, pero obliga a comprobar el tipo (*narrowing*, próxima slide) antes de operar con él.

</div>

---
layout: default
---

# Union types y narrowing

```ts
function formatId(id: string | number): string {
  if (typeof id === 'number') {
    return id.toString().padStart(6, '0')
  }
  return id.toUpperCase()
}

formatId(42)       // => "000042"
formatId('abc')    // => "ABC"
```

<div class="mt-4 text-sm opacity-80">

`string | number` es un **union type**: el valor puede ser cualquiera de los dos. Dentro del `if`, TypeScript **angosta** (*narrows*) el tipo automáticamente según el chequeo (`typeof`) — dentro de esa rama, `id` ya es tratado como `number`, sin necesitar ninguna conversión manual.

</div>

---
layout: default
---

# Literal types

```ts
let role: 'alumno' | 'profesor' | 'admin'

role = 'alumno'      // ✅
role = 'invitado'    // ❌ Type '"invitado"' is not assignable...
```

<div class="mt-4 text-sm opacity-80">

Un **literal type** no es "un string cualquiera" — es exactamente ese valor, o uno de un conjunto cerrado de valores. Es una forma de modelar, con el propio sistema de tipos, un conjunto fijo de opciones válidas (una alternativa más liviana a un `enum` cuando alcanza con comparar strings).

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

`type` es más general que `interface`: además de objetos, puede nombrar unions, tipos primitivos, tipos de función y combinaciones entre todos ellos. `interface` solo describe objetos (y se puede extender/fusionar de formas que `type` no permite).

</div>

---
layout: default
---

# `interface` vs. `type`: cuál usar

<div class="grid grid-cols-2 gap-6 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100">

**`interface`**

- Pensada para la forma de objetos y clases.
- Se puede extender (`extends`) y fusionar declaraciones del mismo nombre.
- Mensajes de error algo más legibles en objetos complejos.

<div class="mt-2 text-xs opacity-70">Preferirla para modelar entidades: props de componentes, modelos de datos.</div>
</div>
<div class="p-4 rounded-lg bg-yellow-50 border border-yellow-300">

**`type`**

- Sirve para *cualquier* tipo: objetos, unions, primitivos, funciones.
- No se puede reabrir/fusionar después de declarado.

<div class="mt-2 text-xs opacity-70">Preferirlo para unions, tipos de función, o combinaciones de otros tipos.</div>
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

Un `enum` agrupa un conjunto fijo de valores con nombre. Cumple un propósito parecido al de los literal types (`'alumno' | 'profesor'`) vistos antes — la diferencia es que un `enum` existe también en el JavaScript compilado (genera código real), mientras que los literal types desaparecen por completo al compilar. Para casos simples, muchos equipos hoy prefieren un union de literal types por ser más liviano; `enum` sigue siendo útil cuando el conjunto de valores necesita existir también como objeto en runtime.

</div>

---
layout: center
---

# Genéricos

---
layout: default
---

# El genérico que ya usaban

```ts
let ids: number[]        // "array de numbers"
let ids: Array<number>   // mismo tipo — Array es un genérico, number es su parámetro

let names: Array<string>
let flags: Array<boolean>
```

<div class="mt-4 text-sm opacity-80">

Un **genérico** es un tipo que recibe otro tipo como parámetro — `Array<T>` no es un tipo fijo, es una plantilla: `Array<number>`, `Array<string>` y `Array<boolean>` son cada uno un tipo distinto, generado a partir de la misma plantilla `Array<T>`. Ya lo venían usando en la slide de tipos básicos, sin el nombre.

</div>

---
layout: default
---

# El genérico de Asincronismo: `Promise<T>`

```ts
async function fetchUser(id: number): Promise<{ name: string; age: number }> {
  const res = await fetch(`/api/users/${id}`)
  return res.json()
}

const user = await fetchUser(1)
user.name   // TS sabe que esto es un string — sin castear nada a mano
```

<div class="mt-4 text-sm opacity-80">

Toda función `async` devuelve una `Promise` — en TypeScript, se tipa **qué** va a resolver esa promesa: `Promise<{ name: string; age: number }>` significa "una promesa que, cuando se resuelve, entrega un objeto con esa forma". Es la misma idea de <code>Array&lt;T&gt;</code> aplicada a Promises — el genérico que vieron en Asincronismo sin nombrarlo todavía.

</div>

---
layout: default
---

# Escribir un genérico propio

```ts
function firstElement<T>(list: T[]): T | undefined {
  return list[0]
}

firstElement([1, 2, 3])          // => number | undefined
firstElement(['a', 'b'])         // => string | undefined
firstElement([true, false])      // => boolean | undefined
```

<div class="mt-4 text-sm opacity-80">

`<T>` declara un **parámetro de tipo**: una variable que representa "el tipo que sea, decidido en cada llamada". La misma función funciona para arrays de cualquier tipo, y TypeScript infiere `T` automáticamente a partir del argumento — sin escribir la función tres veces (una por tipo) ni resignar el chequeo de tipos con `any`.

</div>

---
layout: center
---

# Repaso funcional, ahora tipado

---
layout: default
---

# Tipando `map`/`filter`/`reduce`

```ts
interface Product {
  name: string
  price: number
}

const products: Product[] = [
  { name: 'Mouse', price: 18000 },
  { name: 'Teclado', price: 25000 },
]

const names: string[] = products.map((p) => p.name)
const expensive: Product[] = products.filter((p) => p.price > 20000)
const total: number = products.reduce((sum, p) => sum + p.price, 0)
```

<div class="mt-4 text-sm opacity-80">

Los mismos `map`/`filter`/`reduce` de JS Funcional — ahora TypeScript conoce la forma de cada elemento (<code>Product</code>) y el tipo de cada resultado, y avisa en el momento si, por ejemplo, se intenta sumar <code>p.name</code> en vez de <code>p.price</code>.

</div>

---
layout: default
---

# Tipando `compose`

```ts
function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C {
  return (a: A) => f(g(a))
}

const double = (x: number): number => x * 2
const toCurrency = (x: number): string => `$${x}`

const doubleAndFormat = compose(toCurrency, double)
doubleAndFormat(500)   // => "$1000"
```

<div class="mt-4 text-sm opacity-80">

`compose` de JS Funcional, tipado con **tres** parámetros de tipo genéricos (`A`, `B`, `C`): el tipo de entrada, el tipo intermedio que devuelve `g`, y el tipo final que devuelve `f`. TypeScript encadena los tipos automáticamente y avisaría si se intentara componer dos funciones cuyos tipos no calzan.

</div>

---
layout: center
---

# Configurar un proyecto TS

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

<div class="mt-4 text-sm opacity-80">

`tsconfig.json` le dice al compilador (`tsc`) qué archivos compilar y con qué reglas. `target` fija a qué versión de JS se transpila; `outDir`/`rootDir` separan fuente y salida; `strict: true` activa el conjunto completo de chequeos estrictos — **muy recomendado** en proyectos nuevos, aunque el ejemplo de la slide anterior (<code>any</code>) siga siendo válido incluso con <code>strict</code> activado, salvo que además se active <code>noImplicitAny</code>.

</div>

---
layout: default
---

# Correr un proyecto TS

```bash
npx tsc              # compila una vez, según tsconfig.json
npx tsc --watch       # recompila automáticamente en cada cambio

npx ts-node src/index.ts   # compila y ejecuta en un solo paso, sin generar .js
```

<div class="mt-4 text-sm opacity-80">

Dos flujos habituales: **compilar y correr** (`tsc` genera el `.js` en `outDir`, después se corre con `node`) o **correr directo** con `ts-node`, que compila en memoria sobre la marcha — más cómodo mientras se desarrolla, no pensado para producción.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-4 text-xs">
<div>

**Tipos**

| Forma | Ejemplo |
|---|---|
| Primitivos | `string`, `number`, `boolean` |
| Array | `number[]` o `Array<number>` |
| Tupla | `[number, number]` |
| Union | `string \| number` |
| Literal | `'alumno' \| 'profesor'` |
| Función | `(a: number) => string` |

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
- [typescriptlang.org — TS for JS Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html) — resumen rápido pensado para quien ya sabe JS
- [totaltypescript.com](https://www.totaltypescript.com/) — artículos y ejercicios gratuitos de nivel intermedio/avanzado

</div>
