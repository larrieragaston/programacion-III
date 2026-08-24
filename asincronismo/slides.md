---
theme: bricks
title: Programación III - Asincronismo
download: true
info: |
  Asincronismo en JavaScript - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: asincronismo, event loop, callbacks, promises, async await, INSPT, UTN
transition: slide-left
mdc: true
---

# Asincronismo

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/javascript.svg" alt="JavaScript" class="h-16 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# De dónde venimos

- En **JS Funcional** vimos funciones puras, HOFs, composición.
- En **JS Contemporáneo** vimos la sintaxis moderna — incluida una fecha que dejamos pendiente: **ES2017 trajo `async`/`await`**.
- Todo lo que vimos hasta acá corre **de una sola vez, en orden, de arriba hacia abajo**. Este deck rompe esa suposición.

<div class="mt-6 text-sm italic opacity-80">

La pregunta de hoy: ¿qué pasa cuando una línea de código tarda — un pedido de red, leer un archivo, esperar un timer — y no querés que el resto del programa se congele mientras tanto?

</div>

---
layout: default
---

# JavaScript es de un solo hilo

- Un **hilo (thread)** ejecuta instrucciones de a una, en orden. JS tiene **un solo hilo principal**.
- No hay dos líneas de código de tu programa corriendo literalmente al mismo tiempo — a diferencia de Java, que ya vieron con threads explícitos.
- Consecuencia directa: si una operación bloquea el hilo, **todo** se congela — no se puede clickear un botón, no se puede scrollear, no corre ningún otro código.

<div class="mt-6 text-sm italic opacity-80">

Entonces, ¿cómo hace un navegador para bajar una imagen, esperar la respuesta de un servidor y seguir siendo usable mientras tanto? Ahí es donde entra la asincronía.

</div>

---
layout: default
---

# Operaciones que tardan

<div class="grid grid-cols-3 gap-4 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100 text-center">

**Red**

Pedidos HTTP (`fetch`), WebSockets — el tiempo lo decide la latencia de la red y el servidor, no tu código.
</div>
<div class="p-4 rounded-lg bg-gray-100 text-center">

**Disco / archivos**

Leer o escribir un archivo (Node), acceder a `localStorage` o una base de datos.
</div>
<div class="p-4 rounded-lg bg-gray-100 text-center">

**Timers**

`setTimeout`, `setInterval` — esperar un tiempo determinado a propósito.
</div>
</div>

<div class="mt-8 text-sm opacity-80">

Ninguna de estas operaciones depende de la CPU — dependen de algo externo (la red, el disco, el reloj). Bloquear el único hilo de JS mientras se espera sería desperdiciar la CPU por completo.

</div>

---
layout: default
---

# Bloquear el hilo: por qué es inaceptable

```js
function blockFor(ms) {
  const end = Date.now() + ms
  while (Date.now() < end) {
    // ocupa la CPU haciendo nada, a propósito
  }
}

console.log('Antes del bloqueo')
blockFor(5000)   // el hilo queda "trabado" acá 5 segundos completos
console.log('Después del bloqueo')
```

<v-click>

<div class="mt-4 text-sm opacity-80">

Durante esos 5 segundos, la página **no responde a nada**: ni clicks, ni scroll, ni animaciones, ni ningún otro código. Este ejemplo simula, a propósito, el problema que la asincronía existe para resolver.

</div>

</v-click>

---
layout: center
---

# El Event Loop

---
layout: default
---

# El Call Stack

```js
function multiply(a, b) { return a * b }
function square(n) { return multiply(n, n) }
function printSquare(n) { console.log(square(n)) }

printSquare(4)
```

<div class="mt-4 text-sm opacity-80">

El **call stack** (pila de llamadas) es donde JS registra qué función se está ejecutando ahora. Cada llamada se **apila** arriba de la anterior; cuando una función termina, se **desapila**. Es puramente sincrónico: una función tiene que terminar (o quedar en pausa) antes de que la de abajo siga.

</div>

<v-click>

<div class="mt-2 text-xs font-mono opacity-70 text-center">

`printSquare(4)` → `square(4)` → `multiply(4, 4)` → se desapila `multiply` → se desapila `square` → se desapila `printSquare`

