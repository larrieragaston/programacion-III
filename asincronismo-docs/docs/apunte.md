# Asincronismo

Todo el código visto hasta ahora en la materia se ejecuta **de una sola vez, de arriba hacia abajo, sin pausas**: cada línea espera a que termine la anterior, y el programa entero corre de punta a punta antes de devolver el control. Ese modelo alcanza mientras cada línea termine casi instantáneamente — sumar dos números, recorrer un array, formatear un string son operaciones que la CPU resuelve en microsegundos.

La pregunta de este tema es qué pasa cuando una línea de código depende de **algo externo** — una respuesta de red, la lectura de un archivo, un timer — que puede tardar milisegundos, segundos, o directamente nunca llegar (una conexión caída, un servidor que no responde). Si el modelo "una cosa a la vez, de punta a punta" siguiera aplicando tal cual, esa espera congelaría el programa entero. Este apunte explica **por qué** eso no pasa en JavaScript, **cómo** logra evitarlo con un solo hilo de ejecución, y **de qué formas concretas** se expresa en código: callbacks, Promises y `async`/`await`, en ese orden histórico.

## JavaScript es de un solo hilo

Un **hilo (thread)** de ejecución procesa instrucciones de a una, en orden estricto. A diferencia de Java — donde ya vieron threads explícitos, capaces de correr código en paralelo real, en núcleos de CPU distintos — **JavaScript tiene un único hilo principal** para ejecutar código. No hay dos líneas del programa corriendo literalmente al mismo tiempo (dejando de lado los *Web Workers*, una herramienta específica para correr JS en un hilo aparte y comunicarse por mensajes, fuera del alcance de este tema, y que en la práctica se usa poco comparado con el resto de lo que se ve acá).

La consecuencia directa: si una operación **bloquea** ese único hilo, todo se detiene — no se puede clickear un botón, no se puede hacer scroll, no corre ningún otro código de la página (ni siquiera repintar la pantalla), hasta que esa operación termine.

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

Durante esos 5 segundos la página **no responde a nada**. Este ejemplo simula, a propósito, exactamente el problema que la asincronía existe para resolver: ¿qué se hace cuando una operación tarda, sin caer en esto?

Vale la pena distinguir dos ideas que suelen confundirse: **concurrencia** y **paralelismo**. Paralelismo es tener dos cosas corriendo literalmente al mismo tiempo, en núcleos de CPU distintos — eso es lo que hacen los threads de Java, y lo que JS **no** hace en su hilo principal. Concurrencia es dar la impresión de que varias cosas avanzan "a la vez" intercalando el trabajo entre ellas, sin que ninguna bloquee a las demás por mucho tiempo — eso sí es lo que logra JavaScript con la asincronía, aunque por debajo siga habiendo un solo hilo haciendo una cosa genuina a la vez. El resto de este apunte explica el mecanismo concreto que hace posible esa concurrencia sin paralelismo real en el hilo de JS.

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

Ninguna de estas operaciones depende de la CPU: dependen de algo externo (la red, el disco, el reloj del sistema). Por eso bloquear el único hilo de JS mientras se espera sería, además de una mala experiencia de uso, un desperdicio literal de CPU — la máquina se queda "mirando" sin hacer nada útil mientras el dato viaja por la red.

### Un ejemplo concreto: la página con noticias, clima y publicidad

Pensemos en una página real, del estilo de un portal de noticias: además del contenido principal, muestra el clima actual y publicidad, cada uno obtenido de un servicio externo distinto e independiente de los otros dos.

Si esos tres pedidos se resolvieran de forma **bloqueante** — uno detrás del otro, sin seguir hasta que el anterior termine — el tiempo total de carga sería la **suma** de los tres tiempos individuales:

```js
function pedirNoticias()   { blockFor(2000); return 'Noticias del día' }
function pedirClima()      { blockFor(1000); return '22°C, soleado' }
function pedirPublicidad() { blockFor(1500); return 'Anuncio: ...' }

console.log(pedirNoticias())     // recién a los 2s
console.log(pedirClima())        // recién a los 3s
console.log(pedirPublicidad())   // recién a los 4.5s
```

