# TypeScript — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. A partir del ejercicio 6 se trabaja con un catálogo de libros — mismo tipo de dominio que en JS Contemporáneo, ahora tipado.

## 1. Tipos básicos

1. Declarar `title: string`, `year: number` y `isAvailable: boolean` con valores de un libro cualquiera.
2. Declarar `pages: number[]` con al menos 3 números.
3. Declarar `coordinates: [number, number]` como una tupla, y confirmar que asignarle un tercer valor da error de compilación.
4. Intentar reasignar `isAvailable = 'sí'` y confirmar el error de compilación. En un comentario, anotar que esa misma línea en JS puro no tira ningún error.

## 2. Tipar funciones

1. Escribir `formatPrice(amount: number, currency?: string): string` que devuelva `"$amount currency"`, usando `'ARS'` como valor por defecto.
2. Escribir `sumAll(...numbers: number[]): number` que sume una cantidad variable de argumentos.
3. Escribir `logWarning(message: string, code?: number): void` que solo imprima por consola (sin `return`).

## 3. `any` vs. `unknown`

1. Declarar `let raw: any = 'hola'` y confirmar (leyendo el código, sin ejecutar) que `raw.toUpperCase()` y `raw()` compilan las dos, aunque la segunda vaya a explotar en runtime.
2. Declarar `let value: unknown = 'hola'` y confirmar que `value.toUpperCase()` da error de compilación.
3. Escribir el `if (typeof value === 'string')` necesario para que `value.toUpperCase()` compile dentro de esa rama.
4. Dentro de esa misma rama, escribir también `(value as string).toUpperCase()` y explicar en un comentario por qué acá el `as` es redundante — TypeScript ya sabe que es un `string` gracias al narrowing del `if`.

## 4. Union types, narrowing y literal types

1. Escribir `describeId(id: string | number): string` que use `typeof` para devolver `"ID numérico: 42"` o `"ID de texto: ABC"` según corresponda.
2. Declarar `type Status = 'pending' | 'shipped' | 'delivered'`.
3. Escribir `statusEmoji(status: Status): string` que devuelva un emoji distinto para cada valor posible (usar un `switch` o una serie de `if`).
4. Intentar llamar a `statusEmoji('cancelled')` y confirmar que TypeScript lo marca como error.

## 5. `?.`, `??` y `!`: valores ausentes

1. Declarar `interface Book { title: string; pages?: number }`.
2. Escribir `pageCount(book: Book): number` que devuelva `book.pages ?? 0`.
3. Probarla con un libro sin `pages` y confirmar que devuelve `0`, no `undefined`.
4. En un comentario, explicar por qué usar `book.pages || 0` en vez de `??` sería un error si algún libro tuviera legítimamente `0` páginas (por ejemplo, un folleto).

## 6. El catálogo tipado

1. Declarar `interface Book { title: string; author: string; year: number; pages: number; available: boolean }`.
2. Declarar `const books: Book[]` con al menos cinco libros.
3. Escribir `describeBook(book: Book): string` que devuelva `"${title} (${year})"`.

## 7. Extender interfaces

1. Declarar `interface DigitalBook extends Book { downloadUrl: string; sizeInMb: number }`.
2. Declarar un objeto `const ebook: DigitalBook` con todas las propiedades necesarias (las heredadas de `Book` más las propias).
3. Escribir una función `describeDigitalBook(book: DigitalBook): string` que reutilice `describeBook` (del ejercicio 6) y le agregue la información del tamaño del archivo.

## 8. `readonly`: inmutabilidad

1. Agregar a `Book` una propiedad `readonly isbn: string`, y actualizar el catálogo del ejercicio 6 con un ISBN para cada libro.
2. Escribir una función `updateTitle(book: Book, title: string)` que intente reasignar tanto `book.isbn` como `book.title` — confirmar cuál de las dos líneas da error de compilación, y cuál compila.
3. Declarar `const isbns: readonly string[]` con los ISBN del catálogo y confirmar que `isbns.push(...)` da error.

## 9. `as const`: constantes de verdad

