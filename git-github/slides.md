---
theme: bricks
title: Programación III - Git & GitHub
download: true
info: |
  Git & GitHub - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: git, github, control de versiones, INSPT, UTN
transition: slide-left
mdc: true
---

# Git & GitHub

Programación III

<div class="flex gap-8 justify-end mr-16 mt-6 items-center">
<img src="/logos/git.svg" alt="Git" class="h-16 opacity-90" />
<img src="/logos/github.svg" alt="GitHub" class="h-14 opacity-90" />
</div>

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: default
---

# El problema sin versionar

```
proyecto_final/
proyecto_final_v2/
proyecto_final_v2_ok/
proyecto_final_v2_ok_definitivo/
proyecto_final_v2_ok_definitivo_AHORA_SI/
```

<v-click>

Problemas:

- No sabemos **qué** cambió entre una carpeta y la siguiente
- No podemos combinar el trabajo de dos personas sobre el mismo archivo
- "Volver atrás" es buscar a mano la carpeta correcta

</v-click>

---
layout: default
---

# ¿Qué es un sistema de control de versiones?

Una herramienta que registra los cambios en un conjunto de archivos a lo largo del tiempo.

<v-click>

Permite:

- Guardar el historial completo — quién cambió qué, y cuándo
- Volver a cualquier versión anterior del proyecto
- Comparar qué cambió entre dos versiones
- Trabajar en equipo sobre los mismos archivos sin pisarse

</v-click>

<v-click>

<div class="mt-6 text-sm italic opacity-80">

No es exclusivo del código — pero es imprescindible para programar en equipo.

</div>

</v-click>

---
layout: default
---

# Antes de Git

El control de versiones no arrancó con Git — pasó por varias generaciones:

<v-click>

- **Sin versionar**: copiar carpetas a mano (`_v2`, `_final`, `_ok`)
- **Local**: el historial vive en la misma máquina — no sirve para trabajar en equipo (ej: RCS, 1982)
- **Centralizado**: un servidor central guarda el historial; hace falta estar conectado a él (CVS, 1986 · Subversion/SVN, 2000)
- **Distribuido**: cada copia tiene el historial completo (Git, 2005 · Mercurial, 2005)

</v-click>

---
layout: default
---

# Centralizado vs. distribuido

<div class="grid grid-cols-2 gap-8 mt-6">
<div class="p-4 rounded-lg bg-red-50 border border-red-200 text-center">

**Centralizado** (ej: SVN)

<div class="mt-4 mx-auto w-32 p-2 rounded bg-red-200 text-sm font-bold">Servidor central</div>
<div class="text-2xl my-1 opacity-60">↓ ↓ ↓</div>
<div class="flex justify-center gap-2 text-xs">
<div class="p-2 rounded bg-white border border-red-200">Copia local</div>
<div class="p-2 rounded bg-white border border-red-200">Copia local</div>
<div class="p-2 rounded bg-white border border-red-200">Copia local</div>
</div>

<div class="mt-4 text-xs opacity-70 text-left">

- Sin conexión al servidor, casi no se puede trabajar
- El servidor es un punto único de falla

</div>
</div>
<div class="p-4 rounded-lg bg-green-50 border border-green-200 text-center">

**Distribuido** (Git)

<div class="flex justify-center gap-2 text-xs mt-4">
<div class="p-2 rounded bg-white border border-green-200">Repo completo</div>
<div class="p-2 rounded bg-white border border-green-200">Repo completo</div>
<div class="p-2 rounded bg-white border border-green-200">Repo completo</div>
</div>
<div class="text-2xl my-1 opacity-60">↔ ↔</div>

<div class="mt-4 text-xs opacity-70 text-left">

- Cada copia tiene el historial completo — funciona offline
- GitHub es *una* copia más, elegida como punto de encuentro

</div>
</div>
</div>

---
layout: default
---

# Git

<img src="/logos/git.svg" alt="Git" class="abs-tr mt-32 mr-20 h-20 opacity-90" />

- Sistema de control de versiones **distribuido**
- Guarda el historial como una serie de **fotos** (snapshots) del proyecto
- Cada foto se llama **commit**
- Corre 100% local — no depende de estar conectado a internet

<div class="mt-6 text-sm italic opacity-80">

No guarda "diferencias línea por línea" — guarda estados completos del proyecto en cada momento.

</div>

---
layout: default
---

# El origen de Git

<div class="flex gap-6 items-start mt-2">
<div class="flex-1">

