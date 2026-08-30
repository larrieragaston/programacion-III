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

# JavaScript es de un solo hilo

- Un **hilo (thread)** ejecuta instrucciones de a una, en orden. JS tiene **un solo hilo principal** para correr código.
- No hay dos líneas de tu programa corriendo literalmente al mismo tiempo — a diferencia de Java, que ya vieron con threads explícitos.
- Consecuencia directa: si una operación bloquea el hilo, **todo** se congela — no se puede clickear un botón, no se puede scrollear, no corre ningún otro código.

<div class="mt-6 text-sm italic opacity-80">

Entonces, ¿qué pasa cuando una línea de código *tarda* — un pedido de red, leer un archivo, esperar un timer? Si hay un solo hilo y hay que quedarse parado esperando ahí mismo, el programa entero queda congelado hasta que esa línea termine. ¿Tiene que ser necesariamente así?

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
layout: default
---

# Otro ejemplo: cargar una página con varias APIs

<div class="text-xs mb-2 opacity-70">Bloqueante — una espera atrás de la otra</div>
<div class="flex items-center gap-1">
<div class="h-9 bg-blue-300 rounded flex items-center justify-center text-xs px-1" style="width: 40%">Noticias — 2s</div>
<div class="h-9 bg-yellow-300 rounded flex items-center justify-center text-xs px-1" style="width: 20%">Clima — 1s</div>
<div class="h-9 bg-pink-300 rounded flex items-center justify-center text-xs px-1" style="width: 30%">Publicidad — 1.5s</div>
</div>
<div class="text-xs mt-1 opacity-70">Total: 2 + 1 + 1.5 = <b>4.5 segundos</b> hasta que la página responde a lo que sea.</div>

```js
function pedirNoticias()    { blockFor(2000); return 'Noticias del día' }
function pedirClima()       { blockFor(1000); return '22°C, soleado' }
function pedirPublicidad()  { blockFor(1500); return 'Anuncio: ...' }

console.log(pedirNoticias())     // recién a los 2s
console.log(pedirClima())        // recién a los 3s
console.log(pedirPublicidad())   // recién a los 4.5s
```

<div class="mt-2 text-sm opacity-80">

Una página real pide noticias, clima y publicidad a servicios distintos e independientes entre sí. Si cada pedido bloqueara el hilo hasta tener respuesta, el tiempo total sería la **suma** de los tres — y ni un solo click funcionaría mientras tanto.

</div>

---
layout: default
---

# La misma página, sin bloquear el hilo

<div class="text-xs mb-2 opacity-70">No bloqueante — las tres arrancan casi al mismo tiempo</div>
<div class="space-y-1.5">
<div class="h-6 bg-blue-300 rounded flex items-center text-xs pl-2" style="width: 55%">Noticias — llega a los 2s</div>
<div class="h-6 bg-yellow-300 rounded flex items-center text-xs pl-2" style="width: 28%">Clima — llega al 1s</div>
<div class="h-6 bg-pink-300 rounded flex items-center text-xs pl-2" style="width: 40%">Publicidad — llega a los 1.5s</div>
</div>
<div class="text-xs mt-1 opacity-70">Total: la página está lista en <b>~2 segundos</b> (la más lenta), no en 4.5.</div>

```js
function pedirNoticias()    { setTimeout(() => console.log('Noticias del día'), 2000) }
function pedirClima()       { setTimeout(() => console.log('22°C, soleado'), 1000) }
function pedirPublicidad()  { setTimeout(() => console.log('Anuncio: ...'), 1500) }

pedirNoticias()
pedirClima()
pedirPublicidad()
console.log('La página ya es usable — nada bloqueó el hilo')
```

<v-click>

<div class="mt-2 text-sm italic opacity-80">

Esto es exactamente lo que va a formalizar `Promise.all` más adelante en este deck: varias operaciones asincrónicas corriendo "al mismo tiempo" en vez de una atrás de la otra, y el hilo principal libre para lo demás durante toda la espera.

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

# El Event Loop: todo junto

<div class="flex justify-center items-stretch gap-3 mt-6 text-xs">
<div class="p-3 rounded-lg border-2 border-blue-400 bg-blue-50 text-center w-36 flex flex-col justify-center">
<div class="font-bold mb-1">1. Call Stack</div>
<div class="opacity-70">código sincrónico</div>
</div>

<v-click>
<div class="flex items-center text-lg opacity-60">→</div>
</v-click>

<div class="p-3 rounded-lg border-2 border-yellow-400 bg-yellow-50 text-center w-36 flex flex-col justify-center">
<div class="font-bold mb-1">2. Web APIs / libuv</div>
<div class="opacity-70">timer, red, disco — corren aparte</div>
</div>

