# TypeScript

## ¿Qué es TypeScript?

Todo el código de la unidad hasta ahora — JS Funcional, JS Contemporáneo, Asincronismo — fue **JavaScript puro**. De acá en adelante (React, Node + Express, MongoDB) el código de este curso se presenta en **TypeScript**.

```js
// JavaScript — esto compila y corre sin quejarse
function applyDiscount(price, rate) {
  return price - price * rate
}

applyDiscount(1000, 0.1)     // => 900, como se esperaba
applyDiscount(1000, '10%')   // => NaN — el error aparece recién en producción
```

JavaScript es dinámico: no hay que declarar tipos, lo cual da flexibilidad para escribir rápido — pero errores tontos como pasar un string donde se esperaba un número recién se descubren **en tiempo de ejecución**, muchas veces lejos de donde ocurrió el error real. Cuanto más grande el proyecto y más gente toca el mismo código, más cuesta esto: nadie avisa si le pasás mal un argumento, y el editor no puede ayudar con autocompletado porque no sabe qué forma tiene cada valor.

```ts
function applyDiscount(price: number, rate: number): number {
  return price - price * rate
}

applyDiscount(1000, 0.1)     // ✅ compila
applyDiscount(1000, '10%')   // ❌ error de compilación, antes de correr nada
// Argument of type 'string' is not assignable to parameter of type 'number'.
```

TypeScript es un **superset** de JavaScript: todo código JS válido es también código TS válido. Agrega anotaciones de tipo que el compilador (`tsc`) chequea — y después **borra por completo** al generar el JavaScript final. En runtime no queda ni rastro de TypeScript: los tipos son una herramienta de la etapa de desarrollo, no algo que exista mientras el programa corre. Por eso se dice "tipado estático": los tipos se verifican en tiempo de **compilación** — mismo bug, mismo lugar, pero detectado en un momento completamente distinto: mientras se escribe el código, no cuando un usuario real ejecuta esa línea.

## Tipos básicos

```ts
let productName: string = 'Mouse'
let price: number = 18000
let inStock: boolean = true

inStock = 'sí'   // ❌ Type 'string' is not assignable to type 'boolean'

let ids: number[] = [1, 2, 3]          // array de numbers
let names: Array<string> = ['Mouse']    // misma idea, sintaxis genérica

let point: [number, number] = [10, 20]   // tupla: largo y tipos fijos
```

`number[]` y `Array<number>` son exactamente el mismo tipo, escrito de dos formas distintas. La segunda ya es una pista de lo que se ve más adelante en este apunte: los **genéricos**. Una **tupla** (`[number, number]`) es un array de largo fijo donde cada posición tiene su propio tipo — útil para representar pares o coordenadas sin necesitar un objeto con nombres de propiedad. En JS puro, la línea de `inStock = 'sí'` no tira ningún error — el valor simplemente cambia de tipo en silencio, y cualquier código que esperaba un `boolean` ahí puede romperse más adelante, sin aviso.

### Inferencia de tipos

```ts
let productName = 'Mouse'   // TS infiere: string
let price = 18000            // TS infiere: number

price = '18000'               // ❌ Type 'string' is not assignable to type 'number'
```

No hace falta anotar **todo** — si TypeScript puede deducir el tipo a partir del valor inicial, alcanza con eso. Las anotaciones explícitas (`: string`, `: number`) importan sobre todo en las firmas de funciones, donde no hay un valor inicial del que inferir el tipo.

## Tipar funciones

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

Parámetros y retorno se anotan igual que las variables. `rate: number = 0.1` es un parámetro **con valor por defecto**; `remaining?: number` es **opcional** — se puede omitir al llamar la función, y dentro del cuerpo su tipo real es `number | undefined`. `void` indica que la función no devuelve nada útil, como `logStockWarning`, que solo tiene un efecto (un `console.warn`). En JS puro, llamar a `logStockWarning('Mouse', '5')` con un string en vez de un número no tira ningún error — acá sí, apenas se escribe la línea.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una función `formatPrice(amount: number, currency?: string): string` que devuelva `"$amount currency"`, usando `'ARS'` como valor por defecto cuando no se pasa `currency`. Probá llamarla con y sin el segundo argumento, y después intentá llamarla con un string en `amount` para confirmar que TypeScript marca el error antes de ejecutar nada.
</div>

