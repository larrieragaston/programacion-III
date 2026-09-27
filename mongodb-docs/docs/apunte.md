# MongoDB

## De un array a una base real

El módulo anterior dejó una API completa, con un problema conocido de antemano: `products` era un array en memoria — cada reinicio del servidor lo borra todo. Este módulo reemplaza ese array por una base de datos real, **MongoDB**, sin tocar las rutas ni los verbos HTTP ya construidos — solo lo que hay del otro lado de cada `req`/`res`.

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

Mismo endpoint, misma forma de respuesta — lo único que cambia es de dónde vienen los datos. Todo lo aprendido en Node+Express (rutas, middleware, CORS, autenticación) queda intacto; esta unidad agrega la capa de persistencia debajo.

## Tipos de bases de datos

### Cómo se dividen

```
Bases de datos
├── Relacionales (SQL)
│   └── PostgreSQL, MySQL, SQL Server, Oracle...
└── No relacionales (NoSQL)
    ├── Documentos    → MongoDB, Couchbase
    ├── Clave-valor   → Redis, DynamoDB
    ├── Columnares    → Cassandra, HBase
    └── Grafos        → Neo4j, ArangoDB
```

MongoDB es una base de **documentos** — una familia dentro de NoSQL, no un sinónimo de NoSQL en sí. "NoSQL" agrupa varios modelos de datos que se apartan del modelo relacional, cada uno resolviendo un problema distinto — no son intercambiables entre sí.

### El objetivo de cada tipo

<div class="card-grid card-grid-3">
<div class="info-card"><h4>Relacional (SQL)</h4>Datos muy estructurados, con relaciones claras y consistencia estricta (transacciones ACID).</div>
<div class="info-card tone-green" style="background:var(--vp-c-green-soft);border-color:#86efac"><h4>Documentos (MongoDB)</h4>Datos semi-estructurados o anidados, con un esquema que puede variar.</div>
<div class="info-card" style="background:var(--vp-c-blue-soft, #eff6ff);border-color:#93c5fd"><h4>Clave-valor (Redis)</h4>Lecturas/escrituras extremadamente rápidas de datos simples: cache, sesiones.</div>
<div class="info-card" style="background:#f3e8ff;border-color:#d8b4fe"><h4>Columnares (Cassandra)</h4>Volúmenes enormes de escritura distribuidos en muchos nodos: series de tiempo, big data.</div>
<div class="info-card tone-yellow" style="background:var(--vp-c-yellow-soft);border-color:#fcd34d"><h4>Grafos (Neo4j)</h4>Relaciones complejas entre entidades: redes sociales, recomendaciones.</div>
</div>

Ninguno de estos tipos reemplaza a los demás — un sistema real suele combinar más de uno (por ejemplo, MongoDB para el catálogo y Redis como cache de sesiones), eligiendo cada pieza según el problema puntual que resuelve.

### SQL vs. NoSQL

<div class="overflow-x-auto">

| | SQL | NoSQL (documentos) |
|---|---|---|
| Esquema | Rígido, definido de antemano | Flexible, puede variar por documento |
| Consistencia | Fuerte (ACID) | Eventual en muchos casos (modelo BASE) |
| Escalado típico | Vertical (más CPU/RAM al servidor) | Horizontal (más servidores, *sharding*) |
| Relaciones | `JOIN` entre tablas | *Embedding* o `populate` |

</div>

Ambos persisten datos, ambos se consultan e indexan — la elección depende de la forma de los datos, no de que uno sea "mejor". Aclaración honesta: desde 2018, Mongo también soporta transacciones ACID multi-documento — la distinción de la tabla es la más común en la práctica, no una regla absoluta que aplique siempre.

### MongoDB: un poco de historia

- **2007** — nace como proyecto interno (**10gen**), buscando una base de documentos para infraestructura propia a gran escala.
- **2009** — se libera como código abierto. El nombre viene de "humongous" (enorme).
- **2010** — con Node recién despegando, surge **Mongoose**: le agrega schemas y validación a Mongo, pensado específicamente para ese ecosistema — la librería que usa este módulo de acá en más.
- **2015** — **WiredTiger** se vuelve el motor de almacenamiento por defecto (versión 3.2), con mejor concurrencia y compresión que el motor original.
- **2016** — lanza **Atlas**, la versión gestionada en la nube — la que usa este curso.
- **Hoy** — soporte multi-modelo (búsqueda de texto, series de tiempo, transacciones ACID desde 2018).

