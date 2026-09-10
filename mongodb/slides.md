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
layout: default
---

# Del array a una base real

<div class="mt-6 text-xl opacity-90">

El módulo anterior dejó una API completa — con un problema conocido de antemano.

</div>

<div class="mt-6 text-base opacity-80">

`products` era un array en memoria: cada vez que el servidor se reinicia, se pierde todo. Este módulo reemplaza ese array por una base de datos real — **MongoDB** — sin tocar las rutas ni los verbos HTTP ya construidos, solo lo que hay del otro lado de cada `req`/`res`.

</div>

```ts
// Node + Express, módulo anterior
const products: Product[] = [ /* ... */ ]
app.get('/products', (req, res) => res.json(products))
```

```ts
// Este módulo: la misma ruta, ahora contra una base real
app.get('/products', async (req, res) => {
  const products = await Product.find()
  res.json(products)
})
```

---
layout: default
---

# ¿Qué es una base NoSQL?

- **SQL** (SQL Server, ya visto en Estructura y Base de Datos): datos en **tablas** con filas y columnas fijas, relacionadas entre sí con claves foráneas y `JOIN`.
- **NoSQL** agrupa varios modelos que se apartan de eso — clave-valor, columnar, grafos, y el que usa MongoDB: **documentos**.
- Un documento es una estructura flexible tipo JSON — cada uno puede tener campos distintos, sin una tabla que los fuerce a ser todos iguales.

<div class="mt-4 text-sm italic opacity-80 text-center">

No es "mejor" que lo relacional — es un modelo distinto, con otros trade-offs, útil cuando los datos son naturalmente irregulares o anidados.

</div>

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

# Conseguir una base

```bash
# Opción 1: instalar MongoDB local
brew install mongodb-community   # macOS, con Homebrew
```

<div class="mt-2 text-sm opacity-80">

**Opción 2, recomendada para este curso:** [MongoDB Atlas](https://www.mongodb.com/atlas) — una base gestionada, gratis para proyectos chicos, sin instalar nada localmente. Da una *connection string* (`mongodb+srv://...`) lista para usar, que funciona igual desde cualquier máquina — útil para trabajar en equipo sin que cada quien tenga su propia base local desincronizada.

</div>

---
layout: default
---

# Instalar Mongoose

```bash
npm install mongoose
```

<div class="mt-4 text-sm opacity-80">

Se podría hablar directo con el driver oficial de MongoDB (`mongodb`), pero **Mongoose** agrega algo que ese driver no tiene: **schemas**. Define la forma esperada de cada documento, valida antes de guardar, y da una API más cómoda — la misma idea de "forma esperada" que una `interface` de TypeScript, ahora aplicada a lo que se persiste.

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

<div class="mt-3 text-sm opacity-80">

`mongoose.connect` es asíncrono — devuelve una Promise que se resuelve cuando la conexión queda lista. La *connection string* nunca va hardcodeada en el código: vive en `.env`, mismo patrón ya visto para `JWT_SECRET` en el módulo anterior.

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

Un `Schema` describe la forma de un documento — qué campos tiene, de qué tipo, y con qué reglas. `required: true` obliga a que el campo esté presente; `default` lo completa solo si no se manda. Mismo `interface Product` de siempre, ahora con las validaciones que TypeScript no puede expresar (van a existir siempre, en runtime — algo que TS, al borrarse en la compilación, no puede hacer).

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

`min` rechaza un precio o stock negativo; `trim` limpia espacios de más; `enum` limita `category` a un conjunto cerrado de valores — el mismo concepto que un *literal type* de TypeScript (`'electronics' | 'clothing' | 'books'`), acá aplicado del lado de la base, en runtime.

</div>

---
layout: default
---

# Crear el modelo

```ts
import mongoose, { Schema } from 'mongoose'

const productSchema = new Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  stock: { type: Number, default: 0 },
})

const Product = mongoose.model('Product', productSchema)

export default Product
```

<div class="mt-2 text-sm opacity-80">

`mongoose.model('Product', productSchema)` registra el schema y devuelve un **modelo**: el objeto que se usa para consultar y escribir en la colección `products` (Mongoose la pluraliza y minimiza el nombre solo). De acá en más, `Product` reemplaza al array en memoria.

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
app.post('/products', async (req, res) => {
  const product = await Product.create(req.body)
  res.status(201).json(product)
})
```

<div class="mt-4 text-sm opacity-80">

`Product.create(req.body)` valida contra el schema y guarda en un solo paso — si falta un campo `required` o `price` es negativo, la Promise rechaza antes de tocar la base, y el error llega al manejador centralizado ya visto en el módulo anterior.

</div>

---
layout: default
---

# Leer

```ts
app.get('/products', async (req, res) => {
  const products = await Product.find()
  res.json(products)
})

app.get('/products/:id', async (req, res) => {
  const product = await Product.findById(req.params.id)
  if (!product) return res.status(404).json({ error: 'No encontrado' })
  res.json(product)
})
```

<div class="mt-2 text-sm opacity-80">

`find()` sin argumentos trae todos los documentos de la colección; `findById` busca por `_id` — Mongoose lo convierte automáticamente desde el string que llega en `req.params.id`.

</div>

---
layout: default
---

# Modificar y borrar

```ts
app.put('/products/:id', async (req, res) => {
  const product = await Product.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
    runValidators: true,
  })
  if (!product) return res.status(404).json({ error: 'No encontrado' })
  res.json(product)
})