- 2005 — el kernel de Linux pierde la licencia gratuita de **BitKeeper**, el sistema centralizado que usaba
- **Linus Torvalds** (creador de Linux) escribe Git en un par de semanas para reemplazarlo
- Prioridades de diseño: velocidad, historial distribuido, integridad de los datos, soportar el trabajo no lineal de miles de colaboradores

<div class="mt-6 text-sm italic opacity-80">

El nombre es jerga británica informal para "persona molesta" — Torvalds bromeó con que, como ya había hecho con Linux, elegía nombrar sus proyectos en base a sí mismo.

</div>

</div>
<div class="shrink-0 text-center">
<img src="/people/linus-torvalds.jpg" alt="Linus Torvalds" class="w-36 rounded-lg shadow" />
<div class="mt-1 text-xs opacity-50">Linus Torvalds, 2014</div>
</div>
</div>

---
layout: default
---

# Características de Git

<v-click>

- **Integridad**: cada commit se identifica con un hash que depende de su contenido — si algo cambia, el hash cambia
- **Ramas livianas**: crear, cambiar y combinar ramas es rápido y casi no ocupa espacio
- **Staging area**: se elige qué cambios entran en el próximo commit, no es todo o nada
- **No lineal**: soporta miles de ramas y colaboradores trabajando en paralelo
- **Gratuito, de código abierto y estándar de facto** de la industria

</v-click>

---
layout: default
---

# Instalar Git

<div class="grid grid-cols-3 gap-4 mt-6 text-sm text-center">
<div class="p-4 rounded-lg bg-gray-100">

**Windows**

Instalador oficial (incluye Git Bash)

</div>
<div class="p-4 rounded-lg bg-gray-100">

**macOS**

```bash
brew install git
```

</div>
<div class="p-4 rounded-lg bg-gray-100">

**Linux**

```bash
sudo apt install git
```

</div>
</div>

<div class="mt-6">

```bash
git --version                               # confirma la instalación

git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

</div>

<div class="mt-4 text-xs opacity-70 text-center">

Descarga oficial: <a href="https://git-scm.com/downloads" target="_blank" rel="noopener">git-scm.com/downloads</a>

</div>

---
layout: default
---

# Modelo mental

Tres áreas de trabajo

<div class="flex items-center justify-center gap-2 mt-10 text-center">
<div class="w-44 p-4 rounded-lg bg-gray-100">

**Working directory**

Los archivos tal como están en el disco

</div>
<div class="flex flex-col items-center px-1 shrink-0">
<div class="text-2xl">→</div>
<div class="text-xs font-mono mt-1">git add</div>
</div>
<div class="w-44 p-4 rounded-lg bg-gray-100">

**Staging area**

Qué cambios van a ir en el próximo commit

</div>
<div class="flex flex-col items-center px-1 shrink-0">
<div class="text-2xl">→</div>
<div class="text-xs font-mono mt-1">git commit</div>
</div>
<div class="w-44 p-4 rounded-lg bg-gray-100">

**Repository**

El historial ya confirmado (`.git/`)

</div>
</div>

---
layout: default
---

# Iniciar un repositorio

```bash
mkdir tienda-online && cd tienda-online
git init
```

```text
Initialized empty Git repository in ~/tienda-online/.git/
```

<div class="mt-4 text-sm opacity-80">

Crea una carpeta oculta `.git/` — a partir de acá, este directorio es un repositorio Git.

</div>

---
layout: default
---

# ¿Qué está pasando?

```bash
git status
```

```text {all}
On branch main
Changes not staged for commit:
	modified:   src/cart.js

Untracked files:
	src/validation.js
```

<v-click>

Objetivo: ver el estado actual del repositorio **antes** de decidir el próximo paso — no modifica nada, es solo información.

</v-click>

<v-click>

Acá dice: `cart.js` ya existía y cambió; `validation.js` es nuevo y todavía no se le dijo nada a Git sobre él.

</v-click>

<v-click>

Conviene correrlo seguido — sobre todo justo antes de `add` o `commit`, para saber qué se está por confirmar.

</v-click>

---
layout: default
---

# Agregar y confirmar cambios

```bash
git add src/validation.js    # un archivo puntual
git add .                    # todos los cambios del directorio actual

git commit -m "Add user validation function"
```

<div class="mt-4 text-sm opacity-80">

El mensaje describe **qué** cambia — no "cambios" o "fix" a secas (más sobre esto en unos slides).

</div>

---
layout: default
---

# Ver el historial

```bash
git log
git log --oneline    # una línea por commit
```

<div class="mt-4">

```bash {all}
$ git log --oneline
a3f9c21 Fix validation error on empty email field
7d1e8b4 Add user validation function
1c2a908 Initial commit
```

</div>

---
layout: default
---

# `.gitignore`

Le dice a Git qué **no** versionar.

```text
node_modules/
dist/
.slidev/
*.log
.env
```

<v-click>

`.env` es particular: ahí van credenciales y claves — **nunca se commitea**.

</v-click>

<v-click>

<div class="mt-4 text-sm">

**En la práctica:**

```bash {all}
$ git status
Untracked files:
	.env