<div class="practice-box">
<p class="practice-label">Para pensar</p>

La tabla de SQL vs. NoSQL compara dos extremos — pero un mismo proyecto real puede necesitar los dos (por ejemplo, MongoDB para el catálogo de productos y una base relacional para la facturación, donde la consistencia estricta importa más). ¿Qué parte de un e-commerce típico elegirías guardar en cada uno, y por qué?
</div>

## Documentos y colecciones

### Documentos como JSON

```json
{
  "_id": "671f3a2b9e1c4a001f8b4567",
  "name": "Mouse",
  "price": 18000,
  "stock": 5,
  "tags": ["periféricos", "oferta"]
}
```

Esto ya lo vienen mandando por la API desde React — un objeto JSON. La diferencia es que ahora, en vez de vivir un instante en memoria mientras dura el request, **se guarda así, tal cual**, en la base. `_id` lo genera Mongo automáticamente — reemplaza el `Date.now()` de práctica del módulo anterior por un identificador real, único de verdad.

### Tablas vs. colecciones

<div class="overflow-x-auto">

| SQL (relacional) | MongoDB (documentos) |
|---|---|
| Tabla | Colección |
| Fila | Documento |
| Columna | Campo |
| Clave primaria | `_id` |
| `JOIN` entre tablas | *Embedding* o *referencing* |

</div>

SQL **normaliza** (separar en tablas, unir con `JOIN`); Mongo permite **desnormalizar** — decidir a propósito qué guardar junto y qué separado, según cómo se vaya a leer. Además, acá el schema es flexible: cada documento puede variar, algo que una tabla SQL no permite sin alterar su estructura.

### Embedding vs. referencing

```json
// Embedding: todo en un solo documento
{ "name": "Mouse", "price": 18000, "category": { "name": "Periféricos" } }
```

```json
// Referencing: un id que apunta a otra colección
{ "name": "Mouse", "price": 18000, "category": "671f3a...b4321" }
```

**Embedding**: la categoría vive adentro del producto — rápido de leer (un solo documento), pero se duplica si varios productos comparten categoría. **Referencing**: el producto guarda el `_id` de su categoría, en una colección aparte — sin duplicar, al costo de un segundo pedido (o un `populate`, más adelante) para traer los datos completos. Ninguno es "el correcto" — es una decisión de diseño según cuántas veces se repite el dato embebido y cuánto cambia con el tiempo.

## Conectar el proyecto

### Conseguir una base: local o remota

<div class="card-grid card-grid-2">
<div class="info-card"><h4>Local</h4>

```bash
brew install mongodb-community
```