2 + 1 + 1.5 = **4.5 segundos** hasta que la página responde a lo que sea — y durante todo ese tiempo, ni un solo click funciona, porque el hilo está bloqueado dentro de `blockFor`.

La versión asincrónica, en cambio, dispara las tres peticiones **sin esperar** una a la otra:

```js
function pedirNoticias()   { setTimeout(() => console.log('Noticias del día'), 2000) }
function pedirClima()      { setTimeout(() => console.log('22°C, soleado'), 1000) }
function pedirPublicidad() { setTimeout(() => console.log('Anuncio: ...'), 1500) }

pedirNoticias()
pedirClima()
pedirPublicidad()
console.log('La página ya es usable — nada bloqueó el hilo')
```

Acá las tres arrancan casi al mismo tiempo (delegadas, como se va a explicar en la próxima sección) y la página queda lista en **~2 segundos** — el tiempo de la más lenta, no la suma — mientras que el `console.log` final se imprime de inmediato, antes de que llegue cualquiera de las tres respuestas.

Gracias al asincronismo en JavaScript, no hace falta bloquear el hilo esperando cada respuesta: se le devuelve el control a JS enseguida y el programa entero sigue respondiendo mientras las tres esperan "en paralelo" (entre comillas, porque como se vio en la sección anterior, no es paralelismo real de CPU — es concurrencia). Este es, ni más ni menos, el problema que el resto de este apunte viene a resolver: callbacks, Promises y `async`/`await` son las formas concretas de expresarlo en código.

<div class="practice-box">
<p class="practice-label">Para pensar</p>

Pensá en una aplicación que uses seguido (una red social, un mapa, un mail). Enumerá al menos tres operaciones que esa app hace que probablemente sean asincrónicas — ¿qué pasaría con la experiencia de uso si esas operaciones fueran bloqueantes en cambio?
</div>

## El modelo mental: Call Stack, Web APIs, Task Queue, Event Loop

Para entender **cómo** JavaScript logra no bloquearse a pesar de tener un solo hilo, hace falta un modelo mental de cuatro piezas que trabajan juntas. Las vemos una por una primero, y al final las juntamos todas en un solo diagrama.

<div class="card-grid card-grid-2">
<div class="info-card" style="background:var(--vp-c-brand-soft)">
<h4>Call Stack</h4>

Dónde vive el código sincrónico mientras se ejecuta.
</div>
<div class="info-card" style="background:var(--vp-c-yellow-soft)">
<h4>Web APIs / libuv</h4>

Donde corren aparte los timers, la red, el disco.
</div>
<div class="info-card tone-green">
<h4>Colas de tareas</h4>

Donde esperan su turno los callbacks ya listos para correr.
</div>
<div class="info-card tone-purple">
<h4>Event Loop</h4>

El mecanismo que conecta todo — decide cuándo le toca a cada cosa.
</div>
</div>

### Call Stack

El **call stack** (pila de llamadas) es donde el motor de JS registra qué función se está ejecutando en cada momento. Cada llamada se **apila** arriba de la anterior; cuando una función termina, se **desapila**. Es puramente sincrónico y estrictamente ordenado: una función tiene que terminar (o quedar en pausa) antes de que la que está debajo en la pila pueda seguir.

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

`'3'` se imprime **antes** que `'2'`, a pesar de que `setTimeout` se llamó primero. JS delegó la espera a otra pieza y siguió de largo con el resto del call stack. ¿A quién se la delega?

### Web APIs (o libuv, en Node)

`setTimeout`, `fetch`, los eventos del DOM, la lectura de archivos — **no los ejecuta el motor de JavaScript en sí**. Los ejecuta el entorno que lo rodea:

- En el **navegador**, ese entorno son las **Web APIs**: parte del navegador, no del lenguaje JavaScript propiamente dicho.
- En **Node.js**, el entorno equivalente es **libuv**, una librería en C que maneja entrada/salida de forma no bloqueante.

