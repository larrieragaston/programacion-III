# Asincronismo

## De dónde venimos

En **JS Funcional** vimos funciones puras, funciones de orden superior y composición. En **JS Contemporáneo** vimos la sintaxis moderna del lenguaje — y quedó una fecha pendiente en la cronología de ECMAScript: **ES2017 introdujo `async`/`await`**. Este apunte cierra ese paréntesis: explica **por qué** hace falta una sintaxis especial para manejar operaciones que tardan, y **cómo** evolucionó esa sintaxis (callbacks → Promises → async/await) hasta llegar a lo que se usa hoy.

Todo el código visto hasta ahora en la materia se ejecuta **de una sola vez, de arriba hacia abajo, sin pausas**. Ese modelo alcanza mientras cada línea termine casi instantáneamente. La pregunta de este tema es qué pasa cuando una línea de código depende de algo externo — una respuesta de red, la lectura de un archivo, un timer — que puede tardar segundos, y **no** se quiere que el resto del programa se congele mientras tanto.

## JavaScript es de un solo hilo

Un **hilo (thread)** de ejecución procesa instrucciones de a una, en orden estricto. A diferencia de Java — donde ya vieron threads explícitos, capaces de correr código en paralelo real — **JavaScript tiene un único hilo principal**. No hay dos líneas del programa corriendo literalmente al mismo tiempo (dejando de lado los *Web Workers*, una herramienta específica para correr JS en un hilo aparte, fuera del alcance de este tema).

La consecuencia directa: si una operación **bloquea** ese único hilo, todo se detiene — no se puede clickear un botón, no se puede hacer scroll, no corre ningún otro código de la página, hasta que esa operación termine.

```js
function blockFor(ms) {
  const end = Date.now() + ms
  while (Date.now() < end) {
    // ocupa la CPU haciendo nada, a propósito — simula trabajo bloqueante
  }
}

console.log('Antes del bloqueo')
blockFor(5000)   // el hilo queda "trabado" acá, 5 segundos completos
console.log('Después del bloqueo')
```

Durante esos 5 segundos la página **no responde a nada**. Este ejemplo simula, a propósito, exactamente el problema que la asincronía existe para resolver.

## Operaciones que tardan

Las aplicaciones web modernas dependen constantemente de operaciones que **no** dependen de la CPU local, sino de algo externo:

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>Red</h4>

Pedidos HTTP (`fetch`), WebSockets. El tiempo lo decide la latencia de la red y el servidor remoto, no el código.
</div>
<div class="info-card">
<h4>Disco / archivos</h4>

Leer o escribir un archivo (típico en Node.js), acceder a `localStorage` o consultar una base de datos.
</div>
<div class="info-card">
<h4>Timers</h4>

`setTimeout`, `setInterval` — esperar un tiempo determinado a propósito, por diseño.
</div>
</div>

Un sitio típico de hoy integra noticias, clima y publicidad, cada una desde una API externa distinta — si esas tres peticiones se resolvieran de forma **síncrona** (una detrás de la otra, bloqueando en cada una), la página tardaría en cargar la suma de los tres tiempos. La asincronía permite lanzar las tres **sin esperar**, y procesar cada respuesta a medida que va llegando — el tiempo total termina siendo, en la práctica, el de la más lenta de las tres, no la suma.

<div class="practice-box">
<p class="practice-label">Para pensar</p>

Pensá en una aplicación que uses seguido (una red social, un mapa, un mail). Enumerá al menos tres operaciones que esa app hace que probablemente sean asincrónicas — ¿qué pasaría con la experiencia de uso si esas operaciones fueran bloqueantes en cambio?
</div>

## El modelo mental: Call Stack, Web APIs, Task Queue, Event Loop

Para entender **cómo** JavaScript logra no bloquearse a pesar de tener un solo hilo, hace falta un modelo mental de cuatro piezas.

### Call Stack

El **call stack** (pila de llamadas) es donde el motor de JS registra qué función se está ejecutando en cada momento. Cada llamada se **apila** arriba de la anterior; cuando una función termina, se **desapila**. Es puramente sincrónico y estrictamente ordenado: una función tiene que terminar antes de que la que está debajo en la pila pueda seguir.