Corre en tu propia máquina (`mongodb://localhost:27017`). Cada quien tiene su propia base, sin compartir datos con el equipo.
</div>
<div class="info-card tone-green" style="background:var(--vp-c-green-soft);border-color:#86efac"><h4>Remota — MongoDB Atlas (recomendada)</h4>Base gestionada, capa gratis para proyectos chicos. Da una <em>connection string</em> (<code>mongodb+srv://...</code>) que funciona igual desde cualquier máquina.</div>
</div>

Para trabajar en equipo, Atlas evita el problema de "en mi máquina esto anda distinto" — todos apuntan a la misma base real, con la misma connection string.

### Explorar Mongo con Compass

**MongoDB Compass** es la interfaz gráfica oficial para conectarse y navegar una base — local o Atlas — sin escribir una sola línea de código. Antes de instalar Mongoose vale la pena abrirla:

- Descargar Compass, pegar la misma *connection string* de la base recién creada, conectar.
- Ver las bases que ya vienen por defecto (`admin`, `config`, `local`) — internas de Mongo, no para datos de la app.
- Crear a mano una base y una colección propia, e insertar un documento de prueba — verlo aparecer como JSON en el árbol de la izquierda.

El objetivo: entender qué es realmente un documento y una colección, antes de que Mongoose agregue una capa de abstracción encima. → [mongodb.com/products/compass](https://www.mongodb.com/products/compass)

<div class="practice-box">
<p class="practice-label">Practicá</p>

Instalá MongoDB Compass, conectate a una base (local o un cluster gratuito de Atlas), y creá a mano una colección `products` con dos o tres documentos de ejemplo, escritos directamente en la interfaz — sin una sola línea de código todavía.
</div>

## MongoDB en el proyecto de Node

### Instalar Mongoose

```bash
npm install mongoose
npm install -D @types/node
```

Se podría hablar directo con el driver oficial de MongoDB (`mongodb`), pero ese driver no valida nada — solo envía y trae documentos tal cual. **Mongoose** es un *ODM* (*Object Document Mapper*) para Node, que surge en 2010, muy pronto en la vida de Node: agrega **schemas** (la forma esperada de un documento), validación antes de guardar, y una API más cómoda — la misma idea de "forma esperada" que una `interface` de TypeScript, ahora aplicada a lo que se persiste.

### Conectar Express a Mongo

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

Mismo código de conexión para los dos casos — lo único que cambia es la *connection string*, fuera del código, en `.env`. `mongoose.connect` es asíncrono, así que conviene esperar a que la conexión esté lista antes de levantar el servidor (`app.listen`), evitando que lleguen requests cuando la base todavía no está disponible.

## Schemas y modelos

### Definir un schema

```ts
import { Schema } from 'mongoose'

const productSchema = new Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true },
  stock: { type: Number, default: 0 },
})
```

Un `Schema` describe la forma de un documento — qué campos tiene, de qué tipo, y con qué reglas. `required: true` obliga a que el campo esté presente; `default` lo completa solo si no se manda. Estas validaciones existen siempre, en runtime — algo que TypeScript, al borrarse en la compilación, no puede ofrecer por sí solo.

### Más validaciones

```ts
const productSchema = new Schema({
  name: { type: String, required: true, trim: true },
  price: { type: Number, required: true, min: 0 },
  stock: { type: Number, default: 0, min: 0 },
  category: { type: String, enum: ['electronics', 'clothing', 'books'] },
})
```

`min` rechaza un precio o stock negativo; `trim` limpia espacios de más; `enum` limita `category` a un conjunto cerrado de valores — el mismo concepto que un *literal type* de TypeScript (`'electronics' | 'clothing' | 'books'`), acá aplicado del lado de la base, en runtime.

### Constraints de un campo, en resumen

<div class="card-grid card-grid-2">
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

### Validación propia con `validate`

```ts
const userSchema = new Schema({
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

`match` alcanza para reglas simples (un formato de email); `validate` recibe una función propia para cualquier regla más específica, con un mensaje de error a medida — útil cuando la condición no se puede expresar con `min`/`max`/`enum` (por ejemplo, "el precio debe ser un múltiplo de 100").

### Crear el modelo, tipado

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

`mongoose.model(...)` registra el schema y devuelve un **modelo**: el objeto para consultar y escribir en la colección (Mongoose pluraliza y minimiza el nombre del modelo para nombrar la colección — `'Product'` se guarda en `products`). `InferSchemaType` lee el schema y arma el tipo solo — ya no hace falta escribir una `interface` aparte que, tarde o temprano, se desincroniza del schema real.

Este atajo alcanza mientras el modelo solo tenga datos. En cuanto agrega comportamiento propio (métodos, estáticos), Mongoose necesita conocer esa forma de antemano — es la próxima sección.

### Métodos de instancia y estáticos

```ts
interface ProductMethods {
  applyDiscount(pct: number): Promise<void>
}
type ProductModelType = Model<Product, {}, ProductMethods> & {
  findCheapest(): Promise<HydratedDocument<Product, ProductMethods> | null>
}

const productSchema = new Schema<Product, ProductModelType, ProductMethods>({
  /* los mismos campos de siempre */
})

productSchema.methods.applyDiscount = async function (pct: number) {
  this.price = this.price * (1 - pct)
  await this.save()
}
productSchema.statics.findCheapest = function () {
  return this.findOne().sort({ price: 1 })
}

const ProductModel = model<Product, ProductModelType>('Product', productSchema)
```

Un método de **instancia** opera sobre un documento ya cargado (`this` es el documento) — se llama como `producto.applyDiscount(0.1)`. Uno **estático** opera sobre el modelo completo (`this` es el modelo) — se llama como `ProductModel.findCheapest()`. Es la misma distinción entre métodos de instancia y de clase ya vista en POO.

El tipo extra (`ProductModelType`, construido con `Model`/`HydratedDocument` de Mongoose) es lo que le permite a TypeScript reconocer estas dos llamadas del lado de quien las usa — sin él, `producto.applyDiscount` compilaría como una propiedad inexistente, aunque el código funcione perfectamente en runtime. Es el precio de agregar comportamiento: `InferSchemaType` solo describe datos, no funciones.

### Middleware de schema: `pre` y `post`

```ts
import bcrypt from 'bcrypt'

userSchema.pre('save', async function () {
  if (!this.isModified('password')) return
  this.password = await bcrypt.hash(this.password, 10)
})
```

Mismo `bcrypt.hash` del módulo anterior — ahora corre solo, antes de cada guardado, sin que cada ruta tenga que acordarse de llamarlo. `isModified('password')` evita rehashear una contraseña que no cambió (por ejemplo, al actualizar solo el email). Con una función `async`, Mongoose espera la Promise sola — no hace falta un `next()` manual, a diferencia de versiones más viejas de la librería. `post('save', ...)` existe igual, para correr algo justo después de guardar (por ejemplo, enviar un email de bienvenida).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Armá un modelo `User` con `email` (único, con `match` de formato) y `password`, y agregale un `pre('save')` que hashee la contraseña con `bcrypt` solo si cambió. Confirmá creando un usuario y mirando en Compass que el campo `password` nunca se ve en texto plano.
</div>

## CRUD contra Mongo

### Crear

```ts
import { Request, Response } from 'express'

app.post('/products', async (req: Request, res: Response) => {
  const product = await ProductModel.create(req.body)
  res.status(201).json(product)
})
```

`ProductModel.create(req.body)` valida contra el schema y guarda en un solo paso — si falta un campo `required` o `price` es negativo, la Promise rechaza antes de tocar la base, y el error llega al manejador centralizado ya visto en el módulo anterior.

### Leer

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

`find()` sin argumentos trae todos los documentos; `findById` busca por `_id` — Mongoose lo convierte automáticamente desde el string que llega en `req.params.id`.

### Queries más útiles

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

`$gte`/`$lte`/`$gt` son operadores de comparación de Mongo — hay muchos más (`$in` para "está en esta lista", `$or` para condiciones alternativas, `$regex` para texto) documentados en la [referencia de operadores de consulta](https://www.mongodb.com/docs/manual/reference/operator/query/).

### Las mismas queries, en Compass

```
// Barra de Filter
{ category: "electronics", price: { $gte: 10000, $lte: 50000 } }

// Barra de Sort
{ price: -1 }
```

Compass no tiene un lenguaje propio: su barra de **Filter** acepta exactamente la misma sintaxis que el argumento de `.find()` en Mongoose, y la de **Sort** la de `.sort()` — lo que se prueba ahí se puede pegar directo en el código, y viceversa. Es una forma rápida de armar y probar un filtro complejo antes de escribirlo en TypeScript, viendo los resultados al instante.

### Modificar y borrar

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

`new: true` hace que devuelva el documento **ya actualizado** (por defecto, Mongoose devuelve el anterior). `runValidators: true` corre las validaciones del schema también en un `update` — sin esto, se pueden colar datos inválidos que `create` sí habría rechazado, porque por defecto Mongoose solo valida al crear.

### El `_id` de Mongo

```ts
const product = await ProductModel.findById('671f3a2b9e1c4a001f8b4567')

console.log(product._id)              // ObjectId('671f3a2b9e1c4a001f8b4567')
console.log(product._id.toString())   // '671f3a2b9e1c4a001f8b4567'
```

`_id` es un **ObjectId**, no un string — 12 bytes que codifican, entre otras cosas, la fecha de creación. Se genera solo, es único sin coordinación entre servidores (a diferencia de un contador incremental, que necesitaría sincronizarse entre instancias), y reemplaza definitivamente el `Date.now()` usado como parche en el módulo anterior. Al viajar por JSON se ve como string; adentro de Mongoose sigue siendo un `ObjectId`.

### Errores de Mongoose

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

Mismo middleware de errores del módulo anterior, ahora distinguiendo dos casos típicos de Mongoose: `ValidationError` (violó una regla del schema) y `CastError` (un `id` que ni siquiera tiene la forma de un `ObjectId`, por ejemplo `"abc"`) — ambos, errores del cliente (`400`), no del servidor.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Sobre tu propio modelo `Product`, armá las cinco rutas del CRUD contra Mongo (reemplazando el array en memoria del módulo anterior) y probá cada una con `curl`. Confirmá con Compass, después de cada operación, que la colección realmente refleja el cambio.
</div>

## Relaciones

### Referenciar otra colección

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

`ref: 'Category'` no guarda la categoría completa — guarda su `_id`, y le dice a Mongoose a qué modelo apunta. Es *referencing*, de la comparación vista antes.

### Traer la relación con `populate`

```ts
const product = await Product.findById(id).populate('category')

console.log(product.category)
// { _id: '...', name: 'Periféricos' }   — no solo el id
```

Sin `populate`, `product.category` sería solo el `ObjectId` guardado. `populate('category')` hace, por dentro, una segunda consulta a `Category` y reemplaza el `id` por el documento completo — el equivalente de Mongoose a un `JOIN`, resuelto en dos pasos en vez de uno. → [mongoosejs.com/docs/populate](https://mongoosejs.com/docs/populate.html)

### Índices: qué son y para qué sirven

- Una estructura auxiliar (por defecto, un **B-tree**) que Mongo mantiene ordenada por el valor de un campo — permite encontrar documentos sin recorrer la colección entera.
- Sin índice, buscar por `email` revisa **todos** los documentos (*collection scan*); con un índice, salta directo a los que coinciden.
- El costo: ocupa espacio en disco/memoria, y hace un poco más lenta cada escritura (hay que actualizar también el índice) — no conviene indexar todo, solo lo que realmente se consulta seguido.

```ts
const userSchema = new Schema({
  email: { type: String, required: true, unique: true },
})
```

`unique: true` ya venía creando un índice único, desde la primera vez que apareció en este apunte, sin nombrarlo como tal hasta ahora.

### Índices compuestos

```ts
productSchema.index({ category: 1, price: -1 })
```

Un índice compuesto cubre **varios** campos a la vez — útil cuando una consulta filtra y ordena por más de uno, como "productos de esta categoría, del más caro al más barato". `1` = ascendente, `-1` = descendente: el **orden** de los campos importa, este índice acelera filtrar por `category` (solo, o junto con `price`), pero no acelera filtrar por `price` solo. → [mongodb.com/docs/manual/indexes](https://www.mongodb.com/docs/manual/indexes/)

<div class="practice-box">
<p class="practice-label">Practicá</p>

Agregale a tu modelo `Product` una referencia a un modelo `Category` nuevo, con `ref`. Escribí una ruta que traiga un producto con su categoría ya resuelta (`populate`), y agregale un índice compuesto sobre `category` + `price` — confirmá con `explain()` en Compass (pestaña Explain Plan) que la consulta usa ese índice.
</div>

## Cheat sheet

<div class="card-grid card-grid-2">
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

## Referencias y recursos

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

## Cierre

El array en memoria de Node+Express era la pieza más frágil de todo el stack — se perdía con cada reinicio. Este módulo lo reemplaza por persistencia real, sobre exactamente las mismas rutas: nada de lo aprendido en el módulo anterior se descarta, se le agrega una capa debajo. El próximo tema (Testing) retoma este mismo proyecto para escribir tests de integración reales contra la base, sin necesitar Mongo instalado en la máquina que corre los tests.