El motor de JS le dice a esa pieza externa "avisame cuando esto termine" y sigue ejecutando el resto del call stack **sin esperar la respuesta**.

Vale la pena entender un poco mejor **dónde** viven exactamente estas piezas y **cómo** logran ejecutarse "aparte", porque quedarse solo con "se ejecutan en otro lado" deja la pregunta a mitad de camino. En el navegador, las Web APIs son código nativo escrito en C++, parte del propio navegador (por ejemplo, del motor Blink en el caso de Chrome) — no están escritas en JavaScript. Y acá está el punto clave: **el navegador en sí mismo sí es una aplicación multi-hilo** (y hasta multi-proceso, según el navegador). Cuando el motor de JS delega un `setTimeout` o un `fetch`, el navegador puede efectivamente contar ese timer o esperar esa respuesta de red en un hilo del sistema operativo completamente aparte del hilo principal de JS — ahí sí hay paralelismo real, solo que ocurre fuera de JavaScript. En Node.js, `libuv` hace algo equivalente combinando mecanismos asincrónicos del propio sistema operativo (`epoll` en Linux, `kqueue` en macOS, IOCP en Windows) para la red, y un *pool* propio de threads (4 por defecto) para operaciones que el sistema operativo no puede resolver de forma asincrónica, como algunas llamadas al sistema de archivos.

Esta es la pieza clave del modelo completo: JS en sí mismo es de un solo hilo, pero el entorno nativo que lo rodea sí puede hacer varias cosas en paralelo real — y recién cuando termina, le entrega el resultado a JS a través de la cola de tareas que se explica a continuación, nunca directamente ni de forma inmediata.

### Task Queue (cola de tareas)

Cuando una Web API (o libuv) termina su trabajo — el timer llegó a cero, la respuesta de red llegó — **no ejecuta el callback inmediatamente**. Lo pone en una cola de espera: la **task queue** (también llamada *callback queue*). El callback que quedó en esa cola **solo se ejecuta cuando el call stack está completamente vacío**.

Esta regla explica por qué `setTimeout(fn, 0)` no ejecuta `fn` de inmediato: igual tiene que esperar su turno en la cola, después de todo el código sincrónico que ya estaba pendiente de ejecutar.

### Trazando la ejecución, paso a paso

Con las tres piezas anteriores ya se puede seguir, línea por línea, un ejemplo con dos timers:

```js
console.log('A')
setTimeout(() => console.log('B'), 0)
console.log('C')
setTimeout(() => console.log('D'), 0)
console.log('E')
```

1. Se apila y corre `console.log('A')` → imprime **A** → se desapila.
2. Se encuentra el primer `setTimeout(..., 0)` → se delega a la Web API, que arranca un timer de 0ms.
3. Se apila y corre `console.log('C')` → imprime **C** → se desapila. (El timer de 0ms ya terminó, pero su callback tiene que esperar en la task queue: el call stack todavía no está vacío.)
4. Se encuentra el segundo `setTimeout(..., 0)` → también se delega; su callback queda encolado detrás del anterior.
5. Se apila y corre `console.log('E')` → imprime **E** → se desapila. Ya no queda código sincrónico: el call stack está vacío.
6. El event loop lo detecta, saca el **primer** callback de la cola (el de "B" — llegó primero) y lo apila → imprime **B**.
7. Call stack vacío otra vez → el event loop saca el siguiente (el de "D") y lo apila → imprime **D**.

Salida real: **A, C, E, B, D**. Ni siquiera un `setTimeout(fn, 0)` corre "inmediatamente": siempre espera a que termine **todo** el código sincrónico, y respeta el orden de llegada a la cola (esto último — orden de llegada, FIFO — importa: si hubiera un tercer timer de 0ms encolado antes que los otros dos por haber sido programado antes en tiempo real aunque aparezca después en el código, igual respeta el orden en que efectivamente entró a la cola).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí `console.log('A')`, seguido de `setTimeout(() => console.log('B'), 0)`, seguido de `console.log('C')`. Antes de ejecutarlo, predecí el orden de salida escribiéndolo en un comentario. Ejecutalo y confirmá si acertaste — y explicá con tus palabras, usando el modelo de las cuatro piezas, por qué el orden es ese y no el orden en que aparecen las líneas.
</div>

