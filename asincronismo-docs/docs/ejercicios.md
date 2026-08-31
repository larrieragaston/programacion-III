# Asincronismo — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. Los primeros trabajan sobre funciones simuladas con `setTimeout`; a partir del ejercicio 17 se usan las APIs públicas reales del apunte (nationalize.io, restcountries.com) con `fetch`. El orden sigue el mismo recorrido que el apunte: primero el modelo del event loop (call stack, Web APIs, colas), después callbacks, después Promises, y por último `async`/`await`.

## 1. Bloquear el hilo (para entenderlo, no para repetirlo)

1. Escribir la función `blockFor(ms)` del apunte (un `while` que ocupa la CPU durante `ms` milisegundos).
2. Ejecutar `console.log('Antes')`, `blockFor(3000)`, `console.log('Después')` en la consola del navegador.
3. Mientras corre `blockFor`, intentar interactuar con la página (scroll, click en algo). Anotar qué se observa.
4. Explicar en un comentario, con tus palabras, por qué pasa eso — conectándolo con que JS tiene un solo hilo.

## 2. Call stack, a mano

1. Escribir tres funciones `multiply(a, b)`, `square(n)` (que use `multiply`) y `printSquare(n)` (que use `square`), como en el apunte.
2. Llamar a `printSquare(5)` y confirmar el resultado.
3. En un comentario, listar el orden exacto en el que se apilan y desapilan las tres funciones.

## 3. Orden de ejecución: sync vs. `setTimeout`

1. Escribir tres `console.log` — uno antes, uno dentro de un `setTimeout(fn, 0)`, y uno después — como en el ejemplo del apunte.
2. Antes de ejecutar, predecir el orden de salida en un comentario.
3. Ejecutar y confirmar si la predicción fue correcta.
4. Repetir el ejercicio, pero esta vez con dos `setTimeout` distintos: uno con `1000` ms y otro con `500` ms, escritos en ese orden en el código. ¿En qué orden se ejecutan?

## 4. Trazando el event loop, paso a paso

1. Escribir el ejemplo del apunte con cinco líneas: `console.log('A')`, `setTimeout(() => console.log('B'), 0)`, `console.log('C')`, `setTimeout(() => console.log('D'), 0)`, `console.log('E')`.
2. Antes de ejecutar, escribir en comentarios los siete pasos del razonamiento (qué se apila, qué se delega, qué queda encolado y cuándo) — no solo el resultado final.
3. Ejecutar y confirmar el orden real de salida.
4. Modificar el ejemplo agregando un tercer `setTimeout(() => console.log('F'), 0)` entre `'C'` y `'D'`. Volver a predecir el orden completo antes de ejecutar.

## 5. Predecir el orden: microtasks y macrotasks mezclados

Este ejercicio es de **lectura**, no de escritura desde cero — la sintaxis de Promises y `async`/`await` recién se ve en detalle más adelante, pero alcanza con reconocerla para seguir el ejemplo.

1. Copiar tal cual el ejemplo combinado del apunte (el que mezcla `setTimeout`, un callback armado con `setTimeout`, `Promise.resolve().then()` y una función `async` con un `await`).
2. Antes de ejecutar, escribir en un comentario el orden completo predicho, justificando cada posición con la regla de prioridad (sincrónico → microtasks → macrotasks).
3. Ejecutar y confirmar.
4. Agregar un segundo `Promise.resolve().then(...)` más, después del que ya existía. ¿En qué posición del orden final aparece? ¿Antes o después de la continuación del `await`?

## 6. Callback simple

1. Escribir una función `fetchUserName(id, callback)` que, usando `setTimeout` con 1 segundo de demora, llame a `callback` con `'Ada'` si `id === 1`, o con `'invitado'` en cualquier otro caso.
2. Llamarla con `id = 1` y con `id = 2`, imprimiendo el resultado en cada callback.
3. Agregar un `console.log` inmediatamente después de cada llamada a `fetchUserName` y confirmar que se imprime antes que el resultado del callback.

## 7. Callback error-first

1. Escribir `getPersonaById(id, callback)` que simule una consulta a una base de datos (con `setTimeout` de 1 segundo): si `id > 0`, invoca `callback(null, { id, nombre: 'Pepe' })`; si no, invoca `callback({ error: true, msg: 'ID inválido' })`.
2. Escribir un callback `procesarPersona(err, res)` que loguee el error si existe, o el resultado si no.
3. Llamar a `getPersonaById` con un `id` válido y con uno inválido, usando `procesarPersona` en ambos casos.

