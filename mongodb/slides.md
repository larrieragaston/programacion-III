---
theme: bricks
title: Programación III - MongoDB
download: true
info: |
  MongoDB - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: mongodb, mongoose, nosql, base de datos, schema, crud, typescript, INSPT, UTN
transition: slide-left
mdc: true
---

# MongoDB

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/mongodb.svg" alt="MongoDB" class="h-16 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: center
---

# Tipos de bases de datos

---
layout: default
---

# Cómo se dividen las bases de datos

<div class="flex flex-col items-center mt-4">
<div class="px-4 py-2 rounded-lg border-2 border-gray-400 bg-gray-100 font-bold text-sm">Bases de datos</div>
<div class="w-px h-5 bg-gray-400"></div>
<div class="flex gap-16">

<div class="flex flex-col items-center">
<div class="px-3 py-1.5 rounded-lg border-2 border-blue-400 bg-blue-50 font-bold text-xs whitespace-nowrap">Relacionales (SQL)</div>
<div class="w-px h-4 bg-blue-300"></div>
<img src="/logos/postgresql.svg" class="h-7" />
<div class="text-[9px] opacity-60 mt-1 text-center">PostgreSQL, MySQL,<br/>SQL Server...</div>
</div>

<div class="flex flex-col items-center">
<div class="px-3 py-1.5 rounded-lg border-2 border-green-400 bg-green-50 font-bold text-xs whitespace-nowrap">No relacionales (NoSQL)</div>
<div class="w-px h-4 bg-green-300"></div>
<div class="flex gap-5 border-t-2 border-green-300 pt-2">
<div class="flex flex-col items-center w-14">
<img src="/logos/mongodb.svg" class="h-6" />
<div class="text-[9px] font-bold mt-1 text-center">Documentos</div>
</div>
<div class="flex flex-col items-center w-14">
<img src="/logos/redis.svg" class="h-6" />
<div class="text-[9px] font-bold mt-1 text-center">Clave-valor</div>
</div>
<div class="flex flex-col items-center w-14">
<img src="/logos/apachecassandra.svg" class="h-6" />
<div class="text-[9px] font-bold mt-1 text-center">Columnares</div>
</div>
<div class="flex flex-col items-center w-14">
<img src="/logos/neo4j.svg" class="h-6" />
<div class="text-[9px] font-bold mt-1 text-center">Grafos</div>
</div>
</div>
</div>

</div>
</div>

<div class="mt-4 text-sm italic opacity-80 text-center">

MongoDB es una base de **documentos** — una familia dentro de NoSQL, no un sinónimo de NoSQL en sí.

</div>

---
layout: default
---

# ¿Para qué sirve cada tipo?

<div class="grid grid-cols-3 gap-3 mt-4 text-sm">
<div class="p-3 rounded-lg bg-gray-100"><div class="flex items-center gap-2 mb-1"><img src="/logos/postgresql.svg" class="h-4" /><strong>Relacional (SQL)</strong></div>Datos muy estructurados, con relaciones claras y consistencia estricta (transacciones ACID).</div>
<div class="p-3 rounded-lg bg-green-50 border border-green-300"><div class="flex items-center gap-2 mb-1"><img src="/logos/mongodb.svg" class="h-4" /><strong>Documentos (MongoDB)</strong></div>Datos semi-estructurados o anidados, con un esquema que puede variar.</div>
<div class="p-3 rounded-lg bg-blue-50 border border-blue-300"><div class="flex items-center gap-2 mb-1"><img src="/logos/redis.svg" class="h-4" /><strong>Clave-valor (Redis)</strong></div>Lecturas/escrituras extremadamente rápidas de datos simples: cache, sesiones.</div>
<div class="p-3 rounded-lg bg-purple-50 border border-purple-300"><div class="flex items-center gap-2 mb-1"><img src="/logos/apachecassandra.svg" class="h-4" /><strong>Columnares (Cassandra)</strong></div>Volúmenes enormes de escritura distribuidos en muchos nodos: series de tiempo, big data.</div>
<div class="p-3 rounded-lg bg-yellow-50 border border-yellow-300"><div class="flex items-center gap-2 mb-1"><img src="/logos/neo4j.svg" class="h-4" /><strong>Grafos (Neo4j)</strong></div>Relaciones complejas entre entidades: redes sociales, recomendaciones.</div>
</div>