## Microtasks y macrotasks

Antes de llegar al diagrama completo, hace falta una precisión importante sobre la "task queue" que se acaba de presentar: en realidad son, como mínimo, **dos colas distintas** con distinta prioridad. Todavía no vimos la sintaxis de Promises ni de `async`/`await` en detalle — eso viene en las próximas secciones — pero alcanza con reconocer los nombres acá para entender el panorama completo antes de ver el diagrama.

- **Macrotasks**: `setTimeout`, `setInterval`, eventos de entrada/salida, y **callbacks comunes** (el mismo mecanismo ya visto arriba).
- **Microtasks**: los callbacks de Promises (`.then`/`.catch`/`.finally`), la continuación del código que sigue después de un `await`, y `queueMicrotask`.

La regla del event loop es: después de cada macrotask, se vacía **por completo** la cola de microtasks antes de pasar a la siguiente macrotask — incluso si aparecen microtasks nuevas mientras se está vaciando la cola. Dicho de otra forma, de mayor a menor prioridad: **código sincrónico → microtasks (Promises, `async`/`await`) → macrotasks (callbacks, timers)**. Las Promises "cortan la fila" por delante de los timers y los callbacks comunes, aunque estos se hayan programado antes en el código.

El siguiente ejemplo combina las tres formas — un timer, un callback común, una Promise y un `await` — para ver la prioridad en acción:

```js
console.log('1: sync')
setTimeout(() => console.log('5: macrotask (setTimeout)'), 0)
function operacionConCallback(cb) { setTimeout(cb, 0) }
operacionConCallback(() => console.log('6: macrotask (callback)'))
Promise.resolve().then(() => console.log('3: microtask (Promise)'))
async function demo() {
  await null
  console.log('4: microtask (después de un await)')
}
demo()
console.log('2: sync')
```

Los dos `console.log` sincrónicos (**1** y **2**) corren primero, de punta a punta — ni una Promise ni un `await` los interrumpen. Después se vacía **toda** la cola de microtasks: la Promise (**3**) y la continuación del `await` (**4**), en el orden en que se encolaron. Recién al final se procesan los macrotasks — el `setTimeout` (**5**) y el callback (**6**), también en orden de llegada. Orden real de salida: **1, 2, 3, 4, 5, 6**.

Esta distinción es una pregunta clásica de entrevista técnica, y también explica bugs reales: código que "debería" ejecutarse en cierto orden y no lo hace, porque se mezclan timers/callbacks con Promises/`async`-`await` sin tener en cuenta la prioridad de las colas. No hace falta memorizar la implementación exacta del motor de JS — alcanza con el modelo mental resumido: **sincrónico → todas las microtasks → una macrotask → repetir**.

## El Event Loop, todo junto

El **event loop** (bucle de eventos, el que le da nombre a todo este mecanismo) es, literalmente, un chequeo que se repite todo el tiempo mientras el programa vive: *"¿está vacío el call stack? Si es así, tomá el próximo callback de la cola correspondiente y apilalo."*

<img src="/images/event-loop-diagram.png" alt="Diagrama del Event Loop de JavaScript: Call Stack, Heap, Web APIs y Callback Queue conectados por el Event Loop" style="max-width:100%;display:block;margin:1.5rem auto" />

<p style="text-align:center;font-size:0.8em;opacity:0.65;margin-top:-0.5rem">
Diagrama de <a href="https://commons.wikimedia.org/wiki/User:Byteslovesbits" target="_blank" rel="noopener">Byteslovesbits</a>, <a href="https://commons.wikimedia.org/wiki/File:JavaScript_Event_Loop.png" target="_blank" rel="noopener">Wikimedia Commons</a> (<a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a>).
</p>

El diagrama simplifica todo a una sola "Callback Queue" — con lo visto en la sección anterior, ya sabemos que en realidad son **dos colas** con distinta prioridad:

<div class="card-grid card-grid-2">
<div class="info-card tone-purple">
<h4>Microtask Queue (mayor prioridad)</h4>

`.then`/`.catch`/`.finally`, continuación de un `await`
</div>
<div class="info-card tone-orange">
<h4>Macrotask Queue (menor prioridad)</h4>

`setTimeout`, callbacks, eventos — la "Callback Queue" del diagrama
</div>
</div>

<div class="practice-box">
<p class="practice-label">Practicá</p>

Sin mirar la respuesta, dibujá (en papel o en un editor de diagramas) las cuatro piezas del modelo completo con sus flechas, y explicáselo en voz alta a un compañero o compañera como si fuera la primera vez que lo escucha. Si te trabás en algún punto, ese es justo el punto que hay que repasar.
</div>

## Callbacks

### Qué es un callback

Un **callback** es una función que se pasa como argumento a otra función — ya se usó esta idea en JS Funcional con `map`/`filter`/`reduce`, donde el callback corre **sincrónicamente**, en el momento mismo de la llamada. En asincronismo hablamos de otra cosa: un callback que se invoca **más adelante**, cuando termina una operación que tarda.

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

Este patrón — una función que recibe un callback y lo invoca cuando termina su trabajo — es exactamente cómo funcionan `fetch`, la lectura de archivos en Node, y casi toda API asincrónica clásica de JavaScript.

"Callback" no es una feature de una versión puntual de ECMAScript — es un patrón que existe desde que JS tiene funciones de primera clase, es decir, desde su primera versión (1997). Antes de que existieran las Promises (recién en **ES2015**), pasarle un callback a una función era la **única** forma de decirle "avisame cuando termines" — no había otro mecanismo en el lenguaje. Sigue vigente hoy: buena parte de Node.js (el módulo `fs`, por ejemplo) y librerías como Express (`(req, res, next) => {...}`) todavía lo usan, así que aprender a leerlo no es un ejercicio histórico — es necesario para trabajar con código real que ya existe.

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
        // y si cada paso necesita, además, manejar su propio error...
      }, handleError)
    }, handleError)
  }, handleError)
}, handleError)
```

¿Por qué anidar? Cada paso necesita un dato que **solo existe adentro del callback anterior** — `fetchOrders` necesita `user.id`, y `user` no existe todavía cuando se llama a `fetchUser`; recién llega como argumento del callback, milisegundos (o segundos) después. Un callback no puede "devolver" su resultado hacia afuera porque la función que lo programó ya terminó de ejecutarse — la única forma de usar ese dato es metiendo el siguiente paso **adentro** de ese mismo callback. Repetir esto varias veces produce la pirámide: **callback hell** (o *pyramid of doom*, "pirámide del desastre").

Los problemas concretos de este estilo:

- **Legibilidad**: el orden real de ejecución no coincide con la indentación — cuesta seguir el flujo con la vista.
- **Manejo de errores**: no hay un único lugar para atrapar errores — cada callback necesita su propio manejo (`handleError` repetido en el ejemplo anterior), y es fácil olvidarse de alguno.
- **Componer operaciones es difícil**: ¿cómo se ejecutan dos de estas llamadas **en paralelo** en vez de en secuencia? Con callbacks puros, hay que orquestarlo a mano contando cuántas terminaron.

Los callbacks no están "mal" en sí — de hecho, hasta las Promises los usan por debajo. El problema específico es **anidarlos** para expresar una secuencia larga. Esto motivó, directamente, la creación de las **Promises** en ES6 (2015).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Tomá el ejemplo de callback hell (`fetchUser` → `fetchOrders` → `fetchOrderDetails` → `fetchShipping`) y contá cuántas veces aparece `handleError`. En la próxima sección se reescribe este mismo flujo con Promises — antes de leerlo, pensá qué esperarías que cambie.
</div>

## Promises

### Qué es una Promise

Una **Promise** es un objeto que representa el resultado — todavía desconocido en el momento de crearla — de una operación asincrónica. Se introdujo en **ES2015 (ES6)**, justamente para resolver el problema de la sección anterior: una forma estándar de encadenar pasos asincrónicos sin anidar callbacks ni repetir el manejo de errores en cada paso. Una Promise siempre está en uno de tres **estados**:

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

Pending es el punto de partida: desde ahí, la Promise pasa a `fulfilled` si se invoca su función `resolve`, o a `rejected` si se invoca `reject` — nunca las dos, y nunca ninguna transición en el otro sentido. Una vez que pasa a `fulfilled` o `rejected`, queda **fija** en ese estado para siempre: no puede "cambiar de opinión" después.

### Crear una Promise

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

`new Promise` recibe una función llamada *executor*, con dos parámetros: `resolve` y `reject`. En código de aplicación real casi no se crean Promises "a mano" así — lo más común es que una función de una librería (`fetch`, un driver de base de datos) ya devuelva una directamente — pero entender este mecanismo interno ayuda a entender todo lo que sigue.

En el ejemplo, cada rama del `if` corresponde a un desenlace distinto:

<div class="card-grid card-grid-2">
<div class="info-card tone-green">

**`resolve(...)`** → estado `fulfilled`, `value` = ese argumento. Pasa si `id > 0`, después de 1 segundo.
</div>
<div class="info-card tone-red">

**`reject(new Error(...))`** → estado `rejected`, `reason` = ese `Error`. Pasa si `id <= 0`.
</div>
</div>

### Consumir una Promise: `.then` / `.catch` / `.finally`

```js
fetchUserName(1)
  .then((name) => console.log(`Hola, ${name}!`))
  .catch((error) => console.error('Falló:', error.message))
  .finally(() => console.log('Terminado (haya salido bien o mal)'))