</div>

</v-click>

---
layout: default
---

# El problema con `setTimeout`

```js
console.log('1')
setTimeout(() => console.log('2'), 1000)
console.log('3')

// => 1
// => 3
// => 2   (recién después de ~1 segundo)
```

<div class="mt-4 text-sm opacity-80">

Si el call stack fuera lo único que existe, `setTimeout` tendría que **bloquear** un segundo entero antes de seguir con `console.log('3')` — pero no es lo que pasa. JS le delega la espera a otra cosa y sigue de largo. ¿A quién se la delega?

</div>

---
layout: default
---

# Web APIs (o libuv, en Node)

- `setTimeout`, `fetch`, eventos del DOM, lectura de archivos — **no los ejecuta el motor de JS**. Los ejecuta el entorno que lo rodea.
- En el **navegador**, ese entorno son las **Web APIs** (parte del navegador, no del lenguaje).
- En **Node.js**, ese entorno es **libuv**, una librería en C que maneja I/O de forma no bloqueante.
- El motor de JS le dice "avisame cuando esto termine" y sigue ejecutando el resto del call stack **sin esperar**.

<div class="mt-6 text-sm italic opacity-80">

Esta es la pieza clave: JS en sí mismo es de un solo hilo, pero el entorno que lo rodea sí puede hacer varias cosas en paralelo (temporizadores, conexiones de red) — y le devuelve el resultado a JS cuando está listo.

</div>

---
layout: default
---

# La Task Queue (cola de tareas)

- Cuando una Web API/libuv termina su trabajo (el timer llegó a cero, la respuesta de red llegó), **no** ejecuta el callback inmediatamente.
- Lo pone en una **cola** — la task queue (también llamada *callback queue* o *macrotask queue*) — a esperar su turno.
- El callback de la cola **solo se ejecuta cuando el call stack está completamente vacío**.

<div class="mt-6 text-sm italic opacity-80">

Esta regla — "esperá a que el stack esté vacío" — es la razón por la que <code>setTimeout(fn, 0)</code> no ejecuta <code>fn</code> inmediatamente: igual tiene que esperar su turno en la cola, después de todo el código sincrónico pendiente.

</div>

---
layout: default
---

# El Event Loop, paso a paso

<div class="flex justify-center gap-4 mt-4 text-xs">
<div class="p-3 rounded-lg border-2 border-blue-400 bg-blue-50 text-center w-40">
<div class="font-bold mb-1">Call Stack</div>
<div class="opacity-70">funciones en ejecución, sincrónico</div>
</div>
<div class="p-3 rounded-lg border-2 border-yellow-400 bg-yellow-50 text-center w-40">
<div class="font-bold mb-1">Web APIs / libuv</div>
<div class="opacity-70">timers, red, disco — trabajan aparte</div>
</div>
<div class="p-3 rounded-lg border-2 border-green-400 bg-green-50 text-center w-40">
<div class="font-bold mb-1">Task Queue</div>
<div class="opacity-70">callbacks listos, esperando turno</div>
</div>
</div>

<div class="mt-6 text-center text-sm">

<v-click>

**1.** El call stack ejecuta código sincrónico. Encuentra `setTimeout(cb, 1000)` y se lo delega a la Web API correspondiente.

</v-click>
<v-click>

**2.** El call stack sigue con el resto del código sincrónico — no espera. Mientras tanto, la Web API cuenta el segundo por su cuenta.

</v-click>
<v-click>

**3.** Cuando el timer termina, la Web API pone `cb` en la task queue. Todavía no se ejecuta.

</v-click>
<v-click>

**4.** El **event loop** — el mecanismo que da nombre a todo esto — chequea todo el tiempo: "¿está vacío el call stack?". En cuanto lo está, saca `cb` de la task queue y lo apila.

</v-click>

</div>

<div class="mt-4 text-sm italic opacity-80 text-center">

<v-click>

El event loop es, literalmente, ese chequeo repetido — "¿stack vacío? pasá el próximo de la cola" — corriendo todo el tiempo mientras el programa vive.

</v-click>

</div>