---
layout: default
---

# SQL vs. NoSQL

<div class="overflow-x-auto mt-3 text-sm">

| | SQL | NoSQL (documentos) |
|---|---|---|
| Esquema | Rígido, definido de antemano | Flexible, puede variar por documento |
| Consistencia | Fuerte (ACID) | Eventual en muchos casos (modelo BASE) |
| Escalado típico | Vertical (más CPU/RAM al servidor) | Horizontal (más servidores, sharding) |
| Relaciones | `JOIN` entre tablas | Embedding o `populate` |

</div>

<div class="mt-2 text-sm opacity-80">

Ambos persisten datos, ambos se consultan e indexan — la elección depende de la forma de los datos, no de que uno sea "mejor". Aclaración honesta: desde 2018, Mongo también soporta transacciones ACID multi-documento — la distinción de arriba es la más común en la práctica, no una regla absoluta.

</div>

---
layout: default
---

# MongoDB: un poco de historia

- **2007** — nace como proyecto interno (**10gen**), buscando una base de documentos para infraestructura propia a gran escala.
- **2009** — se libera como código abierto. El nombre viene de "humongous" (enorme).
- **2010** — con Node recién despegando, surge **Mongoose**: le agrega schemas y validación a Mongo, pensado específicamente para ese ecosistema.
- **2015** — **WiredTiger** se vuelve el motor de almacenamiento por defecto (versión 3.2), con mejor concurrencia y compresión.
- **2016** — lanza **Atlas**, la versión gestionada en la nube — la que usa este curso.
- **Hoy** — soporte multi-modelo (búsqueda de texto, series de tiempo, transacciones ACID desde 2018).

---
layout: default
---

# Documentos como JSON

```json
{
  "_id": "671f3a2b9e1c4a001f8b4567",
  "name": "Mouse",
  "price": 18000,
  "stock": 5,
  "tags": ["periféricos", "oferta"]
}
```

<div class="mt-4 text-sm opacity-80">

Esto ya lo vienen mandando por la API desde React — un objeto JSON. La diferencia es que ahora, en vez de vivir un instante en memoria mientras dura el request, **se guarda así, tal cual**, en la base. `_id` lo genera Mongo automáticamente — reemplaza el `Date.now()` de práctica del módulo anterior por un identificador real, único de verdad.

</div>

---
layout: default
---

# Tablas vs. colecciones

<div class="overflow-x-auto mt-3 text-sm">

| SQL (relacional) | MongoDB (documentos) |
|---|---|
| Tabla | Colección |
| Fila | Documento |
| Columna | Campo |
| Clave primaria | `_id` |
| `JOIN` entre tablas | *Embedding* o *referencing* |

</div>

<div class="mt-2 text-sm opacity-80">

SQL **normaliza** (separar en tablas, unir con `JOIN`); Mongo permite **desnormalizar** — decidir a propósito qué guardar junto y qué separado, según cómo se vaya a leer. Además, acá el schema es flexible: cada documento puede variar.

</div>

---
layout: default
---

# Embedding vs. referencing

```json
// Embedding: todo en un solo documento
{ "name": "Mouse", "price": 18000, "category": { "name": "Periféricos" } }
```

```json
// Referencing: un id que apunta a otra colección
{ "name": "Mouse", "price": 18000, "category": "671f3a...b4321" }
```

<div class="mt-3 text-sm opacity-80">

**Embedding**: la categoría vive adentro del producto — rápido de leer (un solo documento), pero se duplica si varios productos comparten categoría. **Referencing**: el producto guarda el `_id` de su categoría, en una colección aparte — sin duplicar, al costo de un segundo pedido (o un `populate`, más adelante) para traer los datos completos.

</div>

---
layout: center
---

# Conectar el proyecto

---
layout: default
---

# Conseguir una base: local o remota

<div class="grid grid-cols-2 gap-4 mt-4 text-sm">
<div class="p-4 rounded-lg bg-blue-50 border border-blue-300">

**Local**

```bash
brew install mongodb-community
```

Corre en tu propia máquina (`mongodb://localhost:27017`). Cada quien tiene su propia base, sin compartir datos con el equipo.

</div>
<div class="p-4 rounded-lg bg-green-50 border border-green-300">

