# Unidad 4 — Spec de desarrollo (JS Funcional + MERN)

> **Este documento está escrito para ser ejecutado por un agente (Claude Code) en una conversación nueva, sin contexto previo.** Todo lo que ese agente necesita saber para construir el material debería estar acá o referenciado con path exacto. Si algo no está claro, el agente debe preguntar antes de asumir — en particular todo lo marcado como "Decisión abierta" más abajo.

## 0. Cómo usar este documento

1. Leer completo antes de escribir una sola línea.
2. Leer también `AGENTS.md`, `README.md` y `.cursor/rules/pdf-to-slidev.mdc` en la raíz de este repo (`programacion-III/`) — ahí están las convenciones técnicas exactas (templates de `package.json`, estructura de la landing, proceso de conversión, bugs conocidos, etc.) que este documento asume y no repite en detalle. `AGENTS.md` es la referencia más completa y actualizada de convenciones generales del repo; este documento se enfoca en el contenido específico de Unidad 4.
3. Correr `git log --oneline -20` y `git status` al empezar: es posible que este trabajo se desarrolle en varias sesiones y ya haya avances parciales del deck en curso.
4. Construir **un deck a la vez**, en el orden de la sección 5. Para cada deck: escribir, probar localmente (`slidev dev`), y recién ahí pasar al siguiente. No adelantar contenido de varios decks en paralelo.
5. **Nunca hacer `git push` a `main` sin permiso explícito del usuario.** El repo tiene un GitHub Action (`.github/workflows/deploy.yml`) que despliega automáticamente a GitHub Pages (sitio público que ven los estudiantes) en cada push a `main`. Un commit/push prematuro publica material sin terminar o sin revisar. Se puede (y conviene) hacer commits locales para ir guardando progreso, pero el push queda a criterio y pedido explícito del usuario.
6. Si en algún punto los ejercicios, ejemplos o alcance de un tema generan dudas de enfoque, preguntar al usuario en vez de asumir — esto es material didáctico real para estudiantes reales, no un ejercicio de código genérico.

---

## 1. Contexto institucional y de la materia

**Institución**: INSPT (Instituto Nacional Superior del Profesorado Técnico), UTN, Argentina. Sitio: https://inspt.utn.edu.ar/ — Carrera: Tecnicatura Superior en Informática Aplicada, https://inspt.utn.edu.ar/carreras/informatica_aplicada/

**Materia**: Programación III, 3er año, anual, 6 hs semanales (192 hs totales: 33,3% teóricas, 66,7% prácticas). Docente de la comisión 3.603 (Turno Noche): Prof. Ing. Gastón Larriera.

**Ubicación curricular**: correlativa de Programación II, Sistemas de Computación I y Estructura y Base de Datos (2do año) — es decir, los estudiantes ya vieron programación imperativa/orientada a objetos (Java, C) y bases de datos relacionales (SQL Server) y pseudocódigo (PSeInt). Se relaciona horizontalmente con Sistemas de Computación II (Redes y Sistemas Distribuidos) y Seminario.

**Fundamentación oficial** (textual del programa): la materia se incluye en el plan de estudios porque "la programación funcional [es] uno de los principales paradigmas de la programación y por estar presente, cada vez más, en las herramientas utilizadas para el desarrollo de sistemas web full-stack".

**Programa analítico — Unidades** (textual):
- **Unidad 1**: Cálculo lambda. Sintaxis de las expresiones: variables, abstracciones y aplicaciones. Currificación. Variables libres y ligadas. Reglas de conversión. Orden de evaluación. Combinadores.
- **Unidad 2**: Programación funcional. Funciones de primera clase y de orden superior, funciones puras, transparencia referencial, inmutabilidad, recursividad, evaluación estricta y no estricta.
- **Unidad 3**: Lenguajes de programación que permiten adoptar el paradigma funcional. Tipos de datos. Evaluación de expresiones. Formas especiales. Funciones primitivas (predicados, aritméticas, relacionales, selectores, etc.). Funciones de orden superior (composición, mapeo, reducción, filtrado, aplicación parcial, etc.). Funciones anónimas. Definición de funciones. Modalidades de ejecución de programas (interpretación, compilación, híbrida).
- **Unidad 4** (la que cubre este documento): **Desarrollo de sistemas web full-stack. Ventajas y desventajas. Aplicación de la programación funcional. Instalación y uso de componentes: front-end (framework de presentación) y back-end (base de datos, framework web y servidor web). Formatos para el intercambio de datos. Pruebas.**

Unidades 1–3 ya están cubiertas en este repo (`introduction/`, `lambda-calculus/` + `lambda-calculus-docs/`, `clojure/` + `clojure-docs/`, `fp-backus/` deprecado). Este documento planifica **solo Unidad 4**: todo lo relacionado a JS funcional y al desarrollo full-stack (MERN).

**Requisito explícito de evaluación relevante**: el programa pide expresamente **"Pruebas"** como parte de la unidad — por eso el testing tiene su propio deck en el núcleo (sección 5.9), no es opcional.

**Recursos necesarios** (textual, ya declarados en la planificación oficial — confirma el stack): "software para desarrollar sistemas web full-stack en JavaScript, por ejemplo: Node.js, Express.js, MongoDB, React".

**Bibliografía oficial relevante a Unidad 4**:
- Aravinth, A. y Machiraju, S. (2018). *Beginning Functional JavaScript*. Apress.
- Kereki, F. (2017). *Mastering JavaScript Functional Programming*. Packt.
- Mantyla, D. (2015). *Functional Programming in JavaScript*. Packt.
- Subramanian, V. (2019). *Pro MERN Stack: Full Stack Web App Development with Mongo, Express, React, and Node*. Apress.

**Nota sobre el cronograma**: existe una planificación de fechas por clase, pero **este documento la ignora a propósito** — el desarrollo del material es independiente de fechas puntuales. La planificación de cuándo se dicta cada deck es una instancia separada, posterior a tener el material construido.

