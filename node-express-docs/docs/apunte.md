# Node + Express

## De React al servidor

Todo el módulo de React asumió que, en algún lugar, existía un servidor respondiendo `/products`. Ese servidor no aparece solo — hay que construirlo. Este módulo arma, del lado del servidor, exactamente lo que el `fetch`/Axios de React esperaba encontrar del otro lado: rutas, JSON, y — más adelante — la autenticación real detrás del token que ya sabían guardar y reenviar.

```tsx
// React, módulo anterior: esto ya lo escribieron
const res = await api.get<Product[]>('/products')
```

```ts
// Este módulo: qué corre del otro lado de esa URL
app.get('/products', (req, res) => {
  res.json(products)
})
```

Es el mismo salto que separa "consumir una API" de "ser una API" — hasta ahora, el código vivía en la computadora de quien lo mira (el navegador); de acá en más, vive en una máquina que nadie ve, atendiendo pedidos de quien sea que se conecte. Ese cambio de rol trae consigo preguntas nuevas que el frontend no tenía que responder: ¿quién puede pedir qué?, ¿qué pasa si dos personas piden lo mismo al mismo tiempo?, ¿cómo se entera el servidor de que un pedido viene de alguien autenticado?

## ¿Qué es Node.js?

Node.js es un **entorno de ejecución** (*runtime*) de JavaScript fuera del navegador — el mismo lenguaje, corriendo en una terminal o un servidor. La distinción entre "lenguaje" y "entorno de ejecución" es la primera idea clave del módulo: JavaScript como lenguaje no sabe nada de archivos, redes o procesos — esas capacidades las agrega el entorno donde corre. El navegador agrega `document`, `window`, `fetch`; Node agrega `fs`, `process`, `http`. Mismo lenguaje, superpoderes distintos según dónde se ejecute.

Por debajo, Node combina dos piezas de C++ que no escribió Node mismo:

- **V8** — el motor de JavaScript de Google Chrome (el mismo que corre el JS de cualquier pestaña abierta). Compila JS a código máquina en tiempo de ejecución (*JIT*, *just-in-time compilation*) — eso es lo que lo hace rápido, no que Node lo interprete línea por línea.
- **libuv** — una librería en C que le da a Node su modelo de E/S asíncrona no bloqueante y el *event loop* — el mismo mecanismo visto en Asincronismo, pero implementado acá a nivel de sistema operativo (usa hilos del sistema operativo por debajo para las operaciones que el propio SO no puede hacer de forma asíncrona, como cierto acceso a disco).

Node no "inventó" el event loop — lo que hizo fue tomar V8 (pensado para correr en una pestaña) y darle, con libuv, acceso a lo que hace falta para ser un servidor: sockets, el sistema de archivos, procesos.

### Historia breve

- **2009** — Ryan Dahl presenta Node.js en JSConf EU, combinando V8 con libuv para resolver un problema puntual: los servidores de la época (Apache, entre otros) manejaban cada conexión con su propio hilo del sistema operativo, un modelo caro en memoria con miles de conexiones simultáneas.
- **2010** — nace **npm**, escrito por Isaac Schlueter, distribuido junto con Node desde entonces — hoy el registro de paquetes más grande del mundo (ya lo vienen usando desde JS Contemporáneo).
- **2014** — un grupo de colaboradores bifurca el proyecto como **io.js**, en desacuerdo con el ritmo de lanzamientos y la gobernanza del proyecto bajo la empresa Joyent.
- **2015** — ambos proyectos se reunifican bajo la recién creada **Node.js Foundation**, con un modelo de gobernanza abierto (no controlado por una sola empresa).
- **2019** — la Node.js Foundation se fusiona con la JS Foundation para formar la **OpenJS Foundation**, que hoy aloja a Node.js junto con otros proyectos del ecosistema (entre ellos, Express).
- **2018 / 2022** — el mismo Ryan Dahl, en una charla titulada *"10 Things I Regret About Node.js"*, presenta **Deno**: un runtime nuevo que corrige decisiones de diseño de Node (seguridad por defecto, TypeScript nativo). Más tarde, **Bun** (2022, de Jarred Sumner) ataca el mismo espacio con otro motor (JavaScriptCore, no V8) y foco en velocidad de arranque.
- **Hoy** — Node sigue siendo el estándar de facto para backends en JavaScript/TypeScript. Deno y Bun compiten en nichos puntuales (seguridad, velocidad de arranque, tooling todo-en-uno) sin haber desplazado a Node como opción por defecto — el ecosistema de paquetes y la base instalada de Node siguen siendo, por lejos, las más grandes.

<div class="overflow-x-auto">

| | Node.js | Deno | Bun |
|---|---|---|---|
| Creado | 2009 (Ryan Dahl) | 2018 (Ryan Dahl) | 2022 (Jarred Sumner) |
| Motor JS | V8 | V8 | JavaScriptCore |
| TypeScript nativo | No (necesita `tsx`/`ts-node`) | Sí | Sí |
| Gestor de paquetes | npm (externo) | Módulos por URL / npm | Incluido, muy rápido |
| Ecosistema/paquetes | Enorme (el de referencia) | Compatible con npm (parcial) | Compatible con npm (mayoría) |

</div>

El mismo lenguaje que hasta ahora solo corría en el navegador, corriendo del otro lado de la conexión — con Node como la opción todavía dominante para aprenderlo primero.

### Por qué Node sirve para un servidor

Un servidor atiende **muchas** requests al mismo tiempo — la mayoría de ese tiempo, esperando algo (una consulta a una base de datos, un archivo, otra API). El mismo modelo de Asincronismo, ahora en el contexto de un servidor, no de un navegador.

```js
// Bloqueante: mientras se lee el archivo, NADA MÁS puede correr
const data = fs.readFileSync('productos.json')
console.log('Esto espera a que termine la línea de arriba')

// No bloqueante: Node sigue atendiendo otras requests mientras se lee
fs.readFile('productos.json', (err, data) => {
  console.log('Esto corre cuando el archivo termina de leerse')
})
console.log('Esto se ejecuta ANTES, sin esperar')
```

