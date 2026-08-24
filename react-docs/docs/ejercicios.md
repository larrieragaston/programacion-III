# React — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. Se recomienda un proyecto nuevo con Vite (`npm create vite@latest` → template `react-ts`) para resolverlos. El catálogo de productos (`interface Product { name: string; price: number }`) es el mismo dominio usado en TypeScript.

## 1. Primer componente

1. Crear un componente `Greeting` que reciba un prop `name: string` (tipado con una `interface GreetingProps`) y muestre `"Hola, {name}!"` en un `<h1>`.
2. Usarlo en `App` con al menos dos valores distintos de `name`.

## 2. Composición

1. Crear un componente `ProductCard` con `interface ProductCardProps { name: string; price: number }` que muestre el nombre y el precio.
2. Crear un componente `ProductList` que renderice tres `ProductCard` distintas, componiéndolas dentro de un `<div>`.

## 3. `useState`: contador

1. Crear un componente `Counter` con `useState(0)`.
2. Agregar dos botones: uno que incremente el contador, otro que lo decremente.
3. Agregar un tercer botón "Reset" que lleve el contador de vuelta a `0`.

## 4. `useState`: no mutar

1. Crear un componente `Cart` con `useState<string[]>([])` para una lista de productos en un carrito.
2. Agregar un botón "Agregar Mouse" que use spread (`[...items, 'Mouse']`) para agregar un ítem — nunca `push`.
3. Agregar un botón "Vaciar" que reemplace el estado por un array vacío.
4. Mostrar la cantidad de ítems con `{items.length}`.

## 5. El catálogo

1. Declarar `interface Product { name: string; price: number; stock: number }`.
2. Declarar un array `const products: Product[]` con al menos cinco productos (fuera de cualquier componente, como datos de ejemplo).
3. Crear un componente `ProductList({ products }: { products: Product[] })` que renderice la lista completa con `map` y `key={p.name}`.

## 6. Renderizado condicional

1. Crear un componente `StockBadge({ stock }: { stock: number })` que muestre `"Sin stock"` si `stock === 0`, o `"Disponible"` en cualquier otro caso.
2. Usarlo dentro de cada `ProductCard` de la lista del ejercicio 5, agregando `stock` al `interface Product` y a los props de `ProductCard`.

## 7. Filtrar con estado

1. Sobre `ProductList`, agregar `useState<boolean>(false)` para un flag `onlyAvailable`.
2. Agregar un botón que alterne (*toggle*) ese estado.
3. Cuando `onlyAvailable` es `true`, filtrar la lista (con `filter`, de JS Funcional) para mostrar solo los productos con `stock > 0` antes de mapearlos.

## 8. Input controlado

1. Crear un componente `SearchBox` con un `<input>` controlado por `useState<string>('')`.
2. Mostrar el valor actual del input en un `<p>` debajo, actualizado en cada tecla.

## 9. Formulario con filtro

1. Combinar el `SearchBox` del ejercicio 8 con el catálogo del ejercicio 5: un componente `ProductFilter({ products }: { products: Product[] })` con un input controlado.
2. Filtrar el catálogo por nombre (`p.name.toLowerCase().includes(query.toLowerCase())`) y renderizar el resultado con `map`/`key`.
3. Mostrar la cantidad de resultados encontrados.

## 10. Formulario con dos campos

1. Extender `ProductFilter` con un segundo input, numérico, para un precio máximo (`useState<number>`).
2. Combinar ambos filtros (nombre y precio máximo) en un único `filter`.
3. Si el input de precio está vacío, no debería filtrar por precio (pensar qué valor inicial y qué condición usar).

## 11. `useEffect` con timer

1. Crear un componente `Clock` que use `useState<number>` para guardar los segundos transcurridos, inicializado en `0`.
2. Usar `useEffect` con `setInterval` para incrementar el contador cada segundo. **Importante**: `useEffect` puede devolver una función de limpieza — usarla para hacer `clearInterval` cuando el componente se desmonte.
3. Mostrar el valor actual en pantalla.

## 12. `useEffect` + `fetch`: conectando con Asincronismo

1. Escribir una función `fetchProducts(): Promise<Product[]>` que simule una llamada a una API (con un `setTimeout` de 1 segundo envuelto en una Promise, como en Asincronismo) y resuelva con el catálogo del ejercicio 5.
2. Crear un componente `AsyncProductList` que use `useState<Product[]>([])` y `useState<boolean>(true)` (para `loading`).
3. Dentro de un `useEffect` con dependencias `[]`, declarar una función `async` interna que llame a `fetchProducts`, actualice el estado con el resultado, y ponga `loading` en `false`.
4. Mientras `loading` es `true`, mostrar `"Cargando..."`; cuando termine, mostrar la lista con `map`/`key`.

## 13. Todo junto

1. Combinar los ejercicios 9 (filtro por nombre), 10 (filtro por precio) y 12 (carga asíncrona) en un único componente `ProductCatalog`.
2. Mientras el catálogo está cargando (`loading`), no mostrar los inputs de filtro — solo el mensaje de carga.
3. Una vez cargado, mostrar los inputs y aplicar ambos filtros sobre los datos ya cargados.

## Para pensar

- `useState` obliga a crear una copia nueva del estado en cada actualización (spread, `map`, `filter`) en vez de mutar el valor anterior. ¿Qué relación tiene esto con la inmutabilidad vista en JS Funcional? ¿Por qué mutar directamente el estado "a veces funciona visualmente" pero es un bug esperando a pasar?
- `key` en una lista renderizada con `map` debería ser, idealmente, un identificador estable de los datos (un `id`), no el índice del array. Investigá o pensá un escenario concreto (por ejemplo, una lista donde se puede eliminar un ítem del medio) donde usar el índice como `key` produzca un bug visible — ¿qué se ve mal en la pantalla?
- `useEffect` con dependencias `[]` corre una sola vez, al montar el componente. ¿Qué pasaría si el `fetch` de productos dependiera de un `categoryId` que puede cambiar (por ejemplo, un selector de categoría)? ¿Qué array de dependencias habría que usar, y por qué `[]` ya no alcanzaría en ese caso?
- Un componente de React se presentó como "una función pura de props/state a JSX". `useEffect` introduce, a propósito, un lugar para código con efectos secundarios (no puro) dentro de un componente. ¿Por qué React separa explícitamente el cuerpo del componente (que debería ser puro) del código de los efectos, en vez de permitir side effects en cualquier parte del componente?