```

- **`.then(onFulfilled)`**: se ejecuta si la Promise se resuelve — recibe el valor resuelto.
- **`.catch(onRejected)`**: se ejecuta si se rechaza — recibe el motivo del rechazo. Es equivalente a `.then(undefined, onRejected)`.
- **`.finally(onSettled)`**: se ejecuta siempre, sin importar el resultado — no recibe ningún valor. Ideal para limpieza (por ejemplo, ocultar un indicador de carga).

### Encadenar Promises

```js
fetchUser(1)
  .then((user) => fetchOrders(user.id))
  .then((orders) => fetchOrderDetails(orders[0].id))
  .then((details) => fetchShipping(details.id))
  .then((shipping) => console.log(shipping))
  .catch((error) => console.error('Algo falló en la cadena:', error.message))
```

Cada `.then` devuelve una **nueva** Promise — por eso se puede seguir encadenando indefinidamente. Si cualquier eslabón de la cadena rechaza, la ejecución **salta directo** al `.catch` más cercano, sin pasar por los `.then` intermedios: un único lugar para manejar errores, en contraste directo con el callback hell de la sección anterior.

Pero esta cadena tiene sus propios límites: sigue sin leerse como código realmente secuencial (hay que seguir el rastro de `.then` en `.then`), y si un paso necesitara un valor de **dos** pasos atrás — no solo el inmediato anterior — hay que arrastrarlo a mano entre callbacks. Es el problema que resuelve `async`/`await`, más adelante en este apunte.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Tomá el ejemplo de callback hell (`fetchUser` → `fetchOrders` → `fetchOrderDetails` → `fetchShipping`) y reescribilo como una cadena de `.then()`. Contá cuántas veces aparece el manejo de errores en cada versión.
</div>

### Errores puntuales en la cadena

El `.catch()` del ejemplo anterior atrapa **cualquier** error que haya ocurrido en algún punto anterior de toda la cadena — no distingue si el problema fue en el primer paso o en el último. Para diferenciar el origen del error hace falta un `.catch` pegado al paso específico, **antes** de encadenar el siguiente `.then`:

```js
fetchUser(1)
  .catch((error) => {
    console.error('No se pudo cargar el usuario:', error.message)
    return null   // sin usuario no hay nada que pedir después
  })
  .then((user) => (user ? fetchOrders(user.id) : []))
  .catch((error) => {
    console.error('No se pudieron cargar las órdenes:', error.message)
    return []
  })
