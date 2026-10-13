---
theme: bricks
title: Programación III - Testing
download: true
info: |
  Testing - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: testing, unit testing, integration testing, e2e, tdd, coverage, jest, vitest, playwright, cypress, husky, INSPT, UTN
transition: slide-left
mdc: true
---

# Testing

Programación III

<div class="flex gap-6 justify-end mr-16 mt-6 items-center">
<img src="/logos/vitest.svg" alt="Vitest" class="h-14 opacity-90" />
<img src="/logos/jest.svg" alt="Jest" class="h-14 opacity-90" />
<img src="/logos/playwright.svg" alt="Playwright" class="h-12 opacity-90" />
<img src="/logos/cypress.svg" alt="Cypress" class="h-12 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# Cerrando el círculo

<div class="mt-6 text-xl opacity-90">

Cada módulo de esta unidad ya probó una parte del stack, por separado.

</div>

<div class="mt-6 text-base opacity-80">

React Testing Library sobre componentes; `supertest` sobre las rutas de Express; `mongodb-memory-server`, mencionado al cerrar Mongo. Este módulo no repite ninguno de esos ejemplos — da el panorama completo: qué tipos de test existen, qué metodologías y patrones los rodean, cómo automatizarlos, y cómo saber si un proyecto está **realmente** cubierto.

</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

Requisito explícito del programa de la materia: "Pruebas" tiene su propio lugar en el núcleo, no es un detalle opcional.

</div>

---
layout: default
---

# Por qué testear

- Un test corre en segundos y detecta una regresión **antes** de que la vea un usuario real — probar todo a mano, cada vez, no escala.
- Da confianza para refactorizar: si algo se rompe al cambiar código, un test lo avisa en el momento, no semanas después.
- Es documentación ejecutable — un test bien nombrado explica qué se espera de una función o pantalla, y se mantiene sincronizado con el código a la fuerza.

<div class="mt-4 text-sm italic opacity-80 text-center">

Ninguna cantidad de tests garantiza cero bugs — sí reduce, mucho, la probabilidad de un bug conocido reapareciendo.

</div>

---
layout: center
---

# Tipos de test

---
layout: default
---

# Tres niveles

<div class="grid grid-cols-3 gap-3 mt-6 text-sm">
<div class="p-3 rounded-lg bg-blue-50 border-2 border-blue-300">

**Unitario**

Prueba **una pieza aislada** — una función, un componente — sin dependencias reales.
</div>
<div class="p-3 rounded-lg bg-yellow-50 border-2 border-yellow-300">

**Integración**

Prueba **varias piezas juntas** — con al menos una dependencia real de por medio.
</div>
<div class="p-3 rounded-lg bg-red-50 border-2 border-red-300">

**End-to-end (e2e)**

Prueba el **sistema completo**, como lo usaría una persona real.
</div>
</div>

<div class="mt-6 text-sm opacity-80">

Tres niveles, cada uno con su propia lógica de cuándo conviene — se ven en detalle en las próximas slides, y vuelven a aparecer con cada tecnología concreta del curso.

</div>

---
layout: default
---

# Tests unitarios

<div class="text-sm opacity-90 mb-2">

Prueban **una sola pieza** — una función, un método — con todas sus dependencias reemplazadas o directamente sin ninguna. Si algo de afuera hiciera falta (una base, una API), ya no es unitario.

</div>

```ts
export function applyDiscount(price: number, rate: number): number {
  if (rate < 0 || rate > 1) throw new Error('rate debe estar entre 0 y 1')
  return price - price * rate
}
```

```ts
test('aplica el descuento correctamente', () => {
  expect(applyDiscount(1000, 0.1)).toBe(900)
})
```

<div class="mt-1 text-xs opacity-80">

Sin red, sin servidor, sin nada externo — por eso corren en milisegundos y se pueden tener miles. En el ecosistema JS/TS, **Jest** y **Vitest** son los más usados (en otros lenguajes existe el mismo concepto: JUnit en Java, pytest en Python).

</div>

---
layout: default
---

# Tests de integración

<div class="text-sm opacity-90 mb-2">