**Remota — [MongoDB Atlas](https://www.mongodb.com/atlas)** *(recomendada)*

Base gestionada, capa gratis para proyectos chicos. Da una *connection string* (`mongodb+srv://...`) que funciona igual desde cualquier máquina.

</div>
</div>

---
layout: default
---

# Explorar Mongo con Compass

<div class="text-sm opacity-90 mb-2">

**MongoDB Compass** es la interfaz gráfica oficial para conectarse y navegar una base — local o Atlas — sin escribir una sola línea de código.

</div>

- Descargar Compass, pegar la misma *connection string* de la slide anterior, conectar.
- Ver las bases que ya vienen por defecto (`admin`, `config`, `local`) — internas de Mongo, no para datos de la app.
- Crear a mano una base y una colección propia, e insertar un documento de prueba — verlo aparecer como JSON en el árbol de la izquierda.

<div class="mt-2 text-sm italic opacity-80 text-center">

El objetivo: entender qué es realmente un documento y una colección, antes de que Mongoose agregue una capa de abstracción encima.

</div>

<div class="mt-2 text-xs opacity-60">

→ [mongodb.com/products/compass](https://www.mongodb.com/products/compass)

</div>

---
layout: center
---

# MongoDB en el proyecto de Node

---
layout: default
---

# Instalar Mongoose

```bash
npm install mongoose
npm install -D @types/node
```

<div class="mt-3 text-sm opacity-80">

Se podría hablar directo con el driver oficial (`mongodb`), pero ese driver no valida nada — solo envía y trae documentos tal cual. **Mongoose** es un *ODM* (*Object Document Mapper*) para Node, que surge en 2010, muy pronto en la vida de Node: agrega **schemas** (la forma esperada de un documento), validación antes de guardar, y una API más cómoda — la misma idea de "forma esperada" que una `interface` de TypeScript, ahora aplicada a lo que se persiste.

</div>

---
layout: default
---

# Conectar Express a Mongo

```ts
import mongoose from 'mongoose'

async function connectDB() {
  await mongoose.connect(process.env.MONGO_URL!)
  console.log('Conectado a MongoDB')
}

connectDB()
```

```bash
# .env.development (local)
MONGO_URL=mongodb://localhost:27017/mi-app

# .env.production (Atlas)
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/mi-app
```

<div class="mt-1 text-sm opacity-80">

Mismo código de conexión para los dos casos — lo único que cambia es la *connection string*, fuera del código, en `.env`.

</div>

---
layout: center
---

# Schemas y modelos

---
layout: default
---

# Definir un schema

```ts
import { Schema } from 'mongoose'

const productSchema = new Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  stock: { type: Number, default: 0 },
})
```

<div class="mt-3 text-sm opacity-80">

Un `Schema` describe la forma de un documento — qué campos tiene, de qué tipo, y con qué reglas. `required: true` obliga a que el campo esté presente; `default` lo completa solo si no se manda. Estas validaciones existen siempre, en runtime — algo que TypeScript, al borrarse en la compilación, no puede ofrecer.

</div>

---
layout: default
---

# Más validaciones

```ts
const productSchema = new Schema({
  name: { type: String, required: true, trim: true },
  price: { type: Number, required: true, min: 0 },
  stock: { type: Number, default: 0, min: 0 },
  category: { type: String, enum: ['electronics', 'clothing', 'books'] },
})
```

<div class="mt-3 text-sm opacity-80">

`min` rechaza un precio o stock negativo; `trim` limpia espacios de más; `enum` limita `category` a un conjunto cerrado de valores — el mismo concepto que un *literal type* de TypeScript, acá aplicado del lado de la base, en runtime.

</div>

---
layout: default
---

# Constraints de un campo

<div class="grid grid-cols-2 gap-6 mt-4 text-sm">
<div class="overflow-x-auto">

| Constraint | Para qué |
|---|---|
| `required` | Campo obligatorio |
| `unique` | Sin valores repetidos (crea un índice) |
| `min` / `max` | Rango permitido, para números |
| `minlength` / `maxlength` | Longitud permitida, para strings |

</div>
<div class="overflow-x-auto">

| Constraint | Para qué |
|---|---|
| `match` | Debe cumplir una expresión regular |
| `enum` | Conjunto cerrado de valores |
| `default` | Valor si no se manda ninguno |
| `validate` | Función de validación propia |

</div>
</div>

---
layout: default
---

# Validación propia con `validate`

```ts
const productSchema = new Schema({
  email: { type: String, required: true, match: /^\S+@\S+\.\S+$/ },
  price: {
    type: Number,
    validate: {
      validator: (v: number) => v > 0,
      message: 'El precio debe ser positivo',
    },
  },
})
```

<div class="mt-3 text-sm opacity-80">

`match` alcanza para reglas simples (un formato de email); `validate` recibe una función propia para cualquier regla más específica, con un mensaje de error a medida.

</div>

---
layout: default
---

# Crear el modelo, tipado

```ts
import { Schema, model, InferSchemaType } from 'mongoose'

const productSchema = new Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  stock: { type: Number, default: 0 },
})

type Product = InferSchemaType<typeof productSchema>
// { name: string; price: number; stock: number }

const ProductModel = model<Product>('Product', productSchema)
```

<div class="mt-2 text-sm opacity-80">

`mongoose.model(...)` registra el schema y devuelve un **modelo**: el objeto para consultar y escribir en la colección. `InferSchemaType` lee el schema y arma el tipo solo — ya no hace falta escribir una `interface` aparte que, tarde o temprano, se desincroniza del schema real. Esto alcanza mientras el modelo solo tenga datos; en cuanto agrega métodos propios (próxima slide), Mongoose sí necesita conocer la forma de antemano.

</div>

---
layout: default
---

# Métodos de instancia y estáticos

```ts
interface ProductMethods { applyDiscount(pct: number): Promise<void> }
type ProductModelType = Model<Product, {}, ProductMethods> & {
  findCheapest(): Promise<HydratedDocument<Product, ProductMethods> | null>
}

const productSchema = new Schema<Product, ProductModelType, ProductMethods>({ /* los mismos campos */ })

productSchema.methods.applyDiscount = async function (pct) {
  this.price = this.price * (1 - pct)
  await this.save()
}
productSchema.statics.findCheapest = function () {
  return this.findOne().sort({ price: 1 })
}
```

<div class="mt-1 text-xs opacity-80">

Un método de **instancia** opera sobre un documento ya cargado (`this` es el documento); uno **estático**, sobre el modelo completo. `ProductModelType` (importando `Model`/`HydratedDocument` de `mongoose`) es lo que le permite a TypeScript reconocer estas llamadas del lado de quien las usa.

</div>

---
layout: default
---

# Middleware de schema: `pre` y `post`

```ts
import bcrypt from 'bcrypt'

userSchema.pre('save', async function () {
  if (!this.isModified('password')) return
  this.password = await bcrypt.hash(this.password, 10)
})
```

<div class="mt-3 text-sm opacity-80">

Mismo `bcrypt.hash` del módulo anterior — ahora corre solo, antes de cada guardado, sin que cada ruta tenga que acordarse de llamarlo. `isModified('password')` evita rehashear una contraseña que no cambió (por ejemplo, al actualizar solo el email). Con una función `async`, Mongoose espera la Promise sola — no hace falta un `next()` manual. `post('save', ...)` existe igual, para correr algo justo después de guardar.

</div>

---
layout: center
---

# CRUD contra Mongo

---
layout: default
---

# Crear

```ts
import { Request, Response } from 'express'

app.post('/products', async (req: Request, res: Response) => {
  const product = await ProductModel.create(req.body)
  res.status(201).json(product)
})
```

<div class="mt-4 text-sm opacity-80">

`ProductModel.create(req.body)` valida contra el schema y guarda en un solo paso — si falta un campo `required` o `price` es negativo, la Promise rechaza antes de tocar la base, y el error llega al manejador centralizado ya visto en el módulo anterior.

</div>

---
layout: default
---

# Leer

```ts
app.get('/products', async (req: Request, res: Response) => {
  const products = await ProductModel.find()
  res.json(products)
})

app.get('/products/:id', async (req: Request, res: Response) => {
  const product = await ProductModel.findById(req.params.id)
  if (!product) return res.status(404).json({ error: 'No encontrado' })
  res.json(product)
})
```

<div class="mt-2 text-sm opacity-80">

`find()` sin argumentos trae todos los documentos; `findById` busca por `_id` — Mongoose lo convierte automáticamente desde el string que llega en `req.params.id`.

</div>

---
layout: default
---

# Queries más útiles

```ts
// Filtrar por categoría y rango de precio
await ProductModel.find({ category: 'electronics', price: { $gte: 10000, $lte: 50000 } })

// Ordenar por precio descendente
await ProductModel.find().sort({ price: -1 })

// Paginar: página 2, 10 por página
await ProductModel.find().skip(10).limit(10)

// Solo ciertos campos, y contar sin traer nada
await ProductModel.find().select('name price')
await ProductModel.countDocuments({ stock: { $gt: 0 } })
```

<div class="mt-1 text-xs opacity-80">

`$gte`/`$lte`/`$gt` son operadores de comparación de Mongo — hay muchos más (`$in`, `$or`, `$regex`) en la referencia de operadores de consulta.

</div>

---
layout: default
---

# Las mismas queries, en Compass

```json
// Barra de Filter
{ category: "electronics", price: { $gte: 10000, $lte: 50000 } }

// Barra de Sort
{ price: -1 }
```

<div class="mt-4 text-sm opacity-80">

Compass no tiene un lenguaje propio: su barra de **Filter** acepta exactamente la misma sintaxis que el argumento de `.find()` en Mongoose, y la de **Sort** la de `.sort()` — lo que se prueba ahí se puede pegar directo en el código, y viceversa.

</div>

---
layout: default
---

# Modificar y borrar

```ts
app.put('/products/:id', async (req: Request, res: Response) => {
  const product = await ProductModel.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
    runValidators: true,
  })
  if (!product) return res.status(404).json({ error: 'No encontrado' })
  res.json(product)
})

app.delete('/products/:id', async (req: Request, res: Response) => {
  await ProductModel.findByIdAndDelete(req.params.id)
  res.status(204).end()
})
```

<div class="mt-1 text-xs opacity-80">

`new: true` hace que devuelva el documento **ya actualizado**. `runValidators: true` corre las validaciones del schema también en un `update` — sin esto, se pueden colar datos inválidos que `create` sí habría rechazado.

</div>

---
layout: default
---

# El `_id` de Mongo

```ts
const product = await ProductModel.findById('671f3a2b9e1c4a001f8b4567')

console.log(product._id)              // ObjectId('671f3a2b9e1c4a001f8b4567')
console.log(product._id.toString())   // '671f3a2b9e1c4a001f8b4567'
```

<div class="mt-3 text-sm opacity-80">

`_id` es un **ObjectId**, no un string — 12 bytes que codifican, entre otras cosas, la fecha de creación. Se genera solo, es único sin coordinación entre servidores, y reemplaza definitivamente el `Date.now()` usado como parche en el módulo anterior. Al viajar por JSON se ve como string; adentro de Mongoose sigue siendo un `ObjectId`.

</div>

---
layout: default
---

# Errores de Mongoose

```ts
app.use((err: any, req: Request, res: Response, next: NextFunction) => {
  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: err.message })
  }
  if (err.name === 'CastError') {
    return res.status(400).json({ error: 'ID inválido' })
  }
  console.error(err)
  res.status(500).json({ error: 'Algo salió mal' })
})
```

<div class="mt-2 text-sm opacity-80">

Mismo middleware de errores del módulo anterior, ahora distinguiendo dos casos típicos de Mongoose: `ValidationError` (violó una regla del schema) y `CastError` (un `id` que ni siquiera tiene la forma de un `ObjectId`) — ambos, errores del cliente (`400`), no del servidor.

</div>

---
layout: center
---

# Relaciones

---
layout: default
---

# Referenciar otra colección

```ts
const categorySchema = new Schema({
  name: { type: String, required: true },
})
const Category = model('Category', categorySchema)

const productSchema = new Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  category: { type: Schema.Types.ObjectId, ref: 'Category' },
})
const Product = model('Product', productSchema)
```

<div class="mt-1 text-sm opacity-80">

`ref: 'Category'` no guarda la categoría completa — guarda su `_id`, y le dice a Mongoose a qué modelo apunta. Es *referencing*, de la comparación de unas slides atrás.

</div>

---
layout: default
---

# Traer la relación con `populate`

```ts
const product = await Product.findById(id).populate('category')

console.log(product.category)
// { _id: '...', name: 'Periféricos' }   — no solo el id
```

<div class="mt-3 text-sm opacity-80">

Sin `populate`, `product.category` sería solo el `ObjectId` guardado. `populate('category')` hace, por dentro, una segunda consulta a `Category` y reemplaza el `id` por el documento completo — el equivalente de Mongoose a un `JOIN`, resuelto en dos pasos en vez de uno.

</div>

<div class="mt-1 text-xs opacity-60">

→ [mongoosejs.com/docs/populate](https://mongoosejs.com/docs/populate.html)

</div>

---
layout: default
---

# Índices: qué son y para qué sirven

- Una estructura auxiliar (por defecto, un **B-tree**) que Mongo mantiene ordenada por el valor de un campo — permite encontrar documentos sin recorrer la colección entera.
- Sin índice, buscar por `email` revisa **todos** los documentos (*collection scan*); con un índice, salta directo a los que coinciden.
- El costo: ocupa espacio en disco/memoria, y hace un poco más lenta cada escritura (hay que actualizar también el índice).

```ts
const userSchema = new Schema({
  email: { type: String, required: true, unique: true },
})
```

<div class="mt-1 text-xs opacity-80">

`unique: true` ya venía creando un índice único, sin nombrarlo como tal hasta ahora.

</div>

---
layout: default
---

# Índices compuestos

```ts
productSchema.index({ category: 1, price: -1 })
```

<div class="mt-3 text-sm opacity-80">

Un índice compuesto cubre **varios** campos a la vez — útil cuando una consulta filtra y ordena por más de uno, como "productos de esta categoría, del más caro al más barato". `1` = ascendente, `-1` = descendente: el **orden** de los campos importa, este índice acelera filtrar por `category` (solo, o junto con `price`), pero no acelera filtrar por `price` solo.

</div>

<div class="mt-1 text-xs opacity-60">

→ [mongodb.com/docs/manual/indexes](https://www.mongodb.com/docs/manual/indexes/)

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
<div>

**Schema y modelo**

| Forma | Ejemplo |
|---|---|
| Definir schema | `new Schema({ campo: {...} })` |
| Inferir el tipo | `InferSchemaType<typeof schema>` |
| Crear el modelo | `model<T>('Product', schema)` |
| Método/estático | `schema.methods.x` / `.statics.x` |
| Hook | `schema.pre('save', fn)` |
| Índice compuesto | `schema.index({ a: 1, b: -1 })` |

</div>
<div>

**CRUD y queries**

| Forma | Para qué |
|---|---|
| `Model.create(data)` | Crear |
| `Model.find()` / `findById(id)` | Leer |
| `.sort()` / `.skip()` / `.limit()` | Ordenar y paginar |
| `.select('campos')` | Traer solo ciertos campos |
| `findByIdAndUpdate(id, data, opts)` | Modificar |
| `findByIdAndDelete(id)` | Borrar |
| `.populate('campo')` | Traer una referencia completa |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [mongodb.com/docs](https://www.mongodb.com/docs/manual/) — documentación oficial de MongoDB
- [mongodb.com/products/compass](https://www.mongodb.com/products/compass) — interfaz gráfica oficial, para navegar la base sin código
- [mongoosejs.com](https://mongoosejs.com/docs/) — documentación oficial de Mongoose
- [mongoosejs.com/docs/typescript](https://mongoosejs.com/docs/typescript.html) — Mongoose + TypeScript, incluido `InferSchemaType`
- [mongoosejs.com/docs/validation](https://mongoosejs.com/docs/validation.html) — todas las validaciones de schema disponibles
- [mongoosejs.com/docs/middleware](https://mongoosejs.com/docs/middleware.html) — `pre`/`post` hooks, en profundidad
- [mongoosejs.com/docs/populate](https://mongoosejs.com/docs/populate.html) — referencias entre colecciones
- [mongodb.com/docs/manual/indexes](https://www.mongodb.com/docs/manual/indexes/) — tipos de índices y cuándo usarlos
- [mongodb.com/docs/manual/query-selectors](https://www.mongodb.com/docs/manual/reference/operator/query/) — todos los operadores de consulta (`$gte`, `$in`, `$or`...)
- [mongodb.com/atlas](https://www.mongodb.com/atlas) — base de datos gestionada, capa gratuita para proyectos chicos
- [npmjs.com/package/mongodb-memory-server](https://www.npmjs.com/package/mongodb-memory-server) — Mongo en memoria para tests, sin instalar nada
- [University de MongoDB](https://learn.mongodb.com/) — cursos gratuitos oficiales, con certificado

</div>