```js
function multiply(a, b) { return a * b }
function square(n) { return multiply(n, n) }
function printSquare(n) { console.log(square(n)) }

printSquare(4)
// pila: printSquare → square → multiply → se desapila multiply
//     → se desapila square → se desapila printSquare
```

Si el call stack fuera lo único que existiera, algo como `setTimeout(fn, 1000)` tendría que **bloquear** un segundo entero antes de que el resto del programa pudiera seguir — pero eso no es lo que pasa en la práctica:

```js
console.log('1')
setTimeout(() => console.log('2'), 1000)
console.log('3')

// => 1
// => 3
// => 2   (recién después de ~1 segundo)
```

`'3'` se imprime **antes** que `'2'`, a pesar de que `setTimeout` se llamó primero. JS delegó la espera a otra pieza y siguió de largo con el resto del call stack.

### Web APIs (o libuv, en Node)

`setTimeout`, `fetch`, los eventos del DOM, la lectura de archivos — **no los ejecuta el motor de JavaScript en sí**. Los ejecuta el entorno que lo rodea:

- En el **navegador**, ese entorno son las **Web APIs**: parte del navegador (implementadas junto al sistema operativo), no del lenguaje JavaScript propiamente dicho.
- En **Node.js**, el entorno equivalente es **libuv**, una librería en C que maneja entrada/salida de forma no bloqueante.

El motor de JS le dice a esa pieza externa "avisame cuando esto termine" y sigue ejecutando el resto del call stack **sin esperar la respuesta**. Por eso, aunque JS mismo sea de un solo hilo, el entorno que lo rodea sí puede tener varias cosas en marcha al mismo tiempo (un timer contando, una conexión de red esperando datos).

### Task Queue (cola de tareas)

Cuando una Web API (o libuv) termina su trabajo — el timer llegó a cero, la respuesta de red llegó — **no ejecuta el callback inmediatamente**. Lo pone en una cola de espera: la **task queue** (también llamada *callback queue*, o *macrotask queue* cuando se distingue de las microtasks, ver más abajo). El callback que quedó en esa cola **solo se ejecuta cuando el call stack está completamente vacío**.

Esta regla explica por qué `setTimeout(fn, 0)` no ejecuta `fn` de inmediato: igual tiene que esperar su turno en la cola, después de todo el código sincrónico que ya estaba pendiente de ejecutar.

### Event Loop

El **event loop** (bucle de eventos, el que le da nombre a todo este mecanismo) es, literalmente, un chequeo que se repite todo el tiempo mientras el programa vive: *"¿está vacío el call stack? Si es así, tomá el próximo callback de la task queue y apilalo."*

<div class="flow-row flow-vertical">
<div class="flow-box tone-brand">Call Stack ejecuta código sync</div>
<div class="flow-arrow"><span class="arrow-glyph">↓</span></div>
<div class="flow-box">Encuentra <code>setTimeout</code> → lo delega a Web APIs</div>
<div class="flow-arrow"><span class="arrow-glyph">↓</span></div>
<div class="flow-box">Call Stack sigue con el resto del código sync (no espera)</div>
<div class="flow-arrow"><span class="arrow-glyph">↓</span></div>
<div class="flow-box">Timer termina → Web APIs pone el callback en la Task Queue</div>
<div class="flow-arrow"><span class="arrow-glyph">↓</span></div>
<div class="flow-box tone-yellow">Event Loop: "¿Call Stack vacío?" → sí → apila el callback</div>
<div class="flow-arrow"><span class="arrow-glyph">↓</span></div>
<div class="flow-box tone-green">El callback se ejecuta</div>
</div>

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí `console.log('A')`, seguido de `setTimeout(() => console.log('B'), 0)`, seguido de `console.log('C')`. Antes de ejecutarlo, predecí el orden de salida escribiéndolo en un comentario. Ejecutalo y confirmá si acertaste — y explicá con tus palabras, usando el modelo de las cuatro piezas, por qué el orden es ese y no el orden en que aparecen las líneas.
</div>

## Callbacks

### Qué es un callback

Un **callback** es, simplemente, una función que se pasa como argumento para que otra la ejecute más adelante. Ya se usó esta idea con `map`/`filter`/`reduce` en JS Funcional — la diferencia acá es que el eje pasa a ser el **momento en el tiempo** en el que se ejecuta, no la transformación de datos.

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

