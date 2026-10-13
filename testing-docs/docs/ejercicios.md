# Testing — Guía de ejercicios

Esta guía no arranca un proyecto nuevo: **cierra** el que vienen construyendo desde React — el mismo catálogo, la misma API de Node + Express, la misma base de MongoDB. Acá no se agrega ninguna pantalla ni ninguna ruta nueva (salvo una, en el ejercicio de TDD) — se agregan los tests que confirman que todo lo construido en las tres guías anteriores funciona, y se automatiza para que siga funcionando.

Esto **no es el proyecto integrador** de la materia — es la continuación natural de lo que ya tenés andando, para practicar todo lo visto en este módulo de forma conectada.

## 1. Instalar Vitest y supertest

1. En el proyecto de Node + Express (el mismo de las guías anteriores), instalar `vitest` y, si todavía no está, `supertest` (`npm install -D vitest supertest @types/supertest`).
2. Agregar un script `"test": "vitest run"` a `package.json`.
3. Crear una carpeta `tests/` junto a `src/`, separada de `e2e/` (que vas a crear más adelante en esta misma guía).

## 2. Primer test unitario

1. Elegí un método que no dependa de la base — por ejemplo, el método de instancia `applyDiscount` del modelo `Product` que armaste en la guía de MongoDB.
2. Escribí un test unitario puro: construí un objeto con la forma esperada (sin guardarlo en la base), llamá al método, y verificá el resultado con el patrón **Arrange / Act / Assert**.
3. Confirmá que corre en milisegundos — no debería necesitar conexión a Mongo para nada.

## 3. Tests de integración con `mongodb-memory-server`

1. Instalar `mongodb-memory-server` (`npm install -D mongodb-memory-server`).
2. En un archivo de setup de tests, levantar una instancia en memoria antes de todos los tests (`beforeAll`) y conectarla con Mongoose, y cerrarla después (`afterAll`) — nunca contra tu base real ni la de Atlas.
3. Escribí un test de integración real con `supertest` contra `GET /products`: sembrá uno o dos productos directamente con el modelo antes del test, y confirmá que el endpoint los devuelve.

## 4. Testear el resto del CRUD

1. Sumá tests de integración para `POST /products` (un caso válido y uno que debería fallar por falta de un campo `required`), `PUT /products/:id` y `DELETE /products/:id`.
2. Para cada ruta, usá `it.each` donde tenga sentido (por ejemplo, varios casos de validación inválida) en vez de repetir el mismo test con mínimos cambios.
3. Limpiá la colección entre tests (`beforeEach` con un `deleteMany({})`) para que no queden datos de un test afectando al siguiente — tests independientes, como vimos en buenas prácticas.

## 5. Mockear una dependencia

1. Si tu endpoint de login llama a algo externo (un email de bienvenida, por ejemplo) o usa `bcrypt` para hashear, elegí uno de los dos para mockear en un test de `POST /auth/login`.
2. Usá `vi.mock(...)` y `vi.mocked(...)` (visto en "TypeScript en los tests") para que el mock quede tipado.
3. Confirmá con `toHaveBeenCalledWith(...)` que la dependencia se llamó con los argumentos esperados, sin depender de que el servicio real esté disponible.

## 6. TDD: una funcionalidad nueva, con red-green-refactor

1. Elegí una funcionalidad chica que todavía no exista — por ejemplo, un endpoint `GET /products/low-stock` que devuelva los productos con `stock` menor a un umbral.
2. **Red**: escribí primero el test de integración que la prueba, confirmá que falla (la ruta ni existe).
3. **Green**: escribí el código mínimo en el controller y la ruta para que el test pase.
4. **Refactor**: con el test en verde, movelo a su propio controller si hace falta, limpiá nombres, agregá validación del query param del umbral si lo tiene.

## 7. Coverage