**Archivo fuente completo**: `Programación III_Planif_2026.docx`, copiado a la raíz de `INSPT/` (un nivel arriba de este repo, en `../Programación III_Planif_2026.docx` relativo a `programacion-III/`) para que quede disponible en el filesystem del proyecto. Todo lo relevante de ese documento para Unidad 4 ya está transcripto arriba; el archivo original queda solo como respaldo/consulta si hiciera falta algo adicional (por ejemplo criterios de evaluación generales, que no son responsabilidad de este spec).

---

## 2. Estado actual del repositorio

Repo: `programacion-III` (GitHub Pages, deploy automático). Sitio publicado: https://larrieragaston.github.io/programacion-III/

**Ya construido** (no tocar salvo que se pida explícitamente):
- `introduction/` — Slidev, presentación de la materia.
- `lambda-calculus/` (Slidev) + `lambda-calculus-docs/` (VitePress: apunte + guía de ejercicios + ejercicios adicionales, con export a PDF vía Playwright).
- `clojure/` (Slidev) + `clojure-docs/` (VitePress, mismo patrón).
- `fp-backus/` (Slidev) — marcado como "Deprecated" en `index.html` (no forma parte del recorrido activo).

**Stack técnico del repo**:
- [Slidev](https://sli.dev/) para las presentaciones (`theme: bricks`).
- [VitePress](https://vitepress.dev/) para los apuntes teóricos + guías de ejercicios extensas.
- [Playwright](https://playwright.dev/) para exportar PDFs (de los slides y de las páginas VitePress).
- GitHub Actions + GitHub Pages para build y deploy automático.
- Cada presentación Slidev es un proyecto standalone con su propio `package.json` (ver template exacto en `.cursor/rules/pdf-to-slidev.mdc`).

**Archivos clave a entender antes de tocar nada**:
- `index.html` — **(actualizado tras el restyling de la sección 5.3bis, ya completado)** landing page como grid de cards filtrable, no la lista por secciones que describía este documento originalmente. Cada `<div class="card">` lleva `data-category="unidad|proximamente|extra|deprecado"` (y `data-pending="true"` si todavía no tiene contenido real, ver 5.3bis) y contiene: título, descripción, pills de vista (`class="view-link"`, una por recurso navegable — Presentación / Material teórico, con `data-dev-port`/`data-dev-path`) y un único menú `card-download-menu` con **todos** los PDFs de esa unidad. Ver AGENTS.md para el detalle completo de esta estructura y cómo "activar" una card placeholder.
- `index.css` — estilos del grid/cards. `.badge-optional` (azul, mismos tokens que "Extra") y `.badge-proximamente` (gris) ya existen — no hace falta crear clases nuevas para marcar contenido no-núcleo o no construido.
- `dev.sh` — **ojo**: a pesar de lo que sugiere el README ("puertos asignados automáticamente"), el script en realidad tiene **arrays hardcodeados** `MODULES=(...)` y `PORTS=(...)`. Cada deck Slidev nuevo que se agregue **tiene que sumarse manualmter a esos dos arrays** en `dev.sh`, si no, no levanta con `npm run dev` desde la raíz.
- `.github/workflows/deploy.yml` — build CI. Tiene bloques hardcodeados por cada sitio VitePress (`lambda-calculus-docs`, `clojure-docs`) antes del loop genérico que busca cualquier carpeta con Slidev en su `package.json`. **Si se crea un sitio VitePress nuevo para Unidad 4 (ver sección 6), hay que agregarle un bloque análogo a este workflow**, siguiendo exactamente el patrón ya usado para los dos existentes (build con `npm ci --ignore-scripts` + `playwright install` + `docs:build` + `print-pdfs.mjs` + copiar `dist` a `_site/<carpeta>/`).
- `.cursor/rules/pdf-to-slidev.mdc` — workflow paso a paso ya documentado para crear un deck Slidev nuevo (slug, `package.json` template, convenciones de `slides.md`, cómo bajar íconos/logos, cómo probar localmente, cuándo commitear). **Seguir este workflow al pie de la letra para cada uno de los 9 decks del núcleo.**

**Convención de logos/íconos**: se bajan de jsDelivr (devicons/simpleicons) a `public/logos/` dentro de cada deck. Ejemplo: `curl -sL "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/<name>/<name>-original.svg" -o public/logos/<name>.svg`. Verificar que cada SVG bajado sea contenido real (no una página HTML de redirect).

---

## 3. Archivos locales de referencia

Estos archivos existen en el filesystem del proyecto y sirven como **checklist de cobertura de contenido**, no como fuente a copiar — todo el contenido nuevo se escribe fresco, en español, en el estilo Slidev ya establecido (ver sección 4).

Ubicados en `../knowledge base/` (relativo a este repo, es decir un nivel arriba, sibling de `programacion-III/`):

- `08 - Intro al Desarrollo Full Stack - Carlos E. Cimino.pdf` → referencia para el deck de panorama full-stack (mencionado dentro de Node+Express o como introducción, ver sección 5.7).
- `09 - Arrays en JavaScript - Carlos E. Cimino.pdf` → referencia para JS Funcional / JS Contemporáneo (arrays, métodos de orden superior).
- `10 - JavaScript Contemporáneo - Carlos E. Cimino.pdf` → referencia directa para el deck de JS Contemporáneo (sección 5.3).
- `11 - Asincronismo en JavaScript - Carlos E. Cimino.pdf` → referencia directa para el deck de Asincronismo (sección 5.4).
- `Web Full Stack - Introducción - Presentación.pdf` → referencia para panorama full-stack / contraste de paradigmas.
- `Web Full Stack - GIT - Presentación.pdf` → referencia para el deck de Git & GitHub (sección 5.1).
- `Web Full Stack - ReactJS - Presentación.pdf` → referencia para el deck de React (sección 5.6).
- `Web Full Stack - TypeScript - Presentación.pptx` → referencia para el deck de TypeScript (sección 5.5).
- `02 - Programación Funcional.pdf` → ya cubierto conceptualmente por Unidad 2/3 del repo, mencionar solo si aporta ejemplos nuevos para JS Funcional.

Estos PDFs son de 2021, de otro docente (Carlos E. Cimino) que también dicta la materia (comisión 3.601) — sirven para no dejar afuera ningún tema que las otras comisiones sí cubren, pero el tono, ejemplos y profundidad son decisión del material nuevo, no una copia.

**Documento oficial completo**: `../Programación III_Planif_2026.docx` (ver sección 1 — lo esencial ya está transcripto ahí).

**Otras carpetas en `INSPT/`** (`clojure-basics/`, `clojure-fullguide/`, `programacion-I-slides/`) no son relevantes para Unidad 4 — pertenecen a Unidad 3 (ya construida) o a otra materia.

---

## 4. Convenciones globales para todo el contenido nuevo

- **Idioma**: contenido explicativo (texto de los slides, apuntes, comentarios de contexto, enunciados de ejercicios) en **español**. Código (nombres de variables, funciones, clases, propiedades, palabras clave del lenguaje, y comentarios *dentro* del código) en **inglés** — así se escribe profesionalmente y así ya está hecho en los decks existentes (Clojure, Cálculo Lambda). Esto es un requisito explícito del docente, no una preferencia menor.
- **Formato de presentaciones**: Slidev, `theme: bricks`, mismo frontmatter que los decks existentes:
  ```yaml
  ---
  theme: bricks
  title: Programación III - <Nombre del deck>
  download: true
  info: |
    <Descripción corta>
    INSPT - UTN
  author: Gastón Larriera
  keywords: <palabras clave>, INSPT, UTN
  transition: slide-left
  mdc: true
  ---
  ```
- **Slug de carpeta**: minúsculas, guiones, en inglés (ver lista de slugs en sección 5).
- **Apertura de cada deck**: retomar explícitamente el deck anterior (mismo recurso narrativo que ya usa `clojure/slides.md` al abrir mencionando Cálculo Lambda) — reforzar que es una progresión continua, no temas sueltos. Los puentes explícitos ya están anotados en cada sección de la 5.
- **Núcleo vs. opcional**: los decks opcionales van en `data-category="extra"` con el badge `.badge-optional` (ya existe en `index.css`, azul, texto "Extra") — no reusar `.badge-deprecated`.
- **Cada deck del núcleo tiene, además del Slidev, un apunte teórico y una guía de ejercicios** — ver arquitectura en sección 6 (es un requisito explícito del docente, no opcional para el núcleo).
- **Ejemplos de código**: preferir ejemplos ejecutables y progresivos (mismo ítem se retoma y se le agrega complejidad) por sobre ejemplos aislados. Cuando sea posible, conectar un ejemplo con el deck anterior (ej.: el mismo array de datos usado en JS Funcional reaparece tipado en TypeScript, y de nuevo persistido en MongoDB).

---

## 5. Orden del núcleo y contenido por deck

**Orden final acordado**: Git & GitHub → JS Funcional → JavaScript Contemporáneo → **restyling de la landing page (paso intermedio, no es un deck — ver sección 5.3bis)** → Asincronismo → TypeScript → React → Node + Express → MongoDB → Pruebas (Testing) → Proyecto integrador (fuera de alcance de este documento, ver sección 8).

### 5.1 Git & GitHub
**Slug**: `git-github`
**Por qué acá**: es tooling, no paradigma, pero todo lo que sigue asume que los estudiantes pueden versionar su código. Entra primero para tenerlo resuelto antes de escribir la primera línea de JS funcional.

**Objetivos**: entender qué problema resuelve el control de versiones; manejar el flujo local básico (`init`, `add`, `commit`, `status`, `log`, `.gitignore`); entender ramas a nivel conceptual (`branch`, `checkout`/`switch`, `merge`); trabajar con GitHub (remoto, `clone`/`push`/`pull`, Pull Requests básicos); buenas prácticas de mensajes de commit.

**Contenido sugerido**: motivación real (por qué no alcanza con `proyecto_final_v2_ok`); modelo mental de Git (snapshots, no diffs), sin profundizar en objetos internos; comandos esenciales ejecutados en vivo; ramas y merge conceptual (sin rebase ni conflictos avanzados); GitHub — remoto, `origin`, PR, README, `.gitignore` para Node (usar el `.gitignore` real de este mismo repo como ejemplo).

**Referencia local**: `Web Full Stack - GIT - Presentación.pdf` (checklist de cobertura).
**Referencias web**: https://git-scm.com/doc · https://docs.github.com/es/get-started · https://learngitbranching.js.org/ (interactivo, útil para ejercicios).

### 5.2 JS Funcional
**Slug**: `js-funcional`
**Por qué acá**: puente directo desde Clojure — mismo paradigma, nuevo lenguaje.

**Objetivos**: trasladar los conceptos de programación funcional ya vistos (Cálculo Lambda → Clojure) a JavaScript; reconocer funciones de primera clase; escribir funciones puras y razonar sobre transparencia referencial; usar y encadenar `map`/`filter`/`reduce` con criterio; entender composición y currificación/aplicación parcial; distinguir mutabilidad vs. inmutabilidad en arrays/objetos.

**Contenido sugerido**: apertura explícita ("en Clojure esto era `(map inc coll)` — ¿cómo se ve en JS?"); funciones de primera clase (asignar, pasar como argumento, retornar funciones); puras vs. impuras (ejemplos con y sin side effects); inmutabilidad (`Object.freeze`, spread para copias, por qué mutar un parámetro recibido es peligroso); HOFs nativos `map`/`filter`/`reduce` (ejemplos progresivos, terminar armando un pipeline de transformación de datos real); composición (`compose`/`pipe` caseros, sin librería todavía); currificación y aplicación parcial (conexión directa con currying de Unidad 1); recursividad en JS (repaso rápido, honestidad sobre la falta de TCO garantizado); cierre con mapa "esto ya lo sabías de Clojure, así se escribe en JS".

**Referencia local**: `02 - Programación Funcional.pdf`, `09 - Arrays en JavaScript - Carlos E. Cimino.pdf`.
**Bibliografía oficial**: Kereki (*Mastering JS Functional Programming*), Mantyla (*Functional Programming in JavaScript*), Aravinth & Machiraju (*Beginning Functional JavaScript*).
**Referencias web**: https://developer.mozilla.org/es/docs/Web/JavaScript/Reference/Global_Objects/Array · https://mostly-adequate.gitbook.io/mostly-adequate-guide/ (buen apunte gratuito de FP en JS, en inglés, útil como fuente de ejemplos) · https://github.com/getify/Functional-Light-JS (Kyle Simpson, gratuito online).

### 5.3 JavaScript Contemporáneo
**Slug**: `js-contemporaneo`
**Por qué acá**: una vez entendido el paradigma, hace falta el vocabulario sintáctico moderno. Separado a propósito de "JS Funcional": acá es sintaxis/historia/ecosistema, no paradigma.

**Objetivos**: ubicar a JS en una línea de tiempo; dominar sintaxis ES6+ necesaria para el resto de la unidad; entender el ecosistema (Node, npm, módulos) al nivel necesario para lo que sigue.

**Contenido sugerido**: breve historia (ES1 1997 → ES3 → ES5 2009: strict mode, JSON, HOFs de arrays → ES6/ES2015: el salto grande → cadencia anual moderna); por qué JS es como es (nace como lenguaje de scripting de navegador en 10 días); `let`/`const` (scope de bloque vs. función, adiós `var`); arrow functions (sintaxis + `this` léxico, la diferencia que realmente importa); template literals; destructuring (objetos y arrays, valores por defecto); spread/rest; módulos ES (`import`/`export`) vs. CommonJS (`require`); Node.js y npm (runtime, paquete, `package.json`, `node_modules` — ya vivido al instalar Slidev/Clojure tooling); optional chaining `?.`, nullish coalescing `??`; `==` vs `===`.

**Referencia local**: `10 - JavaScript Contemporáneo - Carlos E. Cimino.pdf`, `09 - Arrays en JavaScript - Carlos E. Cimino.pdf`.
**Referencias web**: https://developer.mozilla.org/es/docs/Web/JavaScript · https://es.javascript.info/ (excelente, ya en español) · https://github.com/tc39/proposals (para contexto de evolución del lenguaje, opcional).

### 5.3bis Restyling de la landing page (paso intermedio — no es un deck)

**✅ Completado** (PR #6, mergeado a `main`). Lo que sigue queda como registro de la decisión de diseño; para la estructura real resultante ver AGENTS.md y `index.html` directamente. La sección 6 más abajo ya está actualizada para reflejar cómo se agrega un tema nuevo a esta landing (activar la card placeholder, no copiar bloques viejos de sección/tarjeta).

**Cuándo**: acá exactamente en la secuencia — después de terminar y commitear JS Contemporáneo (5.3), antes de arrancar Asincronismo (5.4). Es un paso único, no se repite por cada deck nuevo (aunque cada deck que se agregue después sí va a necesitar su entrada nueva en el grid resultante, siguiendo el patrón que este restyling deja establecido).

**Qué es**: rediseño de la landing page del repo — los tres archivos en la raíz `index.html` / `index.css` / `index.js` — mismo propósito que tiene hoy (linkear el Slidev y el sitio VitePress de cada tema), reorganizado como un grid de tarjetas filtrable en vez de la lista apilada por secciones actual.

**Origen y ubicación del handoff**: mockup de alta fidelidad armado por el usuario con Claude (Claude design/artifacts). El paquete completo ya está copiado dentro de este repo en `landing-redesign/` (a partir de `Website UI mockups.zip` en Downloads, que puede no seguir estando disponible más adelante — por eso quedó copiado acá):
- `landing-redesign/README.md` — spec de diseño completo y detallado: colores, spacing y tipografía exactos (tomados del `index.css` actual, salvo los estados nuevos de dropdown/badge que son valores nuevos), estructura de cada sección, interacciones. **Leer completo antes de implementar.**
- `landing-redesign/reference.html` — referencia estática en HTML/CSS plano del layout. No es código de producción para copiar tal cual: hay que recrear el layout dentro de los `index.html`/`index.css`/`index.js` existentes del repo, no reemplazarlos por este archivo.
- `landing-redesign/logo-inspt.png` — logo INSPT/UTN usado en el header, copia del que ya está en la raíz del repo.

**Resumen del cambio** (detalle completo, con valores exactos de spacing/color, en `landing-redesign/README.md`):
- Header con gradiente (`#1e3a5f → #2563eb`), logo a la izquierda, título "Programación III" centrado, y 3 pills de link a la derecha (Campus Virtual, Mail al docente, Web INSPT).
- Fila de chips de filtro: "Todas (N)", "Unidades", "Próximamente", "Extra", "Deprecado" — en el mockup el filtrado es solo visual, en la implementación real hay que cablear el show/hide por categoría.
- Grid de cards, 3 columnas en desktop / 1 en mobile (mismo breakpoint ~640px que ya usa `index.css`). Orden fijo de categorías: Unidades → Próximamente → Extra → Deprecado (siempre última). Sin número de unidad en la card (se sacó a propósito respecto de la iteración anterior).
- Badge de categoría arriba a la izquierda (solo en Próximamente/Extra/Deprecado, cada una con su color); las cards de Deprecado además llevan `opacity:.5` en toda la card.
- La descarga deja de ser un link único por archivo: pasa a ser un trigger "Descargar ▾" que abre un dropdown listando todos los archivos descargables de esa unidad (slides, apunte, guía de ejercicios, ejercicios adicionales — los que apliquen en cada caso).

**Restricciones técnicas explícitas del handoff — no romper al implementar**:
- Mantener la lógica de redirección a puerto de dev que ya tiene `index.js` (atributos `data-dev-port` / `data-dev-path` en el link principal de cada card).
- Mantener el chequeo de disponibilidad de PDF (HEAD request que deshabilita y marca "No disponible" los links de descarga rotos).
- El toggle de dropdown (abrir con click, cerrar con click afuera o Escape, un solo panel abierto a la vez) ya existe hoy para `.card-download-menu` — adaptarlo al nuevo diseño, no reescribirlo de cero.

**Alcance**: solo los 3 archivos raíz (`index.html`, `index.css`, `index.js`). No toca ningún deck Slidev ni ningún sitio `-docs/`. Contenido real a usar en el grid: los decks ya construidos y commiteados hasta ese punto (Introducción, Cálculo Lambda, Clojure, Git & GitHub, JS Funcional, JS Contemporáneo), con sus datos reales.

**Mapear los módulos futuros como "Próximamente"**: además de las cards con contenido real, agregar una card placeholder (sin links funcionales, sin `data-dev-port`, con el badge "Próximamente") por cada módulo del núcleo que todavía no está construido a esa altura, para que el grid quede completo desde el primer día del restyling y cada deck nuevo después solo tenga que "activar" su card en vez de crearla de cero. Lista completa a esa fecha (ver seccion 5 para el detalle de cada uno):
- Asincronismo (5.4)
- TypeScript (5.5)
- React (5.6)
- Node + Express (5.7)
- MongoDB (5.8)
- Pruebas / Testing (5.9)

Los opcionales de la sección 7 (Next.js, Tailwind CSS, NestJS, React Native con Expo) van en la categoría "Extra" con el mismo criterio de placeholder — están confirmados como fuera del núcleo pero mapeados igual, así quedan visibles como contenido adicional planeado. Cuando se construya cada deck real, su card pasa de "Próximamente"/"Extra" a la categoría "Unidades" con sus links reales.

### 5.4 Asincronismo
**Slug**: `asincronismo`
**Por qué acá**: cierra el bloque de "JS puro" antes de subir a TypeScript. Tema históricamente más difícil — deck propio con ejemplos ejecutables.

**Objetivos**: entender por qué JS es de un solo hilo y qué problema resuelve la asincronía; explicar el event loop a nivel funcional (call stack, task/microtask queue) sin ir a implementación de motor; leer/escribir callbacks y reconocer "callback hell"; usar Promises (`.then`/`.catch`/`.finally`, `Promise.all`); usar `async`/`await` con manejo de errores.

**Contenido sugerido**: motivación (operaciones que tardan: red, disco, timers — por qué bloquear el hilo es inaceptable); call stack + Web APIs/libuv + task queue (candidato fuerte para animación paso a paso con `<v-click>`); callbacks (ejemplo simple → anidado, "callback hell" real); Promises (estados pending/fulfilled/rejected, encadenamiento, `Promise.all`/`Promise.race` mencionado); `async`/`await` como azúcar sobre Promises (reescribir el mismo ejemplo tres formas: callback → promise → async/await); manejo de errores asincrónicos (por qué un `try/catch` sincrónico no atrapa un error dentro de un callback no-async); cierre con microtask vs. macrotask (`setTimeout` vs. `Promise`, nivel "para que no sorprenda en una entrevista").

**Referencia local**: `11 - Asincronismo en JavaScript - Carlos E. Cimino.pdf`.
**Referencias web**: https://developer.mozilla.org/es/docs/Web/JavaScript/Guide/Asynchronous · https://javascript.info/async · Video "What the heck is the event loop anyway?" (Philip Roberts, JSConf) — buscar en YouTube, muy usado en cátedras para explicar el event loop visualmente.

### 5.5 TypeScript
**Slug**: `typescript`
**Por qué acá**: pivot explícito. Todo lo anterior fue JS puro; de acá en adelante (React, Node+Express, MongoDB) el código se presenta en TS.

**Objetivos**: entender qué problema resuelve el tipado estático sobre JS; tipar variables, funciones (parámetros y retorno), objetos e interfaces; usar tipos union y genéricos básicos (`Array<T>`, `Promise<T>`); configurar y correr un proyecto TS mínimo (`tsc`/`tsconfig.json` o `ts-node`); tipar las funciones puras y HOFs ya vistas en JS Funcional.

**Contenido sugerido**: motivación honesta (JS dinámico da flexibilidad y errores tontos que aparecen tarde; TS es JS + capa de tipos que se borra al compilar); tipos básicos (`string`/`number`/`boolean`, arrays tipados, tuplas); `interface`/`type` para modelar objetos (conectar con lo que se va a usar en MongoDB/React más adelante); tipado de funciones (parámetros, retorno, opcionales); union types y narrowing básico; genéricos, introducidos con `Array<T>` (ya lo vienen usando sin saberlo) y `Promise<T>` (conexión directa con Asincronismo); repaso funcional tipando 2-3 ejemplos del deck de JS Funcional (`map`/`filter`/`reduce`, `compose`); config mínima (`tsconfig.json` esencial, `strict: true` recomendado, cómo correr con `ts-node` o build+`node`).

**Referencia local**: `Web Full Stack - TypeScript - Presentación.pptx`.
**Referencias web**: https://www.typescriptlang.org/docs/handbook/intro.html · https://www.typescriptlang.org/play (playground, útil para demos en vivo).

### 5.6 React
**Slug**: `react`
**Por qué acá (antes de backend/DB)**: decisión pedagógica explícita — los estudiantes ya vieron paradigmas imperativos/OO y bases relacionales en los dos primeros años. El salto de paradigma más grande para ellos es el modelo declarativo/basado en componentes, y conecta directo con el eje funcional del curso: un componente de React es, en esencia, una función pura de `props`/`state` a JSX.

**Objetivos**: entender el modelo mental de React (UI como función del estado); crear componentes funcionales, props, composición de componentes; manejar estado local con `useState`; entender inmutabilidad aplicada al estado; manejar efectos con `useEffect` a nivel introductorio (fetch de datos); renderizar listas con `key`, formularios controlados; proyecto en TS desde este deck en adelante.

**Contenido sugerido**: apertura explícita ("un componente de React es una función pura: mismos props/state → mismo JSX" — cita directa al deck de JS Funcional); JSX (qué es realmente: azúcar sobre `React.createElement`, no magia); componentes funcionales + props tipados (`interface Props`); `useState` (por qué no se puede mutar el estado directo — conexión directa con inmutabilidad); renderizado condicional y de listas (`map` de nuevo — otra conexión directa), `key`; formularios controlados (`onChange`, estado sincronizado); `useEffect` introductorio (fetch a una API pública simple, manejo de loading/error); mención de que el styling puede resolverse con CSS plano acá — Tailwind queda para el deck opcional.

**Referencia local**: `Web Full Stack - ReactJS - Presentación.pdf`.
**Referencias web**: https://react.dev/learn (documentación oficial, ya orientada a hooks y componentes funcionales) · https://react.dev/learn/keeping-components-pure (conecta directo con el eje funcional del curso).

### 5.7 Node + Express
**Slug**: `node-express`
**Por qué acá**: primer paso al backend, terreno más "conocido" para ellos que React (lógica de servidor ya vista conceptualmente en materias anteriores) — sirve de contraste explícito: "esto se parece más a lo que ya sabían, esto es lo nuevo".

**Objetivos**: entender Node.js como runtime de JS fuera del navegador; levantar un servidor HTTP con Express; definir rutas y verbos HTTP (CRUD conceptual antes de tocar base de datos); middlewares (concepto y uso: `express.json()`, logging, manejo de errores); estructura mínima de un proyecto backend en TS; formatos de intercambio de datos (JSON como estándar — requisito explícito del programa oficial).

**Contenido sugerido**: Node como runtime (motor V8 + APIs de sistema); Express (servidor "Hello World" mínimo, después rutas); HTTP simple pero en serio (método, path, status codes 200/201/400/404/500); middleware (`(req, res, next)`, ejemplo de logging casero, `express.json()`); CRUD en memoria (array en el server) antes de MongoDB — separar el concepto de "API REST" del de "persistencia real"; manejo de errores centralizado (middleware de error); todo en TS (tipar `Request`/`Response`, reusar interfaces del deck de TypeScript).

**Referencia local**: `08 - Intro al Desarrollo Full Stack - Carlos E. Cimino.pdf`, `Web Full Stack - Introducción - Presentación.pdf`.
**Bibliografía oficial**: Subramanian, *Pro MERN Stack*.
**Referencias web**: https://expressjs.com/es/ (documentación en español) · https://nodejs.org/es/docs · https://github.com/typicode/json-server (útil para ejemplos/ejercicios de API rápidas).

### 5.8 MongoDB
**Slug**: `mongodb`
**Por qué acá**: cierra el backend agregando persistencia real, después de entender la API sin base de datos.

**Objetivos**: entender el modelo de documentos (NoSQL) contrastado con lo relacional ya conocido (SQL Server); CRUD real con MongoDB/Mongoose; diseño básico de esquemas/documentos; conectar el backend Express a Mongo; formatos de intercambio de datos — de "array en memoria" a documento persistido.

**Contenido sugerido**: contraste explícito con SQL Server (tablas/filas/joins vs. colecciones/documentos, sin necesidad de joins, embedding vs. referencing); documentos como JSON (conexión directa: "esto ya lo veníamos mandando por la API, ahora se guarda así"); Mongoose (esquemas tipados conectando con TypeScript, modelos, validaciones básicas); CRUD contra Mongo real reemplazando el array en memoria del deck anterior (mismo endpoint, ahora persistente); conexión (`mongoose.connect`), variables de entorno (`.env`, no commitear secretos); errores comunes (validación, tipos, IDs de Mongo).

**Bibliografía oficial**: Subramanian, *Pro MERN Stack*.
**Referencias web**: https://www.mongodb.com/docs/manual/ · https://mongoosejs.com/docs/ · https://www.mongodb.com/docs/atlas/ (para correr Mongo gestionado gratis, evita instalar Mongo local en las máquinas del laboratorio).

### 5.9 Pruebas (Testing)
**Slug**: `testing`
**Por qué acá**: requisito explícito de la planificación oficial ("Pruebas"). Va al final del núcleo porque recién ahí hay suficiente superficie (funciones puras, componentes, endpoints) para testear con sentido.

**Objetivos**: entender por qué probar sistemáticamente el software (requisito explícito del programa); escribir tests unitarios de funciones puras (conexión directa con JS Funcional: las funciones puras son triviales de testear, por eso importan); testear componentes React a nivel introductorio; testear endpoints de Express; vocabulario de unit vs. integration testing, mocks (nivel conceptual).

**Contenido sugerido**: motivación ("¿cómo sabés que tu código funciona, más allá de probarlo a mano una vez?"); por qué las funciones puras son fáciles de testear (cierre narrativo del eje funcional de toda la materia); Vitest o Jest — **decisión abierta, ver sección 8** — test unitario simple (`describe`/`it`/`expect`, testear una función pura de JS Funcional); testing de componentes con React Testing Library; testing de endpoints con `supertest`; mención de mocks (mockear la conexión a Mongo en un test de endpoint, nivel conceptual).

**Referencias web**: https://vitest.dev/ · https://jestjs.io/es-ES/ · https://testing-library.com/docs/react-testing-library/intro/ · https://github.com/ladjs/supertest.

---

## 6. Apuntes teóricos y guías de ejercicios

**Requisito del docente**: cada tema del núcleo (sección 5.1 a 5.9) necesita, además del deck de Slidev, un **apunte teórico** (texto explicativo más extenso que lo que entra en un slide) y una **guía de ejercicios** — exactamente el mismo tipo de material que ya existe para Cálculo Lambda y Clojure (`lambda-calculus-docs/`, `clojure-docs/`), con apunte + guía de ejercicios + PDF exportado.

**Decisión de arquitectura (confirmada)**: cada tema es un par de carpetas independientes en la raíz del repo, **`<slug>/`** (Slidev) + **`<slug>-docs/`** (VitePress) — el mismo patrón exacto que ya usan `clojure/`+`clojure-docs/` y `lambda-calculus/`+`lambda-calculus-docs/`. Se descartó la alternativa de un único sitio VitePress consolidado (`unidad-4-docs/`) para toda la unidad: rompía la consistencia con el resto del repo (cada presentación ya es un proyecto standalone) y hacía más difícil navegar/mantener cada tema como una unidad autocontenida. El primer deck del núcleo (`git-github/` + `git-github-docs/`) ya sigue este patrón — usarlo como plantilla exacta para los siguientes 8.

Para no repetir 9 veces la configuración de CI que esto implicaría, `.github/workflows/deploy.yml` ya no hardcodea un bloque por sitio VitePress nuevo: además de los dos bloques ya existentes para `lambda-calculus-docs`/`clojure-docs` (que quedan como están, tienen lógica propia), hay un loop genérico que detecta **cualquier** carpeta con `"vitepress"` en su `package.json` y la construye automáticamente (`docs:build` + `scripts/print-pdfs.mjs` + copiar `dist` a `_site/<carpeta>/`). Cada `<slug>-docs/` nuevo que siga el patrón de `git-github-docs/` se integra solo, sin tocar el workflow.

**Estructura por tema** (repetir para cada uno de los 9, tomando `git-github-docs/` como plantilla):
```
<slug>-docs/
├── package.json              # mismo patrón que clojure-docs/package.json — puerto docs:dev propio (ver más abajo)
├── utn-mark-logo.png          # copiar de clojure-docs/ o git-github-docs/, usado en el encabezado del PDF
├── docs/
│   ├── index.md               # landing con hero (mismo patrón que clojure-docs/docs/index.md), single-topic
│   ├── apunte.md
│   ├── ejercicios.md
│   ├── public/
│   │   └── favicon.svg        # copiar de cualquier -docs/ existente, es el mismo para todo el repo
│   └── .vitepress/
│       ├── config.ts          # copiar de git-github-docs/, cambiar title/description/base/nav
│       └── theme/
│           ├── index.ts       # idéntico en todos los -docs/, copiar tal cual
│           └── custom.css     # idéntico en todos los -docs/, copiar tal cual
└── scripts/
    └── print-pdfs.mjs         # copiar de git-github-docs/, cambiar PRINT_PORT (ver abajo) y los paths de copia cruzada
```

**Convenciones de contenido**:
- `apunte.md`: explicación teórica extendida en español, con ejemplos de código en inglés (mismas convenciones de idioma que los slides). Más denso que un slide — acá sí entra la explicación completa, no solo el punteo.
- `ejercicios.md`: guía de ejercicios progresiva (de más simple a más complejo), en español, alineada 1 a 1 con los objetivos de la sección 5 del tema correspondiente.
- `scripts/print-pdfs.mjs` de cada `<slug>-docs/` copia los PDF generados **al `<slug>/` del deck Slidev hermano** (`<slug>/pdfs/originales/` y `<slug>/public/pdfs/originales/`), no se sirven desde el propio `<slug>-docs/`. Es el mismo patrón que ya usa `clojure-docs` (`copyPdfToClojureSlidevPublic`) — así el build de Slidev empaqueta el PDF en su propio `dist` y el link de descarga en `index.html` apunta a `./<slug>/pdfs/originales/<slug>-apunte.pdf`, no a `./<slug>-docs/...`.

**Puertos ya usados / a reservar por tema** (`docs:dev` sube de a 2, `PRINT_PORT` sube de a 1 — verificado contra los `package.json`/`scripts/print-pdfs.mjs` reales, no asumido):

| Tema | `docs:dev` port | `PRINT_PORT` | Estado |
|---|---|---|---|
| lambda-calculus-docs | 5173 | 4173 | ✅ construido |
| clojure-docs | 5175 | 4174 | ✅ construido |
| git-github-docs | 5177 | 4175 | ✅ construido |
| js-funcional-docs | 5179 | 4176 | ✅ construido |
| js-contemporaneo-docs | 5181 | 4177 | ✅ construido |
| asincronismo-docs | 5183 | 4178 | ✅ construido |
| typescript-docs | 5185 | 4179 | ✅ construido |
| react-docs | 5187 | 4180 | ✅ construido |
| node-express-docs | 5189 | 4181 | pendiente |
| mongodb-docs | 5191 | 4182 | pendiente |
| testing-docs | 5193 | 4183 | pendiente |

El deck Slidev hermano (`<slug>/`) usa el siguiente puerto libre en la secuencia `dev.sh` (3031, 3032, ... — ver array `PORTS` en `dev.sh`). **Nota histórica**: Asincronismo (3038), TypeScript (3039) y React (3040) se construyeron en branches paralelos a partir de `main` (no secuenciales entre sí) — los puertos se asignaron de antemano siguiendo el orden de esta tabla para que no chocaran al mergear. Los tres ya están mergeados a `main`. Próximo tema del núcleo usa `3041`.

**Cambios necesarios en el resto del repo por cada tema nuevo** (no olvidar):
- `index.html`: **no se agregan tarjetas nuevas** para los 6 temas restantes del núcleo (5.4 a 5.9) — ya existe una card placeholder `data-category="proximamente" data-pending="true"` para cada uno. Hay que **activarla**: sacarle `data-pending`, cambiar `data-category` a `"unidad"`, sacar el `<span class="badge ...">`, y agregar el bloque `.card-actions` real (pills `.view-link` a `./<slug>/` y `./<slug>-docs/` + el `.card-download-menu` con los PDFs) — copiar la estructura completa de una card de unidad ya activada (ej. la de "JS Contemporáneo") como plantilla exacta, cambiando slug/puertos/textos. Para un tema fuera del núcleo (sección 7) que no tenía placeholder reservado, agregar una card nueva con `data-category="extra"` al final del bloque de Extras. Ver AGENTS.md para el detalle completo de esta estructura.
- `dev.sh`: agregar `<slug>` (el deck Slidev) a los arrays `MODULES`/`PORTS` y sumar un color a `--prefix-colors` si hace falta. Los sitios `-docs` (VitePress) **no** se agregan a `dev.sh` — se levantan a mano con `npm run docs:dev` desde su carpeta.
- `.gitignore`: agregar las 4 líneas del patrón ya usado para cada `<slug>`/`<slug>-docs` existente (dist/cache de VitePress + PDFs generados en `originales/`) — fácil de olvidar porque no rompe nada visiblemente hasta que alguien commitea un PDF grande sin querer.
- `.github/workflows/deploy.yml`: **no hace falta tocarlo** para los `-docs` nuevos (loop genérico, ver arriba) ni para los decks Slidev nuevos (loop genérico ya existente que detecta `"slidev"` en `package.json`).

---

## 7. Opcionales / Avanzado

Se presentan después del núcleo, marcados con `data-category="extra"` (badge `.badge-optional`, ya existe en `index.css`) en `index.html`. Pensados para estudiantes que terminan el integrador con tiempo, o como referencia a futuro. **No llevan apunte/guía de ejercicios obligatorios** salvo que el usuario pida lo contrario — son extensión, no núcleo evaluable. Los 4 ya tienen su card placeholder (`data-pending="true"`) en la landing — ver 5.3bis.

### Next.js
**Slug**: `nextjs`. Extensión directa de React: ruteo basado en archivos, renderizado en servidor (SSR/SSG), API routes. Requiere React sólido antes de tocarlo. Referencia: https://nextjs.org/docs

### Tailwind CSS
**Slug**: `tailwind`. Utility-first CSS. Contenido liviano: clases utilitarias, configuración mínima, integración a un proyecto React/Next existente. Referencia: https://tailwindcss.com/docs

### NestJS
**Slug**: `nestjs`. Framework de backend sobre Node (generalmente sobre Express), TypeScript-first, fuertemente orientado a objetos (decoradores, inyección de dependencias, módulos, al estilo Angular). Presentar explícitamente como contraste de filosofía: el curso entero viene construido sobre un eje funcional, y Nest resuelve el mismo problema con una arquitectura deliberadamente distinta (OO, decoradores, DI) — no es "continuación" de Node+Express sino "otra forma de resolver lo mismo". Referencia: https://docs.nestjs.com/

### React Native con Expo
**Slug**: `expo`. Agregado a pedido explícito del docente. Desarrollo mobile multiplataforma (iOS + Android) reusando el conocimiento de React ya visto, con la ventaja de que Expo permite desarrollar y probar en el dispositivo (vía app "Expo Go" + QR) sin necesitar Xcode/Android Studio instalados — funciona igual de bien en Windows, Linux o macOS, lo cual es relevante porque los estudiantes no todos tienen Mac.

**Objetivos**: entender qué es React Native (mismo modelo de componentes de React, renderiza a vistas nativas en vez de al DOM); levantar un proyecto con Expo CLI; componentes core (`View`, `Text`, `ScrollView`, `Image` — el equivalente mobile de `div`/`span`/`img`); estilos con `StyleSheet` (parecido a CSS-in-JS, pero no es CSS real); navegación básica (`expo-router` o `react-navigation`); correr la app en un dispositivo físico vía Expo Go.

**Contenido sugerido**: contraste explícito con el deck de React ("mismo modelo mental — componentes, props, state, hooks — pero no hay DOM, ni HTML, ni CSS real"); Expo CLI (`npx create-expo-app`), estructura de proyecto; componentes core y su equivalencia con HTML; `StyleSheet.create` (por qué no es CSS, aunque se parezca); navegación entre pantallas; correr en Expo Go (QR) — demo en vivo si es posible.

**Referencias web**: https://docs.expo.dev/ · https://reactnative.dev/docs/getting-started · https://reactnavigation.org/docs/getting-started

---

## 8. Fuera de alcance de este documento (decisiones abiertas / próxima instancia)

- **Proyecto integrador (capstone MERN)**: alcance, si es consigna abierta o cerrada, criterios de evaluación — pendiente, instancia de planificación aparte con el usuario.
- **Vitest vs. Jest** para el deck de Testing (sección 5.9): ambos son razonables, preguntar preferencia del usuario antes de comprometerse (Vitest si el resto del stack usa herramientas más modernas tipo Vite; Jest si se prioriza lo más documentado/extendido en la industria).
- **Mapeo de decks a clases/fechas puntuales**: explícitamente fuera de alcance por pedido del usuario — se hace en otra instancia, después de tener el contenido construido.

---

## 9. Checklist de "hecho" por deck

Antes de dar un deck por terminado y pasar al siguiente:

- [ ] `slides.md` sigue el frontmatter y convenciones de la sección 4.
- [ ] Contenido en español, código en inglés, sin mezclar.
- [ ] Abre retomando explícitamente el deck anterior.
- [ ] Corre localmente sin errores (`cd <slug> && ulimit -n 10240 && npx slidev --port <puerto>`), todos los slides renderizan, sin imágenes rotas.
- [ ] `package.json` sigue el template de `.cursor/rules/pdf-to-slidev.mdc`, con `build --base /programacion-III/<slug>/` correcto.
- [ ] Apunte teórico y guía de ejercicios escritos en `<slug>-docs/docs/` (apunte.md + ejercicios.md), siguiendo la plantilla de `git-github-docs/`.
- [ ] `index.html` actualizado: card placeholder correspondiente activada (`data-category="unidad"`, sin `data-pending`, sin badge, con pills de vista y menú de descarga reales) — ver sección 6.
- [ ] `dev.sh` actualizado si se quiere levantar el deck en el entorno de desarrollo local junto a los demás.
- [ ] Nada commiteado a `main` sin pedido explícito del usuario; si se commitea localmente, mensaje de commit claro y en español o inglés consistente con el resto del historial del repo (ver `git log` para el tono ya usado).

---

## 10. Próximos pasos

1. Revisión de este documento por el usuario (contenido, orden, alcance, decisiones abiertas de la sección 8).
2. `git-github/` + `git-github-docs/` ya construidos como plantilla — usarlos como referencia exacta de estructura para los 8 temas restantes.
3. Construcción deck por deck, en el orden de la sección 5, cada uno probado localmente antes de pasar al siguiente.
4. Decks opcionales (sección 7) y proyecto integrador: después del núcleo completo, instancias separadas.
