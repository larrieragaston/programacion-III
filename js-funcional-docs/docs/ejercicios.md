# JS Funcional — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. Se recomienda resolverlos en orden — varios reutilizan el catálogo de productos que se arma en el ejercicio 1.

## 1. El catálogo

1. Crear un archivo `catalogo.js`.
2. Declarar un array `products` con al menos cinco productos, cada uno con `name`, `price`, `category` y `stock` (se puede reutilizar el catálogo del apunte y agregar uno o dos productos propios).
3. Sin usar ningún método de array todavía, escribir un `for` clásico que imprima el `name` de cada producto — esto sirve como punto de comparación para lo que sigue.

## 2. Funciones de primera clase

1. Escribir una función `formatPrice(price)` que devuelva el precio formateado como string (por ejemplo, `"$45.000"`).
2. Guardar `formatPrice` dentro de un objeto `formatters` junto con otra función `formatStock(stock)` que devuelva `"Disponible"` o `"Sin stock"` según corresponda.
3. Escribir una función `describe(product, formatters)` que reciba un producto y el objeto `formatters`, y devuelva un string combinando `name`, el resultado de `formatters.formatPrice` y el de `formatters.formatStock`.
4. Llamarla para cada producto del catálogo del ejercicio 1.

## 3. Puras vs. impuras

1. Escribir una función **impura** `applyGlobalDiscount(products, rate)` que recorra el array con un `for` y module directamente el `price` de cada objeto (mutando el catálogo original).
2. Probarla sobre el catálogo del ejercicio 1 y confirmar que, después de llamarla, el array original quedó modificado.
3. Reescribirla como una función **pura** `withGlobalDiscount(products, rate)` que devuelva un array **nuevo**, sin modificar el original (usar `map` y spread de objetos).
4. Confirmar que, después de llamar a la versión pura, `products` sigue intacto.

## 4. Inmutabilidad

1. Escribir una función `restock(products, productName, amount)` que debería sumarle `amount` al `stock` del producto que tenga `name === productName`, **sin mutar** ni el array ni los objetos originales.
2. Implementarla combinando `map` con spread de objetos (no usar `push`, ni asignar directamente sobre un elemento del array).
3. Escribir un test manual: guardar el catálogo original en una variable aparte antes de llamar a `restock`, y después comparar (con `console.log` o `assert`) que el original no cambió.

## 5. `map`

1. A partir del catálogo, generar un array `names` con únicamente los nombres de los productos.
2. Generar un array `pricesWithTax` con el precio de cada producto incrementado un 21% (sin modificar el catálogo original).
3. Generar un array de strings usando la función `describe` del ejercicio 2 combinada con `map` (en vez de un bucle manual).

## 6. `filter`

1. Obtener un array `inStock` con los productos que tienen `stock > 0`.
2. Obtener un array `expensive` con los productos que cuestan más de $100.000.
3. Combinar ambos criterios en un solo `filter` (con `&&`) para obtener los productos caros que además tienen stock.

## 7. `reduce`

1. Calcular `totalInventoryValue`: la suma de `price * stock` de todos los productos, usando `reduce`.
2. Calcular `productCountByCategory`: un objeto donde cada clave es una categoría y el valor es la cantidad de productos de esa categoría (por ejemplo `{ accesorios: 2, monitores: 1 }`).
3. Calcular `mostExpensiveProduct`: el producto con el `price` más alto, usando `reduce` sin ordenar el array primero.

## 8. Pipeline

1. En un solo pipeline encadenado (`filter` → `filter` → `reduce`, sin variables intermedias), calcular el valor total del stock disponible de la categoría `"accesorios"`.
2. Agregar un `.map` al principio de la cadena para aplicar primero un 10% de descuento a todos los precios, y después calcular el mismo total que en el punto anterior sobre los precios ya descontados.
3. Compararlo con la resolución equivalente en Clojure: escribir, como comentario, la misma operación con `->>`, `filter` y `reduce`.

## 9. Composición

1. Escribir las funciones puras `applyDiscount(rate)` (devuelve una función que aplica ese descuento a un precio), `addTax(price)` y `roundPrice(price)`.
2. Escribir un `compose` y un `pipe` propios (sin copiar el del apunte de memoria — implementarlos de nuevo).
3. Usar `pipe` para construir `finalPrice`, que aplique en orden: 15% de descuento → impuesto → redondeo.
4. Probar `finalPrice` sobre tres precios distintos del catálogo.

## 10. Currying y aplicación parcial

1. Escribir `applyDiscount(rate, price)` sin currificar (función de dos argumentos).
2. Currificarla a mano: `applyDiscountCurried = rate => price => ...`.
3. A partir de la versión currificada, crear `applyBlackFridayDiscount` con un descuento fijo del 30%, y `applyClearanceDiscount` con un 50%, sin escribir de nuevo la lógica del descuento.
4. Resolver el mismo punto 3, pero partiendo de la versión **sin currificar** y usando `fn.bind(null, ...)` en lugar de currying manual.

## 11. Recursividad

1. Escribir una función recursiva `sumStock(products)` que sume el `stock` de todos los productos sin usar `reduce` ni ningún bucle (`for`/`while`).
2. Escribir una función recursiva `countInCategory(products, category)` que cuente cuántos productos hay de una categoría dada.
3. Probar `sumStock` con un array de más de 10.000 elementos generado con un bucle simple. Si tira `RangeError: Maximum call stack size exceeded`, anotar a partir de qué tamaño aproximado ocurre en tu entorno, y reescribir esa misma función usando `reduce` para comparar.

## Para pensar

- ¿Por qué `Object.freeze(products[0])` no alcanza para evitar que alguien haga `products[0] = otroProducto`? ¿Qué diferencia hay entre congelar un objeto y no poder reasignar la variable que lo contiene?
- El ejercicio 11 mostró que JS no garantiza *tail call optimization*. ¿Qué hace que la versión con `reduce` no tenga ese problema, si por dentro también recorre todo el array?
- En Clojure, `(map inc coll)` nunca muta `coll`. ¿Qué tendría que hacer un equipo de trabajo en JS (convenciones, revisión de código, herramientas) para conseguir esa misma garantía, ya que el lenguaje no la da gratis?