$ echo ".env" >> .gitignore
$ git status
# .env ya no aparece en la lista — Git lo ignora
```

</div>

</v-click>

---
layout: center
---

# Ramas (branches)

---
layout: default
---

# ¿Qué es una rama?

Una línea de desarrollo independiente. Por defecto: `main`.

Crear una rama nueva permite probar algo **sin afectar** el código que ya funciona.

```bash
git branch feature/login          # crea la rama
git switch feature/login          # se posiciona en esa rama

git switch -c feature/login       # crea y se posiciona en un solo paso
```

<v-click>

<div class="mt-4 text-sm opacity-80">

Esto es lo que hace posible trabajar en equipo: cada persona (o cada feature) avanza en su propia rama, en paralelo, sin pisar el trabajo de las demás — y se integra todo a `main` recién cuando está listo.

</div>

</v-click>

---
layout: default
---

# Convenciones para nombrar ramas

<div class="text-sm">

| Prefijo | Se usa para |
|---|---|
| `feature/` | una funcionalidad nueva |
| `fix/` | corregir un bug |
| `docs/` | solo documentación |
| `refactor/` | cambio interno sin alterar comportamiento |
| `test/` | agregar o corregir tests |
| `chore/` | mantenimiento (dependencias, configuración) |

</div>

<v-click>

<div class="mt-4 text-sm">

- Alineado a los mismos tipos que vamos a ver en **Conventional Commits** más adelante — el nombre de la rama ya anticipa qué va a decir el commit
- `kebab-case`, corto y descriptivo: `feature/carrito-compras`, no `feature/JuanCambios`
- Una rama = un cambio lógico — no mezclar varias features en la misma
- Borrarla después del merge, ya cumplió su función

</div>

</v-click>

---
layout: default
---

# Ramas en paralelo

Un repo real no tiene una sola rama a la vez — tiene varias, en distintos estados:

<svg viewBox="0 0 720 300" class="w-full max-w-3xl mx-auto mt-2">
  <!-- main -->
  <line x1="40" y1="260" x2="680" y2="260" stroke="#3b82f6" stroke-width="3" />
  <circle cx="70" cy="260" r="7" fill="#3b82f6" />
  <circle cx="300" cy="260" r="7" fill="#3b82f6" />
  <circle cx="680" cy="260" r="7" fill="#3b82f6" />

  <!-- feature/login: ya fusionada -->
  <path d="M 140 260 C 160 260, 160 170, 180 170 L 260 170 C 280 170, 280 260, 300 260" fill="none" stroke="#22c55e" stroke-width="3" />
  <circle cx="140" cy="260" r="6" fill="#22c55e" />
  <circle cx="200" cy="170" r="6" fill="#22c55e" />
  <circle cx="240" cy="170" r="6" fill="#22c55e" />

  <!-- feature/cart: en progreso -->
  <path d="M 340 260 C 360 260, 360 130, 380 130 L 520 130" fill="none" stroke="#8b5cf6" stroke-width="3" />
  <path d="M 520 130 L 650 130" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-dasharray="6 6" />
  <circle cx="340" cy="260" r="6" fill="#8b5cf6" />
  <circle cx="420" cy="130" r="6" fill="#8b5cf6" />
  <circle cx="480" cy="130" r="6" fill="#8b5cf6" />

  <!-- feature/payments: recién creada -->
  <path d="M 560 260 C 575 260, 575 205, 590 205 L 610 205" fill="none" stroke="#f97316" stroke-width="3" />
  <path d="M 610 205 L 650 205" fill="none" stroke="#f97316" stroke-width="3" stroke-dasharray="6 6" />
  <circle cx="560" cy="260" r="6" fill="#f97316" />
  <circle cx="600" cy="205" r="6" fill="#f97316" />

  <!-- labels -->
  <text x="40" y="283" style="font-size:13px;font-family:monospace;fill:#374151">main</text>
  <text x="680" y="245" style="font-size:11px;font-family:sans-serif;fill:#6b7280" text-anchor="end">HEAD</text>
  <text x="180" y="158" style="font-size:12px;font-family:monospace;fill:#16a34a">feature/login</text>
  <text x="380" y="118" style="font-size:12px;font-family:monospace;fill:#7c3aed">feature/cart</text>
  <text x="560" y="195" style="font-size:12px;font-family:monospace;fill:#ea580c">feature/payments</text>
</svg>

<div class="flex justify-center gap-6 mt-2 text-xs">
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#22c55e"></span> fusionada</div>
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#8b5cf6"></span> en progreso</div>
<div class="flex items-center gap-1"><span class="inline-block w-3 h-3 rounded-full" style="background:#f97316"></span> recién creada</div>
</div>

---
layout: default
---

# Merge

Cuando el trabajo en la rama está listo, se combina de vuelta a `main`:

```bash
git switch main
git merge feature/login
```

```text
Updating 1c2a908..a3f9c21
Fast-forward
 src/validation.js | 12 ++++++++++++
 1 file changed, 12 insertions(+)
