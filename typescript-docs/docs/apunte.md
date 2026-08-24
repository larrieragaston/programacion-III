# TypeScript

## El pivot de la unidad

Todo el código de la unidad hasta ahora — JS Funcional, JS Contemporáneo, Asincronismo — fue **JavaScript puro**. De acá en adelante (React, Node + Express, MongoDB) el código de este curso se presenta en **TypeScript**. Ya apareció algo parecido a un genérico sin llamarlo así: `Promise<T>`, en Asincronismo. Vuelve a aparecer en este apunte, ahora explicado con nombre y propio.

TypeScript no es un lenguaje nuevo — es JavaScript con una capa extra encima. Este apunte explica qué problema resuelve esa capa y cómo se usa.

## El problema que resuelve

```js
// JavaScript — esto compila y corre sin quejarse
function applyDiscount(price, rate) {
  return price - price * rate
}

applyDiscount(1000, 0.1)     // => 900, como se esperaba
applyDiscount(1000, '10%')   // => NaN — el error aparece recién en producción
```

JavaScript es dinámico: no hay que declarar tipos, lo cual da flexibilidad para escribir rápido — pero errores tontos como pasar un string donde se esperaba un número recién se descubren **en tiempo de ejecución**, muchas veces lejos de donde ocurrió el error real (una función que recibe el valor equivocado tres llamadas más adelante de donde se originó el bug).

```ts
function applyDiscount(price: number, rate: number): number {
  return price - price * rate
}

applyDiscount(1000, 0.1)     // ✅ compila
applyDiscount(1000, '10%')   // ❌ error de compilación, antes de correr nada
// Argument of type 'string' is not assignable to parameter of type 'number'.
```

TypeScript es un **superset** de JavaScript: todo código JS válido es también código TS válido. Agrega anotaciones de tipo que el compilador (`tsc`) chequea — y después **borra por completo** al generar el JavaScript final. En runtime no queda ni rastro de TypeScript: los tipos son una herramienta de la etapa de desarrollo, no algo que exista mientras el programa corre. Por eso se dice "tipado estático": los tipos se verifican en tiempo de **compilación**, con el objetivo de adelantar el error al momento de escribir el código, en vez de descubrirlo con un usuario real en producción.

## Tipos básicos

```ts
let name: string = 'Ada'
let age: number = 29
let isActive: boolean = true

let ids: number[] = [1, 2, 3]        // array de numbers
let names: Array<string> = ['Ada']    // misma idea, sintaxis genérica

let point: [number, number] = [10, 20]   // tupla: largo y tipos fijos
```

`number[]` y `Array<number>` son exactamente el mismo tipo, escrito de dos formas distintas. La segunda ya es una pista de lo que se ve más adelante en este apunte: los **genéricos**. Una **tupla** (`[number, number]`) es un array de largo fijo donde cada posición tiene su propio tipo — útil para representar pares o coordenadas sin necesitar un objeto con nombres de propiedad.

### Inferencia de tipos

```ts
let name = 'Ada'        // TS infiere: string
let age = 29             // TS infiere: number

name = 42                 // ❌ Type 'number' is not assignable to type 'string'
```

No hace falta anotar **todo** — si TypeScript puede deducir el tipo a partir del valor inicial, alcanza con eso. Las anotaciones explícitas (`: string`, `: number`) importan sobre todo en las firmas de funciones, donde no hay un valor inicial del que inferir el tipo.

## Tipar funciones

```ts
function greet(name: string, greeting: string = 'Hola'): string {
  return `${greeting}, ${name}!`
}

function logError(message: string, code?: number): void {
  console.error(code ? `[${code}] ${message}` : message)
}

const double = (x: number): number => x * 2
```