<v-click>
<div class="flex items-center text-lg opacity-60">→</div>
</v-click>

<div class="p-3 rounded-lg border-2 border-green-400 bg-green-50 text-center w-36 flex flex-col justify-center">
<div class="font-bold mb-1">3. Task Queue</div>
<div class="opacity-70">callbacks listos, en orden de llegada</div>
</div>
</div>

<v-click>

<div class="mt-4 p-3 rounded-lg border-2 border-purple-400 bg-purple-50 text-xs text-center mx-auto" style="max-width: 34rem">

↩ <b>4. Event Loop</b>: mientras el programa vive, chequea todo el tiempo "¿está vacío el call stack?" — en cuanto lo está, saca el primero de la task queue y lo apila. Así el ciclo vuelve a empezar.

</div>

</v-click>

<v-click>

<div class="mt-4 text-sm italic opacity-80 text-center">

Cuatro piezas que ya vimos por separado — esta es la foto de cómo interactúan entre sí, y en qué orden, mientras el programa corre.

</div>

</v-click>

---
layout: default
---

# Trazando la ejecución, paso a paso

```js
console.log('A')
setTimeout(() => console.log('B'), 0)
console.log('C')
setTimeout(() => console.log('D'), 0)
console.log('E')
```

<div class="mt-4 text-xs">

<v-click>

<div class="mb-1.5">1. Se apila y corre `console.log('A')` → imprime **A** → se desapila.</div>

</v-click>

<v-click>

<div class="mb-1.5">2. Se encuentra el primer `setTimeout(..., 0)` → se delega a la Web API, que arranca un timer de 0ms.</div>

</v-click>

<v-click>

<div class="mb-1.5">3. Se apila y corre `console.log('C')` → imprime **C** → se desapila. (El timer de 0ms ya terminó, pero su callback tiene que esperar en la task queue: el call stack todavía no está vacío.)</div>

</v-click>

<v-click>

<div class="mb-1.5">4. Se encuentra el segundo `setTimeout(..., 0)` → también se delega; su callback queda encolado detrás del anterior.</div>

</v-click>

<v-click>

<div class="mb-1.5">5. Se apila y corre `console.log('E')` → imprime **E** → se desapila. Ya no queda código sincrónico: el call stack está vacío.</div>

</v-click>

<v-click>

<div class="mb-1.5">6. El event loop lo detecta, saca el **primer** callback de la cola (el de "B" — llegó primero) y lo apila → imprime **B**.</div>

</v-click>

<v-click>

<div class="mb-1.5">7. Call stack vacío otra vez → el event loop saca el siguiente (el de "D") y lo apila → imprime **D**.</div>

</v-click>

</div>

<v-click>

<div class="mt-4 text-sm font-mono text-center opacity-90">

Salida real: A, C, E, B, D

</div>

</v-click>

<v-click>

<div class="mt-2 text-sm italic opacity-80 text-center">

Ni siquiera un `setTimeout(fn, 0)` corre "inmediatamente": siempre espera a que termine **todo** el código sincrónico, y respeta el orden de llegada a la cola.

</div>

</v-click>

---
layout: center
---

# Callbacks

---
layout: default
---

# Qué es un callback

<div class="text-sm">

Un **callback** es una función que se pasa como argumento a otra función — ya usamos esto en JS Funcional (`map`, `filter`, `reduce`), donde el callback corre **sincrónicamente**, en el momento mismo de la llamada. En asincronismo hablamos de otra cosa: un callback que se invoca **más adelante**, cuando termina una operación que tarda.

</div>

```js
// callback síncrono (ya conocido): corre YA, durante la llamada
[1, 2, 3].map((n) => n * 2)

// callback asíncrono: corre DESPUÉS, cuando el timer termina
function fetchUserName(id, callback) {
  setTimeout(() => {
    callback(id === 1 ? 'Ada' : 'invitado')
  }, 1000)
}

fetchUserName(1, (name) => console.log(`Hola, ${name}!`))
console.log('Esto se imprime primero')
```

<div class="mt-3 text-xs opacity-80">

"Callback" no es una feature de una versión puntual de ECMAScript — existe desde que JS tiene funciones de primera clase, desde su primera versión (1997). Antes de que existieran las Promises (recién en **ES2015**), pasarle un callback era la **única** forma de decirle a una función "avisame cuando termines". Sigue vigente hoy: buena parte de Node.js (`fs`, por ejemplo) y librerías como Express (`(req, res, next) => {...}`) todavía lo usan.

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