## 8. Callback hell (a propósito)

1. Escribir tres funciones simuladas con callback: `fetchUser(id, cb)`, `fetchOrders(userId, cb)` y `fetchOrderCount(orderId, cb)` — cada una con un `setTimeout` corto y un resultado inventado cualquiera.
2. Encadenarlas **anidando** los callbacks: llamar a `fetchUser`, dentro de su callback llamar a `fetchOrders` con el `id` del usuario, y dentro de ese callback llamar a `fetchOrderCount` con el primer pedido.
3. Contar cuántos niveles de indentación tiene el resultado final.
4. En un comentario, escribir qué pasaría si cada una de las tres funciones pudiera fallar y hubiera que manejar el error en cada nivel por separado.

## 9. De callback a Promise

1. Reescribir las tres funciones del ejercicio 8 (`fetchUser`, `fetchOrders`, `fetchOrderCount`) para que devuelvan una `Promise` en vez de recibir un callback (usando `new Promise((resolve, reject) => {...})`).
2. Encadenar las tres con `.then()`, en vez de anidar callbacks.
3. Agregar un único `.catch()` al final y comparar: ¿cuántas veces aparece el manejo de errores acá, contra el ejercicio 8?

## 10. Crear y probar una Promise a mano

1. Escribir una función `fetchUserName(id)` que devuelva una Promise: si `id > 0`, se resuelve con `'Ada'` o `'invitado'` (como en el apunte); si `id <= 0`, rechaza con un `Error('id inválido')`.
2. Consumirla con `.then(...).catch(...).finally(...)`, imprimiendo algo distinto en cada uno de los tres métodos.
3. Llamarla una vez con un `id` válido y otra con uno inválido, y confirmar que en cada caso se ejecuta la rama esperada — y que `.finally` corre en **ambos** casos.
4. En un comentario, escribir qué valor tendría `value`/`reason` en cada uno de los tres estados posibles de la Promise que creaste.

## 11. Errores puntuales en la cadena

1. A partir de las Promises del ejercicio 9, armar una cadena donde el primer `.catch()` esté pegado **inmediatamente** después de `fetchUser` (no después de `fetchOrders`), y haga `return null` en vez de cortar todo.
2. Agregar un `.then()` que chequee si el valor recibido es `null` (en cuyo caso no llama a `fetchOrders`, devuelve `[]` directamente) o sigue la cadena normalmente si no.
3. Agregar un segundo `.catch()` al final, para los errores de `fetchOrders`.
4. Forzar un error en `fetchUser` (por ejemplo, pasándole un `id` inválido) y confirmar que el mensaje de consola indica claramente que el problema fue en `fetchUser`, no en `fetchOrders`.

## 12. `Promise.all`

1. Con las funciones del ejercicio 9 (o inventando tres funciones nuevas que devuelvan Promises con distintos tiempos de demora), usar `Promise.all` para dispararlas todas a la vez.
2. Medir el tiempo total con `console.time`/`console.timeEnd` alrededor de la llamada.
3. Comparar ese tiempo contra encadenarlas con `.then()` una después de la otra (mismo `console.time`). Confirmar que `Promise.all` es más rápido cuando las operaciones no dependen entre sí.

## 13. `Promise.allSettled`

1. Armar un array de tres llamadas a una función que devuelva Promises (por ejemplo, `fetchUserName` del ejercicio 10), donde al menos una de ellas esté armada para rechazar (un `id` inválido).
2. Usar `Promise.allSettled` en vez de `Promise.all` y recorrer el array de resultados con `.forEach`, imprimiendo el valor si `status === 'fulfilled'` o el motivo si `status === 'rejected'`.
3. Repetir el mismo array de llamadas pero con `Promise.all` en vez de `Promise.allSettled`. Confirmar y explicar en un comentario la diferencia de comportamiento entre ambos.

## 14. `Promise.all` contra una función sincrónica

1. Escribir tres funciones **sincrónicas** (sin `setTimeout`, sin Promises) que tarden un rato en CPU — por ejemplo, usando algo similar a `blockFor` del ejercicio 1 con distintos tiempos.
2. Envolver cada llamada en `Promise.resolve(miFuncionSincronica())` y pasarlas a `Promise.all`.
3. Medir el tiempo total con `console.time`/`console.timeEnd`. Compararlo contra la suma de los tres tiempos individuales de `blockFor`.
4. En un comentario, explicar por qué el resultado confirma (o no) que `Promise.all` no acelera código que ya era bloqueante.