```

Un `.catch()` intermedio no corta la cadena: atrapa el error de los pasos anteriores y, si no vuelve a lanzar (`throw`) ni devuelve una promise rechazada, la cadena sigue con el valor que ese `.catch` devuelva — acá, `null` primero y `[]` después, en vez de romper todo. Así se pueden manejar distintos errores en distintos puntos de la cadena, en vez de un único `.catch` final para todo.

El costo de este enfoque: cuantos más puntos de manejo de errores hay, más difícil es seguir el flujo de la cadena a simple vista — otra razón, además de la ya mencionada, por la que conviene conocer `async`/`await`.

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

La diferencia clave con encadenar `.then()` es que acá las tres llamadas arrancan **al mismo tiempo**, no una después de la otra — el mismo principio que se vio con el ejemplo de la página cargando noticias, clima y publicidad en paralelo: el tiempo total es el de la más lenta, no la suma.

Ojo con una expectativa frecuente: `Promise.all` **no crea hilos ni paraleliza CPU**. Solo tiene sentido para operaciones **asincrónicas** (I/O) — las tres arrancan y quedan delegadas a la vez, así que el tiempo total es el de la más lenta. Si `fetchUser` fuera una función **sincrónica** (bloqueante), envolverla en `Promise.all` no cambia absolutamente nada: el hilo sigue siendo uno solo, y las tres seguirían ejecutándose una atrás de la otra — `Promise.all` no le agrega concurrencia real a código que ya era bloqueante, porque el problema de fondo (bloquear el único hilo) sigue estando ahí. La ganancia de `Promise.all` viene específicamente de que las operaciones delegadas **ya estaban** liberando el hilo mientras esperaban.

Otro error habitual, más sutil, aparece al combinar `Promise.all` con `await` dentro de un bucle: si se hace `for (const id of ids) { await fetchUser(id) }`, cada `fetchUser` espera a que termine el anterior antes de arrancar — es una cadena secuencial disfrazada, aunque el código "parezca" simple. Para conseguir el arranque simultáneo hace falta crear primero el array de Promises (`ids.map(fetchUser)`) y recién ahí pasarlo a `Promise.all`.

Mención rápida de otro método relacionado: **`Promise.race`** se resuelve o rechaza con la **primera** promise del array que termine, para lo que sea (éxito o error) — útil, por ejemplo, para implementar un timeout corriendo en paralelo con la operación real.

<div class="practice-box">
<p class="practice-label">Para pensar</p>

Si `Promise.all` no crea hilos ni paraleliza CPU, ¿por qué igual sirve para acelerar el tiempo total cuando las operaciones son asincrónicas (network, timers)? Conectá la respuesta con lo que se explicó sobre dónde "viven" realmente las Web APIs.
</div>

### Otro método útil: `Promise.allSettled`

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

Introducido en **ES2020**. A diferencia de `Promise.all`, nunca rechaza — espera a que **todas** las promises terminen, sea como sea, y devuelve un array con el resultado de cada una: `{ status: 'fulfilled', value }` o `{ status: 'rejected', reason }`. Útil cuando se necesita el resultado de cada operación aunque alguna falle, en vez de descartar todo por un solo error — por ejemplo, cargar varios widgets independientes de un dashboard, donde si uno falla, los demás igual deberían mostrarse.

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

Introducido en **ES2017 (ES8)**, después que las Promises (ES2015), para resolver justo lo que se veía en la sección anterior: cadenas de `.then` que crecen y dejan de leerse como una secuencia simple. `async`/`await` **no reemplaza** a las Promises: por debajo es exactamente el mismo motor, `async`/`await` es solo sintaxis. La diferencia es puramente de legibilidad: el código con `async`/`await` se lee de arriba hacia abajo, como si fuera sincrónico, aunque no lo sea.

Dos reglas básicas: `await` solo se puede usar dentro de una función marcada `async` (con la excepción moderna del *top-level await*, ES2022, fuera del alcance de este apunte). Y una función `async` **siempre devuelve una Promise** — aunque su `return` interno sea un valor común, queda envuelto automáticamente en una Promise resuelta con ese valor. Esto vale también para los errores: si dentro de una función `async` se hace `throw` de forma sincrónica (sin usar Promises para nada), el resultado es una Promise **rechazada** con ese error, no una excepción que rompa el programa ahí mismo — es lo que permite que un `try`/`catch` alrededor de un `await` también atrape errores lanzados de forma "normal" dentro de la misma función.

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
<div class="info-card" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d">
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
    return await fetchOrders(user.id)
  } catch (error) {
    if (error.status === 404) console.error('Usuario no encontrado')
    else console.error('Error inesperado:', error.message)
    return []
  }
}
```

