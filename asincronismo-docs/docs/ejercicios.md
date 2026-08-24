# Asincronismo — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. Los primeros trabajan sobre funciones simuladas con `setTimeout`; a partir del ejercicio 8 se usan las APIs públicas reales del apunte (nationalize.io, restcountries.com) con `fetch`.

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

## 4. Callback simple

1. Escribir una función `fetchUserName(id, callback)` que, usando `setTimeout` con 1 segundo de demora, llame a `callback` con `'Ada'` si `id === 1`, o con `'invitado'` en cualquier otro caso.
2. Llamarla con `id = 1` y con `id = 2`, imprimiendo el resultado en cada callback.
3. Agregar un `console.log` inmediatamente después de cada llamada a `fetchUserName` y confirmar que se imprime antes que el resultado del callback.

## 5. Callback error-first

1. Escribir `getPersonaById(id, callback)` que simule una consulta a una base de datos (con `setTimeout` de 1 segundo): si `id > 0`, invoca `callback(null, { id, nombre: 'Pepe' })`; si no, invoca `callback({ error: true, msg: 'ID inválido' })`.
2. Escribir un callback `procesarPersona(err, res)` que loguee el error si existe, o el resultado si no.
3. Llamar a `getPersonaById` con un `id` válido y con uno inválido, usando `procesarPersona` en ambos casos.

## 6. Callback hell (a propósito)

1. Escribir tres funciones simuladas con callback: `fetchUser(id, cb)`, `fetchOrders(userId, cb)` y `fetchOrderCount(orderId, cb)` — cada una con un `setTimeout` corto y un resultado inventado cualquiera.
2. Encadenarlas **anidando** los callbacks: llamar a `fetchUser`, dentro de su callback llamar a `fetchOrders` con el `id` del usuario, y dentro de ese callback llamar a `fetchOrderCount` con el primer pedido.
3. Contar cuántos niveles de indentación tiene el resultado final.
4. En un comentario, escribir qué pasaría si cada una de las tres funciones pudiera fallar y hubiera que manejar el error en cada nivel por separado.

## 7. De callback a Promise

1. Reescribir las tres funciones del ejercicio 6 (`fetchUser`, `fetchOrders`, `fetchOrderCount`) para que devuelvan una `Promise` en vez de recibir un callback (usando `new Promise((resolve, reject) => {...})`).
2. Encadenar las tres con `.then()`, en vez de anidar callbacks.
3. Agregar un único `.catch()` al final y comparar: ¿cuántas veces aparece el manejo de errores acá, contra el ejercicio 6?

## 8. `Promise.all`

1. Con las funciones del ejercicio 7 (o inventando tres funciones nuevas que devuelvan Promises con distintos tiempos de demora), usar `Promise.all` para dispararlas todas a la vez.
2. Medir el tiempo total con `console.time`/`console.timeEnd` alrededor de la llamada.
3. Comparar ese tiempo contra encadenarlas con `.then()` una después de la otra (mismo `console.time`). Confirmar que `Promise.all` es más rápido cuando las operaciones no dependen entre sí.

## 9. `async`/`await`

1. Tomar la cadena de `.then()` del ejercicio 7 y reescribirla como una función `async` usando `await` en cada paso.
2. Envolver el cuerpo en un `try`/`catch` y confirmar que un error en cualquiera de las tres funciones simuladas se atrapa correctamente.
3. Forzar un error a propósito (por ejemplo, hacer que `fetchOrders` rechace si el `userId` es par) y confirmar que el `catch` lo atrapa.

## 10. El `try`/`catch` que no atrapa nada

1. Escribir la función `loadUser(id)` del apunte: un `try`/`catch` sincrónico que envuelve un `setTimeout` cuyo callback hace `throw` si `id <= 0`.
2. Ejecutarla con un `id` inválido y confirmar que el `catch` **no** se ejecuta (el error aparece como no capturado en la consola).
3. En un comentario, explicar por qué pasa esto usando el modelo de call stack / task queue / event loop del apunte.
4. Reescribir la misma función usando una Promise (o `async`/`await`) en vez de un `setTimeout` con `throw` directo, y confirmar que ahora sí se puede atrapar el error con `catch`.

## 11. `fetch` real: nationalize.io

1. Escribir una función `async averiguarPais(nombre)` que haga `fetch` a `https://api.nationalize.io/?name=${nombre}`, chequee `res.ok`, y loguee el `country_id` con mayor `probability` (usando `reduce`, como en el apunte).
2. Probarla con al menos tres nombres distintos.
3. Envolver el cuerpo en `try`/`catch` y forzar un error escribiendo mal la URL (por ejemplo, `nazme=` en vez de `name=`). Confirmar que el `catch` lo atrapa y no rompe el programa.

## 12. Encadenar dos `fetch` reales

1. A partir de `averiguarPais` del ejercicio anterior, agregar un segundo `fetch` a `https://restcountries.com/v3.1/alpha/${paisId}` usando el `country_id` obtenido en el primer paso.
2. Mostrar el nombre del país en español (`translations.spa.common`) usando el resultado del segundo `fetch`.
3. Todo dentro de un único `try`/`catch`, chequeando `res.ok` en **ambas** llamadas.

## 13. Microtasks vs. macrotasks

1. Escribir el ejemplo del apunte: un `console.log` sync, un `setTimeout(fn, 0)`, un `Promise.resolve().then(fn)`, y otro `console.log` sync — en ese orden en el código.
2. Antes de ejecutar, predecir el orden completo de salida en un comentario.
3. Ejecutar y confirmar.
4. Agregar un segundo `Promise.resolve().then(fn)` extra, entre los dos que ya había. ¿En qué posición del orden de salida aparece?

## Para pensar

- ¿Por qué `fetch` no rechaza automáticamente cuando el servidor responde con un código de error HTTP (404, 500)? ¿Qué problema traería que sí lo hiciera, para casos donde justamente se quiere leer el cuerpo de una respuesta de error?
- Un componente de interfaz necesita mostrar un spinner de carga mientras espera datos, y ocultarlo tanto si la carga fue exitosa como si falló. ¿Qué método de Promise (o construcción equivalente con `async`/`await`) es el más adecuado para ocultar el spinner, sin duplicar esa línea en el `then` y en el `catch`?
- `Promise.all` rechaza apenas la primera promise del array rechaza, sin esperar a las demás. Investigá qué método alternativo de `Promise` existe para esperar a que **todas** terminen (con éxito o error) y devolver el resultado de cada una por separado — ¿en qué situación real convendría usar ese en vez de `Promise.all`?
- Con lo que se vio en microtasks vs. macrotasks: si un mismo programa combina varios `setTimeout` con distintos delays y varias Promises encadenadas, ¿alcanza con mirar los valores de los delays para predecir el orden final de ejecución? Justificá con un ejemplo propio.
