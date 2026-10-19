# Node + Express — Guía de ejercicios

Como en React, acá tampoco hay ejercicios sueltos: es la construcción incremental de una sola API — el backend real del mismo catálogo de productos — donde cada ejercicio agrega una pieza nueva sobre lo que ya se armó en el anterior, en el mismo proyecto.

Esto **no es el proyecto integrador** de la materia — es una API chica, acotada, pensada para practicar todo lo visto en este módulo de forma conectada, no para entregar.

Un detalle importante: esta guía está diseñada a propósito para que, al terminarla, tengas exactamente la API que el catálogo de React (guía de ejercicios de ese módulo) necesita — mismas rutas, misma forma de los datos. El `interface Product` de React tenía `name`, `price` y `stock`, y sumó `category` en el ejercicio 15; acá se arranca directamente con las cuatro, más un `id`. El último ejercicio de esta guía es, literalmente, volver al proyecto de React y apuntarlo a esta API real.

## 1. Preparar el proyecto

1. Crear una carpeta `products-api`, correr `npm init -y` adentro.
2. Instalar Express y las herramientas de TypeScript: `npm install express` y `npm install -D typescript @types/express @types/node tsx`.
3. Crear un `tsconfig.json` con `module`/`moduleResolution` en `"NodeNext"`, `strict: true` y `outDir`/`rootDir` apuntando a `dist`/`src`.
4. Crear las carpetas `src/routes/`, `src/controllers/`, `src/middleware/`, `src/services/`, `src/data/` (todavía vacías) — se van a ir llenando a medida que avanza la guía.
5. Crear `src/app.ts` (arma la `app`, sin escuchar nada) y `src/index.ts` (la importa y recién ahí llama a `app.listen`) — separados desde el principio, para no tener que reorganizar más adelante cuando aparezcan los tests.

## 2. Primer endpoint

1. En `app.ts`, crear `const app = express()` y una ruta `GET /` que responda `res.json({ status: 'ok' })`, tipando `req`/`res` con `Request`/`Response` de Express.
2. Exportar `app` como default.
3. En `index.ts`, importar `app`, definir `const PORT = 4000` y llamar a `app.listen(PORT, () => console.log(...))`.
4. Correr el servidor con `npx tsx src/index.ts` y confirmar la respuesta con el navegador o `curl http://localhost:4000`.

## 3. El catálogo, en memoria

1. Declarar en `src/data/products.ts`:
   ```ts
   export interface Product {
     id: number
     name: string
     price: number
     stock: number
     category: string
   }
   export const products: Product[] = [ /* al menos cinco, con categorías distintas */ ]
   ```
2. Agregar a `app.ts` una ruta `GET /products` que devuelva el array completo con `res.json(products)`.
3. Agregar `GET /products/:id` que busque por `id` (`Number(req.params.id)`) y responda `404` si no existe.
4. Probar las dos rutas con `curl`, incluyendo un `id` inexistente para confirmar el `404`.

## 4. Crear productos

1. Agregar `app.use(express.json())` **antes** de las rutas que lo necesiten — sin esto, `req.body` va a ser `undefined`.
2. Agregar `POST /products`, que arme un producto nuevo con `{ id: Date.now(), ...req.body }`, lo agregue al array y responda `201` con el producto creado.
3. Probar con `curl -X POST ... -H "Content-Type: application/json" -d '{"name":"...", "price":..., "stock":..., "category":"..."}'` y confirmar que aparece después en `GET /products`.

## 5. Modificar y borrar

1. Agregar `PUT /products/:id`: buscar el índice, responder `404` si no existe, y si existe reemplazar combinando `{ ...products[index], ...req.body }`.
2. Agregar `DELETE /products/:id`: buscar el índice, responder `404` si no existe, y si existe sacarlo del array con `splice` y responder `204` sin body.
3. Confirmar las tres rutas nuevas (`POST`, `PUT`, `DELETE`) con `curl`, revisando que `GET /products` refleje cada cambio.

## 6. Organizar con `Router` y controllers

1. Mover toda la lógica de las rutas de productos a funciones en `src/controllers/products.ts` (`getAllProducts`, `getProductById`, `createProduct`, `updateProduct`, `deleteProduct`), cada una tipada con `Request`/`Response`.
2. Crear `src/routes/products.ts` con un `Router()` que conecte cada verbo/URL con su controller.
3. En `app.ts`, reemplazar las rutas sueltas por `app.use('/products', productsRouter)`.
4. Confirmar que las cinco operaciones siguen funcionando exactamente igual — este ejercicio reorganiza el código, no cambia el comportamiento.