- Node corre en **un solo hilo** de JavaScript, pero nunca se queda bloqueado esperando una operación de E/S (archivo, red, base de datos) — la delega (a libuv, que sí puede usar varios hilos del sistema operativo por debajo) y sigue atendiendo otras requests mientras tanto.
- Cuando esa operación termina, su callback (o su `Promise`) se resuelve en el **event loop** — la misma cola de tareas ya vista en el navegador, corriendo acá del lado del servidor.
- Por eso un servidor Node puede atender miles de conexiones simultáneas con relativamente pocos recursos, siempre que el código no bloquee ese único hilo con cómputo pesado y sincrónico (un `for` gigante, un hash costoso hecho de forma sincrónica) — ahí sí, todas las demás requests quedan esperando.

Node no es "más rápido" que otros lenguajes en cómputo puro (Python, Java o Go pueden ganarle en tareas de CPU intensiva) — es eficiente específicamente en **I/O concurrente**, que es la mayor parte del trabajo real de una API típica: la mayoría de las requests pasan más tiempo esperando una base de datos que haciendo cuentas.

<div class="practice-box">
<p class="practice-label">Para pensar</p>

Si Node corre en un solo hilo, ¿qué pasaría si un endpoint hiciera un cálculo sincrónico pesado (por ejemplo, procesar una imagen grande a mano, sin liberar el hilo)? ¿A quién afectaría, además de a quien hizo esa request?
</div>

## Primeros pasos

### Iniciar un proyecto Node

```bash
node --version   # confirmar que está instalado
npm --version

mkdir products-api && cd products-api
npm init -y       # genera package.json con valores por defecto
```

`npm init -y` ya lo vieron en JS Contemporáneo — nada nuevo en el comando en sí. La diferencia está en lo que se instala **adentro** de este `package.json`: hasta ahora, herramientas de build para el navegador (Vite, Slidev); de acá en más, un servidor pensado para correr sin interfaz gráfica.

### Un servidor con el módulo nativo `http`

```ts
import http from 'http'

const server = http.createServer((req, res) => {
  if (req.url === '/products' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify([{ name: 'Mouse', price: 18000 }]))
    return
  }
  res.writeHead(404)
  res.end('Not found')
})

server.listen(4000, () => console.log('Server on port 4000'))
```

`http` viene incluido en Node, sin instalar nada — es, literalmente, lo que hay debajo de cualquier framework de este módulo. `createServer` recibe una función que corre **una vez por cada request** que llega al puerto (acá, `4000`); dentro, hay que comparar `url` y `method` a mano para decidir qué responder.

Con una sola ruta, esto ya es tedioso: armar los headers a mano, convertir a JSON, comparar strings para rutear. Con veinte rutas, parámetros dinámicos (`/products/42`) y necesidad de leer el body de un `POST`, se vuelve inmanejable — ese es, exactamente, el problema que resuelve un framework.

### ¿Qué es Express?

- Un **framework minimalista** (*"unopinionated"*, sin imponer una estructura de carpetas obligatoria) construido sobre el módulo `http` — no lo reemplaza, lo simplifica.
- Lo creó **TJ Holowaychuk** en 2010, inspirado en **Sinatra** (un framework minimalista de Ruby) — la misma idea de "rutas + funciones", sin la maquinaria pesada de un framework completo.
- Resuelve exactamente lo que el ejemplo anterior tuvo que hacer a mano: rutear por `url`/`method`, parsear el body, encadenar lógica con middleware.
- Hoy lo mantiene la **OpenJS Foundation** (la misma que aloja a Node.js) — sigue siendo el estándar de facto para APIs en Node desde hace más de una década.

<div class="overflow-x-auto">

| | Express | Fastify | Koa | Hono | NestJS |
|---|---|---|---|---|---|
| Lanzamiento | 2010 | 2016 | 2013 (mismo autor que Express) | 2021 | 2017 |
| Estilo | Minimalista, callbacks/middleware | Minimalista, foco en performance | Minimalista, `async`/`await` desde el diseño | Minimalista, multi-runtime (Node, Deno, Bun, edge) | Framework completo (como Angular, con decoradores) |
| Curva de entrada | Baja | Baja-media | Baja | Baja | Alta |
| Cuándo conviene | Estándar de facto, mayoría de tutoriales y proyectos | Cuando el throughput es crítico | Base minimalista para armar algo propio | Deploys en el borde (*edge*) o multi-runtime | Proyectos grandes, en equipo, con arquitectura estricta |

</div>

Express sigue siendo la puerta de entrada más común al desarrollo backend en JavaScript — no porque sea técnicamente superior a las alternativas, sino porque su simplicidad lo vuelve el punto de partida más didáctico: se ve, en pocas líneas, exactamente qué hace cada pieza.

### Instalar Express

```bash
npm install express
npm install -D typescript @types/express @types/node tsx
```

```ts
// index.ts
import express, { Request, Response } from 'express'

const app = express()

app.get('/', (req: Request, res: Response) => {
  res.send('Hola, Programación III')
})

app.listen(4000, () => console.log('Servidor en http://localhost:4000'))
```

`express()` crea la aplicación — el objeto sobre el que se registran rutas y middleware durante todo el módulo. `Request`/`Response` son los tipos que trae `@types/express` (Express en sí está escrito en JavaScript puro; `@types/express` es una definición de tipos escrita por la comunidad, distribuida por separado, siguiendo el mismo patrón `@types/*` ya visto en TypeScript). Todo el código de este módulo es TypeScript real desde esta primera línea, no JS con nombres en inglés.

`tsx` corre el archivo `.ts` directamente, compilándolo al vuelo en memoria — similar a `ts-node`, ya visto en TypeScript, pero más rápido porque usa `esbuild` por debajo en vez del compilador oficial de TypeScript. Para producción, lo normal es compilar antes con `tsc` y correr el JavaScript resultante — `tsx` (como `ts-node`) es una herramienta pensada para desarrollo, no para el servidor final.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Armá un proyecto con `npm init -y`, instalá Express y TypeScript, y escribí un `index.ts` con dos rutas `GET`: `/` que devuelva un saludo con `res.send`, y `/salud` que devuelva `res.json({ status: 'ok' })`. Corré el servidor con `npx tsx index.ts` y confirmá ambas rutas con el navegador o con `curl`.
</div>

## Rutas y verbos HTTP

### El protocolo, por debajo

Cada request/response entre React y esta API viaja como texto plano sobre **HTTP** (*HyperText Transfer Protocol*) — el mismo protocolo que trae cualquier página web al navegador. Un request HTTP tiene, en esencia, tres partes: una línea con el método y la URL (`GET /products HTTP/1.1`), un conjunto de **headers** (metadatos: `Content-Type`, `Authorization`, `Accept`...) y, opcionalmente, un **body** con datos. La respuesta tiene la misma forma: una línea de estado (`HTTP/1.1 200 OK`), headers, y un body opcional.