```

<v-click>

Si ambas ramas modificaron las mismas líneas de un mismo archivo, Git no puede decidir solo — eso es un **conflicto de merge**, y se resuelve a mano.

</v-click>

---
layout: center
---

# Trabajando con GitHub

---
layout: default
---

# GitHub

<img src="/logos/github.svg" alt="GitHub" class="abs-tr mt-32 mr-20 h-20 opacity-90" />

- Servicio que **aloja** repositorios Git en la nube
- Agrega colaboración: Pull Requests, revisión de código, Issues
- **Actions**: automatización y CI/CD integrados al repositorio
- **Projects**: tableros tipo kanban para organizar el trabajo
- **Pages**: hosting gratuito para sitios estáticos desde un repo
- Git es la herramienta; GitHub es *un lugar* donde alojar un repositorio Git

<div class="mt-6 text-xs opacity-70">

<a href="https://github.com" target="_blank" rel="noopener">github.com</a>

</div>

---
layout: default
---

# GitHub y sus competidores

GitHub es el más usado, pero no el único que aloja repositorios Git:

<div class="grid grid-cols-3 gap-4 mt-6 text-sm">
<div class="p-4 rounded-lg bg-gray-100 text-center">

<img src="/logos/github.svg" alt="GitHub" class="h-8 mx-auto mb-2" />

**GitHub**

Pull Requests · el más usado · de Microsoft · Actions gratis en repos públicos

<div class="mt-2 text-xs opacity-70"><a href="https://github.com" target="_blank" rel="noopener">github.com</a></div>

</div>
<div class="p-4 rounded-lg bg-gray-100 text-center">

<img src="/logos/gitlab.svg" alt="GitLab" class="h-8 mx-auto mb-2" />

**GitLab**

Merge Requests · fuerte en CI/CD · se puede auto-alojar · todo-en-uno (registry, monitoreo)

<div class="mt-2 text-xs opacity-70"><a href="https://gitlab.com" target="_blank" rel="noopener">gitlab.com</a></div>

</div>
<div class="p-4 rounded-lg bg-gray-100 text-center">

<img src="/logos/bitbucket.svg" alt="Bitbucket" class="h-8 mx-auto mb-2" />

**Bitbucket**

Pull Requests · integrado con Jira/Trello · de Atlassian · gratis para equipos de hasta 5

<div class="mt-2 text-xs opacity-70"><a href="https://bitbucket.org" target="_blank" rel="noopener">bitbucket.org</a></div>

</div>
</div>

<div class="mt-6 text-sm italic opacity-80">

El concepto (Git) es el mismo en los tres — lo que cambia es la plataforma de colaboración alrededor.

</div>

---
layout: default
---

# Crear cuenta en GitHub

1. Ir a <a href="https://github.com/join" target="_blank" rel="noopener">github.com/join</a>
2. Elegir un nombre de usuario — va a aparecer en la URL de todos los repos (`github.com/tu-usuario`)
3. Verificar el email

<div class="mt-6 text-sm opacity-80">

Con la cuenta creada ya se puede: crear repositorios, clonar los de otras personas, y participar de Pull Requests.

</div>

<v-click>

<div class="mt-6 text-sm">

**Recomendaciones**

- Usuario profesional y corto — va a acompañar el perfil de por vida (evitar apodos)
- Usar el mismo usuario que en LinkedIn/portfolio, para que sea fácil de encontrar
- Completar el perfil: foto, nombre y una bio corta
- Activar la verificación en dos pasos (2FA) en la configuración de seguridad

</div>

</v-click>

---
layout: default
---

# `origin`

La conexión entre nuestro repositorio local y el remoto se llama, por convención, `origin`.

```bash
git clone https://github.com/tu-usuario/tienda-online.git   # trae una copia local
git push origin main                                          # sube commits locales
git pull origin main                                          # trae commits nuevos
```

---
layout: default
---

# Pull Requests

En equipo, **no** se hace `push` directo a `main`.

1. Se crea una rama con el cambio propuesto
2. Se sube esa rama al remoto
3. Se abre un **Pull Request**: una propuesta de "traer estos cambios a `main`"
4. Otra persona revisa, comenta, aprueba (o pide cambios)
5. Recién ahí se mezcla

<div class="mt-6 text-sm italic opacity-80">

Este es el flujo que vamos a usar en los trabajos prácticos de acá en adelante.

</div>

---
layout: default
---

# El ciclo completo de una feature

<div class="flex flex-wrap items-center justify-center gap-2 mt-10 text-xs">
<div class="px-3 py-2 rounded-lg bg-blue-50 border border-blue-200 font-mono">switch -c feature/x</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-blue-50 border border-blue-200 font-mono">commits</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-blue-50 border border-blue-200 font-mono">push</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-orange-50 border border-orange-200">Pull Request</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-orange-50 border border-orange-200">Revisión</div>
<div class="opacity-50">→</div>
<div class="px-3 py-2 rounded-lg bg-green-50 border border-green-200 font-mono">merge</div>
</div>

<div class="text-center mt-6 text-sm opacity-70">

↺ y se repite con la próxima rama

</div>

<div class="mt-8 mx-auto max-w-lg p-3 rounded-lg bg-gray-100 text-xs text-center font-mono">

feature/agregar-favoritos → 4 commits → push → PR #23 → 2 comentarios → merge a main

</div>

---
layout: default
---

# Buenas prácticas de commit

<div class="grid grid-cols-2 gap-6 mt-4">
<div class="p-4 rounded-lg bg-red-50 border border-red-200">

**Mal**

```bash
git commit -m "cambios"
git commit -m "fix"
git commit -m "asdf"
```

</div>
<div class="p-4 rounded-lg bg-green-50 border border-green-200">

**Bien**

```bash
git commit -m "Fix validation error \
on empty email field"
```

</div>
</div>

<div class="mt-6">

- Modo imperativo: `Add`, `Fix`, `Remove` — no `Added`, `Fixing`
- Corto y descriptivo — si hace falta más detalle, en líneas siguientes

</div>

---
layout: default
---

# Conventional Commits

Un estándar (no obligatorio, pero muy usado) para el mensaje: `<tipo>(<alcance>): <descripción>`

<div class="mt-3 text-sm">

| Tipo | Se usa para |
|---|---|
| `feat` | una funcionalidad nueva |
| `fix` | corregir un bug |
| `docs` | solo documentación |
| `refactor` | cambio interno sin alterar comportamiento |
| `test` | agregar o corregir tests |

</div>

<div class="mt-3">

```bash
git commit -m "feat(auth): agregar validación de email"
git commit -m "fix(cart): corregir cálculo de totales con descuento"
```

</div>

<div class="mt-3 text-xs opacity-70 text-center">

Especificación completa: <a href="https://www.conventionalcommits.org/es/" target="_blank" rel="noopener">conventionalcommits.org</a>

</div>

---
layout: default
---

# Git cheat sheet

<div class="grid grid-cols-2 gap-8 mt-2 text-sm">
<div>

**Local**

| Comando | Qué hace |
|---|---|
| `git init` | Crea un repo nuevo |
| `git status` | Estado actual |
| `git add <archivo>` | Manda al staging |
| `git commit -m "..."` | Confirma un commit |
| `git log --oneline` | Historial resumido |
| `.gitignore` | Qué no versionar |

</div>
<div>

**Ramas y remoto**

| Comando | Qué hace |
|---|---|
| `git branch <nombre>` | Crea una rama |
| `git switch <rama>` | Cambia de rama |
| `git switch -c <rama>` | Crea y cambia |
| `git merge <rama>` | Combina ramas |
| `git clone <url>` | Copia local del remoto |
| `git push`/`pull origin <rama>` | Sube/trae commits |

</div>
</div>

---
layout: default
---

# Referencias y recursos

<div class="space-y-3 mt-2">

- [git-scm.com](https://git-scm.com/) — sitio oficial de Git, documentación y el libro *Pro Git* gratis
- [git-scm.com/docs](https://git-scm.com/docs) — referencia completa de comandos
- [docs.github.com](https://docs.github.com/es/get-started) — documentación oficial de GitHub (Pull Requests, Issues, etc.)
- [GitHub Skills](https://skills.github.com/) — cursos interactivos oficiales de GitHub
- [learngitbranching.js.org](https://learngitbranching.js.org/) — practicar ramas y merges de forma visual e interactiva

</div>