Con `async`/`await`, el manejo de errores vuelve a ser el `try`/`catch` de siempre: si cualquier `await` de adentro rechaza, la ejecución salta directo al `catch` — el mismo comportamiento que `.catch()` en una cadena de Promises, pero con la sintaxis sincrónica ya conocida de Java/C. Para diferenciar tipos de error alcanza con inspeccionar el objeto `error` adentro del mismo `catch` (por `instanceof`, por un código de estado, etc.), como con `error.status === 404` de arriba.

### Un `try`/`catch` sincrónico no alcanza

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

El `throw` de adentro del callback de `setTimeout` ocurre **mucho después** de que el `try`/`catch` que lo rodea ya terminó de ejecutarse (recordar el event loop: el callback corre recién cuando el stack está vacío, en otra "vuelta" completamente distinta). El error termina como una excepción no capturada, no dentro del `catch`.

Con Promises/`async`-`await` esto **no pasa**: el `.catch()` (o el `try`/`catch` de una función `async`) sí está diseñado para atrapar errores que ocurren "más adelante en el tiempo" — es una de las razones de fondo por las que Promises reemplazaron a los callbacks para este tipo de flujo.

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
| Microtask | Cola de `.then`/`.catch`/`await` — prioridad alta |
| Macrotask | Cola de `setTimeout`/callbacks — prioridad baja |

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

## Referencias y recursos

<div class="card-grid card-grid-2">
<div>

**Asincronismo y Event Loop**

- [MDN — Asynchronous JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript/Guide/Asynchronous)
- [MDN — Concurrency model and event loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model)
- [javascript.info — Event loop: microtasks and macrotasks](https://javascript.info/event-loop)
- [MDN — In depth: Microtasks](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide/In_depth)
- ["What the heck is the event loop anyway?"](https://www.youtube.com/watch?v=8aGhZQkoFbQ) — Philip Roberts, JSConf
- ["In The Loop"](https://www.youtube.com/watch?v=cCOL7MC4Pl0) — Jake Archibald, JSConf.Asia
- [Diagrama del Event Loop](https://commons.wikimedia.org/wiki/File:JavaScript_Event_Loop.png) — Byteslovesbits, Wikimedia Commons (CC BY-SA 4.0)

</div>
<div>

**Callbacks, Promises y `async`/`await`**

- [MDN — Callback function](https://developer.mozilla.org/en-US/docs/Glossary/Callback_function)
- [MDN — Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
- [MDN — Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [MDN — async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)
- [javascript.info — Async](https://javascript.info/async)
- ["You Don't Know JS: Async & Performance"](https://github.com/getify/You-Dont-Know-JS/tree/1st-ed/async%20%26%20performance) — Kyle Simpson, libro gratuito
- [nationalize.io](https://nationalize.io/) y [restcountries.com](https://restcountries.com/) — las APIs públicas usadas en los ejemplos de este apunte

</div>
</div>

## Cierre

El objetivo de este tema es tener resuelto el modelo mental completo de la asincronía en JavaScript — call stack, Web APIs, colas de tareas (macro y microtasks), event loop — y las tres formas de expresarla en código: callbacks, Promises y `async`/`await`. De acá en adelante, en el resto de la unidad (TypeScript, React, Node + Express, MongoDB), el código asincrónico va a aparecer todo el tiempo — cada pedido HTTP, cada consulta a una base de datos — y se asume este apunte como base, igual que la sintaxis moderna de JS Contemporáneo.
