---
theme: bricks
title: Programación III - Node + Express
download: true
info: |
  Node + Express - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: node, express, http, middleware, rest, api, cors, jwt, bcrypt, typescript, INSPT, UTN
transition: slide-left
mdc: true
---

# Node + Express

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/nodejs.svg" alt="Node.js" class="h-16 opacity-90" />
<img src="/logos/express.svg" alt="Express" class="h-14 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# De React al servidor

<div class="mt-6 text-xl opacity-90">

Todo el módulo de React asumió que, en algún lugar, existía un servidor respondiendo `/products`.

</div>

<div class="mt-6 text-base opacity-80">

Ese servidor no aparece solo — hay que construirlo. Este módulo arma, del lado del servidor, exactamente lo que el `fetch`/Axios de React esperaba encontrar del otro lado: rutas, JSON, y — más adelante — la autenticación real detrás del token que ya sabían guardar y reenviar.

</div>

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

---
layout: default
---

# ¿Qué es Node.js?

<div class="mt-6 text-xl opacity-90">

Node.js es un **entorno de ejecución** de JavaScript fuera del navegador — el mismo lenguaje, corriendo en una terminal o un servidor.

</div>

<div class="mt-6 text-base opacity-80">

Usa el mismo motor que Chrome (**V8**) para ejecutar JS, pero sin ventana, sin DOM, sin `document` — a cambio, expone APIs propias de un sistema: archivos (`fs`), procesos (`process`), red (`http`).

</div>

<div class="grid grid-cols-2 gap-4 mt-6 text-base">
<div class="p-4 rounded-lg bg-gray-100">En el navegador: <code>document</code>, <code>window</code>, <code>fetch</code>, <code>localStorage</code> — pensado para una página con la que interactúa una persona.</div>
<div class="p-4 rounded-lg bg-gray-100">En Node: <code>fs</code>, <code>process</code>, <code>http</code> — pensado para correr sin interfaz, como un programa de servidor.</div>
</div>

---
layout: default
---

# Historia breve

- **2009** — Ryan Dahl crea Node.js: combina el motor V8 con `libuv`, una librería en C para E/S asíncrona no bloqueante.
- **2010** — nace **npm** junto con Node — hoy el registro de paquetes más grande del mundo (ya lo vienen usando desde JS Contemporáneo).
- **2015** — el proyecto se estabiliza bajo la **Node.js Foundation**, tras una división de la comunidad (io.js) que terminó reunificándose.
- **Hoy** — sigue siendo el estándar de facto para backends en JavaScript/TypeScript, con alternativas más nuevas ganando terreno (Deno, Bun) que resuelven problemas puntuales de Node sin reemplazarlo todavía.

<div class="mt-4 text-sm italic opacity-80">

El mismo lenguaje que hasta ahora solo corría en el navegador, corriendo del otro lado de la conexión.

</div>

---
layout: default
---

# Por qué Node sirve para un servidor

<div class="text-sm opacity-80 mb-2">

Un servidor atiende **muchas** requests al mismo tiempo — la mayoría, esperando algo (una consulta a una base de datos, un archivo, otra API). El mismo modelo de Asincronismo, ahora en el contexto de un servidor.

</div>

- Node corre en **un solo hilo**, pero nunca se queda bloqueado esperando una operación de E/S (archivo, red, base de datos) — la delega y sigue atendiendo otras requests mientras tanto.
- Cuando esa operación termina, su callback (o su `Promise`) se resuelve en el **event loop** — el mismo mecanismo ya visto en el navegador, corriendo acá del lado del servidor.
- Por eso un servidor Node puede atender miles de conexiones simultáneas con relativamente pocos recursos, siempre que el código no bloquee el hilo con cómputo pesado y sincrónico.

<div class="mt-4 text-sm italic opacity-80 text-center">

No es "más rápido" que otros lenguajes en cómputo puro — es eficiente específicamente en I/O concurrente, que es la mayor parte del trabajo de una API típica.

</div>

---
layout: center
---

# Primeros pasos

---
layout: default
---

# Iniciar un proyecto Node