## `any` vs. `unknown`

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

`any` **apaga el chequeo de tipos** por completo — es escribir JavaScript disfrazado de TypeScript, y anula buena parte del motivo por el que se eligió el lenguaje. `unknown` es la alternativa segura: acepta cualquier valor igual que `any` (útil para datos externos, como una respuesta HTTP), pero obliga a comprobar la forma real (*narrowing*, próxima sección) antes de operar con él. `as { name: string }` es una **type assertion**: el "casteo" de TypeScript — le dice al compilador "confiá en que esto tiene esta forma", sin volver a chequearlo. A diferencia de un cast de Java o C#, no convierte nada en runtime: es pura información para el compilador, que se borra al compilar — si la aserción está mal, el error recién aparece en runtime, exactamente como sin TypeScript. Por eso conviene usarla solo después de haber comprobado algo de verdad, como con el `if` de arriba.

## Union types y narrowing

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

`string | number` es un **union type**: el valor puede ser cualquiera de los dos tipos listados. Dentro del `if`, TypeScript **angosta** (*narrows*) el tipo automáticamente según el chequeo (`typeof`) — dentro de esa rama, `id` ya es tratado como `number` sin necesitar ninguna conversión manual, y en la rama implícita del `return` final queda tratado como `string`. El `'name' in json` de la sección anterior es otra forma de narrowing: comprueba si existe una propiedad, en vez de un tipo primitivo.

## `?.`, `??` y `!`: trabajar con valores ausentes

```ts
interface Product {
  name: string
  price: number
  stock: number
}

function getStock(product?: Product): number {
  return product?.stock ?? 0
}

getStock(undefined)                              // => 0
getStock({ name: 'Mouse', price: 1, stock: 5 })    // => 5

const trusted = product!.stock   // "confiá en mí, esto no es null/undefined"
```

**`?.`** (*optional chaining*): si lo de la izquierda es `null`/`undefined`, corta ahí y devuelve `undefined`, en vez de explotar. **`??`** (*nullish coalescing*): da un valor por defecto **solo** si lo de la izquierda es `null`/`undefined` — a diferencia de `||`, que también reemplazaría `0`, `''` o `false` (un error común: `stock ?? 0` mantiene un stock de `0` real, mientras que `stock || 0` lo pisaría por las dudas). **`!`** (*non-null assertion*) apaga el chequeo puntual: le dice al compilador que confíe en que ahí nunca va a haber `null`/`undefined`. Si la certeza está mal, explota en runtime exactamente igual que sin TypeScript — conviene usarlo con cuidado, solo cuando de verdad no hay dudas.

## Literal types

```ts
type ProductCategory = 'electronics' | 'clothing' | 'books'

function shippingDays(category: ProductCategory): number {
  return category === 'books' ? 2 : 5
}

shippingDays('electronics')   // ✅
shippingDays('food')          // ❌ Type '"food"' is not assignable...
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

`interface` define la **forma** de un objeto: qué propiedades tiene y de qué tipo es cada una. Cualquier objeto que "encaje" en esa forma es válido — no hace falta declarar explícitamente que `mouse` "implementa" `Product`, alcanza con que tenga las propiedades correctas. Esto se llama ***structural typing*** (tipado estructural), y es distinto del ***nominal typing*** de lenguajes como Java o C#, donde sí hay que declarar la relación explícitamente (`class Mouse implements Product`). En JS puro, un typo como `{ name: 'Mouse', pryce: 18000, stock: 5 }` no lo detecta nadie hasta que alguien ejecute `describe(mouse)` y el resultado salga mal.

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

### `readonly`: inmutabilidad con tipos

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

La misma idea de no mutar que se vio en JS Funcional con `map`/`filter` (crear algo nuevo en vez de modificar lo existente) — ahora reforzada por el compilador. `readonly` no cambia nada en el JavaScript final (se borra al compilar, como todo tipo), pero avisa **en tiempo de compilación** si el propio código intenta reasignar una propiedad o mutar un array que se declaró como si no debiera cambiar.

### `as const`: ¿y las constantes?

```ts
const config = { role: 'admin', level: 1 }
config.role = 'user'          // ✅ compila — el objeto no es readonly, solo la variable