## 15. `async`/`await`

1. Tomar la cadena de `.then()` del ejercicio 9 y reescribirla como una función `async` usando `await` en cada paso.
2. Envolver el cuerpo en un `try`/`catch` y confirmar que un error en cualquiera de las tres funciones simuladas se atrapa correctamente.
3. Forzar un error a propósito (por ejemplo, hacer que `fetchOrders` rechace si el `userId` es par) y confirmar que el `catch` lo atrapa.
4. Agregar una condición dentro del mismo `catch` que distinga, por alguna propiedad del error (por ejemplo `error.status` o `error.message`), entre dos tipos de error distintos, con un mensaje diferente para cada uno.

## 16. El `try`/`catch` que no atrapa nada

1. Escribir la función `loadUser(id)` del apunte: un `try`/`catch` sincrónico que envuelve un `setTimeout` cuyo callback hace `throw` si `id <= 0`.
2. Ejecutarla con un `id` inválido y confirmar que el `catch` **no** se ejecuta (el error aparece como no capturado en la consola).
3. En un comentario, explicar por qué pasa esto usando el modelo de call stack / task queue / event loop del apunte.
4. Reescribir la misma función usando una Promise (o `async`/`await`) en vez de un `setTimeout` con `throw` directo, y confirmar que ahora sí se puede atrapar el error con `catch`.

## 17. `fetch` real: nationalize.io

1. Escribir una función `async averiguarPais(nombre)` que haga `fetch` a `https://api.nationalize.io/?name=${nombre}`, chequee `res.ok`, y loguee el `country_id` con mayor `probability` (usando `reduce`, como en el apunte).
2. Probarla con al menos tres nombres distintos.
3. Envolver el cuerpo en `try`/`catch` y forzar un error escribiendo mal la URL (por ejemplo, `nazme=` en vez de `name=`). Confirmar que el `catch` lo atrapa y no rompe el programa.

## 18. Encadenar dos `fetch` reales

1. A partir de `averiguarPais` del ejercicio anterior, agregar un segundo `fetch` a `https://restcountries.com/v3.1/alpha/${paisId}` usando el `country_id` obtenido en el primer paso.
2. Mostrar el nombre del país en español (`translations.spa.common`) usando el resultado del segundo `fetch`.
3. Todo dentro de un único `try`/`catch`, chequeando `res.ok` en **ambas** llamadas.
4. Como cierre: medir con `console.time`/`console.timeEnd` cuánto tarda esta versión secuencial (el segundo `fetch` depende del primero), y explicar en un comentario por qué acá **no** tendría sentido usar `Promise.all` para estas dos llamadas puntuales.

## Para pensar

- ¿Por qué `fetch` no rechaza automáticamente cuando el servidor responde con un código de error HTTP (404, 500)? ¿Qué problema traería que sí lo hiciera, para casos donde justamente se quiere leer el cuerpo de una respuesta de error?
- Un componente de interfaz necesita mostrar un spinner de carga mientras espera datos, y ocultarlo tanto si la carga fue exitosa como si falló. ¿Qué método de Promise (o construcción equivalente con `async`/`await`) es el más adecuado para ocultar el spinner, sin duplicar esa línea en el `then` y en el `catch`?
- El apunte explica que, en el navegador, las Web APIs corren en threads del sistema operativo separados del hilo de JS — es decir, ahí sí hay paralelismo real, aunque JS en sí siga siendo de un solo hilo. ¿Cambia esto la respuesta a "JavaScript es de un solo hilo"? Distinguí, en tus palabras, qué parte del sistema es de un solo hilo y cuál no.
- Si una función `async` hace `throw new Error('algo')` de forma completamente sincrónica (sin ningún `await` de por medio), ¿el programa se rompe ahí mismo como con una función normal, o pasa otra cosa? Probalo y explicá el resultado conectándolo con "una función `async` siempre devuelve una Promise".
- Con lo que se vio en microtasks vs. macrotasks: si un mismo programa combina varios `setTimeout` con distintos delays, varias Promises encadenadas y una función `async`, ¿alcanza con mirar los valores de los delays para predecir el orden final de ejecución? Justificá con un ejemplo propio.
- `Promise.all` rechaza apenas la primera promise del array rechaza, sin esperar a las demás, y `Promise.allSettled` en cambio espera a todas. Pensá una situación real (no la del apunte) donde convendría usar cada uno de los dos, y explicá por qué.