```bash
node --version   # confirmar que está instalado
npm --version

mkdir products-api && cd products-api
npm init -y       # genera package.json con valores por defecto
```

<div class="mt-4 text-sm opacity-80">

`npm init -y` ya lo vieron en JS Contemporáneo — nada nuevo acá. La diferencia es lo que se instala **adentro** de este `package.json`: hasta ahora, herramientas de build (Vite, Slidev); de acá en más, un servidor.

</div>

---
layout: default
---

# Un servidor con el módulo nativo `http`

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

<div class="mt-2 text-sm opacity-80">

`http` viene incluido en Node, sin instalar nada — pero mirá cuánto código hace falta para **una sola** ruta: comparar `url` y `method` a mano, armar los headers, convertir a JSON. Con 20 rutas, esto se vuelve inmanejable.

</div>

---
layout: default
---

# ¿Qué es Express?

- Un **framework minimalista** construido sobre el módulo `http` — no lo reemplaza, lo simplifica.
- Resuelve exactamente lo que el ejemplo anterior tuvo que hacer a mano: rutear por `url`/`method`, parsear el body, encadenar lógica con middleware.
- Es el estándar de facto para APIs en Node desde hace más de una década — con alternativas más nuevas (Fastify, Koa, Hono) que compiten en rendimiento o estilo, sin desplazarlo todavía como opción por defecto.

<div class="mt-6 text-sm italic opacity-80 text-center">

La misma relación que JSX tiene con `React.createElement`: no es magia nueva, es una capa que evita escribir a mano algo tedioso y repetitivo.

</div>

---
layout: default
---

# Instalar Express

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

<div class="mt-2 text-sm opacity-80">

`Request`/`Response` son los tipos que trae `@types/express` — se usan desde acá en más, en cada handler: todo el código de este módulo es TypeScript real, no JS con nombres en inglés. `tsx` corre el archivo directamente, sin compilar a mano — similar a `ts-node`, ya visto en TypeScript.

</div>

<div class="mt-1 text-xs italic opacity-50">

Doc: <a href="https://expressjs.com/es/4x/api.html">expressjs.com/es/4x/api</a>

</div>

---
layout: center
---

# Rutas y verbos HTTP

---
layout: default
---

# Verbos HTTP: el vocabulario de una API REST

<div class="overflow-x-auto mt-4 text-sm">

| Verbo | Para qué | Ejemplo |
|---|---|---|
| **GET** | Leer, sin efectos secundarios | `GET /products` |
| **POST** | Crear un recurso nuevo | `POST /products` |
| **PUT** | Reemplazar un recurso completo | `PUT /products/1` |
| **PATCH** | Modificar parcialmente | `PATCH /products/1` |
| **DELETE** | Borrar | `DELETE /products/1` |

</div>

<div class="mt-4 text-sm opacity-80">

**REST** (*REpresentational State Transfer*) es una convención, no una ley del lenguaje: usar el verbo HTTP correcto según la acción, y la URL para identificar **qué** recurso (no la acción — `/products/1`, no `/getProduct?id=1`). Axios, en el módulo anterior, ya venía usando esta misma convención (`api.get`, y lo mismo existe como `api.post`/`api.put`/`api.delete`).

</div>

---
layout: default
---

# Status codes más usados

<div class="grid grid-cols-3 gap-3 mt-6 text-sm">
<div class="p-3 rounded-lg bg-green-50 border border-green-300 text-center"><strong>200 OK</strong><br/>Todo salió bien</div>
<div class="p-3 rounded-lg bg-green-50 border border-green-300 text-center"><strong>201 Created</strong><br/>Se creó un recurso</div>
<div class="p-3 rounded-lg bg-green-50 border border-green-300 text-center"><strong>204 No Content</strong><br/>OK, sin nada que devolver</div>
<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-300 text-center"><strong>400 Bad Request</strong><br/>El request está mal formado</div>
<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-300 text-center"><strong>401 Unauthorized</strong><br/>Falta autenticarse</div>
<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-300 text-center"><strong>403 Forbidden</strong><br/>Autenticado, pero sin permiso</div>
<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-300 text-center"><strong>404 Not Found</strong><br/>El recurso no existe</div>
<div class="p-3 rounded-lg bg-red-50 border border-red-300 text-center"><strong>500 Server Error</strong><br/>Algo falló del lado del servidor</div>
<div class="p-3 rounded-lg bg-gray-100 text-center opacity-70">Hay muchos más — estos cubren el 90% de los casos reales</div>
</div>

