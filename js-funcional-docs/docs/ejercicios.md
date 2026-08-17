# JS Funcional — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. Se recomienda resolverlos en orden — varios reutilizan la playlist que se arma en el ejercicio 1. A propósito usan un dominio distinto al catálogo de productos del apunte y las slides: la idea es aplicar los mismos conceptos sobre datos que no viste todavía, no transcribir un ejemplo ya resuelto.

## 1. La playlist

1. Crear un archivo `playlist.js`.
2. Declarar un array `songs` con al menos cinco canciones, cada una con `title`, `artist`, `genre`, `durationSec` (duración en segundos) y `plays` (reproducciones). Que al menos una tenga `plays: 0`.
3. Sin usar ningún método de array todavía, escribir un `for` clásico que imprima el `title` de cada canción — esto sirve como punto de comparación para lo que sigue.

## 2. Funciones de primera clase

1. Escribir una función `formatDuration(durationSec)` que devuelva la duración en formato `"m:ss"` (por ejemplo, `225` segundos → `"3:45"`, con los segundos siempre en dos dígitos).
2. Guardar `formatDuration` dentro de un objeto `formatters` junto con otra función `formatPlays(plays)` que devuelva `"Sin reproducciones"` si `plays === 0`, o el número con separador de miles en caso contrario (por ejemplo, `"1.800.000"`, usar `toLocaleString('es-AR')`).
3. Escribir una función `describe(song, formatters)` que reciba una canción y el objeto `formatters`, y devuelva un string combinando `title`, `artist`, el resultado de `formatters.formatDuration` y el de `formatters.formatPlays`.
4. Llamarla para cada canción de la playlist del ejercicio 1.

## 3. Puras vs. impuras

1. Escribir una función **impura** `applyViralBoost(songs, multiplier)` que recorra el array con un `for` y multiplique directamente el `plays` de cada canción (mutando la playlist original).
2. Probarla sobre la playlist del ejercicio 1 y confirmar que, después de llamarla, el array original quedó modificado.
3. Reescribirla como una función **pura** `withViralBoost(songs, multiplier)` que devuelva un array **nuevo**, sin modificar el original (usar `map` y spread de objetos).
4. Confirmar que, después de llamar a la versión pura, `songs` sigue intacto.

## 4. Inmutabilidad

1. Escribir una función `addPlays(songs, songTitle, amount)` que debería sumarle `amount` al `plays` de la canción que tenga `title === songTitle`, **sin mutar** ni el array ni los objetos originales.
2. Implementarla combinando `map` con spread de objetos (no usar `push`, ni asignar directamente sobre un elemento del array).
3. Escribir un test manual: guardar la playlist original en una variable aparte antes de llamar a `addPlays`, y después comparar (con `console.log` o `assert`) que el original no cambió.

## 5. `map`

1. A partir de la playlist, generar un array `titles` con únicamente los títulos de las canciones.
2. Generar un array `durationsFormatted` con la duración de cada canción formateada como `"m:ss"` (usando `formatDuration` del ejercicio 2).
3. Generar un array de strings usando la función `describe` del ejercicio 2 combinada con `map` (en vez de un bucle manual).

## 6. `filter`

1. Obtener un array `played` con las canciones que tienen `plays > 0`.
2. Obtener un array `longSongs` con las canciones que duran más de 5 minutos (`durationSec > 300`).
3. Combinar ambos criterios en un solo `filter` (con `&&`) para obtener las canciones largas que además tienen reproducciones.

## 7. `reduce`

1. Calcular `totalDuration`: la suma de `durationSec` de todas las canciones, usando `reduce`.
2. Calcular `songCountByGenre`: un objeto donde cada clave es un género y el valor es la cantidad de canciones de ese género (por ejemplo `{ rock: 2, pop: 1 }`).
3. Calcular `mostPlayedSong`: la canción con más `plays`, usando `reduce` sin ordenar el array primero.

## 8. Pipeline

1. En un solo pipeline encadenado (`filter` → `filter` → `reduce`, sin variables intermedias), calcular la duración total de las canciones de género `"rock"` que tienen reproducciones.
2. Agregar un `.map` al principio de la cadena para aplicar primero un boost del 20% a `plays` de todas las canciones, y después calcular el mismo total que en el punto anterior sobre la playlist ya boosteada.
3. Compararlo con la resolución equivalente en Clojure: escribir, como comentario, la misma operación con `->>`, `filter` y `reduce`.

## 9. Composición

1. Escribir las funciones puras `applyBoost(rate)` (devuelve una función que aplica ese boost a un valor de `plays`), `addBonusPlays(amount)` y `roundPlays(plays)`.
2. Escribir un `compose` y un `pipe` propios (sin copiar el del apunte de memoria — implementarlos de nuevo).
3. Usar `pipe` para construir `finalPlays`, que aplique en orden: 25% de boost → 1000 reproducciones bonus → redondeo.
4. Probar `finalPlays` sobre tres valores de `plays` distintos de la playlist.

## 10. Currying y aplicación parcial

1. Escribir `applyBoost(rate, plays)` sin currificar (función de dos argumentos).
2. Currificarla a mano: `applyBoostCurried = rate => plays => ...`.
3. A partir de la versión currificada, crear `applyViralBoost` con un boost fijo del 200%, y `applyModerateBoost` con un 20%, sin escribir de nuevo la lógica del boost.
4. Resolver el mismo punto 3, pero partiendo de la versión **sin currificar** y usando `fn.bind(null, ...)` en lugar de currying manual.

## 11. Recursividad

1. Escribir una función recursiva `sumDuration(songs)` que sume la `durationSec` de todas las canciones sin usar `reduce` ni ningún bucle (`for`/`while`).
2. Escribir una función recursiva `countInGenre(songs, genre)` que cuente cuántas canciones hay de un género dado.
3. Probar `sumDuration` con un array de más de 10.000 elementos generado con un bucle simple. Si tira `RangeError: Maximum call stack size exceeded`, anotar a partir de qué tamaño aproximado ocurre en tu entorno, y reescribir esa misma función usando `reduce` para comparar.

## Para pensar

- ¿Por qué `Object.freeze(songs[0])` no alcanza para evitar que alguien haga `songs[0] = otraCancion`? ¿Qué diferencia hay entre congelar un objeto y no poder reasignar la variable que lo contiene?
- El ejercicio 11 mostró que JS no garantiza *tail call optimization*. ¿Qué hace que la versión con `reduce` no tenga ese problema, si por dentro también recorre todo el array?
- En Clojure, `(map inc coll)` nunca muta `coll`. ¿Qué tendría que hacer un equipo de trabajo en JS (convenciones, revisión de código, herramientas) para conseguir esa misma garantía, ya que el lenguaje no la da gratis?
