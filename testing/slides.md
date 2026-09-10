---
theme: bricks
title: Programación III - Testing
download: true
info: |
  Testing - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: testing, unit testing, integration testing, e2e, coverage, jest, vitest, supertest, playwright, INSPT, UTN
transition: slide-left
mdc: true
---

# Testing

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/vitest.svg" alt="Vitest" class="h-14 opacity-90" />
<img src="/logos/jest.svg" alt="Jest" class="h-14 opacity-90" />
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

React Testing Library sobre componentes; `supertest` sobre las rutas de Express; `mongodb-memory-server`, mencionado al cerrar Mongo. Este módulo no repite ninguno de esos ejemplos — da el panorama completo: qué tipos de test existen, cómo se combinan, y cómo saber si un proyecto está **realmente** cubierto, más allá de la sensación de "ya probé esto a mano".

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
- Es documentación ejecutable — un test bien nombrado explica qué se espera de una función o pantalla, y se mantiene sincronizado con el código a la fuerza (si el código cambia y el comportamiento no, el test debería seguir pasando).

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

Prueba **una pieza aislada** — una función, un componente — sin sus dependencias reales.
</div>
<div class="p-3 rounded-lg bg-yellow-50 border-2 border-yellow-300">

**Integración**

Prueba **varias piezas juntas** — una ruta Express con su base de datos, un componente con sus hijos reales.
</div>
<div class="p-3 rounded-lg bg-red-50 border-2 border-red-300">

**End-to-end (e2e)**

Prueba el **sistema completo**, como lo usaría una persona real — un navegador, contra la app corriendo entera.
</div>
</div>

<div class="mt-6 text-sm opacity-80">

Ya vistos en la unidad: `applyDiscount` sola es **unitario**; `supertest` contra una ruta que sí toca la base es **integración**. Ninguno de los módulos anteriores llegó a escribir un e2e — se menciona acá, al cierre.

</div>

---
layout: default
---

# La pirámide de testing

<div class="flex flex-col items-center mt-6 text-sm">
<div class="w-32 py-2 bg-red-100 border-2 border-red-300 text-center rounded-t-lg">e2e</div>
<div class="w-64 py-2 bg-yellow-100 border-2 border-yellow-300 text-center">Integración</div>
<div class="w-96 py-2 bg-blue-100 border-2 border-blue-300 text-center rounded-b-lg">Unitarios</div>
</div>

<div class="mt-6 text-sm opacity-80">

Cuantos **más** tests, más abajo en la pirámide: los unitarios son rápidos, baratos y estables — conviene tener muchos. Los e2e son lentos, caros de mantener y frágiles (un cambio de diseño rompe el test sin que la lógica haya cambiado) — se reservan para los flujos más críticos, unos pocos, no para cada pantalla.

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

`supertest` sin base real es unitario (prueba solo la lógica de la ruta); combinado con `mongodb-memory-server` pasa a ser un test de integración — la línea entre niveles depende de **qué tan real** es lo que hay del otro lado del test, no de la herramienta usada.

</div>

---
layout: default
---

# Patrón AAA

```ts
test('applyDiscount resta el porcentaje', () => {
  // Arrange: preparar los datos
  const price = 1000
  const rate = 0.1

  // Act: ejecutar lo que se prueba
  const result = applyDiscount(price, rate)

  // Assert: verificar el resultado
  expect(result).toBe(900)
})
```

<div class="mt-3 text-sm opacity-80">

**Arrange / Act / Assert** — un mismo esqueleto para casi cualquier test, sin importar el nivel: preparar el escenario, ejecutar una sola acción, y verificar un resultado. Un test que mezcla varios "Act" seguidos suele ser señal de que en realidad son dos tests distintos.

</div>

---
layout: default
---

# Test doubles: mocks, stubs y spies

<div class="grid grid-cols-3 gap-3 mt-4 text-sm">
<div class="p-3 rounded-lg bg-gray-100">

**Stub**

Devuelve una respuesta fija, sin lógica real — "si te preguntan, contestá esto".
</div>
<div class="p-3 rounded-lg bg-gray-100">

**Mock**

Un stub que además **verifica** cómo lo llamaron — el `jest.mock`/`vi.mock` ya visto en Node + Express.
</div>
<div class="p-3 rounded-lg bg-gray-100">

**Spy**

Envuelve una función **real** y registra sus llamadas, sin reemplazar su comportamiento.
</div>
</div>

<div class="mt-6 text-sm italic opacity-80 text-center">

Los tres son "dobles de test" — reemplazos controlados de una dependencia real, para no depender de una API externa, un timer, o una base de datos en un test unitario.

</div>

---
layout: default
---

# Tests en CI

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
<div class="p-3 rounded-lg bg-gray-100"><strong>Statement coverage</strong> — % de sentencias ejecutadas (similar a líneas, más preciso con varias por línea).</div>
</div>