---
layout: default
---

# `req` y `res`: parámetros y query params

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

<div class="mt-1 text-sm opacity-80">

Mismo vocabulario que `useParams`/`useSearchParams` de React Router, del otro lado de la conexión: ahí, el navegador **leía** la URL; acá, Express la **recibe** — `req.params` para lo obligatorio (`:id`), `req.query` para lo opcional (`?category=...`). Nota: ambos llegan siempre como **string**, aunque parezcan números.

</div>

---
layout: center
---

# Middleware

---
layout: default
---

# Middleware, ahora del lado del servidor

<div class="text-sm opacity-80 mb-2">

Un middleware es una función que se ubica en el medio del flujo de una request y puede inspeccionarla, modificarla, o cortarla — mismo concepto ya visto en React con `RequireAuth`, del lado del cliente.

</div>

```ts
import { Request, Response, NextFunction } from 'express'

function logger(req: Request, res: Response, next: NextFunction) {
  console.log(`${req.method} ${req.url}`)
  next()   // sin next(), la request se queda colgada — nunca llega a su ruta
}

app.use(logger)   // corre en TODAS las rutas, en el orden en que se declaran
```

<div class="mt-2 text-sm opacity-80">

`app.use` registra un middleware **global**. El orden importa: cada request pasa por ellos de arriba hacia abajo, en el mismo orden en que se escribieron.

</div>

---
layout: default
---

# Middleware con datos de usuario

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

<div class="mt-2 text-sm opacity-80">

Un ejemplo más útil que un logger: exige un dato antes de dejar pasar la request, y lo deja disponible en `req.user` para las rutas de abajo. `declare global` le enseña a TypeScript que `Request` ahora tiene `user` — sin esto, asignarlo sería un error de tipos. Es una versión simplificada; la real, verificando un token en vez de un header a ojo, se arma en Autenticación.

</div>

---
layout: default
---

# `express.json()`: el middleware que faltaba

```ts
app.use(express.json())   // parsea el body si es JSON, antes de llegar a la ruta

app.post('/products', (req: Request, res: Response) => {
  console.log(req.body)   // ya viene parseado, como un objeto
  res.status(201).json(req.body)
})
```

<div class="mt-3 text-sm opacity-80">

Sin este middleware, `req.body` sería `undefined` — Express no parsea el body por defecto, hay que pedírselo explícitamente. Viene incluido en Express (no hace falta instalar nada aparte).

</div>

---
layout: center
---

# CRUD en memoria

---
layout: default
---

# El catálogo: leer

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

<div class="mt-1 text-sm opacity-80">

Mismo `interface Product` de siempre, con un `id` nuevo: hace falta un identificador estable para pedir, modificar o borrar **uno solo**. Por ahora, a mano — MongoDB lo va a generar automáticamente.

</div>

---
layout: default
---

# El catálogo: crear

```ts
app.post('/products', (req: Request, res: Response) => {
  const newProduct: Product = { id: Date.now(), ...req.body }
  products.push(newProduct)
  res.status(201).json(newProduct)
})
```

<div class="mt-4 text-sm opacity-80">

`Date.now()` como `id` es una solución de práctica, no de producción (dos requests en el mismo milisegundo colisionarían) — otra razón más para que una base de datos real los genere, como se ve en el próximo tema.

</div>

---
layout: default
---

# El catálogo: modificar y borrar

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

<div class="mt-2 text-sm opacity-80">

Mismo patrón en las dos: buscar el índice, chequear que exista, y recién ahí aplicar el cambio. `PUT` combina lo existente con lo nuevo (`{ ...products[index], ...req.body }`); `DELETE` responde `204` — vacío, porque no hay nada que devolver.

</div>

---
layout: default
---

# Organizar rutas con `express.Router()`

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

<div class="mt-1 text-sm opacity-80">