app.delete('/products/:id', async (req, res) => {
  await Product.findByIdAndDelete(req.params.id)
  res.status(204).end()
})
```

<div class="mt-1 text-xs opacity-80">

`new: true` hace que devuelva el documento **ya actualizado** (por defecto, Mongoose devuelve el anterior). `runValidators: true` corre las validaciones del schema también en un `update` — sin esto, se pueden colar datos inválidos que `create` sí habría rechazado.

</div>

---
layout: default
---

# El `_id` de Mongo

```ts
const product = await Product.findById('671f3a2b9e1c4a001f8b4567')

console.log(product._id)              // ObjectId('671f3a2b9e1c4a001f8b4567')
console.log(product._id.toString())   // '671f3a2b9e1c4a001f8b4567'
```

<div class="mt-3 text-sm opacity-80">

`_id` es un **ObjectId**, no un string — 12 bytes que codifican, entre otras cosas, la fecha de creación. Se genera solo, es único sin coordinación entre servidores (a diferencia de un contador incremental), y reemplaza definitivamente el `Date.now()` usado como parche en el módulo anterior. Al viajar por JSON se ve como string; adentro de Mongoose sigue siendo un `ObjectId`.

</div>

---
layout: default
---

# Errores de Mongoose

```ts
app.use((err, req, res, next) => {
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
const Category = mongoose.model('Category', categorySchema)

const productSchema = new Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  category: { type: Schema.Types.ObjectId, ref: 'Category' },
})
const Product = mongoose.model('Product', productSchema)
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

---
layout: default
---

# Índices

```ts
const userSchema = new Schema({
  email: { type: String, required: true, unique: true },
})
```

<div class="mt-4 text-sm opacity-80">

`unique: true` crea un **índice único** sobre `email` — Mongo rechaza cualquier intento de guardar un segundo documento con el mismo valor, a nivel de base de datos (no solo validado en el código). Un índice además acelera las búsquedas por ese campo, al costo de un poco más de espacio y de tiempo al escribir.

</div>

---
layout: default
---

# TypeScript + Mongoose

```ts
import mongoose, { Schema, Document } from 'mongoose'
interface Product {
  name: string
  price: number
  stock: number
}
interface ProductDocument extends Product, Document {}
const productSchema = new Schema<ProductDocument>({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  stock: { type: Number, default: 0 },
})
const ProductModel = mongoose.model<ProductDocument>('Product', productSchema)
```

<div class="mt-2 text-sm opacity-80">

`Schema<ProductDocument>` tipa el schema — `ProductModel.find()` ya devuelve documentos tipados, con autocompletado, en vez de `any`.

</div>

---
layout: default
---

# Variables de entorno

```bash
# .env
MONGO_URL=mongodb+srv://usuario:clave@cluster.mongodb.net/mi-app
```

```ts
import 'dotenv/config'
import mongoose from 'mongoose'

mongoose.connect(process.env.MONGO_URL!)
```

<div class="mt-3 text-sm opacity-80">

La *connection string* incluye usuario y contraseña — exactamente el tipo de secreto que nunca va al repositorio. Mismo patrón ya establecido: `.env` fuera de git, `.env.local` para overrides personales, nada hardcodeado en el código fuente.

</div>

---
layout: default
---

# Qué sigue

- La API ya persiste de verdad — reinicia el servidor todas las veces que quiera, los datos siguen ahí.
- El módulo de **Testing** puede ahora escribir tests de integración reales: `mongodb-memory-server` levanta una base temporal en memoria para cada corrida, sin tocar la base real ni necesitar Mongo instalado en la máquina que corre los tests.

<div class="mt-6 text-sm italic opacity-80 text-center">

React pide datos, Express los sirve, Mongo los guarda — el stack completo, de punta a punta.

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
| Definir schema | `new Schema({ name: { type: String, required: true } })` |
| Crear el modelo | `mongoose.model('Product', schema)` |
| Conectar | `mongoose.connect(url)` |
| Validación | `required`, `min`/`max`, `enum`, `unique` |
| Referencia | `{ type: ObjectId, ref: 'Category' }` |

</div>
<div>

**CRUD**

| Forma | Para qué |
|---|---|
| `Model.create(data)` | Crear |
| `Model.find()` / `findById(id)` | Leer |
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
- [mongoosejs.com](https://mongoosejs.com/docs/) — documentación oficial de Mongoose, incluida su guía de TypeScript
- [mongodb.com/atlas](https://www.mongodb.com/atlas) — base de datos gestionada, capa gratuita para proyectos chicos
- [mongoosejs.com/docs/validation.html](https://mongoosejs.com/docs/validation.html) — todas las validaciones de schema disponibles
- [mongoosejs.com/docs/populate.html](https://mongoosejs.com/docs/populate.html) — referencias entre colecciones, en profundidad
- [npmjs.com/package/mongodb-memory-server](https://www.npmjs.com/package/mongodb-memory-server) — Mongo en memoria para tests, sin instalar nada

</div>
