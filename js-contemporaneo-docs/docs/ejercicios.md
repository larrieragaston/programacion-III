# JS Contemporáneo — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. Los primeros son ejercicios cortos de sintaxis; a partir del ejercicio 6 se arma y reutiliza un catálogo de una biblioteca — un dominio distinto al del apunte y las slides, a propósito.

## 1. `let` vs. `var`

1. Escribir un `for` clásico con `var i` que guarde 3 funciones en un array — cada función debería, al ejecutarse, imprimir el valor de `i` en ese momento.
2. Ejecutar las 3 funciones guardadas y anotar qué imprime cada una. ¿Es lo que esperabas?
3. Repetir el mismo `for`, cambiando `var` por `let`, y comparar el resultado con el punto 2.
4. Explicar con tus palabras, en un comentario, a qué se debe la diferencia.

## 2. Arrow functions y `this`

1. Escribir una función constructora tradicional `Timer(seconds)` que guarde `seconds` en `this.seconds`, y que usando `setTimeout` con una **función tradicional** intente imprimir `this.seconds` después de 100ms.
2. Ejecutarla y anotar qué imprime (probablemente no lo esperado).
3. Reescribir el mismo `setTimeout` usando una **arrow function**, y confirmar que ahora sí imprime el valor correcto.
4. Explicar en un comentario por qué cambia el resultado.

## 3. Template literals

1. Declarar variables `title`, `author` y `year` con los datos de un libro cualquiera.
2. Construir un string `citation` con template literals que arme una cita en el formato `"Título (Autor, Año)"`.
3. Construir un string multilínea `summary` (usando backticks, sin `\n`) con al menos 3 líneas describiendo el mismo libro.

## 4. Parámetros por defecto, rest y spread

1. Escribir una función `formatPrice(amount, currency = 'ARS')` que devuelva el string `"$amount currency"` (por ejemplo, `formatPrice(1500)` → `"$1500 ARS"`).
2. Escribir una función `sumAll(...numbers)` que sume una cantidad variable de argumentos usando `reduce`.
3. Declarar un array `prices = [100, 250, 80]` y llamar a `sumAll` pasándole el array con spread, sin escribir los números a mano.

## 5. Destructuring

1. Declarar `const person = { name: 'Ada', age: 29, address: { city: 'Londres' } }`.
2. Desestructurar `name` y `age` en una sola línea, renombrando `age` a `edad`.
3. Desestructurar `city` desde dentro de `address` en la misma línea que el punto anterior (destructuring anidado).
4. Escribir una función `greet` que reciba directamente un objeto con `name` y un `greeting` opcional (con valor por defecto `"Hola"`) desestructurado en la firma, y devuelva `"${greeting}, ${name}!"`.

## 6. El catálogo

1. Crear un archivo `biblioteca.js`.
2. Declarar un array `books` con al menos cinco libros, cada uno con `title`, `author`, `year`, `pages` y `available` (booleano). Que al menos uno tenga `available: false`.
3. Con destructuring de array, extraer el primer y el último libro del catálogo en dos variables, sin usar índices (`books[0]`, `books[books.length - 1]`).

## 7. Modificar el catálogo

1. Con `push`, agregar un libro nuevo al final de `books`.
2. Con `unshift`, agregar otro libro al principio.
3. Con `splice`, quitar el libro que quedó en la posición 2 (índice 2) sin usar `pop` ni `shift`.
4. Después de cada operación, imprimir `books.length` para confirmar que cambió.

## 8. Derivar sin mutar

1. Usando `slice`, obtener un array `firstThree` con los primeros tres libros del catálogo, sin modificar `books`.
2. Usando `concat`, construir un array `extendedCatalog` que sea `books` más dos libros nuevos, sin modificar `books`.
3. Confirmar con `console.log` que `books` no cambió en ninguno de los dos pasos.
4. **Opcional** (si tu versión de Node lo soporta, ver `node -v` en el apunte): repetí el punto 1 del ejercicio 9 (ordenar por `year`) pero con `toSorted()` en vez de spread + `sort()`, y comparalo — ¿cuál preferís?

## 9. `sort`

1. Ordenar una copia del catálogo (¡no mutar `books`! copiarlo primero con spread) por `year` ascendente, usando una función comparadora.
2. Ordenar otra copia por `pages` descendente.
3. Ordenar una tercera copia por `author` alfabéticamente, usando `localeCompare`.

## 10. Buscar en el catálogo

1. Con `find`, obtener el primer libro disponible (`available: true`).
2. Con `findIndex`, obtener la posición de un libro por su `title` exacto.
3. Con `some`, verificar si hay al menos un libro publicado antes de 1950.
4. Con `every`, verificar si todos los libros tienen más de 100 páginas.

## 11. `forEach`, `Array.from` y `flatMap`

1. Con `forEach`, recorrer `books` e imprimir por consola una línea por libro con el formato `"${title} (${year})"` — sin construir ningún array nuevo.
2. Con `Array.from`, crear un array `bookNumbers` de 5 elementos con los números del 1 al 5, usando la función mapeadora de `Array.from` (sin escribir el array a mano).
3. Declarar `const extraCatalog = [{ title: 'Libro extra', author: 'Anónimo', year: 2020, pages: 50, available: true }]` y, con `flatMap` sobre `[books, extraCatalog]`, armar un único array `allBooks` con todos los libros de ambos catálogos.
4. Con `Array.isArray`, confirmar que `allBooks` es un array — y que, por ejemplo, `allBooks[0].title` no lo es.

## 12. Optional chaining y nullish coalescing

1. Agregar a uno de los libros del catálogo una propiedad `reviews` con un array de objetos `{ author, rating }`, y a otro libro no agregarle esa propiedad.
2. Escribir una función `firstReviewRating(book)` que devuelva el `rating` de la primera reseña usando **optional chaining**, sin que tire error para el libro que no tiene `reviews`.
3. Usando **nullish coalescing**, hacer que `firstReviewRating` devuelva `"Sin reseñas"` en vez de `undefined` cuando no hay ninguna.

## 13. `==` vs. `===`

1. Escribir al menos tres comparaciones con `==` que den `true` pero que con `===` den `false` (a partir de valores del catálogo, por ejemplo comparando `year` con su versión en string).
2. Para cada una, escribir un comentario explicando qué conversión de tipos está haciendo `==` por detrás.

## Para pensar

- ¿Por qué la convención moderna es evitar `var` casi por completo? Pensalo en términos de qué bugs evita `let`/`const` que con `var` eran comunes.
- `??` y `||` se comportan igual para casi todos los valores, salvo un puñado de casos puntuales. ¿En qué situación real de un formulario o una API podría un bug por usar `||` en vez de `??` pasar desapercibido en las pruebas y aparecer recién en producción?
- ES Modules y CommonJS pueden convivir en un mismo proyecto Node. ¿Qué señales (extensión de archivo, configuración de `package.json`, sintaxis del propio código) permiten reconocer cuál se está usando en un proyecto que no escribiste vos?
- Corré `node -v` en tu máquina — ¿tu versión soporta `toSorted()`/`with()` (ES2023)? Si tuvieras que trabajar en dos proyectos que necesitan versiones distintas de Node al mismo tiempo, ¿cómo resolverías eso sin reinstalar Node cada vez? (pista: buscá qué es `nvm`).