La versión más usada durante años fue **HTTP/1.1** (1997); **HTTP/2** (2015) y **HTTP/3** (sobre el protocolo QUIC, 2022) la fueron reemplazando de a poco, enfocados en rendimiento (múltiples requests por una sola conexión, compresión de headers) — son detalles de transporte que Express maneja por debajo, sin cambiar en nada el código que se escribe en este módulo.

### El vocabulario de una API REST

<div class="overflow-x-auto">

| Verbo | Para qué | Ejemplo | ¿Idempotente? |
|---|---|---|---|
| **GET** | Leer, sin efectos secundarios | `GET /products` | Sí |
| **POST** | Crear un recurso nuevo | `POST /products` | No |
| **PUT** | Reemplazar un recurso completo | `PUT /products/1` | Sí |
| **PATCH** | Modificar parcialmente | `PATCH /products/1` | No (en general) |
| **DELETE** | Borrar | `DELETE /products/1` | Sí |

</div>

**Idempotente** significa que repetir la misma operación varias veces produce el mismo resultado que hacerla una sola vez — `DELETE /products/1` repetido cinco veces deja el mismo estado final que hacerlo una vez (el producto no existe); `POST /products` repetido cinco veces crea cinco productos distintos. Es una propiedad útil para decidir, por ejemplo, si es seguro reintentar una request automáticamente ante una falla de red.

**REST** (*REpresentational State Transfer*) es el nombre que Roy Fielding le dio, en su tesis doctoral del año 2000, a un conjunto de convenciones para diseñar APIs sobre HTTP: usar el verbo correcto según la acción, y la URL para identificar **qué** recurso (no la acción — `/products/1`, no `/getProduct?id=1`). No es un protocolo ni un estándar con una autoridad que lo certifique — es una convención ampliamente adoptada, y "API REST" en la práctica suele significar "API HTTP que sigue más o menos estas convenciones", con distintos grados de adhesión estricta. Axios, en el módulo anterior, ya venía usando esta misma convención (`api.get`, y lo mismo existe como `api.post`/`api.put`/`api.delete`).

### Status codes más usados

<div class="card-grid card-grid-3">
<div class="info-card tone-green" style="background:var(--vp-c-green-soft);border-color:#86efac"><h4>200 OK</h4>Todo salió bien</div>
<div class="info-card tone-green" style="background:var(--vp-c-green-soft);border-color:#86efac"><h4>201 Created</h4>Se creó un recurso</div>
<div class="info-card tone-green" style="background:var(--vp-c-green-soft);border-color:#86efac"><h4>204 No Content</h4>OK, sin nada que devolver</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d"><h4>400 Bad Request</h4>El request está mal formado</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d"><h4>401 Unauthorized</h4>Falta autenticarse</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d"><h4>403 Forbidden</h4>Autenticado, pero sin permiso</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d"><h4>404 Not Found</h4>El recurso no existe</div>
<div class="info-card tone-red" style="background:var(--vp-c-red-soft);border-color:#fca5a5"><h4>500 Server Error</h4>Algo falló del lado del servidor</div>
</div>