Prueban **varias piezas juntas**, con al menos una dependencia real de por medio — una ruta Express contra una base real, un componente con sus hijos reales en vez de mockeados.

</div>

```ts
import request from 'supertest'
import app from '../app'

test('GET /products devuelve el catálogo', async () => {
  const res = await request(app).get('/products')
  expect(res.status).toBe(200)
})
```

<div class="mt-2 text-sm opacity-80">

Ya visto en Node + Express: acá `app` es real. La base puede ser real también (con `mongodb-memory-server`) o no, según qué parte se quiera probar — la línea entre unitario e integración depende de **qué tan real** es lo que hay alrededor, no de la herramienta usada.

</div>

---
layout: default
---

# Tests end-to-end (E2E)

<div class="text-sm opacity-90 mb-2">

Prueban el **sistema completo**, sin ningún reemplazo — un navegador real, contra la app corriendo entera, con su backend y su base reales.

</div>

- Simulan exactamente lo que haría una persona: abrir una página, hacer clic, escribir, leer lo que aparece en pantalla.
- Son los más lentos y los más caros de mantener — un cambio de diseño puede romperlos sin que la lógica haya cambiado.
- Las herramientas (**Playwright**, **Cypress**) se ven en profundidad más adelante en este módulo.

<div class="mt-2 text-sm italic opacity-80 text-center">

Por eso se reservan para los flujos más críticos de la app — no para repetir ahí lo que ya probaron los niveles anteriores.

</div>

---
layout: default
---

# La pirámide de testing

<div class="flex flex-col items-center mt-4 text-sm">
<div class="w-32 py-2 bg-red-100 border-2 border-red-300 text-center rounded-t-lg">e2e</div>
<div class="w-64 py-2 bg-yellow-100 border-2 border-yellow-300 text-center">Integración</div>
<div class="w-96 py-2 bg-blue-100 border-2 border-blue-300 text-center rounded-b-lg">Unitarios</div>
</div>

<div class="mt-3 text-sm opacity-80">

Propuesta de **Mike Cohn** (2009, *Succeeding with Agile*), popularizada por Martin Fowler. Su enfoque es la **velocidad y el costo** del feedback: cuantos más tests rápidos y baratos (unitarios), más rápido se entera el equipo si algo se rompió — los e2e, lentos y frágiles, se reservan para los flujos más críticos, unos pocos.

</div>

<div class="mt-1 text-xs opacity-60">

→ [martinfowler.com/bliki/TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)

</div>

---
layout: default
---

# Otro modelo: la Testing Trophy

<div class="flex flex-col items-center mt-4 text-sm">
<div class="w-28 py-1.5 bg-red-100 border-2 border-red-300 text-center rounded-t-lg">e2e</div>
<div class="w-80 py-2.5 bg-yellow-100 border-2 border-yellow-300 text-center font-bold">Integración</div>
<div class="w-56 py-1.5 bg-blue-100 border-2 border-blue-300 text-center">Unitarios</div>
<div class="w-72 py-1.5 bg-gray-100 border-2 border-gray-300 text-center rounded-b-lg">Estáticos (lint, tipos)</div>
</div>

<div class="mt-3 text-xs opacity-80">

Propuesta de **Kent C. Dodds** (2017): **menos unitarios, más integración**. Su enfoque no es la velocidad sino la **confianza por esfuerzo invertido** — un test de integración, aunque sea más lento que uno unitario, suele probar cómo las piezas trabajan juntas de verdad, en vez de piezas aisladas que nadie usa solas. Surge porque React Testing Library y `supertest` volvieron esos tests rápidos y baratos, algo que no era cierto cuando se diseñó la pirámide. Ninguno de los dos modelos es una ley — son heurísticas para decidir dónde conviene poner el esfuerzo.

</div>

<div class="mt-1 text-xs opacity-60">