Este patrón — una función que recibe un callback y lo invoca cuando termina su trabajo — es exactamente cómo funcionan `fetch`, la lectura de archivos en Node, y casi toda API asincrónica clásica de JavaScript.

Una convención muy extendida (sobre todo en Node.js) es la del **callback "error-first"**: el callback siempre recibe el posible error como primer parámetro (`null` si no hubo error) y el resultado como segundo:

```js
function getPersonaById(id, callback) {
  setTimeout(() => {
    if (id > 0) {
      callback(null, { id, nombre: 'Pepe' })
    } else {
      callback({ error: true, msg: 'ID inválido' })
    }
  }, 1000)
}

getPersonaById(10, (err, res) => {
  if (err) {
    console.error('Error:', err.msg)
  } else {
    console.log('Encontrado:', res)
  }
})
```

### Callback hell

El problema aparece cuando **varias** operaciones asincrónicas dependen unas de otras en secuencia — cada resultado hace falta para lanzar la siguiente llamada:

```js
fetchUser(1, (user) => {
  fetchOrders(user.id, (orders) => {
    fetchOrderDetails(orders[0].id, (details) => {
      fetchShipping(details.id, (shipping) => {
        console.log(shipping)
        // y cada paso necesita, además, su propio manejo de error...
      }, handleError)
    }, handleError)
  }, handleError)
}, handleError)
```

Cada callback queda anidado **dentro** del anterior, y el código crece hacia la derecha en vez de hacia abajo. Este patrón tiene nombre propio: **callback hell** (o *pyramid of doom*, "pirámide del desastre").

Los problemas concretos de este estilo:

- **Legibilidad**: la indentación no refleja el orden lógico del programa de forma clara a simple vista.
- **Manejo de errores**: no hay un único lugar para atrapar errores — cada nivel necesita su propio `handleError`, repetido, y es fácil olvidarse de alguno.
- **Componer operaciones es difícil**: expresar "ejecutá estas tres cosas en paralelo, no en secuencia" con callbacks puros exige orquestar el conteo a mano.

Los callbacks no están "mal" en sí — de hecho, hasta las Promises los usan por debajo. El problema específico es **anidarlos** para expresar una secuencia larga. Esto motivó, directamente, la creación de las **Promises** en ES6 (2015).

## Promises

### Qué es una Promise

Una **Promise** es un objeto que representa el resultado — todavía desconocido en el momento de crearla — de una operación asincrónica. Siempre está en uno de tres **estados**:

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>pending</h4>

Estado inicial: la operación todavía no terminó.
</div>
<div class="info-card tone-green">
<h4>fulfilled</h4>

Terminó con éxito — tiene un valor resultado.
</div>
<div class="info-card tone-red">
<h4>rejected</h4>

Terminó con error — tiene un motivo (`reason`) de rechazo.
</div>
</div>

Una vez que una Promise pasa de `pending` a `fulfilled` o `rejected`, queda **fija** en ese estado para siempre — no puede "cambiar de opinión" después.

### Crear una Promise

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

`new Promise` recibe una función llamada *executor*, con dos parámetros: `resolve` (llamarla marca la Promise como `fulfilled`, con ese valor) y `reject` (la marca como `rejected`, con ese motivo). En código de aplicación real casi no se crean Promises "a mano" así — lo más común es que una función de una librería (`fetch`, un driver de base de datos) ya devuelva una directamente — pero entender este mecanismo interno ayuda a entender todo lo que sigue.

### Consumir una Promise: `.then` / `.catch` / `.finally`

```js
fetchUserName(1)
  .then((name) => console.log(`Hola, ${name}!`))
  .catch((error) => console.error('Falló:', error.message))
  .finally(() => console.log('Terminado (haya salido bien o mal)'))
```

- **`.then(onFulfilled)`**: se ejecuta si la Promise se resuelve — recibe el valor resuelto.
- **`.catch(onRejected)`**: se ejecuta si se rechaza — recibe el motivo del rechazo. Es equivalente a `.then(undefined, onRejected)`.
- **`.finally(onSettled)`**: se ejecuta siempre, sin importar el resultado — ideal para limpieza (por ejemplo, ocultar un indicador de carga).