Los códigos de estado se agrupan por su primer dígito: **1xx** (informativos, poco usados directamente), **2xx** (éxito), **3xx** (redirecciones), **4xx** (error del cliente — el pedido está mal), **5xx** (error del servidor — el pedido estaba bien, algo falló procesándolo). Distinguir 4xx de 5xx en el propio código es una señal útil para quien consume la API: un 4xx dice "revisá lo que mandaste", un 5xx dice "el problema es nuestro". La lista completa (más de 60 códigos) está documentada en el [listado de status codes de MDN](https://developer.mozilla.org/es/docs/Web/HTTP/Status) — estos ocho cubren el 90% de los casos reales de una API típica.

### `req` y `res`: parámetros y query params

```ts
app.get('/products/:id', (req: Request, res: Response) => {
  const id = req.params.id              // parámetro de ruta
  const category = req.query.category   // query param, ?category=...
  res.status(200).json({ id, category })
})
```

```
GET /products/42?category=electronics

→ 200 OK
{ "id": "42", "category": "electronics" }
```

Mismo vocabulario que `useParams`/`useSearchParams` de React Router, del otro lado de la conexión: ahí, el navegador **leía** la URL; acá, Express la **recibe** — `req.params` para lo obligatorio (`:id`, parte de la ruta), `req.query` para lo opcional (`?category=...`, después del `?`). Nota importante: ambos llegan siempre como **string**, aunque parezcan números — `req.params.id` es `"42"`, no `42`, y hay que convertirlo explícitamente (`Number(req.params.id)`) antes de compararlo con un número.

`req` también trae `req.headers` (los metadatos del pedido — se usa más adelante para leer `Authorization`) y `req.body` (el contenido, una vez configurado el middleware correspondiente). `res` no se limita a `.json()`: `res.send()` responde texto o HTML crudo, `res.status(code)` fija el status antes de encadenar `.json()`/`.send()`, y `res.set(header, valor)` permite agregar headers propios a la respuesta.

## Middleware

Un middleware es una función que se ubica en el medio del flujo de una request y puede inspeccionarla, modificarla, o cortarla — mismo concepto ya visto en React con `RequireAuth`, del lado del cliente. En Express es, literalmente, el mecanismo central sobre el que está construido todo el framework: hasta las propias rutas son, por debajo, una forma particular de middleware.

```ts
import { Request, Response, NextFunction } from 'express'

function logger(req: Request, res: Response, next: NextFunction) {
  console.log(`${req.method} ${req.url}`)
  next()   // sin next(), la request se queda colgada — nunca llega a su ruta
}

app.use(logger)   // corre en TODAS las rutas, en el orden en que se declaran
```

`app.use` registra un middleware **global**. El orden importa, y es una de las fuentes de bugs más comunes al empezar con Express: cada request pasa por los middlewares de arriba hacia abajo, en el mismo orden en que se escribieron en el código — un middleware de autenticación registrado *después* de las rutas que debería proteger, simplemente no las protege.

### Un ejemplo más útil: datos de usuario

```ts
declare global {
  namespace Express {
    interface Request { user?: any }   // se afina más en Autenticación
  }
}

function attachUser(req: Request, res: Response, next: NextFunction) {
  const userId = req.headers['x-user-id']
  if (!userId) return res.status(401).json({ error: 'Falta identificarse' })
  req.user = { userId }
  next()
}
```

Exige un dato antes de dejar pasar la request, y lo deja disponible en `req.user` para las rutas de abajo. `declare global` le enseña a TypeScript que el tipo `Request` de Express ahora tiene una propiedad `user` — es una técnica llamada **module augmentation**, ya vista de forma más general en TypeScript: sin esto, asignar `req.user = ...` sería un error de tipos, porque el `Request` original de `@types/express` no contempla esa propiedad. Es una versión simplificada del middleware de autenticación real (que verifica un token, no un header a ojo) — se arma con todo detalle en la sección de Autenticación.

### `express.json()`: el middleware que faltaba

```ts
app.use(express.json())   // parsea el body si es JSON, antes de llegar a la ruta

app.post('/products', (req: Request, res: Response) => {
  console.log(req.body)   // ya viene parseado, como un objeto
  res.status(201).json(req.body)
})
```

Sin este middleware, `req.body` sería `undefined` — Express no parsea el body por defecto, hay que pedírselo explícitamente. Antes de la versión 4.16 de Express (2017) hacía falta instalar por separado una librería aparte (`body-parser`); hoy viene incluido en el propio paquete de Express, sin instalar nada extra. `express.json()` acepta, opcionalmente, un límite de tamaño (`express.json({ limit: '1mb' })`) — una protección razonable contra bodies enormes enviados a propósito para saturar el servidor.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Escribí un middleware `requireApiKey` que lea un header `x-api-key` y corte la request con `403` si no coincide con un valor fijo (por ejemplo, `'secreta123'`). Registralo con `app.use` y confirmá, con `curl`, que una request sin el header (o con el valor equivocado) recibe `403`, y una con el valor correcto sigue de largo.
</div>

## CRUD en memoria

### Leer

```ts
interface Product {
  id: number
  name: string
  price: number
}
const products: Product[] = [
  { id: 1, name: 'Mouse', price: 18000 },
  { id: 2, name: 'Teclado', price: 25000 },
]
app.get('/products', (req: Request, res: Response) => {
  res.json(products)
})
app.get('/products/:id', (req: Request, res: Response) => {
  const product = products.find((p) => p.id === Number(req.params.id))
  if (!product) return res.status(404).json({ error: 'No encontrado' })
  res.json(product)
})
```

Mismo `interface Product` de siempre, con un `id` nuevo: hace falta un identificador estable para pedir, modificar o borrar **uno solo**. Por ahora, un array en memoria — vive mientras el proceso de Node esté corriendo, y se pierde por completo con cada reinicio. MongoDB, en el próximo tema, lo reemplaza por persistencia real, generando además el `id` automáticamente.

### Crear

```ts
app.post('/products', (req: Request, res: Response) => {
  const newProduct: Product = { id: Date.now(), ...req.body }
  products.push(newProduct)
  res.status(201).json(newProduct)
})
```

`Date.now()` como `id` es una solución de práctica, no de producción: dos requests en el mismo milisegundo colisionarían (poco probable a mano, pero perfectamente posible bajo carga real) — otra razón más para que una base de datos real los genere, como se ve en el próximo tema. `201 Created` (no `200`) es el status correcto para una creación exitosa — una convención chica, pero parte de "usar bien" el protocolo en vez de responder siempre `200`.

### Modificar y borrar

```ts
app.put('/products/:id', (req: Request, res: Response) => {
  const index = products.findIndex((p) => p.id === Number(req.params.id))
  if (index === -1) return res.status(404).json({ error: 'No encontrado' })
  products[index] = { ...products[index], ...req.body }
  res.json(products[index])
})
app.delete('/products/:id', (req: Request, res: Response) => {
  const index = products.findIndex((p) => p.id === Number(req.params.id))
  if (index === -1) return res.status(404).json({ error: 'No encontrado' })
  products.splice(index, 1)
  res.status(204).end()
})
```

Mismo patrón en las dos: buscar el índice, chequear que exista, y recién ahí aplicar el cambio. `PUT` combina lo existente con lo nuevo (`{ ...products[index], ...req.body }`) — en un sentido estricto, `PUT` debería reemplazar el recurso *completo*, y `PATCH` sería el verbo correcto para una modificación parcial; en la práctica, muchas APIs (incluida esta) usan `PUT` para ambos casos por simplicidad, algo común pero no puramente "RESTful". `DELETE` responde `204` — vacío, porque no hay nada que devolver, y por convención un `204` nunca lleva body.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Sobre el array `products`, agregá una ruta `PATCH /products/:id/stock` que reciba `{ delta: number }` en el body y sume ese valor al `stock` del producto (rechazando con `400` si el resultado quedaría negativo). No hace falta tocar `PUT`/`DELETE` — es una ruta nueva, con su propia validación puntual.
</div>

### Organizar rutas con `express.Router()`

```ts
// routes/products.ts
import { Router } from 'express'
import { getAllProducts, getProductById, createProduct } from '../controllers/products'

const router = Router()

router.get('/', getAllProducts)
router.get('/:id', getProductById)
router.post('/', createProduct)

export default router
```

```ts
// index.ts
import productsRouter from './routes/products'

app.use('/products', productsRouter)   // todas las rutas de arriba, bajo /products
```

Un solo archivo con todas las rutas no escala — `Router()` agrupa las de un mismo recurso en su propio archivo, montado bajo un prefijo común con `app.use('/products', ...)`. Dentro del router, las rutas se declaran relativas a ese prefijo (`'/'`, `'/:id'`) — Express arma la URL completa por composición. Misma idea de organización que `routes/`/`components/` en React: separar por responsabilidad, no tener todo en un archivo gigante.

### Los controllers, en código

```ts
// controllers/products.ts
import { Request, Response } from 'express'
import { products } from '../data/products'

export function getAllProducts(req: Request, res: Response) {
  res.json(products)
}
export function getProductById(req: Request, res: Response) {
  const product = products.find((p) => p.id === Number(req.params.id))
  if (!product) return res.status(404).json({ error: 'No encontrado' })
  res.json(product)
}
```

Exactamente el mismo código de las secciones de CRUD — movido a su propio archivo, exportado función por función (`createProduct` sigue el mismo patrón, movido tal cual). `router.get('/', getAllProducts)` ya no define la lógica ahí mismo, solo la conecta con su URL. Esta separación — rutas por un lado (qué URL/verbo dispara qué), controllers por otro (qué hace esa lógica) — es una versión liviana del patrón **MVC** (*Model-View-Controller*), sin la parte de "View" porque una API no renderiza HTML: solo devuelve datos.

### Manejo de errores centralizado

```ts
app.get('/products/:id', (req: Request, res: Response, next: NextFunction) => {
  try {
    const product = products.find((p) => p.id === Number(req.params.id))
    if (!product) throw new Error('No encontrado')
    res.json(product)
  } catch (err) {
    next(err)   // delega el error al middleware de abajo
  }
})
// al final de todas las rutas:
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err)
  res.status(500).json({ error: err.message })
})
```

Un middleware con **cuatro** parámetros (incluido `err`) es un manejador de errores para Express — se registra al final de todas las rutas, y Express lo reconoce específicamente por tener cuatro parámetros (no por su nombre ni su posición relativa a otra cosa). Captura lo que llegue por `next(err)`, sin repetir `try`/`catch` en cada ruta.

`console.error` alcanza para practicar; en un proyecto real conviene una librería de logging dedicada en vez de `console.log`/`console.error` sueltos — dan niveles (`info`, `warn`, `error`), timestamps, y la posibilidad de mandar la salida a un archivo o a un servicio externo, no solo a la terminal. Dos opciones habituales en Node: **Winston** (más configurable, con "transports" para distintos destinos) y **Pino** (más liviano y rápido, pensado para alto volumen de logs). Ninguna reemplaza a `console.error` conceptualmente — lo hacen más manejable en producción.

## CORS

### Por qué el navegador bloquea la request

React corre en `http://localhost:5173`; la API, en `http://localhost:4000` — **orígenes distintos** (un origen se define por protocolo + dominio + puerto; basta con que uno de los tres cambie). Por seguridad, el navegador bloquea por defecto cualquier request de un origen a otro — es la política de mismo origen (*same-origin policy*), pensada para que una página maliciosa no pueda, silenciosamente, hacer pedidos en nombre de quien la está mirando hacia otro sitio donde esa persona tiene una sesión abierta.

```
Access to fetch at 'http://localhost:4000/products' from origin
'http://localhost:5173' has been blocked by CORS policy
```

Este es, probablemente, el primer error real que se ve al conectar el React del módulo anterior con una API propia — no es un bug del código, es el navegador cumpliendo su trabajo. Lo resuelve el **servidor**, no el cliente: es la API la que tiene que decir explícitamente, en un header de la respuesta, "acepto requests de este origen".

Para ciertos requests (métodos distintos de `GET`/`HEAD`/`POST`, o con headers no estándar como `Authorization`), el navegador ni siquiera llega a mandar el pedido real primero: manda un pedido `OPTIONS` de "sondeo" (*preflight*) preguntando si el origen y el método están permitidos, y solo si la respuesta lo autoriza, manda el pedido real. Todo esto ocurre automáticamente en el navegador, sin que el código de React tenga que hacer nada — pero explica por qué, mirando la pestaña de Red del navegador, a veces aparece una request `OPTIONS` extra antes de un `POST` o `PUT`.

### Resolverlo con `cors`

```bash
npm install cors
npm install -D @types/cors
```

```ts
import cors from 'cors'

app.use(cors())   // por defecto, permite cualquier origen — cómodo en desarrollo

app.use(cors({ origin: 'https://mi-tienda.com' }))   // en producción, restringido
```

`cors()` agrega los headers (`Access-Control-Allow-Origin`, entre otros) que le dicen al navegador "este origen está permitido", y responde automáticamente a los pedidos `OPTIONS` de preflight. Sin argumentos, permite cualquier origen (`*`) — razonable mientras se desarrolla, pero en producción conviene restringirlo al dominio real del frontend: dejar `cors()` abierto de par en par en un servidor público es, en la práctica, renunciar a la protección que da la same-origin policy sin necesidad real de hacerlo. El objeto de configuración también acepta `methods` (qué verbos permitir) y `credentials` (si se aceptan cookies entre orígenes) — documentado en el [repositorio de `cors` en npm](https://www.npmjs.com/package/cors).

## Configuración del proyecto

### Variables de entorno con `dotenv`

Mismo problema ya visto con `.env` en Vite (URLs distintas por ambiente, secretos fuera del código) — Node no lo resuelve nativamente como Vite: hace falta una librería. La idea de fondo — separar la **configuración** (qué puerto, qué secretos, a qué base conectarse) del **código** — es uno de los principios de la metodología [**12-Factor App**](https://12factor.net/es/config), un conjunto de buenas prácticas para apps de servidor escritas por ingenieros de Heroku en 2011, todavía citado como referencia hoy.

```bash
npm install dotenv
```

```bash
# .env.development
PORT=4000
JWT_SECRET=un-secreto-de-desarrollo

# .env.production
PORT=8080
JWT_SECRET=un-secreto-mucho-mas-largo-y-real
```

```ts
// index.ts — primera línea del archivo
import dotenv from 'dotenv'
dotenv.config({ path: `.env.${process.env.NODE_ENV || 'development'}` })

const port = Number(process.env.PORT) || 4000
```

A diferencia de Vite, `dotenv` **no** elige el archivo solo según el ambiente — hay que decírselo explícitamente con `path`, comparando contra `process.env.NODE_ENV` (una variable que, por convención, muchas herramientas del ecosistema Node leen para saber si están en desarrollo o producción, pero que hay que fijar a mano — Node no la define sola). `process.env.PORT` siempre es un **string** (o `undefined` si no está definida); convertir a número a mano cuando haga falta, como acá con `Number(...)`. Los archivos `.env*` nunca deberían subirse a un repositorio git — solo un `.env.example` sin valores reales, a modo de plantilla.

### `tsconfig.json` para un proyecto Node

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
```

Mismas opciones ya vistas en TypeScript, con una diferencia clave: `module`/`moduleResolution` en `"NodeNext"` en vez de `"ESNext"`/`"bundler"` — acá no hay un bundler (Vite) resolviendo los imports antes de que el código llegue al navegador; es Node ejecutando los archivos directamente, así que TypeScript necesita generar imports compatibles con cómo Node resuelve módulos de verdad (incluida la extensión de archivo en ciertos casos). `outDir`/`rootDir` separan el código fuente (`src/`) del compilado (`dist/`) — lo que se sube a producción o se ejecuta con `node` es el contenido de `dist/`, nunca los `.ts` originales directamente.

## Autenticación

### Por qué hace falta más que "usuario y contraseña"

Antes de los tokens, el modelo más común era **basado en sesión**: el servidor, tras un login, guarda en su propia memoria (o en una base) quién está logueado, y le entrega al navegador un identificador de sesión en una cookie — cada request posterior manda esa cookie, y el servidor busca la sesión correspondiente. Funciona, pero exige que el servidor recuerde el estado de cada sesión activa (*stateful*).

El enfoque con **JWT** (visto ya, del lado del cliente, en React) es **stateless**: el servidor no guarda nada — toda la información necesaria (quién es, qué rol tiene, hasta cuándo es válido) viaja dentro del propio token, firmado para que nadie pueda alterarlo sin ser detectado. Esto simplifica escalar horizontalmente (cualquier instancia del servidor puede validar el token sin consultar una base de sesiones compartida), al costo de no poder "olvidar" un token antes de su expiración sin mecanismos adicionales (como una lista de tokens revocados).

### El backend es el responsable

- **Genera el token** — nadie más puede emitir uno válido, porque nadie más tiene el secreto (o la clave privada) que lo firma.
- **Nunca guarda la contraseña en texto plano** — guarda su hash y compara contra ese hash en cada login. Importante: no es "encriptar y desencriptar" — un hash **no se puede revertir**, solo comparar.
- **Decide cuándo un token es válido** (firma correcta, no vencido) y puede invalidarlo antes de tiempo si hace falta (con mecanismos extra, como una lista negra o un `refresh token` propio).
- El cliente solo hace dos cosas: guardar el token, y reenviarlo — toda la lógica de "quién sos" vive del lado del servidor.

Por eso `bcrypt.compare` (próxima sección) no "desencripta" nada — recalcula el hash del intento y lo compara contra el guardado.

### Anatomía de un JWT

Un JWT (definido formalmente en el [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)) es un string con tres partes separadas por puntos: `header.payload.signature`. Las primeras dos están codificadas en Base64URL — **codificadas, no encriptadas**: cualquiera puede pegar un JWT en [jwt.io](https://jwt.io/) y leer exactamente qué contiene, sin necesitar ninguna clave. Lo único que el secreto protege es la **firma** — sin el secreto correcto, no se puede generar una firma válida para un contenido alterado, así que el servidor puede confiar en que un token con firma válida no fue modificado después de emitirse.

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsInJvbGUiOiJhZG1pbiJ9.4f8a...
└──── header ────┘   └──────── payload ─────────┘  └ signature ┘
{ "alg": "HS256" }   { "userId": 1, "role": "admin" }
```

Justamente porque el payload es legible por cualquiera, nunca debería llevar datos sensibles (una contraseña, un número de tarjeta) — solo lo mínimo necesario para identificar y autorizar (`userId`, `role`, fecha de expiración).

### HS256 vs. RS256: cómo se firma el token

<div class="card-grid card-grid-2">
<div class="info-card"><h4>HS256 (simétrica)</h4>Un solo secreto — la misma clave firma y verifica. Simple y rápido, pero cualquiera con el secreto puede firmar tokens falsos. La que usa este curso.</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d"><h4>RS256 (asimétrica)</h4>Un par de claves: la <strong>privada</strong> firma (solo el backend la tiene), la <strong>pública</strong> verifica — se puede repartir sin dar poder de emitir tokens nuevos.</div>
</div>

RS256 tiene sentido con varios servicios que necesitan **verificar** un token sin poder **crear** uno (microservicios, por ejemplo, donde solo el servicio de autenticación tiene la clave privada, y los demás solo necesitan la pública para confirmar que un token es legítimo). Con un solo backend, como acá, HS256 alcanza y es más simple de manejar — no hay ninguna ventaja de seguridad real en usar RS256 si es el mismo servidor el que firma y el que verifica.

### `bcrypt`: hashear contraseñas

```bash
npm install bcrypt
npm install -D @types/bcrypt
```

```ts
import bcrypt from 'bcrypt'

const hashed = await bcrypt.hash('miContraseña123', 10)
// '$2b$10$N9qo8uLOickgx2ZMRZoMy...'

const isValid = await bcrypt.compare('miContraseña123', hashed)   // true
const isWrong = await bcrypt.compare('otraCosa', hashed)          // false
```

`bcrypt` está basado en el cifrado **Blowfish**, adaptado por Niels Provos y David Mazières en 1999 específicamente para ser lento a propósito — una propiedad deseable acá, a diferencia de casi cualquier otro contexto de programación: cuanto más cara la operación, más caro se vuelve para un atacante probar contraseñas por fuerza bruta. `bcrypt.hash` es de **una sola vía**: no se puede "deshacer" para recuperar la contraseña original, solo comparar (`compare`) si un intento coincide con el hash guardado.

El `10` es el costo del algoritmo (*salt rounds*): cada unidad que sube, duplica el tiempo de cómputo. El hash resultante incluye, embebida en el propio string (`$2b$10$...`), la **sal** (*salt*) — un valor aleatorio generado en cada llamada, que garantiza que dos personas con la misma contraseña obtengan hashes distintos, evitando ataques con tablas precalculadas (*rainbow tables*).

### JWT: firmar un token

Retomando de React: un token certifica "quién sos" sin reenviar la contraseña en cada pedido. Ahora, del lado que lo **genera**.

```bash
npm install jsonwebtoken
npm install -D @types/jsonwebtoken
```

```ts
import jwt from 'jsonwebtoken'

const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET!,
  { expiresIn: '1h' }
)
```

`jwt.sign` codifica el *payload* (acá, `userId`/`role`) y lo firma con un secreto — como se vio antes, cualquiera puede **leer** el contenido de un JWT, pero solo quien tiene el secreto puede generar una firma válida o confirmar que no fue alterado. `expiresIn` agrega automáticamente un campo `exp` al payload; `jwt.verify` (usado en el middleware de autenticación) rechaza un token vencido sin que haga falta chequearlo a mano.

### Los usuarios, en memoria

```ts
interface User {
  id: number
  email: string
  passwordHash: string
  role: 'admin' | 'client'
}

const users: User[] = [
  { id: 1, email: 'ada@mail.com', passwordHash: '$2b$10$N9qo8u...', role: 'admin' },
]
```

Mismo patrón que `products`: un array en memoria, con la contraseña ya hasheada (nunca en texto plano) — el `passwordHash` de ejemplo es un hash real de `bcrypt.hash`, no un string inventado.

### Endpoint de login completo

```ts
app.post('/auth/login', async (req: Request, res: Response) => {
  const { email, password } = req.body
  const user = users.find((u) => u.email === email)
  if (!user) return res.status(401).json({ error: 'Credenciales inválidas' })

  const isValid = await bcrypt.compare(password, user.passwordHash)
  if (!isValid) return res.status(401).json({ error: 'Credenciales inválidas' })

  const token = jwt.sign({ userId: user.id, role: user.role }, process.env.JWT_SECRET!, {
    expiresIn: '1h',
  })
  res.json({ token })
})
```

Mismo mensaje de error para "no existe el email" y "la contraseña no coincide" — a propósito: si fueran distintos, alguien podría usarlo para descubrir qué emails están registrados (un caso concreto de **enumeración de usuarios**, listado como riesgo en la [Authentication Cheat Sheet de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)). En un endpoint de login expuesto públicamente, conviene además limitar cuántos intentos se aceptan por minuto desde una misma IP (*rate limiting*, con una librería como `express-rate-limit`) — sin eso, nada impide probar contraseñas por fuerza bruta a alta velocidad.

### Middleware de autenticación

```ts
function requireAuth(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization
  const token = authHeader?.split(' ')[1]   // "Bearer <token>"
  if (!token) return res.status(401).json({ error: 'No autorizado' })
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET!)
    next()
  } catch {
    res.status(401).json({ error: 'Token inválido o vencido' })
  }
}
app.get('/profile', requireAuth, (req: Request, res: Response) => {
  res.json({ userId: req.user.userId })
})
```

Cierra el círculo con React: el header `Authorization: Bearer <token>` que el interceptor de Axios agregaba en cada request es, literalmente, lo que este middleware lee y verifica acá. `jwt.verify` lanza una excepción si la firma no coincide o si el token venció — de ahí el `try`/`catch`, distinto del resto del módulo, que usa `next(err)` para delegar: acá conviene responder directamente `401`, porque no es un error inesperado del servidor, es el resultado normal de un token inválido.

### Autorización por rol

```ts
function requireAdmin(req: Request, res: Response, next: NextFunction) {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'No tenés permiso' })
  }
  next()
}

app.delete('/products/:id', requireAuth, requireAdmin, deleteProduct)
```

Dos middlewares encadenados en la misma ruta — corren en orden: primero confirma que hay una sesión válida (`requireAuth`), después que esa sesión tiene el rol necesario (`requireAdmin`). `401` ("no sé quién sos") y `403` ("sé quién sos, pero no podés") son errores distintos a propósito — confundirlos es un error común: `403` nunca debería aparecer sin que antes se haya identificado a quien hace el pedido.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Armá `/auth/login` completo (con `bcrypt.compare` + `jwt.sign`) contra un array `users` propio, y una ruta `GET /profile` protegida con `requireAuth`. Probalo con `curl`: primero sin token (esperando `401`), después con el token que devuelve el login.
</div>

## Scaffolding recomendado

```
src/
├── routes/        # products.ts, auth.ts — solo definen qué URL va a dónde
├── controllers/   # getAllProducts, createProduct... la lógica de cada ruta
├── middleware/    # requireAuth, requireAdmin, el logger, el manejador de errores
├── services/      # auth.ts (bcrypt/jwt), email.ts...
├── data/          # products.ts, users.ts — los arrays en memoria, por ahora
├── app.ts         # crea la app, registra middleware y rutas
└── index.ts       # arranca el servidor (app.listen)
```

Mismo criterio de organización ya visto en React (`components/`, `routes/`, `services/`): separar por responsabilidad en vez de por tipo técnico de archivo. Separar `app.ts` (arma la `app`, sin escuchar nada) de `index.ts` (la importa y recién ahí llama a `.listen`) no es solo prolijidad: `supertest`, más adelante, importa `app` directo — si `app.listen` estuviera en el mismo archivo, cada test abriría un puerto real de más, algo lento e innecesario para un test.

## Probar la API

```bash
curl http://localhost:4000/products

curl -X POST http://localhost:4000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Monitor","price":80000}'

curl http://localhost:4000/profile \
  -H "Authorization: Bearer <token>"
```

`curl` alcanza para probar rápido desde la terminal: `-X` fija el verbo (por defecto es `GET`), `-H` agrega un header, `-d` manda un body (y automáticamente cambia el verbo a `POST` si no se especificó otro). Para un flujo más cómodo (guardar requests, ver la respuesta formateada, organizar por colecciones), herramientas como **Postman**, **Insomnia** o **Thunder Client** (extensión de VS Code) hacen lo mismo con una interfaz gráfica — sin necesitar todavía un frontend real corriendo.

## Testing del backend

### Vitest o Jest: dos alternativas

<div class="card-grid card-grid-2">
<div class="info-card"><h4>Jest</h4>El más usado en proyectos ya existentes. Necesita configuración extra para TypeScript/ESM (<code>ts-jest</code> o Babel).</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d"><h4>Vitest</h4>Más nuevo. TypeScript/ESM nativo, sin configuración extra — y es el mismo motor que ya usa Vite en el frontend.</div>
</div>

```bash
npm install -D jest @types/jest ts-jest   # Jest
npm install -D vitest                     # Vitest
```

Mismo `describe`/`it`/`expect` en los dos — migrar de uno a otro es casi gratis, porque ambos comparten una API muy similar (Vitest se diseñó, a propósito, para ser compatible con la de Jest). Ojo con `ts-jest`: al momento de escribir esto, todavía no soporta TypeScript 7 (recién liberado, con un compilador nuevo escrito en Go) — si al instalar `typescript` a secas aparece un error de `ts-jest` sobre la "compiler API", fijar `"typescript": "^6"` en el `package.json` lo resuelve. Vitest no tiene este problema, porque no usa el compilador de TypeScript para transformar el código — usa `esbuild`.

Los mismos tres niveles de testing (unitario, de integración, end-to-end) que se retoman con más profundidad en el próximo módulo aplican acá: un test de una función pura (como el de abajo) es unitario; uno con `supertest` contra `app` es de integración, porque ejercita rutas, middleware y controllers juntos, aunque sin un servidor real escuchando en un puerto.

### Mismo test, en los dos

```ts
// Jest — pricing.test.ts
import { applyDiscount } from './pricing'

test('applyDiscount resta el %', () => {
  expect(applyDiscount(1000, 0.1)).toBe(900)
})
```

```ts
// Vitest — pricing.test.ts
import { it, expect } from 'vitest'
import { applyDiscount } from './pricing'

it('applyDiscount resta el %', () => {
  expect(applyDiscount(1000, 0.1)).toBe(900)
})
```

`applyDiscount`, ya tipada en TypeScript — una función pura es, literalmente, el caso más simple de testear: mismo input, mismo output, sin nada que mockear. Jest expone `test`/`expect` como globales, sin necesidad de importarlos; Vitest los importa explícitamente (o se activan como globales con la opción `globals: true` en su configuración, para escribir tests idénticos a los de Jest sin el import).

### Testear un endpoint con `supertest`

```ts
import request from 'supertest'
import app from '../app'

test('GET /products devuelve el catálogo', async () => {
  const res = await request(app).get('/products')
  expect(res.status).toBe(200)
  expect(res.body).toHaveLength(2)
})
```

`supertest` envuelve la instancia de `app` directamente, sin levantar un puerto real (arma un servidor efímero solo para la duración de ese test) — funciona igual con Jest o con Vitest. Responde `200` porque la ruta no tiene ninguna condición que la haga fallar; el body tiene longitud `2` porque el array en memoria (Mouse, Teclado) arranca así — en un test real conviene **sembrar** un estado conocido antes de cada test (por ejemplo, en un hook `beforeEach`), para no depender de qué haya quedado de una corrida anterior o del orden en que se ejecutan los tests.

### Mockear una dependencia

```ts
// Jest
jest.mock('../services/email')
import { sendWelcomeEmail } from '../services/email'

test('el registro avisa por mail', async () => {
  await registerUser({ email: 'ada@mail.com' })
  expect(sendWelcomeEmail).toHaveBeenCalledWith('ada@mail.com')
})
```

```ts
// Vitest
vi.mock('../services/email')
import { sendWelcomeEmail } from '../services/email'

test('el registro avisa por mail', async () => {
  await registerUser({ email: 'ada@mail.com' })
  expect(sendWelcomeEmail).toHaveBeenCalledWith('ada@mail.com')
})
```

`mock(...)` reemplaza el módulo real por una versión falsa y controlada — acá, para no mandar un email real en cada corrida de tests (y para no depender de que un servicio externo esté disponible solo para poder correr los tests). El `expect` no comprueba que el mail se haya enviado de verdad, solo que la función se **llamó** con los datos correctos: alcanza para testear `registerUser` de forma aislada, sin depender de un servicio externo — la próxima unidad retoma esta misma idea bajo el nombre más general de **test doubles** (mocks, stubs, spies).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Instalá Vitest y `supertest`, y escribí dos tests contra tu propia API: uno que confirme que `GET /products` devuelve `200` y un array, y otro que confirme que `POST /auth/login` con credenciales inválidas devuelve `401`. No hace falta levantar el servidor a mano — `supertest` lo hace por vos, importando `app`.
</div>

## Cheat sheet

<div class="card-grid card-grid-2">
<div>

**Servidor y rutas**

| Forma | Ejemplo |
|---|---|
| Crear la app | `const app = express()` |
| Ruta | `app.get('/products', (req, res) => {...})` |
| Parámetro de ruta | `req.params.id` |
| Query param | `req.query.category` |
| Body (con `express.json()`) | `req.body` |
| Responder JSON | `res.status(200).json(data)` |
| Organizar rutas | `Router()` + `app.use('/prefix', router)` |

</div>
<div>

**Middleware, seguridad y testing**

| Forma | Para qué |
|---|---|
| `app.use(fn)` | Middleware global, en orden |
| `cors()` | Permitir requests de otro origen |
| `(err, req, res, next) => {}` | Manejo de errores centralizado |
| `bcrypt.hash`/`compare` | Hashear y verificar contraseñas |
| `jwt.sign`/`verify` | Emitir y validar tokens |
| `dotenv/config` | Variables de entorno |
| `request(app).get(...)` | Testear un endpoint (`supertest`) |
| `jest.mock`/`vi.mock` | Mockear una dependencia |

</div>
</div>

## Referencias y recursos

- [nodejs.org/es/docs](https://nodejs.org/es/docs) — documentación oficial de Node.js, en español
- [nodejs.org — The Node.js Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) — cómo funciona el event loop, explicado por el propio equipo de Node
- [expressjs.com/es](https://expressjs.com/es/) — documentación oficial de Express, en español
- [developer.mozilla.org — HTTP](https://developer.mozilla.org/es/docs/Web/HTTP) — métodos, status codes y headers, como referencia completa
- [developer.mozilla.org — CORS](https://developer.mozilla.org/es/docs/Web/HTTP/CORS) — la explicación más completa del mecanismo de CORS
- [12factor.net/es](https://12factor.net/es/config) — la metodología detrás de "configuración vía variables de entorno"
- [jwt.io](https://jwt.io/) — documentación y debugger de JSON Web Tokens
- [RFC 7519](https://www.rfc-editor.org/rfc/rfc7519) — la especificación formal de JWT
- [OWASP — Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) — buenas prácticas de autenticación, mantenidas por la comunidad de seguridad
- [npmjs.com/package/bcrypt](https://www.npmjs.com/package/bcrypt) — hashing de contraseñas
- [npmjs.com/package/cors](https://www.npmjs.com/package/cors) · [npmjs.com/package/dotenv](https://www.npmjs.com/package/dotenv)
- [vitest.dev](https://vitest.dev/) · [jestjs.io/es-ES](https://jestjs.io/es-ES/) · [npmjs.com/package/supertest](https://www.npmjs.com/package/supertest)
- [github.com/goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices) — buenas prácticas reales, mantenido por la comunidad

## Cierre

El objetivo de este tema es entender qué hay del otro lado de cada `fetch`/Axios de React: un servidor Express con rutas, middleware, y — cuando hace falta — autenticación real con JWT. El array en memoria usado en todos los ejemplos es, a propósito, la pieza más frágil de todo esto: se pierde con cada reinicio del servidor. El próximo tema (MongoDB) lo reemplaza por persistencia real, sobre exactamente las mismas rutas — nada de lo aprendido acá se descarta, se le agrega una capa debajo.