const frozen = { role: 'admin', level: 1 } as const
frozen.role = 'user'          // ❌ Cannot assign to 'role' because it is a read-only property

let role = 'admin'            // tipo: string
let fixedRole = 'admin' as const   // tipo: 'admin' (literal, no se ensancha)
```

`const` (de JavaScript) solo evita **reasignar la variable** — el objeto que contiene se puede seguir mutando por dentro, como `config.role` en el ejemplo. `as const` (de TypeScript) es la pieza que faltaba: es el mismo `as` visto en `any` vs. `unknown`, aplicado no a un tipo propio sino a la palabra `const` — le pide al compilador tratar el valor como su versión más específica posible: todas las propiedades pasan a ser `readonly` de forma recursiva, y los strings/numbers quedan fijados como su valor literal en vez de ensancharse a `string`/`number`. Es la forma de lograr, con un objeto, algo parecido a lo que `const` ya hacía con un primitivo.

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

`type` es más general que `interface`: además de objetos, puede nombrar unions, tipos primitivos, tipos de función y combinaciones entre todos ellos. `interface` solo describe objetos — y tiene un comportamiento particular que vale la pena conocer antes de elegir entre uno y otro.

### Ojo con las interfaces: se fusionan

```ts
interface Product { name: string }
// en otro archivo del mismo proyecto, sin saber que ya existía...
interface Product { price: number }
// TS no avisa nada — combina ambas declaraciones en una sola
const mouse: Product = { name: 'Mouse', price: 18000 }   // ✅ compila
```

Esto se llama ***declaration merging***: dos `interface` con el **mismo nombre** no chocan, TS las combina sola. Es una función real y deliberada (extender un tipo de una librería que no controlás) — pero en un proyecto grande, si dos módulos usan el mismo nombre **sin querer**, la fusión es silenciosa, y el error puede aparecer mucho después, lejos de la causa real.

```ts
type Product = { name: string }
type Product = { price: number }   // ❌ Error: Duplicate identifier 'Product'.
```

`type` es más estricto acá: el mismo nombre dos veces es directamente un error de compilación. Por eso, en equipos grandes, hay quienes prefieren `type` para que un choque de nombres accidental se note enseguida, en vez de fusionarse en silencio.

### `interface` vs. `type`: cuál usar

<div class="card-grid card-grid-2">
<div class="info-card">
<h4>interface</h4>

Pensada para la forma de objetos y clases. Se puede extender (<code>extends</code>) y **fusiona** declaraciones repetidas del mismo nombre (a propósito o no). Mensajes de error algo más legibles en objetos complejos.

<div class="card-note">Preferirla para modelar entidades: props de componentes, modelos de datos.</div>
</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
<h4>type</h4>

Sirve para cualquier tipo: objetos, unions, primitivos, funciones. **No** se puede reabrir/fusionar después de declarado — nombre repetido es error.

<div class="card-note">Preferirlo para unions, tipos de función, o cuando un choque de nombres debe fallar fuerte.</div>
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

Un `enum` agrupa un conjunto fijo de valores con nombre. Cumple un propósito parecido al de los literal types (`ProductCategory`, visto antes) — la diferencia real es que un `enum` existe también en el JavaScript compilado (genera un objeto real en runtime), mientras que los literal types desaparecen por completo al compilar, igual que el resto de las anotaciones de tipo. Para casos simples, muchos equipos hoy prefieren un union de literal types por ser más liviano (nada que generar, nada que importar); `enum` sigue siendo útil cuando el conjunto de valores necesita existir también como objeto navegable en runtime (por ejemplo, para iterar sus claves).

## Genéricos

### ¿Qué es un genérico?

```ts
function identity<T>(value: T): T {
  return value
}

identity<number>(42)        // T = number  → devuelve 42
identity<string>('hola')    // T = string  → devuelve 'hola'