### Encadenar Promises

```js
fetchUser(1)
  .then((user) => fetchOrders(user.id))
  .then((orders) => fetchOrderDetails(orders[0].id))
  .then((details) => fetchShipping(details.id))
  .then((shipping) => console.log(shipping))
  .catch((error) => console.error('Algo falló en la cadena:', error.message))
```

Cada `.then` devuelve una **nueva** Promise — por eso se puede seguir encadenando indefinidamente. Si cualquier eslabón de la cadena rechaza, la ejecución **salta directo** al `.catch` más cercano, sin pasar por los `.then` intermedios: un único lugar para manejar errores, en contraste directo con el callback hell de la sección anterior — el mismo comportamiento de "salto" que ya conocen de un `try`/`catch` tradicional.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Tomá el ejemplo de callback hell (`fetchUser` → `fetchOrders` → `fetchOrderDetails` → `fetchShipping`) y reescribilo como una cadena de `.then()`. Contá cuántas veces aparece el manejo de errores en cada versión.
</div>

### Ejecutar en paralelo: `Promise.all`

```js
Promise.all([
  fetchUser(1),
  fetchUser(2),
  fetchUser(3),
])
  .then((users) => console.log('Los tres llegaron:', users))
  .catch((error) => console.error('Al menos uno falló:', error.message))
```

`Promise.all` recibe un array de Promises y devuelve **una sola** Promise que se resuelve cuando **todas** terminaron, con un array de resultados en el mismo orden en que se pasaron. Si **cualquiera** de ellas rechaza, `Promise.all` rechaza inmediatamente con ese motivo — aunque las demás sigan corriendo en segundo plano.

La diferencia clave con encadenar `.then()` es que acá las tres llamadas arrancan **al mismo tiempo**: si cada una tarda 1 segundo, el total es de aproximadamente 1 segundo, no 3 — a diferencia de una cadena, donde cada paso espera al anterior.

Mención rápida de otro método relacionado: **`Promise.race`** se resuelve o rechaza con la **primera** promise del array que termine, para lo que sea (éxito o error) — útil, por ejemplo, para implementar un timeout corriendo en paralelo con la operación real.

## `async`/`await`

### Azúcar sintáctica sobre Promises

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

`async`/`await` **no es un mecanismo nuevo** — es sintaxis que se traduce, por debajo, a Promises encadenadas. La diferencia es puramente de legibilidad: el código con `async`/`await` se lee de arriba hacia abajo, como si fuera sincrónico, aunque no lo sea.

Dos reglas básicas: `await` solo se puede usar dentro de una función marcada `async` (con la excepción moderna del *top-level await*, ES2022, fuera del alcance de este apunte). Y una función `async` **siempre devuelve una Promise** — aunque su `return` interno sea un valor común, queda envuelto automáticamente en una Promise resuelta con ese valor.

### El mismo ejemplo, tres formas

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>Callback</h4>

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
<div class="info-card">
<h4>Promise</h4>

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
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
<h4>async/await</h4>

```js
const user =
  await fetchUser(1)
const orders =
  await fetchOrders(user.id)
console.log(orders)
```
</div>
</div>

Las tres versiones resuelven exactamente lo mismo. Ninguna reemplaza del todo a las otras dos: hay que saber leer las tres, porque las tres aparecen en código real — sobre todo callbacks y Promises, en librerías de terceros que no se controlan.

### Manejo de errores con `try`/`catch`

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

Con `async`/`await`, el manejo de errores vuelve a ser el `try`/`catch` de siempre: si cualquier `await` de adentro rechaza, la ejecución salta directo al `catch` — el mismo comportamiento que `.catch()` en una cadena de Promises, pero con la sintaxis sincrónica ya conocida de Java/C.

Un punto importante para no dar por sentado: un `try`/`catch` **sincrónico** alrededor de código asincrónico **no** atrapa un error que ocurre más adelante, dentro de un callback:

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