## 7. Middleware propio: logger

1. Escribir un middleware `logger(req, res, next)` en `src/middleware/logger.ts` que imprima `${req.method} ${req.url}` por consola, tipando los tres parámetros (`Request`, `Response`, `NextFunction`).
2. Registrarlo con `app.use(logger)`, **antes** de las rutas.
3. Confirmar, mirando la consola del servidor, que cada request hecha con `curl` o el navegador deja su línea — y que si el middleware no llama a `next()`, la request se queda colgada (probalo comentando el `next()` un momento, y volvé a ponerlo).

## 8. Manejo de errores centralizado

1. Elegir una ruta (por ejemplo `GET /products/:id`) y envolver su lógica en `try`/`catch`, llamando a `next(err)` en el `catch` en vez de responder ahí mismo.
2. Agregar, al final de `app.ts` (después de todas las rutas), un middleware de cuatro parámetros `(err, req, res, next)` que loguee el error y responda `500` con `{ error: err.message }`.
3. Forzar un error a propósito (por ejemplo, lanzando `throw new Error('probando')` en algún handler) y confirmar que lo captura el middleware final, no un stack trace crudo en la terminal.

## 9. CORS: conectar con React

1. Instalar `cors` y sus tipos (`npm install cors` / `npm install -D @types/cors`).
2. Agregar `app.use(cors())` en `app.ts`.
3. Si ya tenés el proyecto de React de la guía anterior, cambiar su `fetch`/Axios para apuntar a `http://localhost:4000` y confirmar en la consola del navegador que el error de CORS desaparece y el catálogo real llega a React (por ahora, van a ser datos distintos a los simulados — eso se resuelve del todo en el ejercicio 18).

## 10. Variables de entorno

1. Instalar `dotenv`.
2. Crear `.env.development` con `PORT=4000`.
3. Al principio de `index.ts`, llamar a `dotenv.config({ path: '.env.development' })` y leer el puerto con `Number(process.env.PORT) || 4000`.
4. Confirmar que cambiar el valor en `.env.development` efectivamente cambia el puerto en el que arranca el servidor.

## 11. Usuarios y contraseñas hasheadas

1. Instalar `bcrypt` y sus tipos.
2. Crear `src/data/users.ts` con `interface User { id: number; email: string; passwordHash: string; role: 'admin' | 'client' }`.
3. Escribir un script chico y descartable (o usar el REPL de Node) que llame a `bcrypt.hash('unaContraseña', 10)` y pegue el resultado como `passwordHash` de un usuario de ejemplo en el array — así el array arranca con una contraseña real, ya hasheada, nunca en texto plano.

## 12. Login con JWT

1. Instalar `jsonwebtoken` y sus tipos, y agregar `JWT_SECRET=algo-secreto` a `.env.development`.
2. Crear `POST /auth/login` que reciba `{ email, password }`, busque el usuario por email, compare la contraseña con `bcrypt.compare`, y responda `401` con el mismo mensaje genérico si el email no existe **o** si la contraseña no coincide.
3. Si las credenciales son válidas, firmar un token con `jwt.sign({ userId: user.id, role: user.role }, process.env.JWT_SECRET!, { expiresIn: '1h' })` y responderlo como `{ token }`.
4. Probar con `curl`, primero con credenciales incorrectas (esperando `401`) y después con las correctas (esperando el token).

## 13. Middleware de autenticación

1. Escribir `requireAuth(req, res, next)` en `src/middleware/requireAuth.ts`: leer el header `Authorization`, extraer el token (`"Bearer <token>"`), verificarlo con `jwt.verify`, y si es válido guardar el resultado en `req.user` y seguir; si falta o es inválido, responder `401`.
2. Agregar la augmentación de tipos (`declare global { namespace Express { interface Request { user?: any } } }`) para que `req.user` no rompa la compilación.
3. Crear `GET /profile`, protegida con `requireAuth`, que responda `{ userId: req.user.userId }`.
4. Confirmar con `curl`: sin token da `401`; con el token del login anterior, responde el `userId` correcto.

## 14. Autorización por rol

1. Escribir `requireAdmin(req, res, next)` que responda `403` si `req.user.role !== 'admin'`, y llame a `next()` si sí.
2. Proteger `DELETE /products/:id` con ambos middlewares encadenados: `requireAuth, requireAdmin`.
3. Confirmar tres casos con `curl`: sin token (`401`), con token de un usuario sin rol admin (`403`), y con token de un usuario admin (`204`, el producto se borra).

## 15. Reorganizar según el scaffolding recomendado