---
layout: center
---

# Callbacks

---
layout: default
---

# Qué es un callback

Un **callback** es, simplemente, una función que se pasa como argumento para que otra la ejecute más adelante — ya usamos esto en `map`/`filter`/`setTimeout`, pero ahora el eje es el **orden en el tiempo**, no la transformación de datos.

```js
function fetchUserName(id, callback) {
  setTimeout(() => {
    const name = id === 1 ? 'Ada' : 'invitado'
    callback(name)
  }, 1000)
}

fetchUserName(1, (name) => {
  console.log(`Hola, ${name}!`)
})

console.log('Esto se imprime primero')
```

<div class="mt-4 text-sm opacity-80">

`fetchUserName` simula una operación que tarda (acá, un timer) y avisa cuando termina llamando al `callback` con el resultado — el mismo patrón que usan `fetch`, lectura de archivos, y casi toda API asincrónica clásica.

</div>

---
layout: default
---

# Callback hell

```js
fetchUser(1, (user) => {
  fetchOrders(user.id, (orders) => {
    fetchOrderDetails(orders[0].id, (details) => {
      fetchShipping(details.id, (shipping) => {
        console.log(shipping)
        // y si cada paso necesita, además, manejar su propio error...
      }, handleError)
    }, handleError)
  }, handleError)
}, handleError)
```

<v-click>

<div class="mt-4 text-sm opacity-80">

Cada paso depende del resultado del anterior, así que cada callback queda **anidado dentro** del anterior — el código crece hacia la derecha en vez de hacia abajo. Este patrón tiene nombre propio: **callback hell** (o *pyramid of doom*).

</div>

</v-click>

---
layout: default
---

# Por qué el callback hell es un problema

- **Legibilidad**: el orden real de ejecución no coincide con la indentación — cuesta seguir el flujo con la vista.
- **Manejo de errores**: no hay un único lugar para atrapar errores — cada callback necesita su propio manejo (`handleError` repetido en el ejemplo anterior), y es fácil olvidarse de alguno.
- **Componer operaciones es difícil**: ¿cómo se ejecutan dos de estas llamadas **en paralelo** en vez de en secuencia? Con callbacks puros, hay que orquestarlo a mano contando cuántas terminaron.

<div class="mt-6 text-sm italic opacity-80">

Los callbacks no están "mal" — siguen siendo la base de todo (hasta las Promises los usan por debajo). El problema es específicamente **anidarlos** para expresar una secuencia. Ahí es donde entran las Promises.

</div>

---
layout: center
---

# Promises

---
layout: default
---

# Qué es una Promise

Una **Promise** es un objeto que representa el resultado (todavía desconocido) de una operación asincrónica. Tiene siempre uno de tres **estados**:

<div class="grid grid-cols-3 gap-4 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100 text-center">

**pending**

Estado inicial — la operación todavía no terminó.
</div>
<div class="p-4 rounded-lg bg-green-50 border border-green-300 text-center">

**fulfilled**

Terminó con éxito — tiene un valor resultado.
</div>
<div class="p-4 rounded-lg bg-red-50 border border-red-300 text-center">

**rejected**

Terminó con error — tiene un motivo (`reason`) de rechazo.
</div>
</div>

<div class="mt-6 text-sm italic opacity-80">

Una vez que una Promise pasa de <code>pending</code> a <code>fulfilled</code> o <code>rejected</code>, queda **fija** para siempre en ese estado — no puede "cambiar de opinión" después.

</div>

---
layout: default
---

# Crear una Promise

```js
function fetchUserName(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id <= 0) {
        reject(new Error('id inválido'))
        return
      }
      resolve(id === 1 ? 'Ada' : 'invitado')
    }, 1000)
  })
}
```

<div class="mt-4 text-sm opacity-80">

`new Promise` recibe una función *executor* con dos parámetros: `resolve` (llamarla marca la promise como `fulfilled`, con ese valor) y `reject` (la marca como `rejected`, con ese motivo). En la práctica, casi no se crean Promises "a mano" así — la mayoría de las veces las devuelve directamente una función de una librería (`fetch`, drivers de bases de datos, etc.) — pero entender el mecanismo de abajo ayuda a entender todo lo que sigue.