---
layout: default
---

# Cómo medirlo

```bash
# Vitest
npm install -D @vitest/coverage-v8
npx vitest run --coverage

# Jest (ya lo trae incluido)
npx jest --coverage
```

```
File          | % Stmts | % Branch | % Funcs | % Lines |
--------------|---------|----------|---------|---------|
pricing.ts    |   100   |    100   |   100   |   100   |
products.ts   |    72   |     50   |    80   |    72   |
```

<div class="mt-2 text-sm opacity-80">

Ambos generan un reporte por archivo (texto en la terminal, y opcionalmente HTML navegable) — útil para encontrar rápido qué archivo quedó menos probado, no solo un número global.

</div>

---
layout: default
---

# ¿Cuánto coverage alcanza?

- **100% no es el objetivo** — se puede llegar ahí con tests triviales que ejecutan una línea sin verificar nada útil (`expect(true).toBe(true)`), inflando el número sin agregar confianza real.
- Un **piso razonable** (60-80%, según el proyecto) sirve como red de seguridad: por debajo de eso, hay demasiado código sin ninguna verificación.
- Coverage mide **qué corrió**, no **qué tan bien se probó** — cien por ciento de cobertura con asserts débiles vale menos que 70% con tests que realmente verifican casos límite.

<div class="mt-4 text-sm italic opacity-80 text-center">

Una métrica útil para detectar código completamente huérfano de tests — no un sustituto de revisar si los tests que existen son buenos.

</div>

---
layout: default
---

# Coverage en el proyecto final

<div class="text-sm opacity-80 mb-2">

Con esa salvedad ya hecha, es una buena idea medirlo también ahí.

</div>

- Es objetivo y automatizable: un umbral (`--coverage.thresholds.lines=70` en Vitest, similar en Jest) puede hacer fallar el CI si el proyecto cae por debajo — mismo mecanismo que un test roto.
- Empuja a testear las partes que en la práctica se suelen saltear (manejo de errores, casos límite) — no solo el camino feliz.
- Como criterio de evaluación, conviene combinarlo con revisar la **calidad** de esos tests (¿verifican algo real?), no usarlo solo.

---
layout: center
---

# Un vistazo a E2E

---
layout: default
---

# Playwright y Cypress

```ts
// Playwright: un flujo completo, en un navegador real
test('agregar un producto al carrito', async ({ page }) => {
  await page.goto('http://localhost:5173/products')
  await page.getByText('Mouse').click()
  await page.getByRole('button', { name: 'Agregar' }).click()
  await expect(page.getByText('1 ítem en el carrito')).toBeVisible()
})
```

<div class="mt-3 text-sm opacity-80">

Ninguno de los dos es nuevo en este repo: **Playwright** es, literalmente, lo que exporta a PDF cada apunte y cada deck de esta materia — la misma herramienta, controlando un navegador real, ahora para simular a una persona usando la app en vez de imprimir una página.

</div>

---
layout: default
---

# Cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-xs">
<div>

**Tipos y patrón**

| Forma | Para qué |
|---|---|
| Unitario | Una pieza aislada |
| Integración | Varias piezas juntas |
| E2E | El sistema completo |
| Arrange/Act/Assert | Esqueleto de cualquier test |
| Mock/Stub/Spy | Reemplazar una dependencia |

</div>
<div>

**Coverage**

| Forma | Para qué |
|---|---|
| `vitest run --coverage` | Reporte de cobertura (Vitest) |
| `jest --coverage` | Reporte de cobertura (Jest) |
| Line/branch/function coverage | Qué se mide, exactamente |
| Piso razonable | 60-80%, no 100% a toda costa |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-2 mt-2 text-sm">

- [vitest.dev/guide/coverage](https://vitest.dev/guide/coverage.html) — coverage con Vitest, configuración y umbrales
- [jestjs.io/es-ES/docs/configuration#collectcoverage-boolean](https://jestjs.io/es-ES/docs/configuration#collectcoverage-boolean) — coverage con Jest
- [testing-library.com](https://testing-library.com/) — React Testing Library
- [npmjs.com/package/supertest](https://www.npmjs.com/package/supertest) · [npmjs.com/package/mongodb-memory-server](https://www.npmjs.com/package/mongodb-memory-server)
- [playwright.dev](https://playwright.dev/) · [cypress.io](https://www.cypress.io/) — testing end-to-end
- [martinfowler.com — Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html) — el artículo original de Martin Fowler sobre la pirámide de testing
- [github.com/goldbergyoni/javascript-testing-best-practices](https://github.com/goldbergyoni/javascript-testing-best-practices) — buenas prácticas de testing en JS/TS, mantenido por la comunidad

</div>
