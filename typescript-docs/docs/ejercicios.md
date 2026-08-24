# TypeScript — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. A partir del ejercicio 5 se trabaja con un catálogo de productos — mismo dominio usado en JS Contemporáneo, ahora tipado.

## 1. Tipos básicos

1. Declarar `title: string`, `year: number` y `isAvailable: boolean` con valores de un libro cualquiera.
2. Declarar `pages: number[]` con al menos 3 números.
3. Declarar `coordinates: [number, number]` como una tupla, y confirmar que asignarle un tercer valor da error de compilación.

## 2. Tipar funciones

1. Escribir `formatPrice(amount: number, currency?: string): string` que devuelva `"$amount currency"`, usando `'ARS'` como valor por defecto.
2. Escribir `sumAll(...numbers: number[]): number` que sume una cantidad variable de argumentos.
3. Escribir `logWarning(message: string, code?: number): void` que solo imprima por consola (sin `return`).

## 3. `any` vs. `unknown`

1. Declarar `let raw: any = 'hola'` y confirmar (leyendo el código, sin ejecutar) que `raw.toUpperCase()` y `raw()` compilan las dos, aunque la segunda vaya a explotar en runtime.
2. Declarar `let value: unknown = 'hola'` y confirmar que `value.toUpperCase()` da error de compilación.
3. Escribir el `if (typeof value === 'string')` necesario para que `value.toUpperCase()` compile dentro de esa rama.

## 4. Union types y narrowing

1. Escribir `describeId(id: string | number): string` que use `typeof` para devolver `"ID numérico: 42"` o `"ID de texto: ABC"` según corresponda.
2. Declarar `type Status = 'pending' | 'shipped' | 'delivered'`.
3. Escribir `statusEmoji(status: Status): string` que devuelva un emoji distinto para cada valor posible (usar un `switch` o una serie de `if`).
4. Intentar llamar a `statusEmoji('cancelled')` y confirmar que TypeScript lo marca como error.

## 5. El catálogo tipado

1. Declarar `interface Book { title: string; author: string; year: number; pages: number; available: boolean }`.
2. Declarar `const books: Book[]` con al menos cinco libros.
3. Escribir `describeBook(book: Book): string` que devuelva `"${title} (${year})"`.

## 6. Extender interfaces

1. Declarar `interface DigitalBook extends Book { downloadUrl: string; sizeInMb: number }`.
2. Declarar un objeto `const ebook: DigitalBook` con todas las propiedades necesarias (las heredadas de `Book` más las propias).
3. Escribir una función `describeDigitalBook(book: DigitalBook): string` que reutilice `describeBook` (del ejercicio 5) y le agregue la información del tamaño del archivo.

## 7. `type` y unions de objetos

1. Declarar `type Ebook = { title: string; downloadUrl: string }` y `type PrintedBook = { title: string; pages: number }`.
2. Declarar `type AnyBook = Ebook | PrintedBook`.
3. Escribir `describeAnyBook(book: AnyBook): string` que use `'downloadUrl' in book` (chequeo de presencia de propiedad, otra forma de narrowing) para distinguir cuál de los dos tipos es, y devuelva un mensaje distinto para cada caso.

## 8. `map`/`filter`/`reduce` tipados

1. Con el `books: Book[]` del ejercicio 5, usar `map` para obtener un `string[]` con los títulos.
2. Usar `filter` para obtener un `Book[]` con los libros disponibles (`available: true`).
3. Usar `reduce` para calcular el total de páginas de todo el catálogo, como un `number`.
4. Intentar (a propósito) sumar `book.title` en vez de `book.pages` dentro del `reduce` y confirmar que TypeScript marca el error antes de ejecutar nada.

## 9. Genérico propio: `firstElement`

1. Escribir `function firstElement<T>(list: T[]): T | undefined`.
2. Probarla con `books` (debería inferir `Book | undefined`), con un array de `number[]` y con un array de `string[]`.
3. Explicar en un comentario por qué el tipo de retorno incluye `undefined` — pensar en qué pasa si `list` está vacía.

## 10. Genérico propio: `pluck`

1. Escribir `function pluck<T, K extends keyof T>(list: T[], key: K): T[K][]`.
2. Probarla con `pluck(books, 'title')` (debería dar `string[]`) y `pluck(books, 'year')` (debería dar `number[]`).
3. Intentar llamarla con una clave que no existe en `Book` (por ejemplo `pluck(books, 'publisher')`) y confirmar que TypeScript lo rechaza.

## 11. `compose` tipado

1. Escribir `function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C`.
2. Escribir dos funciones propias — por ejemplo `toUpperCase(s: string): string` y `exclaim(s: string): string` (que agregue `"!"` al final) — y componerlas con `compose`.
3. Aplicar la función compuesta al título de un libro del catálogo.

## 12. `Promise<T>`: conectando con Asincronismo

1. Escribir una función `async function fetchBookById(id: number): Promise<Book>` que simule una consulta (con un `setTimeout` envuelto en una Promise, como en Asincronismo) y resuelva con un `Book` del catálogo según el `id`.
2. Escribir una función `async function loadAndDescribe(id: number): Promise<string>` que use `await fetchBookById(id)` y devuelva el resultado de `describeBook` (ejercicio 5) sobre ese libro.
3. Confirmar que TypeScript conoce el tipo de `book` dentro de `loadAndDescribe` sin necesitar ninguna anotación extra en esa línea — viene inferido de `Promise<Book>`.

## 13. `tsconfig.json`

1. Crear una carpeta de proyecto nueva y correr `npx tsc --init`.
2. Ubicar en el archivo generado las opciones `target`, `outDir`, `rootDir` y `strict`, y escribir en un comentario qué hace cada una (usar el apunte como referencia).
3. Crear `src/index.ts` con cualquiera de las funciones de los ejercicios anteriores, y compilarlo con `npx tsc`. Confirmar que aparece el `.js` correspondiente en `outDir`.
4. Correr el mismo archivo con `npx ts-node src/index.ts`, sin el paso de compilación manual, y comparar.

## Para pensar

- `any` y `unknown` aceptan los mismos valores en la asignación, pero se comportan muy distinto al **usarlos**. ¿En qué situación real de un proyecto (por ejemplo, procesando la respuesta de una API externa) el uso de `any` en vez de `unknown` podría esconder un bug hasta producción?
- `interface` permite fusionar dos declaraciones del mismo nombre (*declaration merging*) — buscá un ejemplo de esto en la documentación oficial. ¿Por qué `type` no permite lo mismo, y en qué situación esa diferencia podría ser justamente la razón para elegir uno sobre el otro?
- Los genéricos (`Array<T>`, `Promise<T>`, `pluck<T, K>`) parecen abstractos al principio, pero ya se venían usando implícitamente en JS Funcional cada vez que se escribía una función que funcionaba "para cualquier tipo de elemento" (como `map`). ¿Qué gana concretamente el código al hacer explícito, con TypeScript, algo que en JS ya funcionaba igual?
- `strict: true` en `tsconfig.json` activa varias reglas a la vez (`noImplicitAny`, `strictNullChecks`, entre otras). Investigá qué hace `strictNullChecks` puntualmente y escribí un ejemplo de código que compile sin esa opción pero falle con ella activada.