¿Por qué anidar? Cada paso necesita un dato que **solo existe adentro del callback anterior** — `fetchOrders` necesita `user.id`, y `user` no existe todavía cuando se llama a `fetchUser`; recién llega como argumento del callback, milisegundos (o segundos) después. Un callback no puede "devolver" su resultado hacia afuera porque la función que lo programó ya terminó de ejecutarse — la única forma de usar ese dato es metiendo el siguiente paso **adentro** de ese mismo callback. Repetir esto varias veces produce la pirámide: **callback hell** (o *pyramid of doom*).

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

Una **Promise** es un objeto que representa el resultado (todavía desconocido) de una operación asincrónica. Se introdujo en **ES2015 (ES6)** — justamente para resolver el problema de la slide anterior: una forma estándar de encadenar pasos asincrónicos sin anidar callbacks ni repetir el manejo de errores en cada paso.

<div class="flex flex-col items-center mt-6 text-sm">
<div class="p-3 rounded-lg bg-gray-100 border border-gray-300 text-center w-44">
<div class="font-bold">pending</div>
<div class="opacity-70 text-xs">estado inicial</div>
</div>
<div class="flex gap-28 mt-1 text-xs opacity-70">
<div>↙ resolve()</div>
<div>reject() ↘</div>
</div>
<div class="flex gap-6 mt-1">
<div class="p-3 rounded-lg bg-green-50 border border-green-300 text-center w-44">
<div class="font-bold">fulfilled</div>
<div class="opacity-70 text-xs">éxito — tiene un valor</div>
</div>
<div class="p-3 rounded-lg bg-red-50 border border-red-300 text-center w-44">
<div class="font-bold">rejected</div>
<div class="opacity-70 text-xs">error — tiene un motivo</div>
</div>
</div>
</div>

<div class="mt-4 text-sm italic opacity-80">

Una vez que una Promise pasa de `pending` a `fulfilled` o `rejected` según cuál de los dos callbacks se invoque, queda **fija** para siempre en ese estado — no puede "cambiar de opinión" después.

</div>

---
layout: default
---

# Crear una Promise

```js
function fetchUserName(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) resolve(id === 1 ? 'Ada' : 'invitado')
      else reject(new Error('id inválido'))
    }, 1000)
  })
}
```

<div class="mt-2 text-xs opacity-80">

`new Promise` recibe una función *executor* con dos parámetros: `resolve` y `reject`. En la práctica casi no se crean Promises "a mano" así — la mayoría de las veces las devuelve directamente una función de librería (`fetch`, drivers de bases de datos) — pero entender el mecanismo de abajo ayuda a entender todo lo que sigue.

</div>

<div class="grid grid-cols-2 gap-3 mt-2 text-xs">
<div class="p-3 rounded-lg bg-green-50 border border-green-300">

**`resolve(...)`** → estado `fulfilled`, `value` = ese argumento. Pasa si `id > 0`, después de 1 segundo.

</div>
<div class="p-3 rounded-lg bg-red-50 border border-red-300">

**`reject(new Error(...))`** → estado `rejected`, `reason` = ese `Error`. Pasa si `id <= 0`.

</div>
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

Cada `.then` devuelve una **nueva Promise** — por eso se puede seguir encadenando. Si cualquier eslabón de la cadena rechaza, la ejecución **salta directo** al `.catch` más cercano, sin pasar por los `.then` intermedios: un único lugar para manejar errores, a diferencia del callback hell de unas slides atrás.

</div>

<v-click>

<div class="mt-2 text-sm italic opacity-80">

Pero esta cadena tiene sus propios límites: sigue sin leerse como código realmente secuencial (hay que seguir el rastro de `.then` en `.then`), y si un paso necesitara un valor de **dos** pasos atrás — no solo el inmediato anterior — hay que arrastrarlo a mano entre callbacks. Es el problema que resuelve `async`/`await`, más adelante en este deck.

</div>

</v-click>

---
layout: default
---

# Errores puntuales en la cadena

```js
fetchUser(1)
  .then((user) => fetchOrders(user.id))
  .catch((error) => {
    console.error('No se pudieron cargar las órdenes:', error.message)
    return []   // la cadena se "recupera" y sigue con este valor
  })
  .then((orders) => fetchShipping(orders[0]?.id))
  .catch((error) => console.error('Tampoco se pudo obtener el envío:', error.message))
```

<div class="mt-4 text-sm opacity-80">