El `throw` de adentro del callback de `setTimeout` ocurre **mucho después** de que el `try`/`catch` que lo rodea ya terminó de ejecutarse — recordando el modelo del event loop, el callback corre recién cuando el call stack está vacío, en una "vuelta" completamente distinta del programa. El error termina como una excepción no capturada, no dentro del `catch`. Con Promises y `async`/`await` esto no pasa: tanto `.catch()` como el `try`/`catch` de una función `async` sí están diseñados para atrapar errores que ocurren "más adelante en el tiempo" — es una de las razones de fondo, más allá de la legibilidad, por las que las Promises reemplazaron a los callbacks para este tipo de flujo.

### Ejemplo real: `fetch` + `async`/`await`

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

`fetch` devuelve una Promise que se resuelve **incluso si la respuesta HTTP es un error** (404, 500) — `fetch` solo rechaza ante fallas de red reales (sin conexión, DNS caído, etc.), no ante un código de estado de error. Por eso hace falta chequear `res.ok` a mano y lanzar el error explícitamente, como en el ejemplo.

Encadenando dos llamadas reales, donde la segunda necesita el resultado de la primera:

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

Con `async`/`await`, este flujo se lee igual de lineal que si fuera código sincrónico — comparar con cómo se vería esta misma secuencia de dos llamadas anidada con callbacks puros, en la sección de callback hell.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí una función `async` que use `fetch` contra <a href="https://api.nationalize.io/?name=test" target="_blank" rel="noopener">nationalize.io</a> con un nombre a elección, maneje el caso de `!res.ok` lanzando un error, y muestre el resultado por consola dentro de un `try`/`catch`. Después, a propósito, escribí mal la URL (por ejemplo `nazme=` en vez de `name=`) y confirmá que el `catch` sigue atrapando el error igual.
</div>

## Microtasks vs. Macrotasks

Lo que se presentó como "task queue" en la sección del event loop en realidad son, como mínimo, **dos colas distintas** con distinta prioridad:

- **Macrotasks**: `setTimeout`, `setInterval`, eventos de entrada/salida.
- **Microtasks**: los callbacks de Promises (`.then`/`.catch`/`.finally`), y `queueMicrotask`.

La regla del event loop es: después de cada macrotask, se vacía **por completo** la cola de microtasks antes de pasar a la siguiente macrotask — incluso si aparecen microtasks nuevas mientras se está vaciando la cola. En otras palabras: las Promises "cortan la fila" por delante de los timers, aunque el timer se haya programado antes en el código.

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

Aunque el `setTimeout` se programó con `0` milisegundos — es decir, "ejecutá esto ya" — la Promise igual se ejecuta primero. El código sincrónico siempre corre completo primero; después se vacía la cola de microtasks entera; recién después se saca **una sola** macrotask de su cola, y se repite el ciclo.

Esta distinción es una pregunta clásica de entrevista técnica, y también explica bugs reales: código que "debería" ejecutarse en cierto orden y no lo hace, porque se mezclan timers con Promises sin tener en cuenta la prioridad de las colas. No hace falta memorizar la implementación exacta del motor de JS — alcanza con el modelo mental resumido: **sincrónico → todas las microtasks → una macrotask → repetir**.

## Cheat sheet

<div class="card-grid card-grid-2">
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

## Referencias y recursos

- [developer.mozilla.org — Asynchronous JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript/Guide/Asynchronous) — guía oficial en español
- [javascript.info — Async](https://javascript.info/async) — callbacks, promises y async/await en profundidad
- ["What the heck is the event loop anyway?"](https://www.youtube.com/watch?v=8aGhZQkoFbQ) — Philip Roberts, JSConf — la charla de referencia sobre el event loop
- [nationalize.io](https://nationalize.io/) y [restcountries.com](https://restcountries.com/) — las APIs públicas usadas en los ejemplos de este apunte

## Cierre

El objetivo de este tema es tener resuelto el modelo mental completo de la asincronía en JavaScript — call stack, Web APIs, task queue, event loop — y las tres formas de expresarla en código: callbacks, Promises y `async`/`await`. De acá en adelante, en el resto de la unidad (TypeScript, React, Node + Express, MongoDB), el código asincrónico va a aparecer todo el tiempo — cada pedido HTTP, cada consulta a una base de datos — y se asume este apunte como base, igual que la sintaxis moderna de JS Contemporáneo.