</div>

---
layout: default
---

# Consumir una Promise: `.then` / `.catch` / `.finally`

```js
fetchUserName(1)
  .then((name) => console.log(`Hola, ${name}!`))
  .catch((error) => console.error('Falló:', error.message))
  .finally(() => console.log('Terminado (haya salido bien o mal)'))
```

- **`.then(onFulfilled)`**: se ejecuta si la promise se resuelve — recibe el valor.
- **`.catch(onRejected)`**: se ejecuta si se rechaza — recibe el motivo. Equivale a `.then(undefined, onRejected)`.
- **`.finally(onSettled)`**: se ejecuta siempre, haya salido bien o mal — no recibe ningún valor. Ideal para limpieza (por ejemplo, ocultar un spinner de carga).

---
layout: default
---

# Encadenar Promises

```js
fetchUser(1)
  .then((user) => fetchOrders(user.id))
  .then((orders) => fetchOrderDetails(orders[0].id))
  .then((details) => fetchShipping(details.id))
  .then((shipping) => console.log(shipping))
  .catch((error) => console.error('Algo falló en la cadena:', error.message))
```

<div class="mt-4 text-sm opacity-80">

Cada `.then` devuelve una **nueva Promise** — por eso se puede seguir encadenando. Si cualquier eslabón de la cadena rechaza, la ejecución **salta directo** al `.catch` más cercano, sin pasar por los `.then` intermedios: un único lugar para manejar errores, a diferencia del callback hell de la slide anterior.

</div>

<v-click>

<div class="mt-2 text-sm italic opacity-80">

Comparar esta cadena con la pirámide de callbacks de unas slides atrás: mismo problema, resuelto sin anidar — la secuencia queda **plana**, de arriba hacia abajo.

</div>

</v-click>

---
layout: default
---

# Ejecutar en paralelo: `Promise.all`

```js
Promise.all([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3),
])
  .then((users) => console.log('Los tres llegaron:', users))
  .catch((error) => console.error('Al menos uno falló:', error.message))
```

<div class="mt-4 text-sm opacity-80">

`Promise.all` recibe un array de Promises y devuelve **una sola** Promise que se resuelve cuando **todas** terminaron, con un array de resultados en el mismo orden. Si **cualquiera** rechaza, `Promise.all` rechaza inmediatamente con ese motivo — aunque las demás sigan corriendo.

</div>

<v-click>

<div class="mt-4 text-sm opacity-80">

Distinto de encadenar con `.then`: acá las tres llamadas arrancan **al mismo tiempo**, no una después de la otra — si cada una tarda 1 segundo, el total es ~1 segundo, no ~3.

</div>

</v-click>

<v-click>

<div class="mt-2 text-xs opacity-70">

Mención rápida: <code>Promise.race</code> se resuelve o rechaza con la **primera** promise del array que termine (para lo que sea, éxito o error) — útil, por ejemplo, para implementar un timeout.

</div>

</v-click>

---
layout: center
---

# `async` / `await`

---
layout: default
---

# `async`/`await`: azúcar sobre Promises

```js
// con .then
function loadUser(id) {
  return fetchUser(id)
    .then((user) => fetchOrders(user.id))
    .then((orders) => orders.length)
}

// con async/await
async function loadUser(id) {
  const user = await fetchUser(id)
  const orders = await fetchOrders(user.id)
  return orders.length
}
```

<div class="mt-4 text-sm opacity-80">

`async`/`await` **no es un mecanismo nuevo** — es sintaxis que se traduce, por debajo, a Promises encadenadas. La diferencia es de legibilidad: el código async/await se lee de arriba hacia abajo, como si fuera sincrónico, aunque no lo sea.

</div>

<v-click>

<div class="mt-2 text-sm opacity-80">

Reglas básicas: `await` solo se puede usar dentro de una función marcada `async` (con alguna excepción moderna de *top-level await*, ES2022). Una función `async` **siempre devuelve una Promise** — aunque el `return` de adentro sea un valor normal, queda envuelto automáticamente.

</div>

</v-click>

---
layout: default
---