Parámetros y retorno se anotan igual que las variables. `code?: number` marca un parámetro **opcional** — se puede omitir al llamar la función, y dentro del cuerpo su tipo real es `number | undefined`. `void` indica que la función no devuelve nada útil (como `logError`, que solo produce un efecto por consola).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una función `formatPrice(amount: number, currency?: string): string` que devuelva `"$amount currency"`, usando `'ARS'` como valor por defecto cuando no se pasa `currency`. Probá llamarla con y sin el segundo argumento, y después intentá llamarla con un string en `amount` para confirmar que TypeScript marca el error antes de ejecutar nada.
</div>

## `any` vs. `unknown`

```ts
let a: any = 'hola'
a.toUpperCase()   // compila — TS no chequea nada sobre "any"
a()                  // compila también — y explota en runtime

let b: unknown = 'hola'
b.toUpperCase()   // ❌ error de compilación: hay que angostar el tipo primero

if (typeof b === 'string') {
  b.toUpperCase()   // ✅ ahora sí — TS sabe que acá b es un string
}
```

`any` **apaga el chequeo de tipos** por completo para esa variable — es escribir JavaScript disfrazado de TypeScript, y anula buena parte del motivo por el que se eligió el lenguaje. `unknown` es la alternativa segura: acepta cualquier valor igual que `any`, pero obliga a comprobar el tipo (*narrowing*, próxima sección) antes de poder operar con él. La recomendación general es evitar `any` en código nuevo — cuando el tipo realmente no se conoce de antemano (por ejemplo, el resultado de parsear un JSON externo), `unknown` es casi siempre la opción correcta.

## Union types y narrowing

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

`string | number` es un **union type**: el valor puede ser cualquiera de los dos tipos listados. Dentro del `if`, TypeScript **angosta** (*narrows*) el tipo automáticamente según el chequeo (`typeof`) — dentro de esa rama, `id` ya es tratado como `number` sin necesitar ninguna conversión manual, y en la rama `else` (implícita, el `return` final) queda tratado como `string`. Este mecanismo — escribir un chequeo normal de JavaScript y dejar que TypeScript deduzca el tipo a partir de él — es la forma más común de trabajar con union types en la práctica.

## Literal types

```ts
let role: 'alumno' | 'profesor' | 'admin'

role = 'alumno'      // ✅
role = 'invitado'    // ❌ Type '"invitado"' is not assignable...
```

Un **literal type** no es "un string cualquiera" — es exactamente ese valor, o uno de un conjunto cerrado de valores. Es una forma de modelar, con el propio sistema de tipos, un conjunto fijo de opciones válidas — una alternativa más liviana a un `enum` (ver más abajo) cuando alcanza con comparar strings, sin necesitar un objeto extra en runtime.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una función `describeId(id: string | number): string` que use `typeof` para distinguir los dos casos y devuelva un mensaje distinto para cada uno (por ejemplo, `"ID numérico: 42"` o `"ID de texto: ABC"`). Después declará `type Status = 'pending' | 'shipped' | 'delivered'` y escribí una función que reciba un `Status` y devuelva un emoji distinto según el valor.
</div>

## Modelar objetos: `interface` y `type`

### `interface`

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

`interface` define la **forma** de un objeto: qué propiedades tiene y de qué tipo es cada una. Cualquier objeto que "encaje" en esa forma es válido — no hace falta declarar explícitamente que `mouse` "implementa" `Product`, alcanza con que tenga las propiedades correctas. Esto se llama ***structural typing*** (tipado estructural), y es distinto del ***nominal typing*** de lenguajes como Java o C#, donde sí hay que declarar la relación explícitamente (`class Mouse implements Product`).

### Extender interfaces

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

`extends` combina interfaces — `DigitalProduct` tiene las propiedades propias más todas las de `Product`. Útil para modelar variantes de un mismo concepto sin repetir campos comunes.

### `type`

```ts
type Product = {
  name: string
  price: number
}

type ID = string | number                          // alias para un union type
type Handler = (event: string) => void               // tipo de una función
type ProductOrId = Product | ID                       // combinación de otros tipos
```