Un solo archivo con todas las rutas no escala — `Router()` agrupa las de un mismo recurso, montado bajo un prefijo común. Misma idea que `routes/`/`components/` en React.

</div>

---
layout: default
---

# Los controllers, en código

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

<div class="mt-2 text-xs opacity-80">

Exactamente el mismo código de las slides de CRUD — movido a su propio archivo, exportado función por función (`createProduct` sigue el mismo patrón, movido tal cual). `router.get('/', getAllProducts)` ya no define la lógica ahí mismo, solo la conecta con su URL.

</div>

---
layout: default
---

# Manejo de errores centralizado

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

<div class="mt-1 text-sm opacity-80">

Un middleware con **cuatro** parámetros (incluido `err`) es un manejador de errores para Express — se registra al final y captura lo que llegue por `next(err)`, sin repetir `try`/`catch` en cada ruta. `console.error` alcanza para practicar; en un proyecto real se reemplaza por una librería de logging (Winston, Pino).

</div>

---
layout: center
---

# CORS

---
layout: default
---

# Por qué el navegador bloquea la request

<div class="text-sm opacity-80 mb-2">

React corre en `http://localhost:5173`; la API, en `http://localhost:4000` — **orígenes distintos** (puerto incluido). Por seguridad, el navegador bloquea por defecto cualquier request de un origen a otro (*same-origin policy*).

</div>

```
Access to fetch at 'http://localhost:4000/products' from origin
'http://localhost:5173' has been blocked by CORS policy
```

<div class="mt-3 text-sm opacity-80">

Este es, probablemente, el primer error real que se ve al conectar el React del módulo anterior con la API de este módulo — no es un bug del código, es el navegador cumpliendo su trabajo. Lo resuelve el **servidor**, no el cliente: es la API la que tiene que decir explícitamente "acepto requests de este origen".

</div>

---
layout: default
---

# Resolverlo con `cors`

```bash
npm install cors
npm install -D @types/cors
```

```ts
import cors from 'cors'

app.use(cors())   // por defecto, permite cualquier origen — cómodo en desarrollo

app.use(cors({ origin: 'https://mi-tienda.com' }))   // en producción, restringido
```

<div class="mt-3 text-sm opacity-80">

`cors()` agrega los headers (`Access-Control-Allow-Origin`, entre otros) que le dicen al navegador "este origen está permitido". Sin argumentos, permite cualquiera — razonable mientras se desarrolla, pero en producción conviene restringirlo al dominio real del frontend.

</div>

<div class="mt-1 text-xs italic opacity-50">

Doc: <a href="https://developer.mozilla.org/es/docs/Web/HTTP/Guides/CORS">developer.mozilla.org — CORS</a>

</div>

---
layout: center
---

# Configuración del proyecto

---
layout: default
---

# Variables de entorno con `dotenv`

<div class="text-sm opacity-80 mb-2">

Mismo problema ya visto con `.env` en Vite (URLs distintas por ambiente, secretos fuera del código) — Node no lo resuelve nativamente como Vite: hace falta una librería.

</div>

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

<div class="mt-1 text-xs opacity-80">

A diferencia de Vite, `dotenv` **no** elige el archivo solo según el ambiente — hay que decírselo explícitamente con `path`. `process.env.PORT` siempre es un **string** (o `undefined`); convertir a número a mano cuando haga falta, como acá con `Number(...)`.

</div>

---
layout: default
---

# `tsconfig.json` para un proyecto Node

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

<div class="mt-3 text-sm opacity-80">

Mismas opciones ya vistas en TypeScript, con una diferencia: `module`/`moduleResolution` en `"NodeNext"` en vez de `"ESNext"`/`"bundler"` — acá no hay un bundler (Vite) resolviendo los imports, es Node ejecutando los archivos directamente.

</div>

---
layout: center
---

# Autenticación

---
layout: default
---

# El backend es el responsable