# El mismo ejemplo, tres formas

<div class="grid grid-cols-3 gap-3 mt-4 text-xs">
<div class="p-3 rounded-lg bg-gray-100">

**Callback**

```js
fetchUser(1, (user) => {
  fetchOrders(
    user.id,
    (orders) => {
      console.log(orders)
    }
  )
})
```
</div>
<div class="p-3 rounded-lg bg-gray-100">

**Promise**

```js
fetchUser(1)
  .then((user) =>
    fetchOrders(user.id)
  )
  .then((orders) =>
    console.log(orders)
  )
```
</div>
<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-300">

**async/await**

```js
const user =
  await fetchUser(1)
const orders =
  await fetchOrders(user.id)
console.log(orders)
```
</div>
</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

Las tres versiones resuelven exactamente lo mismo. Ninguna "reemplaza" del todo a las anteriores: hay que saber leer las tres, porque las tres aparecen en código real (sobre todo callbacks y Promises, en librerías que no se controlan).

</div>

---
layout: default
---

# Manejo de errores con `try`/`catch`

```js
async function loadUserOrders(id) {
  try {
    const user = await fetchUser(id)
    const orders = await fetchOrders(user.id)
    return orders
  } catch (error) {
    console.error('No se pudo cargar:', error.message)
    return []
  }
}
```

<div class="mt-4 text-sm opacity-80">

Con `async`/`await`, el manejo de errores vuelve a ser el `try`/`catch` de siempre: si cualquier `await` de adentro rechaza, la ejecución salta directo al `catch` — mismo comportamiento que `.catch()` en una cadena de Promises, pero con la sintaxis sincrónica que ya conocían de Java/C.

</div>

---
layout: default
---

# Un `try`/`catch` sincrónico no alcanza

```js
function loadUser(id) {
  try {
    setTimeout(() => {
      if (id <= 0) throw new Error('id inválido')
      console.log('Usuario cargado')
    }, 1000)
  } catch (error) {
    console.error('Esto NUNCA se ejecuta:', error.message)
  }
}
```

<v-click>

<div class="mt-4 text-sm opacity-80">

El `throw` de adentro del callback de `setTimeout` ocurre **mucho después** de que el `try`/`catch` que lo rodea ya terminó de ejecutarse (recordar el event loop: el callback corre recién cuando el stack está vacío, en otra "vuelta" completamente distinta). El error termina como una excepción no capturada, no dentro del `catch`.

</div>

</v-click>

<v-click>

<div class="mt-2 text-sm opacity-80">

Con Promises/`async`-`await` esto **no pasa**: el `.catch()` (o el `try`/`catch` de una función `async`) sí está diseñado para atrapar errores que ocurren "más adelante en el tiempo" — es una de las razones de fondo por las que Promises reemplazaron a los callbacks para este tipo de flujo.

</div>

</v-click>

---
layout: default
---

# Ejemplo real: `fetch` + `async`/`await`

```js
async function averiguarPais(nombre) {
  try {
    const res = await fetch(`https://api.nationalize.io/?name=${nombre}`)
    if (!res.ok) throw new Error(res.statusText)

    const data = await res.json()
    const masProbable = data.country.reduce((a, b) =>
      a.probability > b.probability ? a : b
    )
    console.log(`País más probable: ${masProbable.country_id}`)
  } catch (error) {
    console.error(error)
  }
}