1. Revisar tu proyecto contra la estructura del apunte (`routes/`, `controllers/`, `middleware/`, `services/`, `data/`, `app.ts`, `index.ts`) y mover lo que haya quedado fuera de lugar — por ejemplo, si `bcrypt`/`jwt.sign` quedaron sueltos dentro del controller de auth, este es el momento de extraerlos a `services/auth.ts`.
2. Confirmar que `app.ts` sigue sin llamar a `.listen` en ningún lado — es lo que va a permitir testear con `supertest` en el ejercicio siguiente sin levantar un puerto real.

## 16. Testear con Vitest y `supertest`

1. Instalar `vitest` y `supertest` (con `@types/supertest` si hace falta).
2. Escribir un test que importe `app` desde `app.ts` y confirme que `GET /products` responde `200` con un array (`expect(res.body).toBeInstanceOf(Array)` o `toHaveLength(...)` según cuántos productos sembraste).
3. Escribir un segundo test para `POST /auth/login` con credenciales inválidas, confirmando `401`.
4. Correr `npx vitest run` y confirmar que los dos tests pasan.

## 17. Mockear un servicio

1. Crear un servicio ficticio `src/services/notifications.ts` con una función `notifyNewProduct(name: string): void` (por ahora, solo un `console.log`).
2. Llamarla desde el controller `createProduct`, después de agregar el producto al array.
3. En el test de creación (nuevo, para `POST /products`), usar `vi.mock('../services/notifications')` y confirmar con `expect(notifyNewProduct).toHaveBeenCalledWith(...)` que se llamó con el nombre correcto — sin que el test dependa de lo que esa función realmente haga.

## 18. Cerrar el círculo con React

1. En el proyecto de React (guía de ejercicios de ese módulo), confirmar que `services/api.ts` usa `baseURL: import.meta.env.VITE_API_URL` y que `.env.development` apunta a `http://localhost:4000/` (ejercicio 19 de esa guía).
2. Con las dos aplicaciones corriendo (`npm run dev` en React, `npx tsx src/index.ts` acá), confirmar que el catálogo que se ve en React es, ahora sí, exactamente el array de `data/products.ts` de esta API — no el simulado de `fetchProducts`.
3. Confirmar que el formulario de Ant Design para cargar un producto nuevo (ejercicio 20 de React) efectivamente crea un producto acá, vía `POST /products`, y que aparece en el catálogo al recargar.
4. El login de React (ejercicio 21 de esa guía) simulaba un token fijo, sin backend real. Como upgrade — no hace falta rehacer esa guía — probá reemplazar esa simulación por una llamada real a `POST /auth/login` de esta API, guardando el token que realmente devuelve el servidor.

## 19. Checklist final

- [ ] Las cinco operaciones sobre `/products` (`GET` lista, `GET` por id, `POST`, `PUT`, `DELETE`) funcionando con `express.Router()` y controllers separados.
- [ ] Un middleware propio (el logger) y un manejo de errores centralizado, sin `try`/`catch` repetido en cada ruta.
- [ ] CORS habilitado y confirmado contra un frontend real.
- [ ] Login con `bcrypt` + JWT, y al menos una ruta protegida con `requireAuth`, y otra con `requireAuth` + `requireAdmin`.
- [ ] Variables de entorno (`PORT`, `JWT_SECRET`) fuera del código, vía `dotenv`.
- [ ] Al menos tres tests pasando con Vitest, incluyendo uno con `supertest` y uno con un mock.
- [ ] El catálogo de React (del módulo anterior) mostrando datos reales de esta API, no los simulados.

## Para pensar

- El mensaje de error de `POST /auth/login` es a propósito el mismo para "no existe el email" y "la contraseña no coincide". ¿Qué otro endpoint de esta misma API se beneficiaría de ese mismo criterio (no distinguir en la respuesta entre dos motivos de fallo distintos)?
- `Date.now()` como `id` en el ejercicio 4 es una solución de práctica. ¿Qué escenario concreto lo rompería en producción? ¿Alcanza con cambiar a un contador incremental en memoria, o el problema de fondo es otro (que los datos viven en un array que se pierde en cada reinicio)?
- Esta guía separó `app.ts` de `index.ts` desde el ejercicio 1, antes de que hiciera falta para nada. ¿En qué otro punto de la guía de React se tomó una decisión parecida — separar algo *antes* de necesitarlo, pensando en un paso posterior?
- El próximo tema reemplaza el array de `data/products.ts` por una colección real de MongoDB, sin tocar las rutas ni los controllers desde afuera. Mirando tu propio código: ¿qué archivos vas a tener que tocar vos para ese cambio, y cuáles deberían quedar exactamente iguales?