- **Genera el token** — nadie más puede emitir uno válido, porque nadie más tiene el secreto (o la clave privada) que lo firma.
- **Nunca guarda la contraseña en texto plano** — guarda su hash y compara contra ese hash en cada login. Importante: no es "encriptar y desencriptar" — un hash **no se puede revertir**, solo comparar.
- **Decide cuándo un token es válido** (firma correcta, no vencido) y puede invalidarlo antes de tiempo si hace falta.
- El cliente solo hace dos cosas: guardar el token, y reenviarlo — toda la lógica de "quién sos" vive del lado del servidor.

<div class="mt-4 text-sm italic opacity-80 text-center">

Por eso `bcrypt.compare` (próxima slide) no "desencripta" nada — recalcula el hash del intento y lo compara contra el guardado.

</div>

---
layout: default
---

# HS256 vs. RS256: cómo se firma el token

<div class="grid grid-cols-2 gap-3 mt-4 text-sm">
<div class="p-3 rounded-lg bg-gray-100">

**HS256 (simétrica)**

Un solo secreto — la misma clave firma y verifica. Simple y rápido, pero cualquiera con el secreto puede firmar tokens falsos. La que usa este curso.
</div>
<div class="p-3 rounded-lg bg-gray-100">

**RS256 (asimétrica)**

Un par de claves: la **privada** firma (solo el backend la tiene), la **pública** verifica — se puede repartir sin dar poder de emitir tokens nuevos.
</div>
</div>

<div class="mt-4 text-sm opacity-80">

RS256 tiene sentido con varios servicios que necesitan **verificar** un token sin poder **crear** uno (microservicios, por ejemplo). Con un solo backend, como acá, HS256 alcanza y es más simple de manejar.

</div>

---
layout: default
---

# `bcrypt`: hashear contraseñas

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

<div class="mt-2 text-sm opacity-80">

`bcrypt.hash` es de **una sola vía**: no se puede "deshacer" para recuperar la contraseña original, solo comparar (`compare`) si un intento coincide con el hash guardado. El `10` es el costo del algoritmo (*salt rounds*) — más alto, más lento de calcular y más difícil de romper por fuerza bruta.

</div>

<div class="mt-1 text-xs italic opacity-50">

Doc: <a href="https://www.npmjs.com/package/bcrypt">npmjs.com/package/bcrypt</a>

</div>

---
layout: default
---

# JWT: firmar un token

<div class="text-sm opacity-80 mb-2">

Retomando de React: un token certifica "quién sos" sin reenviar la contraseña en cada pedido. Ahora, del lado que lo **genera**.

</div>

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

<div class="mt-2 text-xs opacity-80">

`jwt.sign` codifica el *payload* (acá, `userId`/`role`) y lo firma con un secreto — cualquiera puede **leer** el contenido de un JWT (no está encriptado, solo codificado), pero solo quien tiene el secreto puede generar una firma válida o confirmar que no fue alterado.

</div>

<div class="mt-1 text-xs italic opacity-50">

Doc: <a href="https://jwt.io/">jwt.io</a> — permite decodificar un token real y ver su contenido

</div>

---
layout: default
---

# Los usuarios, en memoria

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

<div class="mt-4 text-sm opacity-80">

Mismo patrón que `products`: un array en memoria, con la contraseña ya hasheada (nunca en texto plano) — el `passwordHash` de ejemplo es un hash real de `bcrypt.hash`, no un string inventado.

</div>

---
layout: default
---

# Endpoint de login completo

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

<div class="mt-1 text-xs opacity-80">

Mismo mensaje de error para "no existe el email" y "la contraseña no coincide" — a propósito: si fueran distintos, alguien podría usarlo para descubrir qué emails están registrados.

</div>

---
layout: default
---

# Middleware de autenticación

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

<div class="mt-1 text-sm opacity-80">

Cierra el círculo con React: el header `Authorization: Bearer <token>` que el interceptor de Axios agregaba en cada request es, literalmente, lo que este middleware lee y verifica acá.

</div>

---
layout: default
---

# Autorización por rol

```ts
function requireAdmin(req: Request, res: Response, next: NextFunction) {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'No tenés permiso' })
  }
  next()
}

// deleteProduct: la misma lógica de borrar ya vista, como controller
app.delete('/products/:id', requireAuth, requireAdmin, deleteProduct)
```

<div class="mt-3 text-sm opacity-80">