`type` es más general que `interface`: además de objetos, puede nombrar unions, tipos primitivos, tipos de función y combinaciones entre todos ellos. `interface` solo describe objetos (y se puede extender/fusionar de formas que `type` no permite).

### `interface` vs. `type`: cuál usar

<div class="card-grid card-grid-2">
<div class="info-card">
<h4>interface</h4>

Pensada para la forma de objetos y clases. Se puede extender (<code>extends</code>) y fusionar declaraciones del mismo nombre. Mensajes de error algo más legibles en objetos complejos.

<div class="card-note">Preferirla para modelar entidades: props de componentes, modelos de datos.</div>
</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
<h4>type</h4>

Sirve para cualquier tipo: objetos, unions, primitivos, funciones. No se puede reabrir/fusionar después de declarado.

<div class="card-note">Preferirlo para unions, tipos de función, o combinaciones de otros tipos.</div>
</div>
</div>

En la práctica se mezclan todo el tiempo en un mismo proyecto — la regla general es "objetos con `interface`, todo lo demás con `type`", pero no es una ley estricta ni todos los equipos la siguen igual.

## `enum`

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

Un `enum` agrupa un conjunto fijo de valores con nombre. Cumple un propósito parecido al de los literal types (`'alumno' | 'profesor'`) vistos antes — la diferencia real es que un `enum` existe también en el JavaScript compilado (genera un objeto real en runtime), mientras que los literal types desaparecen por completo al compilar, igual que el resto de las anotaciones de tipo. Para casos simples, muchos equipos hoy prefieren un union de literal types por ser más liviano (nada que generar, nada que importar); `enum` sigue siendo útil cuando el conjunto de valores necesita existir también como objeto navegable en runtime (por ejemplo, para iterar sus claves).

## Genéricos

### El genérico que ya usaban

```ts
let ids: number[]        // "array de numbers"
let ids: Array<number>   // mismo tipo — Array es un genérico, number es su parámetro

let names: Array<string>
let flags: Array<boolean>
```

Un **genérico** es un tipo que recibe otro tipo como parámetro — `Array<T>` no es un tipo fijo, es una plantilla: `Array<number>`, `Array<string>` y `Array<boolean>` son cada uno un tipo distinto, generado a partir de la misma plantilla `Array<T>`. Ya se venía usando esta idea desde la sección de tipos básicos, sin el nombre.

### El genérico de Asincronismo: `Promise<T>`

```ts
async function fetchUser(id: number): Promise<{ name: string; age: number }> {
  const res = await fetch(`/api/users/${id}`)
  return res.json()
}

const user = await fetchUser(1)
user.name   // TS sabe que esto es un string — sin castear nada a mano
```

Toda función `async` devuelve una `Promise` — en TypeScript, se tipa **qué** va a resolver esa promesa: `Promise<{ name: string; age: number }>` significa "una promesa que, cuando se resuelve, entrega un objeto con esa forma". Es la misma idea de `Array<T>` aplicada a Promises — el genérico que ya apareció en Asincronismo sin nombrarlo todavía.

### Escribir un genérico propio

```ts
function firstElement<T>(list: T[]): T | undefined {
  return list[0]
}

firstElement([1, 2, 3])          // => number | undefined
firstElement(['a', 'b'])         // => string | undefined
firstElement([true, false])      // => boolean | undefined
```

`<T>` declara un **parámetro de tipo**: una variable que representa "el tipo que sea, decidido en cada llamada". La misma función funciona para arrays de cualquier tipo, y TypeScript infiere `T` automáticamente a partir del argumento pasado — sin escribir la función tres veces (una por tipo) ni resignar el chequeo de tipos recurriendo a `any`.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una interfaz `Product { name: string; price: number }`. Después escribí una función genérica `pluck<T, K extends keyof T>(list: T[], key: K): T[K][]` que extraiga un array con solo los valores de una propiedad dada (por ejemplo, `pluck(products, 'name')` debería devolver un array de strings). No hace falta entender `keyof` a fondo todavía — alcanza con probar que funciona y notar que TypeScript infiere el tipo de retorno correcto según la propiedad elegida.
</div>