identity<number>('hola')    // ❌ Argument of type 'string' is not assignable to parameter of type 'number'
```

Un **genérico** es un tipo que recibe otro tipo como parámetro — igual que un parámetro común, pero en vez de un valor se pasa un tipo. `<T>` declara esa "variable de tipo": se completa en cada llamada (`T = number`, `T = string`, ...), y TypeScript chequea que el argumento realmente coincida con lo que se pidió.

### Genéricos en objetos: `interface<T>`

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

La misma idea aplicada a un objeto en vez de a una función: `ApiResponse<T>` es una plantilla, no un tipo cerrado — `data` va a tener la forma de lo que sea `T` en cada uso. `ApiResponse<Product>` y `ApiResponse<Product[]>` son dos tipos distintos, generados a partir de la misma interfaz genérica, sin escribirla dos veces.

### Ya los venían usando: `Array<T>` y `Promise<T>`

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

Mismo patrón que `identity<T>` y `ApiResponse<T>`: una plantilla (`Array<T>`, `Promise<T>`) con un tipo concreto adentro. `Array<number>` es "un array donde `T = number`"; `Promise<Product>` es "una promesa que, cuando se resuelve, entrega un `Product`" — el genérico que ya apareció en Asincronismo, ahora con nombre y sabiendo por qué funciona así.

### Por qué hace falta un genérico propio

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

Escribir una función por tipo funciona, pero obliga a duplicar la misma lógica cada vez. Unificarlas con `any[]` evita la duplicación, pero devuelve `any` — se pierde el tipo, y un typo como `p.priec` compila igual. Hace falta una sola función que mantenga el tipo específico de cada llamada: ahí entra un genérico propio.

### Escribir un genérico propio

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

`<T>` declara un **parámetro de tipo**: una variable que representa "el tipo que sea, decidido en cada llamada". La misma función funciona para arrays de cualquier tipo, y TypeScript infiere `T` automáticamente a partir del argumento pasado — sin escribir la función una vez por tipo ni resignar el chequeo de tipos recurriendo a `any`.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una interfaz `Product { name: string; price: number }`. Después escribí una función genérica `pluck<T, K extends keyof T>(list: T[], key: K): T[K][]` que extraiga un array con solo los valores de una propiedad dada (por ejemplo, `pluck(products, 'name')` debería devolver un array de strings). No hace falta entender `keyof` a fondo todavía — alcanza con probar que funciona y notar que TypeScript infiere el tipo de retorno correcto según la propiedad elegida.
</div>

### Utility types: transformar tipos existentes

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

`Pick`, `Partial`, `Omit` y `Record` son **genéricos ya incluidos** en TypeScript: toman un tipo existente y devuelven una versión transformada, sin reescribirla a mano. Se usan todo el tiempo en proyectos reales — para tipar el cuerpo de un `PATCH` HTTP, o un diccionario de productos por nombre — y van a volver a aparecer en lo que viene (React, Node).

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

## Probar y correr TypeScript

### La forma más rápida: el Playground

No hace falta instalar nada para probar los ejemplos de este apunte: en [typescriptlang.org/play](https://www.typescriptlang.org/play) se escribe TypeScript en el navegador y se ve todo en vivo — el panel izquierdo muestra el código TypeScript, el derecho el JavaScript que genera (para ver qué "le hace" el compilador), y los errores de tipos aparecen subrayados en rojo ahí mismo, sin compilar nada a mano. Todavía no se vio cómo armar un proyecto de Node — para ir probando código por su cuenta, esta es la forma más simple.

### Instalar y correr TypeScript en tu máquina

```bash
npm install -g typescript ts-node   # instalación global — sin armar un proyecto

tsc archivo.ts          # compila un archivo suelto → archivo.js
node archivo.js           # => 900