Dos middlewares encadenados en la misma ruta — corren en orden: primero confirma que hay una sesión válida (`requireAuth`), después que esa sesión tiene el rol necesario (`requireAdmin`). `401` ("no sé quién sos") y `403` ("sé quién sos, pero no podés") son errores distintos a propósito.

</div>

---
layout: default
---

# Scaffolding recomendado

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

<div class="mt-2 text-sm opacity-80">

Mismo criterio de organización ya visto en React (`components/`, `routes/`, `services/`). Separar `app.ts` (arma la `app`, sin escuchar nada) de `index.ts` (la importa y recién ahí llama a `.listen`) no es solo prolijidad: `supertest`, más adelante, importa `app` directo — si `app.listen` estuviera en el mismo archivo, cada test abriría un puerto real de más.

</div>

---
layout: center
---

# Probar la API

---
layout: default
---

# Probar sin un frontend

```bash
curl http://localhost:4000/products

curl -X POST http://localhost:4000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Monitor","price":80000}'

curl http://localhost:4000/profile \
  -H "Authorization: Bearer <token>"
```

<div class="mt-3 text-sm opacity-80">

`curl` alcanza para probar rápido desde la terminal. Para un flujo más cómodo (guardar requests, ver la respuesta formateada), herramientas como **Postman** o **Thunder Client** (extensión de VS Code) hacen lo mismo con una interfaz gráfica — sin necesitar todavía un frontend real corriendo.

</div>

---
layout: center
---

# Testing del backend

---
layout: default
---

# Vitest o Jest: dos alternativas

<div class="grid grid-cols-2 gap-3 mt-4 text-sm">
<div class="p-3 rounded-lg bg-gray-100">

**Jest**

El más usado en proyectos ya existentes. Necesita configuración extra para TypeScript/ESM (`ts-jest` o Babel).

```bash
npm install -D jest @types/jest ts-jest
```

</div>
<div class="p-3 rounded-lg bg-gray-100">

**Vitest**

Más nuevo. TypeScript/ESM nativo, sin configuración extra — y es el mismo motor que ya usa Vite en el frontend.

```bash
npm install -D vitest
```

</div>
</div>

<div class="mt-4 text-sm opacity-80">

Mismo `describe`/`it`/`expect` en los dos — migrar de uno a otro es casi gratis. Ojo con `ts-jest`: al momento de escribir esto, todavía no soporta TypeScript 7 (recién liberado) — si al instalar `typescript` a secas aparece un error de `ts-jest` sobre la "compiler API", fijar `"typescript": "^6"` en el `package.json` lo resuelve. Vitest no tiene este problema.

</div>

---
layout: default
---

# Mismo test, en los dos

<div class="grid grid-cols-2 gap-3 text-xs mt-2">
<div>

**Jest**

```ts
// pricing.test.ts
import { applyDiscount } from './pricing'

test('applyDiscount resta el %', () => {
  expect(applyDiscount(1000, 0.1)).toBe(900)
})
```

</div>
<div>

**Vitest**

```ts
// pricing.test.ts
import { it, expect } from 'vitest'
import { applyDiscount } from './pricing'

it('applyDiscount resta el %', () => {
  expect(applyDiscount(1000, 0.1)).toBe(900)
})
```

</div>
</div>

<div class="mt-3 text-sm opacity-80">

`applyDiscount`, ya tipada en TypeScript — una función pura es, literalmente, el caso más simple de testear: mismo input, mismo output, sin nada que mockear. Jest expone `test`/`expect` como globales; Vitest los importa explícitamente (o se activan con `globals: true` en su configuración).

</div>

---
layout: default
---

# Testear un endpoint con `supertest`

```ts
import request from 'supertest'
import app from '../app'

test('GET /products devuelve el catálogo', async () => {
  const res = await request(app).get('/products')
  expect(res.status).toBe(200)
  expect(res.body).toHaveLength(2)
})
```

<div class="mt-1 text-sm opacity-80">