## Repaso funcional, ahora tipado

### Tipando `map`/`filter`/`reduce`

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

Los mismos `map`/`filter`/`reduce` de JS Funcional — ahora TypeScript conoce la forma de cada elemento (`Product`) y el tipo de cada resultado, y avisa en el momento si, por ejemplo, se intenta sumar `p.name` en vez de `p.price` dentro del `reduce`.

### Tipando `compose`

```ts
function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C {
  return (a: A) => f(g(a))
}

const double = (x: number): number => x * 2
const toCurrency = (x: number): string => `$${x}`

const doubleAndFormat = compose(toCurrency, double)
doubleAndFormat(500)   // => "$1000"
```

`compose` de JS Funcional, tipado con **tres** parámetros de tipo genéricos (`A`, `B`, `C`): el tipo de entrada, el tipo intermedio que devuelve `g`, y el tipo final que devuelve `f`. TypeScript encadena los tipos automáticamente y marcaría un error de compilación si se intentara componer dos funciones cuyos tipos no calzan (por ejemplo, si `f` esperara un `string` pero `g` devolviera un `number`).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Tipá una función `pipe` (la versión de `compose` que aplica las funciones de izquierda a derecha, ya vista en JS Funcional) usando los mismos tres parámetros de tipo genéricos que `compose`. Probala componiendo tres funciones propias sobre un array de `Product` — por ejemplo, filtrar por precio, mapear a nombres, y unir en un string con `join`.
</div>

## Configurar un proyecto TS

### `tsconfig.json`

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

`tsconfig.json` le dice al compilador (`tsc`) qué archivos compilar y con qué reglas. `target` fija a qué versión de JavaScript se transpila el código; `outDir`/`rootDir` separan la carpeta de fuente (`.ts`) de la carpeta de salida (`.js`); `strict: true` activa el conjunto completo de chequeos estrictos — **muy recomendado** en proyectos nuevos, aunque el ejemplo de `any` visto antes siga siendo válido incluso con `strict` activado, salvo que además se active explícitamente `noImplicitAny`.

### Correr un proyecto TS

```bash
npx tsc              # compila una vez, según tsconfig.json
npx tsc --watch       # recompila automáticamente en cada cambio

npx ts-node src/index.ts   # compila y ejecuta en un solo paso, sin generar .js
```

Dos flujos habituales: **compilar y correr** (`tsc` genera el `.js` en `outDir`, después se corre con `node`) o **correr directo** con `ts-node`, que compila en memoria sobre la marcha — más cómodo mientras se desarrolla, pero no pensado para producción (ahí conviene el paso de build explícito).

## Cheat sheet

<div class="card-grid card-grid-2">
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

## Referencias y recursos

- [typescriptlang.org — Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — documentación oficial, completa y bien organizada
- [typescriptlang.org — Playground](https://www.typescriptlang.org/play) — probar TS en el navegador, sin instalar nada
- [typescriptlang.org — TS for JS Programmers](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html) — resumen rápido pensado para quien ya sabe JS
- [totaltypescript.com](https://www.totaltypescript.com/) — artículos y ejercicios gratuitos de nivel intermedio/avanzado

## Cierre

El objetivo de este tema es poder tipar con confianza lo que ya se sabía hacer en JavaScript — variables, funciones, HOFs — y entender interfaces y genéricos lo suficiente como para leer y escribir el código TS del resto de la unidad (React, Node + Express, MongoDB). No hace falta dominar el sistema de tipos a fondo (hay mucho más: mapped types, conditional types, utility types como `Partial<T>` o `Pick<T, K>`) — ese nivel se gana con la práctica, a medida que aparece la necesidad real en el proyecto integrador.