1. Declarar `const defaultBook = { available: true, pages: 100 }` (sin `as const`) e intentar reasignar `defaultBook.available` — confirmar que compila.
2. Declarar la misma constante con `as const` y confirmar que ahora la reasignación da error.
3. Comparar (con el mouse sobre la variable en el editor, o en el Playground) el tipo inferido de `pages` en cada versión: `number` en la primera, `100` en la segunda.

## 10. `type` y unions de objetos

1. Declarar `type Ebook = { title: string; downloadUrl: string }` y `type PrintedBook = { title: string; pages: number }`.
2. Declarar `type AnyBook = Ebook | PrintedBook`.
3. Escribir `describeAnyBook(book: AnyBook): string` que use `'downloadUrl' in book` (chequeo de presencia de propiedad, otra forma de narrowing) para distinguir cuál de los dos tipos es, y devuelva un mensaje distinto para cada caso.

## 11. Ojo con las interfaces: se fusionan

1. En un archivo nuevo y aislado (sin tocar el catálogo de los ejercicios anteriores), declarar `interface Draft { title: string }` y, más abajo en el mismo archivo, una segunda declaración `interface Draft { published: boolean }`.
2. Confirmar que TypeScript no da ningún error, y que un objeto `const d: Draft = { title: 'x', published: false }` compila usando propiedades de las dos declaraciones.
3. Repetir lo mismo con `type Draft = { title: string }` seguido de `type Draft = { published: boolean }`, y confirmar que esta vez sí da un error de identificador duplicado.

## 12. `enum`: géneros fijos

1. Declarar `enum BookGenre { Fiction = 'fiction', NonFiction = 'non-fiction', Reference = 'reference' }`.
2. Agregar una propiedad `genre: BookGenre` a `Book` (o a una copia de prueba de la interfaz, para no romper los ejercicios anteriores) y asignarle un género a algún libro.
3. Escribir `isFiction(book: Book): boolean` que compare `book.genre === BookGenre.Fiction`.
4. En un comentario, explicar qué cambiaría si en vez de `enum` se hubiera usado `type BookGenre = 'fiction' | 'non-fiction' | 'reference'` — ¿el comportamiento de `isFiction` sería distinto?

## 13. `map`/`filter`/`reduce` tipados

1. Con el `books: Book[]` del ejercicio 6, usar `map` para obtener un `string[]` con los títulos.
2. Usar `filter` para obtener un `Book[]` con los libros disponibles (`available: true`).
3. Usar `reduce` para calcular el total de páginas de todo el catálogo, como un `number`.
4. Intentar (a propósito) sumar `book.title` en vez de `book.pages` dentro del `reduce` y confirmar que TypeScript marca el error antes de ejecutar nada.

## 14. Genérico propio: `firstElement`

1. Escribir `function firstElement<T>(list: T[]): T | undefined`.
2. Probarla con `books` (debería inferir `Book | undefined`), con un array de `number[]` y con un array de `string[]`.
3. Explicar en un comentario por qué el tipo de retorno incluye `undefined` — pensar en qué pasa si `list` está vacía.

## 15. Genéricos en un objeto: `ApiResponse<T>`

1. Declarar `interface ApiResponse<T> { data: T; status: number }`.
2. Declarar una constante de tipo `ApiResponse<Book>` y otra de tipo `ApiResponse<Book[]>`, con datos inventados.
3. Escribir una función genérica `unwrap<T>(response: ApiResponse<T>): T` que devuelva solo el `data`, y confirmar (pasándole cada una de las constantes anteriores) que TypeScript infiere el tipo correcto en cada llamada.

## 16. Genérico propio: `pluck`

1. Escribir `function pluck<T, K extends keyof T>(list: T[], key: K): T[K][]`.
2. Probarla con `pluck(books, 'title')` (debería dar `string[]`) y `pluck(books, 'year')` (debería dar `number[]`).
3. Intentar llamarla con una clave que no existe en `Book` (por ejemplo `pluck(books, 'publisher')`) y confirmar que TypeScript lo rechaza.

## 17. Utility types: transformar el catálogo