ts-node archivo.ts       # compila y ejecuta en un solo paso, sin generar el .js
```

No hace falta un proyecto de Node (con `package.json`, carpetas `src/`, etc.) para esto: alcanza con instalar TypeScript de forma global y correrlo sobre un único archivo suelto. Cuando más adelante se arme un proyecto real — con React, por ejemplo — TypeScript se instala como dependencia **de ese proyecto** en vez de global, y ahí sí aparece un `package.json`, un `tsconfig.json` y una estructura de carpetas armados en serio.

### `tsconfig.json`

Apenas se arma un proyecto real (por ejemplo, con React) aparece uno de estos junto al `package.json`.

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

`tsconfig.json` le dice al compilador (`tsc`) qué archivos compilar y con qué reglas. `target` fija a qué versión de JavaScript se transpila el código; `outDir`/`rootDir` separan la carpeta de fuente (`.ts`) de la carpeta de salida (`.js`); `esModuleInterop` permite mezclar `import`/`export` con paquetes viejos de CommonJS sin fricción.

### `tsconfig.json`: opciones que importan

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

`strict: true` activa **varios** flags a la vez — entre ellos `noImplicitAny` (obliga a tipar en vez de inferir `any` en silencio) y `strictNullChecks` (`null`/`undefined` dejan de aceptarse en cualquier lado, hay que declararlos explícitamente: de ahí sale la necesidad de `?.`/`??` vistos antes). `lib` importa cuando el código usa APIs del navegador (`document`, `fetch`) — sin `"DOM"` ahí, TS ni sabe que existen. `sourceMap` permite debuggear el `.ts` original en el navegador/editor, no el `.js` compilado. `skipLibCheck` acelera la compilación salteando el chequeo de tipos de las librerías instaladas. `include`/`exclude` acotan qué carpetas mira el compilador — **muy recomendado**, sobre todo `strict`, en cualquier proyecto nuevo.

### Cómo leer un error de compilación

```ts
applyDiscount(1000, '10%')
```

```
archivo.ts:5:21 - error TS2345: Argument of type 'string' is not
assignable to parameter of type 'number'.

5 applyDiscount(1000, '10%')
                      ~~~~~~
```

**`archivo:línea:columna`** — dónde está el problema. **`TS2345`** — el código del error (googleable: buscar "TS2345" lleva directo a la explicación). El mensaje describe qué esperaba TS y qué recibió. El **`~~~~~~`** señala la expresión exacta que lo disparó — no toda la línea.

| Código | Significa |
|---|---|
| `TS2322` | un valor no es asignable a ese tipo (lo más común) |
| `TS2339` | esa propiedad no existe en el tipo (típico de un typo) |
| `TS2345` | un argumento no coincide con el parámetro esperado |
| `TS18048` / `TS2532` | el valor puede ser `undefined`, hay que comprobarlo antes |

## Cheat sheet

<div class="card-grid card-grid-2">
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

## Referencias y recursos

- [typescriptlang.org — Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — documentación oficial, completa y bien organizada
- [typescriptlang.org — Playground](https://www.typescriptlang.org/play) — probar TS en el navegador, sin instalar nada
- [typescriptlang.org — TSConfig Reference](https://www.typescriptlang.org/tsconfig) — todas las opciones de `tsconfig.json`, explicadas una por una
- [typescriptlang.org — Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html) — referencia de `Partial`, `Pick`, `Omit`, `Record` y el resto
- [totaltypescript.com](https://www.totaltypescript.com/) — artículos y ejercicios gratuitos de nivel intermedio/avanzado, de Matt Pocock
- [freeCodeCamp — Learn TypeScript](https://www.freecodecamp.org/news/learn-typescript-beginners-guide/) — curso introductorio gratuito, con proyecto práctico
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) — convenciones reales de un equipo grande, útil para ver cómo se usa TS "en serio"
- [type-challenges](https://github.com/type-challenges/type-challenges) — ejercicios de la comunidad para practicar el sistema de tipos, de básico a muy avanzado
- [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped) — el repositorio de tipos (`@types/...`) para librerías JS que no traen los suyos

## Cierre

El objetivo de este tema es poder tipar con confianza lo que ya se sabía hacer en JavaScript — variables, funciones, HOFs — y entender interfaces, genéricos y utility types lo suficiente como para leer y escribir el código TS del resto de la unidad (React, Node + Express, MongoDB). No hace falta dominar el sistema de tipos a fondo (hay mucho más: mapped types, conditional types, utility types más avanzados) — ese nivel se gana con la práctica, a medida que aparece la necesidad real en el proyecto integrador.