averiguarPais('Manolo')   // => "País más probable: ES"
```

<div class="mt-4 text-sm opacity-80">

`fetch` devuelve una Promise que se resuelve **incluso si la respuesta es un error HTTP** (404, 500) — no rechaza sola en esos casos. Por eso hay que chequear `res.ok` a mano y lanzar el error nosotros, si corresponde.

</div>

---
layout: default
---

# Encadenar dos llamadas async reales

```js
async function averiguarPaisCompleto(nombre) {
  try {
    const res = await fetch(`https://api.nationalize.io/?name=${nombre}`)
    if (!res.ok) throw new Error(res.statusText)
    const data = await res.json()

    const paisId = data.country.reduce((a, b) =>
      a.probability > b.probability ? a : b
    ).country_id

    const resPais = await fetch(`https://restcountries.com/v3.1/alpha/${paisId}`)
    if (!resPais.ok) throw new Error(resPais.statusText)
    const [pais] = await resPais.json()

    console.log(`Probablemente seas de ${pais.translations.spa.common}`)
  } catch (error) {
    console.error(error)
  }
}
```

<div class="mt-4 text-sm opacity-80">

Dos `fetch` en secuencia (el segundo necesita el resultado del primero) — con `async`/`await`, el código se lee igual de lineal que si fuera sincrónico. Comparar con cómo se vería este mismo flujo anidado con callbacks puros.

</div>

---
layout: center
---

# Microtasks vs. Macrotasks

---
layout: default
---

# Dos colas, no una

- Lo que llamamos "task queue" en realidad son (al menos) **dos colas** con distinta prioridad:
- **Macrotasks**: `setTimeout`, `setInterval`, eventos de I/O.
- **Microtasks**: callbacks de Promises (`.then`/`.catch`/`.finally`), `queueMicrotask`.
- **Regla del event loop**: después de cada macrotask, se vacía **toda** la cola de microtasks antes de pasar a la siguiente macrotask — incluso si aparecen microtasks nuevas mientras se vacía la cola.

<div class="mt-6 text-sm italic opacity-80">

En otras palabras: las Promises "cortan la fila" por delante de los timers, aunque el timer se haya programado antes.

</div>

---
layout: default
---

# El orden que sorprende

```js
console.log('1: sync')

setTimeout(() => console.log('2: macrotask (setTimeout)'), 0)

Promise.resolve().then(() => console.log('3: microtask (Promise)'))

console.log('4: sync')

// Orden real de salida:
// 1: sync
// 4: sync
// 3: microtask (Promise)
// 2: macrotask (setTimeout)
```

<div class="mt-4 text-sm opacity-80">

Aunque el `setTimeout` se programó con `0` milisegundos — es decir, "ejecutá esto ya" — la Promise se ejecuta primero. El código sincrónico siempre corre completo primero; después se vacía la cola de microtasks completa; recién después se saca **una** macrotask de su cola.

</div>

---
layout: default
---

# Por qué importa

- Es una pregunta clásica de entrevista técnica — vale la pena poder explicar el orden del ejemplo anterior sin dudar.
- Explica bugs reales: código que "debería" ejecutarse en cierto orden y no lo hace, porque se mezclan timers con Promises sin tener en cuenta la prioridad de las colas.
- No hace falta memorizar la implementación exacta del motor — alcanza con el modelo mental: **sync → todas las microtasks → una macrotask → repetir**.

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-4 text-xs">
<div>

**Conceptos**

| Término | Qué es |
|---|---|
| Call stack | Funciones en ejecución, sincrónico |
| Web APIs / libuv | Ejecutan timers, red, disco aparte |
| Task queue | Callbacks listos, esperando su turno |
| Event loop | El chequeo "¿stack vacío? seguí" |
| Microtask | Cola de `.then`/`.catch` — prioridad alta |
| Macrotask | Cola de `setTimeout`/eventos — prioridad baja |

</div>
<div>

**Sintaxis**

| Forma | Ejemplo |
|---|---|
| Callback | `fn(arg, (result) => {...})` |
| Crear Promise | `new Promise((resolve, reject) => {...})` |
| Consumir | `p.then(...).catch(...).finally(...)` |
| Paralelo | `Promise.all([p1, p2, p3])` |
| async/await | `const x = await fn()` |
| Errores async | `try { await fn() } catch (e) {...}` |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2">

- [developer.mozilla.org — Asynchronous JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript/Guide/Asynchronous) — guía oficial en español
- [javascript.info — Async](https://javascript.info/async) — callbacks, promises y async/await en profundidad
- ["What the heck is the event loop anyway?"](https://www.youtube.com/watch?v=8aGhZQkoFbQ) — Philip Roberts, JSConf — la charla de referencia sobre el event loop, muy recomendada
- [nationalize.io](https://nationalize.io/) y [restcountries.com](https://restcountries.com/) — las APIs públicas usadas en los ejemplos de este deck

</div>