`supertest` envuelve la instancia de `app` directamente, sin levantar un puerto real — funciona igual con Jest o con Vitest. Responde `200` porque la ruta no tiene ninguna condición que la haga fallar; el body tiene longitud `2` porque el array en memoria (Mouse, Teclado) arranca así — en un test real conviene **sembrar** un estado conocido antes de cada test, para no depender de qué haya quedado de una corrida anterior.

</div>

<div class="mt-1 text-xs italic opacity-50">

Doc: <a href="https://www.npmjs.com/package/supertest">npmjs.com/package/supertest</a>

</div>

---
layout: default
---

# Mockear una dependencia

<div class="grid grid-cols-2 gap-3 text-xs mt-2">
<div>

**Jest**

```ts
jest.mock('../services/email')
import { sendWelcomeEmail } from '../services/email'

test('el registro avisa por mail', async () => {
  await registerUser({ email: 'ada@mail.com' })
  expect(sendWelcomeEmail)
    .toHaveBeenCalledWith('ada@mail.com')
})
```

</div>
<div>

**Vitest**

```ts
vi.mock('../services/email')
import { sendWelcomeEmail } from '../services/email'

test('el registro avisa por mail', async () => {
  await registerUser({ email: 'ada@mail.com' })
  expect(sendWelcomeEmail)
    .toHaveBeenCalledWith('ada@mail.com')
})
```

</div>
</div>

<div class="mt-3 text-sm opacity-80">

`mock(...)` reemplaza el módulo real por una versión falsa y controlada — acá, para no mandar un email real en cada corrida de tests. El `expect` no comprueba que el mail se haya enviado de verdad, solo que la función se **llamó** con los datos correctos: alcanza para testear `registerUser` de forma aislada, sin depender de un servicio externo.

</div>

---
layout: default
---

# Qué sigue

- El array en memoria se pierde cada vez que el servidor reinicia — el próximo tema (**MongoDB**) lo reemplaza por persistencia real, sobre las mismas rutas y el mismo patrón de `Router()`.
- El módulo de **Testing**, más adelante, retoma esto con más profundidad: tests de integración contra una base real mockeada (`mongodb-memory-server`), la pirámide de testing, y qué tipo de test conviene en cada capa de la aplicación.

<div class="mt-6 text-sm italic opacity-80 text-center">

Con esto, el círculo full-stack está completo: un componente de React pidiendo datos, y un servidor Express respondiéndolos — probado.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
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

**Middleware y seguridad**

| Forma | Para qué |
|---|---|
| `app.use(fn)` | Middleware global, en orden |
| `express.json()` | Parsear el body |
| `cors()` | Permitir requests de otro origen |
| `(err, req, res, next) => {}` | Manejo de errores centralizado |
| `bcrypt.hash`/`compare` | Hashear y verificar contraseñas |
| `jwt.sign`/`verify` | Emitir y validar tokens |
| `dotenv/config` | Variables de entorno |
| `test`/`expect` (Jest o Vitest) | Unit tests |
| `request(app).get(...)` | Testear un endpoint (`supertest`) |
| `jest.mock`/`vi.mock` | Mockear una dependencia |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [nodejs.org/es/docs](https://nodejs.org/es/docs) — documentación oficial de Node.js, en español
- [expressjs.com/es](https://expressjs.com/es/) — documentación oficial de Express, en español
- [developer.mozilla.org — HTTP](https://developer.mozilla.org/es/docs/Web/HTTP) — métodos, status codes y headers, como referencia completa
- [jwt.io](https://jwt.io/) — documentación y debugger de JSON Web Tokens (permite decodificar un token y ver su contenido)
- [npmjs.com/package/bcrypt](https://www.npmjs.com/package/bcrypt) — hashing de contraseñas
- [npmjs.com/package/cors](https://www.npmjs.com/package/cors) · [npmjs.com/package/dotenv](https://www.npmjs.com/package/dotenv)
- [vitest.dev](https://vitest.dev/) · [jestjs.io/es-ES](https://jestjs.io/es-ES/) · [npmjs.com/package/supertest](https://www.npmjs.com/package/supertest)
- [github.com/goldbergyoni/nodebestpractices](https://github.com/goldbergyoni/nodebestpractices) — buenas prácticas reales, mantenido por la comunidad

</div>