1. Declarar `type BookPreview = Pick<Book, 'title' | 'author'>`.
2. Declarar `type BookUpdate = Partial<Book>`.
3. Escribir `updateBook(title: string, changes: BookUpdate): void` (el cuerpo puede ser un `console.log`) y llamarla pasando solo `{ available: false }` como `changes`.
4. Declarar `type BookCatalog = Record<string, Book>` y usarlo para indexar un libro por su título.

## 18. `compose` tipado

1. Escribir `function compose<A, B, C>(f: (b: B) => C, g: (a: A) => B): (a: A) => C`.
2. Escribir dos funciones propias — por ejemplo `toUpperCase(s: string): string` y `exclaim(s: string): string` (que agregue `"!"` al final) — y componerlas con `compose`.
3. Aplicar la función compuesta al título de un libro del catálogo.

## 19. `Promise<T>`: conectando con Asincronismo

1. Escribir una función `async function fetchBookByTitle(title: string): Promise<Book>` que simule una consulta (con un `setTimeout` envuelto en una Promise, como en Asincronismo) y resuelva con un `Book` del catálogo según el `title`.
2. Escribir una función `async function loadAndDescribe(title: string): Promise<string>` que use `await fetchBookByTitle(title)` y devuelva el resultado de `describeBook` (ejercicio 6) sobre ese libro.
3. Confirmar que TypeScript conoce el tipo de `book` dentro de `loadAndDescribe` sin necesitar ninguna anotación extra en esa línea — viene inferido de `Promise<Book>`.

## 20. Cómo leer un error de compilación

1. Sin ejecutar todavía nada, mirar este fragmento y escribir en un comentario qué código de error (`TSxxxx`) esperás que tire TypeScript y por qué:
   ```ts
   function findBook(title: string): Book {
     return books.find((b) => b.title === title)
   }
   ```
2. Pegarlo en el Playground (o en tu editor) y confirmar el código de error real — ¿coincide con lo que escribiste?
3. Corregirlo (pista: `Array.find` puede devolver `undefined`) y confirmar que compila.

## 21. Instalar y correr TypeScript en tu máquina

1. Instalar TypeScript de forma global: `npm install -g typescript ts-node`.
2. Guardar cualquiera de las funciones de los ejercicios anteriores en un archivo suelto (`archivo.ts`, sin proyecto armado) y compilarlo con `tsc archivo.ts` — confirmar que aparece `archivo.js` al lado.
3. Correr el mismo archivo con `ts-node archivo.ts`, sin el paso de compilación manual, y comparar.
4. Probar `npx tsc --init` en una carpeta vacía para ver un `tsconfig.json` generado, y ubicar en él las opciones `target`, `outDir` y `strict` (usar el apunte como referencia).

## Para pensar

- `any` y `unknown` aceptan los mismos valores en la asignación, pero se comportan muy distinto al **usarlos**. ¿En qué situación real de un proyecto (por ejemplo, procesando la respuesta de una API externa) el uso de `any` en vez de `unknown` podría esconder un bug hasta producción?
- Después de probar la fusión de interfaces en el ejercicio 11, ¿en qué situación real de un proyecto grande esa fusión silenciosa podría esconder un bug en vez de ser la extensión deliberada que se buscaba?
- Los genéricos (`Array<T>`, `Promise<T>`, `ApiResponse<T>`, `pluck<T, K>`) parecen abstractos al principio, pero ya se venían usando implícitamente en JS Funcional cada vez que se escribía una función que funcionaba "para cualquier tipo de elemento" (como `map`). ¿Qué gana concretamente el código al hacer explícito, con TypeScript, algo que en JS ya funcionaba igual?
- `Partial<Book>` vuelve **todas** las propiedades opcionales, incluidas las que probablemente nunca deberían serlo (como `title`). ¿Cómo se podrían combinar `Partial` y `Pick` para expresar "solo `available` y `pages` son opcionales, el resto sigue siendo obligatorio"?
- `strict: true` en `tsconfig.json` activa varias reglas a la vez (`noImplicitAny`, `strictNullChecks`, entre otras). Investigá qué hace `strictNullChecks` puntualmente y escribí un ejemplo de código que compile sin esa opción pero falle con ella activada.