1. Instalar `@vitest/coverage-v8` y correr `npx vitest run --coverage`.
2. Abrir `coverage/index.html` y revisar qué archivo quedó con menor cobertura — probablemente el manejo de errores o alguna rama de validación que ningún test ejercitó todavía.
3. Escribí al menos un test nuevo apuntado específicamente a cerrar ese hueco, y confirmá que el porcentaje sube.
4. Configurá un umbral (`coverage.thresholds` en `vitest.config.ts`, por ejemplo 60% en líneas) y confirmá que `vitest run --coverage` falla si lo bajás a propósito.

## 8. Pre-commit hooks con Husky

1. Instalar `husky` y `lint-staged`, correr `npx husky init`.
2. Configurar `.lintstagedrc.json` para correr `vitest related --run` sobre los `.ts` modificados.
3. Rompé un test a propósito, intentá hacer `git commit`, y confirmá que Git lo rechaza. Arreglalo y confirmá que el commit pasa.

## 9. CI con GitHub Actions y branch protection

1. Agregar `.github/workflows/test.yml` con un job `test` que instale dependencias y corra `npm test`.
2. Pushear una rama con ese workflow y abrir un Pull Request — confirmar que el check aparece y corre solo.
3. Si tenés permisos de administrador sobre el repositorio, activar en *Settings → Branches* un branch protection rule sobre tu rama principal que requiera ese check para poder mergear.

## 10. Instalar Playwright

1. En el proyecto de React (el mismo de su propia guía de ejercicios), correr `npm init playwright@latest` — TypeScript, carpeta `e2e`, instalar los navegadores.
2. Confirmar que el test de ejemplo que genera corre con `npx playwright test`.

## 11. Un test E2E real, contra todo el stack

1. Con el backend de Node + Express corriendo (conectado a Mongo) y el frontend de React corriendo (`npm run dev`), escribí un test E2E que: abra el catálogo, busque un producto por nombre con el buscador ya construido en la guía de React, y confirme que aparece en los resultados.
2. Sumá un segundo test que inicie sesión (con el login real que armaron si siguieron la guía de MongoDB hasta el final) y confirme que una ruta protegida del frontend ya no redirige a `/login`.
3. Hacé fallar uno de los dos a propósito (por ejemplo, buscando un producto que no existe) y mirá el *trace* que genera Playwright para entender qué pasó.

## 12. Cerrar el círculo

1. Con todo lo anterior armado, corré en este orden: `npm run test` (unitarios + integración) en el backend, y después `npx playwright test` (E2E) con los dos servidores levantados.
2. Si configuraste CI en el ejercicio 9, confirmá que el mismo workflow correría estos tests automáticamente en cada Pull Request de acá en adelante.

## Checklist final

- [ ] Al menos un test unitario puro (sin tocar la base) y varios de integración (con `mongodb-memory-server`) sobre las rutas de productos.
- [ ] Al menos un mock tipado (`vi.mocked`) sobre una dependencia externa del login o del registro.
- [ ] Una funcionalidad nueva construida siguiendo red-green-refactor, con su test escrito antes que el código.
- [ ] Coverage corrido, con al menos un hueco real identificado y cerrado, y un umbral configurado.
- [ ] Pre-commit con Husky bloqueando commits con tests rotos.
- [ ] Un workflow de CI corriendo los tests en cada Pull Request.
- [ ] Al menos un test E2E con Playwright, contra el frontend y el backend reales juntos.

## Para pensar

- El ejercicio 3 pide limpiar la colección entre tests (`beforeEach`). ¿Qué pasaría si dos archivos de test corrieran en paralelo contra la misma base en memoria? ¿Es un problema real acá, o `mongodb-memory-server` ya lo resuelve de otra forma?
- En el ejercicio 6 hiciste TDD sobre una ruta nueva. ¿Te costó más o menos que escribir el código primero y el test después, como en los ejercicios anteriores? ¿En qué tipo de funcionalidad creés que TDD ayuda más, y en cuál estorba?
- Esta guía separó deliberadamente los tests de integración (contra una base en memoria) de los E2E (contra el stack completo, real). Si tuvieras que elegir solo uno de los dos para correr en cada Pull Request — por tiempo de CI — ¿cuál elegirías, y qué tipo de bug te arriesgás a dejar pasar con esa elección?
