# MongoDB — Guía de ejercicios

Como con Node + Express, tampoco acá hay ejercicios sueltos: esta guía **continúa el mismo proyecto** de la guía anterior — el mismo servidor Express, las mismas rutas — reemplazando el array en memoria por persistencia real en MongoDB, paso a paso.

Esto **no es el proyecto integrador** de la materia — es la continuación natural de la API que venías construyendo, para practicar todo lo visto en este módulo de forma conectada.

Un detalle importante: el objetivo final de esta guía es que, al terminarla, tu API tenga exactamente el mismo contrato (mismas rutas, misma forma de respuesta) que ya usa el catálogo de React — la única diferencia visible desde afuera va a ser que, al reiniciar el servidor, los datos siguen ahí.

## 1. Conseguir una base y explorarla con Compass

1. Crear un cluster gratuito en [MongoDB Atlas](https://www.mongodb.com/atlas) (recomendado) o instalar MongoDB local (`brew install mongodb-community`).
2. Instalar [MongoDB Compass](https://www.mongodb.com/products/compass) y conectarlo con la *connection string* de tu base.
3. Sin escribir código todavía: crear a mano, desde Compass, una base `mi-app` con una colección `products` y un documento de prueba — para ver qué pinta tiene un documento real antes de que Mongoose entre en escena.

## 2. Instalar Mongoose y conectar

1. En tu proyecto de Node + Express, instalar Mongoose: `npm install mongoose`.
2. Agregar `MONGO_URL` a `.env.development` (tu base local o de prueba) y a `.env.production` (la connection string de Atlas).
3. Escribir una función `connectDB()` asíncrona que llame a `mongoose.connect(process.env.MONGO_URL!)`, y llamarla **antes** de `app.listen` en `index.ts` — para no aceptar requests mientras la conexión todavía no está lista.

## 3. El schema de `Product`

1. Reemplazar el `interface Product` de la guía anterior por un `Schema` de Mongoose con los mismos campos (`name`, `price`, `stock`, `category`), agregando `required`/`min`/`trim` donde corresponda.
2. Usar `InferSchemaType<typeof productSchema>` para derivar el tipo `Product`, sin escribir una interfaz aparte.
3. Crear el modelo con `model<Product>('Product', productSchema)` y exportarlo — este `ProductModel` reemplaza al array `products` de acá en más.

## 4. CRUD contra Mongo

1. Reemplazar cada ruta del CRUD en memoria (`GET /products`, `GET /products/:id`, `POST /products`, `PUT /products/:id`, `DELETE /products/:id`) por su equivalente contra `ProductModel` (`find`, `findById`, `create`, `findByIdAndUpdate` con `{ new: true, runValidators: true }`, `findByIdAndDelete`).
2. Probar cada ruta con `curl` y confirmar que responde exactamente igual que antes (mismos status codes, misma forma de JSON) — el contrato con React no debería notar la diferencia.
3. Después de cada operación, refrescar la colección en Compass y confirmar visualmente que el cambio realmente se guardó.

## 5. Manejo de errores de Mongoose

1. Extender el middleware de errores centralizado para distinguir `ValidationError` (responder `400` con el mensaje del schema) y `CastError` (responder `400` con `"ID inválido"`) de cualquier otro error (`500`).
2. Probar creando un producto sin `name` (esperando `400`, no un `500` genérico) y pidiendo `GET /products/no-es-un-id` (esperando `400` por `CastError`, no un `404`).

## 6. Queries más ricas

1. Agregar un query param opcional a `GET /products` para filtrar por categoría: `?category=electronics` arma un filtro `{ category: req.query.category }` solo si el parámetro vino.
2. Agregar `?sort=price` que ordene los resultados con `.sort({ price: 1 })` cuando esté presente.
3. Antes de escribir el código, probá el filtro y el sort equivalentes directamente en las barras de Filter/Sort de Compass — confirmá que devuelven lo mismo que tu endpoint.

## 7. `Category` como su propio modelo

1. Crear un modelo `Category` con un campo `name` (`required`, `unique`).
2. Cambiar el campo `category` de `Product`, de string libre a `{ type: Schema.Types.ObjectId, ref: 'Category' }`.
3. Agregar `.populate('category')` a la ruta `GET /products/:id`, para que devuelva el producto con la categoría ya resuelta, no solo su `id`.
4. Crear una ruta `POST /categories` para poder cargar categorías antes de asignarlas a un producto.

## 8. Usuarios reales, con hash automático

1. Crear un modelo `User` con `email` (`required`, `unique`, con `match` de formato) y `password` (`required`).
2. Agregarle un `pre('save')` que hashee la contraseña con `bcrypt` solo si cambió (`this.isModified('password')`).
3. Reemplazar el array `users` en memoria de la guía anterior por este modelo: `POST /auth/login` ahora busca con `UserModel.findOne({ email })` en vez de `.find()` sobre un array.

## 9. Índices

1. Confirmar en Compass (pestaña *Indexes* de la colección `users`) que `email` ya tiene un índice único — creado solo por el `unique: true` del schema.
2. Agregarle a `Product` un índice compuesto sobre `category` y `price` (`productSchema.index({ category: 1, price: -1 })`), pensado para la consulta combinada del ejercicio 6.

## 10. Métodos y estáticos en el modelo

1. Agregarle a `Product` un método de instancia `applyDiscount(pct: number)` que reduzca el precio y guarde el documento.
2. Agregarle un método estático `findCheapest()` que devuelva el producto más barato (`findOne().sort({ price: 1 })`).
3. Exponer una ruta (por ejemplo `POST /products/:id/discount`) que use el método de instancia, y otra (`GET /products/cheapest`) que use el estático.

## 11. Cerrar el círculo: reiniciar el servidor

1. Con el servidor corriendo y algunos productos cargados, apagalo (`Ctrl+C`) y volvé a levantarlo.
2. Pedí `GET /products` de nuevo — los datos siguen ahí. Esto era, literalmente, el problema que abrió el módulo de Node + Express: un array en memoria no sobrevive un reinicio, y ahora sí.
3. Confirmá que el catálogo de React (guía de ese módulo) también sigue mostrando esos mismos datos, sin haber cambiado una línea del lado del frontend.

## Checklist final

- [ ] `Product` y `Category` como modelos de Mongoose, con validaciones (`required`, `min`, `enum` donde corresponda) y sin interfaces duplicadas (`InferSchemaType`).
- [ ] Las cinco rutas del CRUD funcionando contra Mongo, con el mismo contrato que tenían contra el array en memoria.
- [ ] Manejo de errores distinguiendo `ValidationError`/`CastError` (`400`) de errores inesperados (`500`).
- [ ] Al menos un filtro y un sort agregados a `GET /products`, probados primero en Compass.
- [ ] `Category` referenciada desde `Product`, con al menos una ruta que use `populate`.
- [ ] `User` con contraseña hasheada automáticamente vía `pre('save')`, nunca en texto plano.
- [ ] Al menos un índice compuesto y confirmación del índice único en `email`.
- [ ] Al menos un método de instancia y uno estático, cada uno expuesto en una ruta.
- [ ] El servidor reiniciado, con los datos todavía ahí.

## Para pensar

- El ejercicio 4 pide que el contrato con React "no note la diferencia" al migrar del array a Mongo. ¿Qué parte de tu código de rutas tuviste que tocar para lograrlo, y qué parte quedó exactamente igual? ¿Qué te dice eso sobre dónde conviene poner la "frontera" entre rutas y persistencia?
- `runValidators: true` en el `PUT` es fácil de olvidar, porque sin él el código igual "funciona" — hasta que alguien manda un dato inválido en un update. ¿Qué otro lugar de esta guía tiene el mismo tipo de trampa (algo que compila y corre, pero deja pasar silenciosamente un caso que debería rechazarse)?
- El próximo módulo (Testing) va a escribir tests de integración contra este mismo proyecto, usando `mongodb-memory-server` para no depender de tu base real. Mirando los modelos que armaste en esta guía: ¿cuáles te parece que son más importantes de testear primero, y por qué?