→ [Kent C. Dodds — Write tests. Not too many. Mostly integration](https://kentcdodds.com/blog/write-tests)

</div>

---
layout: default
---

# Testing de regresión

<div class="text-sm opacity-90 mb-2">

Confirmar que un cambio **nuevo** no rompió algo que **ya andaba** — literalmente el nombre: evitar que el software "regrese" a un estado con bugs ya resueltos. No es un cuarto nivel: es el **rol** que cumple cualquier test cuando la suite se corre repetidamente, no una sola vez.

</div>

```ts
// Bug real: alguien llamó applyDiscount(1000, 10) pensando en
// "10%" en vez de 0.1 — el precio dio -9000 en vez de rechazarlo
test('rechaza una tasa fuera de 0-1 (regresión del bug #142)', () => {
  expect(() => applyDiscount(1000, 10)).toThrow()
})
```

<div class="mt-1 text-xs opacity-80">

Este test existe **porque ese bug pasó una vez** — si alguien saca la validación sin darse cuenta, el test lo frena antes de que vuelva a producción. Nombrarlo con la referencia al bug (o un comentario) es una práctica común, para que quede claro por qué existe.

</div>

---
layout: center
---

# Herramientas por tecnología

---
layout: default
---

# Qué usa cada capa

<div class="overflow-x-auto mt-4 text-sm">

| Capa | Herramientas | Nivel típico |
|---|---|---|
| React (componentes) | Vitest/Jest + React Testing Library | Unitario / integración |
| Express (endpoints) | Vitest/Jest + `supertest` | Integración |
| MongoDB | `mongodb-memory-server` | Integración |
| Sistema completo | Playwright / Cypress | E2E |

</div>

<div class="mt-4 text-sm opacity-80">

`supertest` sin base real es unitario (prueba solo la lógica de la ruta); combinado con `mongodb-memory-server` pasa a ser un test de integración — la misma idea de la slide anterior, ahora con las herramientas concretas del curso.

</div>

---
layout: center
---

# Patrones y metodología

---
layout: default
---

# Patrón AAA

<div class="grid grid-cols-2 gap-3 text-xs">

```ts
test('applyDiscount resta %', () => {
  // Arrange
  const price = 1000
  const rate = 0.1
  // Act
  const result = applyDiscount(price, rate)
  // Assert
  expect(result).toBe(900)
})
```

```tsx
// Mismo patrón, con RTL
test('el botón suma uno', () => {
  // Arrange
  render(<Counter />)
  // Act
  fireEvent.click(
    screen.getByRole('button', { name: 'Sumar' })
  )
  // Assert
  expect(screen.getByText('1')).toBeInTheDocument()
})
```

</div>

<div class="mt-1 text-xs opacity-80">

**Arrange / Act / Assert** — un mismo esqueleto para casi cualquier test, sea una función pura o un componente: preparar el escenario, ejecutar una sola acción, verificar un resultado. Un test con varios "Act" seguidos suele ser, en realidad, dos tests.

</div>

---
layout: default
---

# Given-When-Then

```gherkin
Scenario: Aplicar un descuento
  Given un producto de $1000
  When se aplica un descuento del 10%
  Then el precio final es $900
```

<div class="mt-3 text-sm opacity-80">

Mismo esqueleto de tres partes que AAA (`Given`=Arrange, `When`=Act, `Then`=Assert) — lo que cambia es el público: nace de **BDD** (*Behavior-Driven Development*) y se escribe en lenguaje de negocio, pensado para que lo lea todo el equipo, no solo quien programa. Herramientas como Cucumber lo convierten en un test real a partir de ese mismo texto.

</div>

<div class="mt-1 text-xs opacity-60">

→ [automationpanda.com — Arrange-Act-Assert](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)

</div>

---
layout: default
---

# Test doubles: los 5 tipos

<div class="text-xs opacity-80 mb-1">

Técnica general — se usan en cualquier test, unitario o de integración, no son específicos de TDD. Reemplazan una dependencia real (una base, un timer, una API externa) por algo controlado:

</div>

<div class="grid grid-cols-3 gap-2 mt-1 text-xs">
<div class="p-2 rounded-lg bg-gray-100"><strong>Dummy</strong><br/>Se pasa porque hace falta el parámetro — a nadie le importa qué hace.</div>
<div class="p-2 rounded-lg bg-gray-100"><strong>Fake</strong><br/>Una implementación liviana que <strong>sí funciona</strong> (un repo en memoria, no la base real).</div>
<div class="p-2 rounded-lg bg-gray-100"><strong>Stub</strong><br/>Devuelve una respuesta fija, prearmada — sin lógica real.</div>
<div class="p-2 rounded-lg bg-gray-100"><strong>Spy</strong><br/>Envuelve algo <strong>real</strong> y registra cómo lo llamaron.</div>
<div class="p-2 rounded-lg bg-gray-100"><strong>Mock</strong><br/>Se arma con expectativas — el test verifica que lo llamaron como esperaba.</div>
</div>

<div class="mt-2 text-sm italic opacity-80 text-center">

La distinción real: Stub/Fake verifican **estado** (mirás el resultado); Mock verifica **comportamiento** (mirás la interacción).

</div>

<div class="mt-1 text-xs opacity-60">

→ [martinfowler.com/bliki/TestDouble](https://martinfowler.com/bliki/TestDouble.html)

</div>

---
layout: default
---

# TDD: red, green, refactor

<div class="flex items-center justify-center gap-3 mt-2 text-sm">
<div class="px-4 py-1.5 rounded-full bg-red-100 border-2 border-red-400 font-bold">🔴 Red</div>
<div class="text-lg opacity-50">→</div>
<div class="px-4 py-1.5 rounded-full bg-green-100 border-2 border-green-400 font-bold">🟢 Green</div>
<div class="text-lg opacity-50">→</div>
<div class="px-4 py-1.5 rounded-full bg-blue-100 border-2 border-blue-400 font-bold">🔵 Refactor</div>
</div>
<div class="flex flex-col items-center -mt-1">
<div class="text-lg opacity-50">↺</div>
<div class="text-xs opacity-60">vuelve a empezar, con el próximo comportamiento chico</div>
</div>

```ts
// 1. Red — el test falla: applyDiscount todavía no existe
test('aplica 10% de descuento', () => {
  expect(applyDiscount(1000, 0.1)).toBe(900)
})
// 2. Green — lo mínimo para que pase
export function applyDiscount(price: number, rate: number) {
  return price - price * rate
}
```

<div class="mt-1 text-xs opacity-80">

Es una **metodología de desarrollo** (el test va antes que el código), no un nivel de test. **Red** fuerza a pensar la interfaz antes de implementar; **Green** prioriza velocidad; **Refactor** limpia con la red de seguridad ya puesta. Si cuesta terminar una vuelta, el paso elegido fue muy grande, no que faltó tiempo.

</div>

---
layout: default
---

# Dentro de TDD: London vs. Chicago

<div class="text-xs opacity-80 mb-1">

Al hacer TDD aparece una pregunta: en el paso <strong>Red</strong>, ¿cuánto mockeo? Dos escuelas responden distinto, usando los test doubles recién vistos:

</div>

```ts
// Chicago (clasicista): usa el Fake de la slide anterior, mira el RESULTADO
it('crea el pedido si hay stock', () => {
  const repo = new FakeProductRepo([{ id: '1', stock: 5 }])
  expect(createOrder('1', repo)).toBe(true)
})
```

```ts
// London (mockista): mockea el repo, mira las LLAMADAS
it('crea el pedido si hay stock', () => {
  const repo = { findById: vi.fn().mockReturnValue({ id: '1', stock: 5 }) }
  createOrder('1', repo)
  expect(repo.findById).toHaveBeenCalledWith('1')
})
```

<div class="mt-1 text-xs opacity-80">

Chicago evita mocks — tests más resistentes a refactors internos. London mockea todas las dependencias para aislar una sola unidad — al costo de acoplarse a <em>cómo</em> está implementada, no solo a <em>qué</em> hace. Ninguna es la "correcta".

</div>

<div class="mt-1 text-xs opacity-60">

→ [chuniversiteit.nl — Chicago and London schools of TDD](https://chuniversiteit.nl/programming/chicago-and-london-schools-of-tdd)

</div>

---
layout: default
---

# Buenas prácticas

- **Un test, una razón para fallar** — si falla, tiene que quedar claro qué se rompió sin leer el código de producción.
- **Tests independientes** — no deberían depender del orden en que corren, ni compartir estado mutable entre sí.
- **Nombres descriptivos** — el nombre es la primera (a veces única) documentación que alguien lee.
- **No testear implementación** — verificar *qué* hace el código, no *cómo* por dentro; si no, cada refactor rompe tests sin que el comportamiento haya cambiado.
- **Tests rápidos** — una suite lenta es una suite que, en la práctica, la gente deja de correr.

<div class="mt-1 text-xs opacity-60">

→ [github.com/goldbergyoni/javascript-testing-best-practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

</div>

---
layout: default
---

# Un test con varios casos

```ts
// TypeScript, con Vitest (en Jest es igual, cambia el import)
import { describe, it, expect } from 'vitest'

describe('applyDiscount', () => {
  it.each([
    [1000, 0, 1000],
    [1000, 0.1, 900],
    [1000, 0.5, 500],
    [1000, 1, 0],
  ])('con precio %i y tasa %p, devuelve %i', (price, rate, expected) => {
    expect(applyDiscount(price, rate)).toBe(expected)
  })

  it('rechaza una tasa negativa', () => {
    expect(() => applyDiscount(1000, -0.1)).toThrow()
  })
})
```

<div class="mt-1 text-xs opacity-80">

`it.each` evita copiar el mismo test cuatro veces — una tabla de casos, incluidos los límite (`0`, `1`), no solo el camino feliz.

</div>

---
layout: default
---

# TypeScript en los tests <img src="/logos/typescript.svg" class="h-6 inline align-middle ml-1"/>

```ts
import { vi } from 'vitest'
import { sendEmail } from './email'
import { registerUser } from './registerUser'

vi.mock('./email')

test('manda un email de bienvenida', async () => {
  const mockedSend = vi.mocked(sendEmail)

  await registerUser('ada@mail.com')

  expect(mockedSend).toHaveBeenCalledWith('ada@mail.com', 'Bienvenido')
})
```

<div class="mt-2 text-sm opacity-80">

`vi.mocked(sendEmail)` no es solo cosmético: le devuelve a `mockedSend` el tipo real de `sendEmail`, con autocompletado y chequeo en los argumentos. Si `sendEmail` cambia de firma, TypeScript avisa en el test — no hace falta el `any` que se cuela al escribir un mock a mano.

</div>

<div class="mt-1 text-xs opacity-60">

→ [vitest.dev/api/vi#vi-mocked](https://vitest.dev/api/vi.html#vi-mocked)

</div>

---
layout: center
---

# Automatizar: pre-commits y CI

---
layout: default
---

# Pre-commit hooks con Husky

```bash
npm install -D husky lint-staged
npx husky init
```

```json
// .lintstagedrc.json
{ "*.ts": "vitest related --run" }
```

<div class="mt-2 text-sm opacity-80">

`husky init` crea `.husky/pre-commit` y un script `prepare` en `package.json` (corre solo con `npm install`, para que quede configurado en cualquier clon del repo). **lint-staged** corre `vitest related` solo sobre los archivos modificados — mucho más rápido que toda la suite en cada commit. Si un test falla, el commit se cancela.

</div>

<div class="mt-1 text-xs opacity-60">

→ [typicode.github.io/husky](https://typicode.github.io/husky/get-started.html) · [github.com/lint-staged/lint-staged](https://github.com/lint-staged/lint-staged)

</div>

---
layout: default
---

# Tests en CI

<img src="/logos/githubactions.svg" class="h-8 opacity-90 mb-1"/>

```yaml
# .github/workflows/test.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
```

<div class="mt-3 text-sm opacity-80">

Mismo GitHub Actions ya visto en Git & GitHub — correr los tests automáticamente en cada `push`/Pull Request, no solo "a mano antes de acordarme". Un PR con un test roto queda marcado en rojo, visible para todo el equipo, antes de mergear.

</div>

---
layout: default
---

# Branch protection

- El job `test` del workflow anterior aparece, automáticamente, como un **status check** sobre cada Pull Request.
- En *Settings → Branches → Branch protection rules*, activar "Require status checks to pass before merging" y elegir ese job por nombre.
- Con eso activado, GitHub **no deja mergear** mientras el check esté en rojo — deja de depender de que alguien se acuerde de mirar.

<div class="mt-1 text-xs opacity-60">

→ [docs.github.com — Managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)

</div>

---
layout: default
---

# ¿Y el rol del QA?

- **Testing manual/exploratorio** — una persona probando la app a mano, buscando casos raros que nadie pensó en automatizar. Insustituible para usabilidad; no tiene sentido para repetir lo mismo mil veces.
- **QA de automatización** — escribe exactamente el tipo de tests de este módulo, a veces como su rol principal dentro de un equipo.

<div class="mt-3 text-sm italic opacity-80 text-center">

No son roles opuestos, se complementan. En un equipo grande suelen ser personas distintas; en uno chico — como el proyecto final — la misma persona hace las dos cosas.

</div>

---
layout: center
---

# Test coverage

---
layout: default
---

# Qué es el coverage

<div class="text-sm opacity-80 mb-2">

**Coverage** (cobertura) mide qué porcentaje del código corrió al menos una vez durante los tests — no si el resultado fue correcto, solo si esa línea se ejecutó.

</div>

<div class="grid grid-cols-2 gap-3 mt-2 text-sm">
<div class="p-3 rounded-lg bg-gray-100"><strong>Line coverage</strong> — % de líneas ejecutadas.</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>Branch coverage</strong> — % de ramas de un `if`/`switch` tomadas (las dos, no solo una).</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>Function coverage</strong> — % de funciones invocadas al menos una vez.</div>
<div class="p-3 rounded-lg bg-gray-100"><strong>Statement coverage</strong> — % de sentencias ejecutadas (más preciso que líneas, si hay varias por línea).</div>
</div>

---
layout: default
---

# Cómo medirlo

```bash
npm install -D @vitest/coverage-v8
npx vitest run --coverage
```

```
File        | % Stmts | % Branch | % Funcs | % Lines |
------------|---------|----------|---------|---------|
pricing.ts  |   60.00 |   100.00 |   33.33 |   50.00 |
```

<div class="mt-2 text-sm opacity-80">

Sin configuración extra, un solo comando genera **dos** reportes a la vez: texto en la terminal (arriba) y uno HTML navegable, en `coverage/index.html`. Jest trae esto mismo incluido, con `npx jest --coverage`.

</div>

---
layout: default
---

# Leer el reporte HTML

- Abrir `coverage/index.html` en el navegador — un listado de archivos, cada uno clickeable.
- Adentro de un archivo, el código fuente se ve resaltado línea por línea:

<div class="grid grid-cols-3 gap-2 mt-2 text-xs">
<div class="p-2 rounded-lg bg-green-100 border border-green-400 text-center">Verde — se ejecutó</div>
<div class="p-2 rounded-lg bg-pink-100 border border-pink-400 text-center">Rosa — nunca se ejecutó</div>
<div class="p-2 rounded-lg bg-yellow-100 border border-yellow-400 text-center">Amarillo — rama parcial</div>
</div>

<div class="mt-3 text-sm italic opacity-80 text-center">

La forma más rápida de encontrar qué falta probar, archivo por archivo — mucho más útil que mirar solo el número global.

</div>

---
layout: default
---

# ¿Cuánto coverage alcanza?

- **100% no es el objetivo** — se llega ahí con tests triviales que ejecutan una línea sin verificar nada útil, inflando el número sin agregar confianza real.
- Un **piso razonable** (60-80%, según el proyecto) sirve como red de seguridad: por debajo, hay demasiado código sin ninguna verificación.
- Coverage mide **qué corrió**, no **qué tan bien se probó** — cien por ciento con asserts débiles vale menos que 70% con tests que verifican casos límite de verdad.

<div class="mt-4 text-sm italic opacity-80 text-center">

Útil para detectar código completamente huérfano de tests — no un sustituto de revisar si los tests que existen son buenos.

</div>

---
layout: default
---

# Automatizar el coverage en CI

```ts
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: { thresholds: { lines: 70, branches: 70 } },
  },
})
```

<div class="mt-2 text-sm opacity-80">

Con un umbral configurado, `vitest run --coverage` termina con código de error si el proyecto cae por debajo — mismo mecanismo que un test roto, corriendo como un paso más del workflow de CI. Para ver la tendencia entre Pull Requests, servicios como <img src="/logos/codecov.svg" class="h-4 inline align-middle"/> **Codecov** suben el reporte y lo comentan directo en el PR.

</div>

<div class="mt-1 text-xs opacity-60">

→ [github.com/codecov/codecov-action](https://github.com/codecov/codecov-action)

</div>

---
layout: center
---

# Testing end-to-end, en profundidad

---
layout: default
---

# Playwright vs. Cypress

<div class="overflow-x-auto mt-3 text-sm">

| | <img src="/logos/playwright.svg" class="h-4 inline align-middle mr-1"/>Playwright | <img src="/logos/cypress.svg" class="h-4 inline align-middle mr-1"/>Cypress |
|---|---|---|
| Navegadores | Chromium, Firefox, WebKit | Chrome/Firefox (WebKit experimental) |
| Velocidad | Paralelización incluida, gratis | Serial por defecto, buen auto-wait |
| Debugging | Sólido | *Time-travel debugger*, muy interactivo |

</div>

<div class="mt-2 text-sm opacity-80">

Ninguno "gana" para siempre — hoy **Playwright** es el punto de partida más común salvo que el debugger interactivo de Cypress pese más para el equipo. Ninguno de los dos es nuevo en este repo: Playwright es, literalmente, lo que exporta a PDF cada apunte y cada deck de esta materia.

</div>

<div class="mt-1 text-xs opacity-60">

→ [playwright.dev](https://playwright.dev/) · [cypress.io](https://www.cypress.io/)

</div>

---
layout: default
---

# Instalar y configurar Playwright

```bash
npm init playwright@latest
```

<div class="text-xs opacity-80 mb-1">

Pregunta, interactivamente: TypeScript o JavaScript, en qué carpeta poner los tests (`tests` o `e2e`), si agregar un workflow de GitHub Actions, si instalar los navegadores ya mismo. Genera `playwright.config.ts` (navegadores a probar, `baseURL`, timeouts, reintentos) y una carpeta con un test de ejemplo.

</div>

```bash
npx playwright test        # corre toda la suite, sin ventana (headless)
npx playwright test --ui   # modo interactivo, para debuggear paso a paso
```

<div class="mt-1 text-xs opacity-60">

→ [playwright.dev/docs/intro](https://playwright.dev/docs/intro)

</div>

---
layout: default
---

# ¿Dónde viven los tests E2E?

```
mi-proyecto/
├── src/              # el código de la app
├── tests/            # unitarios e integración, junto al código
└── e2e/              # tests end-to-end, carpeta propia
    └── cart.spec.ts
```

- Viven en el **mismo repo** que el resto del proyecto — no hace falta (ni es lo común) un repo aparte.
- Corren contra la app ya **levantada** — local o contra un ambiente de staging, nunca mockeando nada del sistema.

<div class="mt-1 text-xs opacity-80">

Playwright y Cypress pueden levantar el servidor solos antes de correr los tests (`webServer` en la config) — el CI no necesita un paso manual aparte.

</div>

---
layout: default
---

# Selectors y auto-wait

```ts
// Frágil: depende de una clase CSS que puede cambiar en cualquier refactor
await page.click('.btn-primary')

// Mejor: depende de lo que vería una persona, no de la implementación
await page.getByRole('button', { name: 'Agregar' }).click()
```

<div class="mt-2 text-sm opacity-80">

**Locators** como `getByRole`/`getByText`/`getByLabel` se prefieren sobre selectores CSS/XPath — son los mismos que ya usan React Testing Library. Además, Playwright espera solo a que el elemento exista **y** sea interactuable antes de actuar (*auto-wait*) — no hace falta un `sleep` manual, a diferencia de automatizaciones más viejas.

</div>

---
layout: default
---

# Un test E2E real

```ts
test('agregar un producto al carrito', async ({ page }) => {
  await page.goto('http://localhost:5173/products')
  await page.getByText('Mouse').click()
  await page.getByRole('button', { name: 'Agregar' }).click()
  await expect(page.getByText('1 ítem en el carrito')).toBeVisible()
})
```

<div class="mt-3 text-sm opacity-80">

Mismo estilo de API que ya se usa para controlar un navegador real en los scripts de export de PDF de este repo — acá, en vez de imprimir una página, simula a una persona usando la app completa.

</div>

---
layout: default
---

# Fragilidad y debugging

- **Flakiness** — un test que a veces pasa y a veces no, casi siempre por timing (una animación, un dato no determinista). El auto-wait lo reduce mucho, no lo elimina del todo.
- `retries` en la config reintenta un test fallido antes de marcarlo rojo — útil en CI, nunca para tapar un bug real.
- Al fallar, Playwright guarda automáticamente screenshot, video y un *trace* navegable — mucho más fácil de debuggear que un log de texto.

```ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  use: { trace: 'on-first-retry', screenshot: 'only-on-failure' },
})
```

<div class="mt-1 text-xs opacity-60">

→ [playwright.dev/docs/trace-viewer](https://playwright.dev/docs/trace-viewer)

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-6 mt-2 text-xs">
<div>

**Niveles, patrones y metodología**

| Forma | Para qué |
|---|---|
| Unit / Integ. / E2E | Aislado / piezas juntas / sistema completo |
| Pirámide / Trophy | Velocidad y costo / confianza por esfuerzo |
| AAA / GWT | Esqueleto de un test |
| 5 test doubles | Dummy, Fake, Stub, Spy, Mock |
| TDD | Red, green, refactor |
| London / Chicago | Cuánto mockeás, dentro de TDD |

</div>
<div>

**Automatizar, medir y E2E**

| Forma | Para qué |
|---|---|
| `npx husky init` | Pre-commit hooks |
| `.lintstagedrc.json` | Correr tests solo en lo modificado |
| Branch protection | Bloquear merge si el check falla |
| `vitest run --coverage` | Reporte de cobertura |
| `coverage.thresholds` | Umbral que falla el build |
| `npm init playwright@latest` | Instalar y configurar E2E |
| `getByRole`/`getByText` | Locators, en vez de CSS frágil |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [martinfowler.com — Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html) · [Test Double](https://martinfowler.com/bliki/TestDouble.html)
- [Kent C. Dodds — Write tests. Not too many. Mostly integration](https://kentcdodds.com/blog/write-tests) — el artículo original de la Testing Trophy
- [chuniversiteit.nl — Chicago and London schools of TDD](https://chuniversiteit.nl/programming/chicago-and-london-schools-of-tdd)
- [vitest.dev/guide/coverage](https://vitest.dev/guide/coverage.html) — coverage con Vitest, configuración y umbrales
- [vitest.dev/api/vi#vi-mocked](https://vitest.dev/api/vi.html#vi-mocked) — mocks tipados en TypeScript
- [jestjs.io/es-ES/docs/configuration#collectcoverage-boolean](https://jestjs.io/es-ES/docs/configuration#collectcoverage-boolean) — coverage con Jest
- [typicode.github.io/husky](https://typicode.github.io/husky/get-started.html) · [github.com/lint-staged/lint-staged](https://github.com/lint-staged/lint-staged)
- [docs.github.com — Branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [github.com/codecov/codecov-action](https://github.com/codecov/codecov-action)
- [testing-library.com](https://testing-library.com/) · [npmjs.com/package/supertest](https://www.npmjs.com/package/supertest) · [npmjs.com/package/mongodb-memory-server](https://www.npmjs.com/package/mongodb-memory-server)
- [playwright.dev/docs/intro](https://playwright.dev/docs/intro) · [playwright.dev/docs/trace-viewer](https://playwright.dev/docs/trace-viewer) · [cypress.io](https://www.cypress.io/)
- [github.com/goldbergyoni/javascript-testing-best-practices](https://github.com/goldbergyoni/javascript-testing-best-practices) — buenas prácticas de testing en JS/TS, mantenido por la comunidad

</div>