Un `.catch()` intermedio no corta la cadena: atrapa el error de los pasos anteriores y, si no vuelve a lanzar (`throw`) ni devuelve una promise rechazada, la cadena sigue con el valor que ese `.catch` devuelva — acá, un array vacío en vez de romper todo. Así se pueden manejar distintos errores en distintos puntos de la cadena, en vez de un único `.catch` final para todo.

</div>

<v-click>

<div class="mt-2 text-sm opacity-80">

El costo: cuantos más puntos de manejo de errores hay, más difícil es seguir el flujo de la cadena a simple vista — otra razón, además de la anterior, por la que conviene conocer `async`/`await`.

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

Distinto de encadenar con `.then`: acá las tres llamadas arrancan **al mismo tiempo**, no una después de la otra — el mismo principio que vimos con el ejemplo de la página cargando noticias, clima y publicidad en paralelo.

</div>

</v-click>

<v-click>

<div class="mt-2 text-xs opacity-70">

Mención rápida: <code>Promise.race</code> se resuelve o rechaza con la **primera** promise del array que termine (para lo que sea, éxito o error) — útil, por ejemplo, para implementar un timeout.

</div>

</v-click>

---
layout: default
---

# Otro método útil: `Promise.allSettled`

```js
Promise.allSettled([
  fetchUser(1),
  fetchUser(-1),   // este va a rechazar
  fetchUser(3),
]).then((results) => {
  results.forEach((r) =>
    r.status === 'fulfilled'
      ? console.log('OK:', r.value)
      : console.log('Falló:', r.reason.message)
  )
})
```

<div class="mt-4 text-sm opacity-80">

Introducido en **ES2020**. A diferencia de `Promise.all`, nunca rechaza — espera a que **todas** las promises terminen, sea como sea, y devuelve un array con el resultado de cada una: `{ status: 'fulfilled', value }` o `{ status: 'rejected', reason }`. Útil cuando querés el resultado de cada operación aunque alguna falle, en vez de descartar todo por un solo error.

</div>

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

<div class="mt-2 text-xs opacity-80">

Introducido en **ES2017 (ES8)**, después que las Promises (ES2015), para resolver lo que veíamos antes: cadenas de `.then` que crecen y dejan de leerse como una secuencia simple.

</div>

<v-click>

<div class="mt-1.5 text-xs opacity-80">

No **reemplaza** a las Promises: por debajo es el mismo motor, `async`/`await` es solo sintaxis. Reglas básicas: `await` solo se usa dentro de una función `async` (salvo *top-level await*, ES2022), y una función `async` **siempre devuelve una Promise**, aunque el `return` de adentro sea un valor normal.

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
    return await fetchOrders(user.id)
  } catch (error) {
    if (error.status === 404) console.error('Usuario no encontrado')
    else console.error('Error inesperado:', error.message)
    return []
  }
}
```

<div class="mt-4 text-sm opacity-80">

Con `async`/`await`, el manejo de errores vuelve a ser el `try`/`catch` de siempre: si cualquier `await` de adentro rechaza, la ejecución salta directo al `catch` — mismo comportamiento que `.catch()` en una cadena de Promises, pero con la sintaxis sincrónica que ya conocían de Java/C. Para diferenciar tipos de error alcanza con inspeccionar el objeto `error` adentro del mismo `catch` (por `instanceof`, por un código de estado, etc.), como con `error.status === 404` de arriba.

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

<div class="mt-1.5 text-xs opacity-80">

Dos `fetch` en secuencia (el segundo necesita el resultado del primero) — con `async`/`await` se lee igual de lineal que si fuera sincrónico. Comparar con este mismo flujo anidado con callbacks puros.

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

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
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
| Paralelo (all) | `Promise.all([p1, p2])` |
| Paralelo (allSettled) | `Promise.allSettled([p1, p2])` |
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
- [developer.mozilla.org — Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises) — referencia completa de Promises
- [javascript.info — Async](https://javascript.info/async) — callbacks, promises y async/await en profundidad
- [javascript.info — Event loop: microtasks and macrotasks](https://javascript.info/event-loop) — la distinción entre colas, explicada con ejemplos
- ["What the heck is the event loop anyway?"](https://www.youtube.com/watch?v=8aGhZQkoFbQ) — Philip Roberts, JSConf — la charla clásica sobre el event loop
- ["In The Loop"](https://www.youtube.com/watch?v=cCOL7MC4Pl0) — Jake Archibald, JSConf.Asia — profundiza en microtasks/macrotasks y rendering, buen siguiente paso
- [nationalize.io](https://nationalize.io/) y [restcountries.com](https://restcountries.com/) — las APIs públicas usadas en los ejemplos de este deck

</div>
