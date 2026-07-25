# Git & GitHub

## Por qué versionar código

Antes de escribir la primera línea de código de un proyecto en equipo, necesitamos poder guardar el historial de nuestro trabajo, volver atrás cuando algo se rompe, y colaborar con otras personas sin pisarnos el código. Ese problema lo resuelve un **sistema de control de versiones**.

Sin uno, la alternativa habitual es algo así:

```
proyecto_final/
proyecto_final_v2/
proyecto_final_v2_ok/
proyecto_final_v2_ok_definitivo/
proyecto_final_v2_ok_definitivo_AHORA_SI/
```

Este esquema tiene varios problemas: no sabemos *qué* cambió entre una carpeta y la siguiente, no podemos combinar el trabajo de dos personas sobre el mismo archivo, y "volver atrás" significa buscar a mano la carpeta correcta.

## Antes de Git: generaciones de control de versiones

El control de versiones no arrancó con Git — pasó por varias generaciones:

- **Sin versionar**: copiar carpetas a mano (`_v2`, `_final`, `_ok`).
- **Local**: el historial vive en la misma máquina — no sirve para trabajar en equipo (ej: RCS, 1982).
- **Centralizado**: un servidor central guarda el historial; hace falta estar conectado a él para casi cualquier operación (CVS, 1986 · Subversion/SVN, 2000).
- **Distribuido**: cada copia tiene el historial completo (Git, 2005 · Mercurial, 2005).

<div class="card-grid card-grid-2">
<div class="info-card tone-red">
<h4>Centralizado (ej: SVN)</h4>

Un servidor central guarda el único historial completo; cada persona tiene solo una copia de trabajo.

<ul class="card-note">
<li>Sin conexión al servidor, casi no se puede trabajar</li>
<li>El servidor es un punto único de falla</li>
</ul>
</div>
<div class="info-card tone-green">
<h4>Distribuido (Git)</h4>

Cada copia (cada clon) tiene el historial completo del proyecto, no solo el estado actual.

<ul class="card-note">
<li>Cada copia funciona offline — no depende de estar conectada</li>
<li>GitHub es <em>una</em> copia más, elegida como punto de encuentro del equipo</li>
</ul>
</div>
</div>

## El origen de Git

- 2005 — el kernel de Linux pierde la licencia gratuita de **BitKeeper**, el sistema centralizado que usaba hasta entonces.
- **Linus Torvalds** (creador de Linux) escribe Git en un par de semanas para reemplazarlo.
- Prioridades de diseño: velocidad, historial distribuido, integridad de los datos, y soportar el trabajo no lineal de miles de colaboradores simultáneos — la escala del propio kernel de Linux.

El nombre es jerga británica informal para "persona molesta" — el propio Torvalds bromeó con que, como ya había hecho con Linux, elegía nombrar sus proyectos en base a sí mismo.

## Qué es Git

**Git** es un sistema de control de versiones **distribuido**: guarda el historial completo de un proyecto como una serie de *fotos* (snapshots) del estado de los archivos en cada momento, no como una lista de diferencias línea por línea. Cada snapshot se llama **commit**. Corre 100% local — no depende de estar conectado a internet para casi ninguna operación cotidiana (`commit`, `log`, `diff`, crear ramas...).

## Qué es GitHub

**GitHub** es un servicio que **aloja** repositorios Git en la nube y agrega funcionalidades de colaboración: Pull Requests, revisión de código, issues. Git es la herramienta; GitHub es *un lugar* donde alojar un repositorio Git — el concepto de Git es exactamente el mismo se use o no se use GitHub.

### GitHub y sus competidores

GitHub es el más usado, pero no el único servicio que aloja repositorios Git. El concepto de Git es el mismo en los tres — lo que cambia es la plataforma de colaboración alrededor:

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>GitHub</h4>

Pull Requests · el más usado · de Microsoft

<div class="card-note"><a href="https://github.com" target="_blank" rel="noopener">github.com</a></div>
</div>
<div class="info-card">
<h4>GitLab</h4>

Merge Requests · fuerte en CI/CD integrado · se puede auto-alojar

<div class="card-note"><a href="https://gitlab.com" target="_blank" rel="noopener">gitlab.com</a></div>
</div>
<div class="info-card">
<h4>Bitbucket</h4>

Pull Requests · integrado con Jira/Trello · de Atlassian

<div class="card-note"><a href="https://bitbucket.org" target="_blank" rel="noopener">bitbucket.org</a></div>
</div>
</div>

## Instalar Git y crear una cuenta en GitHub

**Instalación**, según el sistema operativo:

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>Windows</h4>

Instalador oficial (incluye Git Bash)
</div>
<div class="info-card">

<h4>macOS</h4>

```bash
brew install git
```
</div>
<div class="info-card">
<h4>Linux</h4>

```bash
sudo apt install git
```
</div>
</div>

Una vez instalado, conviene confirmarlo y configurar la identidad que va a quedar registrada en cada commit:

```bash
git --version                               # confirma la instalación

git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Descarga oficial: [git-scm.com/downloads](https://git-scm.com/downloads).

**Crear una cuenta en GitHub:**

1. Ir a [github.com/join](https://github.com/join).
2. Elegir un nombre de usuario — va a aparecer en la URL de todos los repos (`github.com/tu-usuario`).
3. Verificar el email.

Con la cuenta creada ya se puede: crear repositorios, clonar los de otras personas, y participar de Pull Requests.

## Modelo mental: snapshots, no diffs

Cada vez que hacemos un commit, Git guarda una foto completa del estado de los archivos que le pedimos que guarde. Internamente es más eficiente que eso (los archivos que no cambiaron no se duplican), pero para razonar sobre Git alcanza con pensar: **"un commit es una foto del proyecto en un momento dado"**.

Un repositorio Git tiene tres áreas conceptuales:

- **Working directory**: los archivos tal como están en el disco, con los que estamos trabajando.
- **Staging area** (o *index*): un área intermedia donde marcamos qué cambios van a formar parte del próximo commit.
- **Repository** (`.git/`): el historial ya guardado — todos los commits confirmados.

<div class="flow-row flow-vertical">
<div class="flow-box"><strong>Working directory</strong><br>Los archivos tal como están en el disco</div>
<div class="flow-arrow"><span class="arrow-glyph">→</span><code>git add</code></div>
<div class="flow-box"><strong>Staging area</strong><br>Qué cambios van a ir en el próximo commit</div>
<div class="flow-arrow"><span class="arrow-glyph">→</span><code>git commit</code></div>
<div class="flow-box"><strong>Repository</strong><br>El historial ya confirmado (<code>.git/</code>)</div>
</div>

El flujo típico es: modificamos archivos en el *working directory* → los agregamos al *staging area* con `git add` → confirmamos ese conjunto de cambios como un commit con `git commit`.

## Comandos esenciales

Los siguientes ejemplos siguen un mismo caso de uso: un proyecto llamado `tienda-online`.

### Iniciar un repositorio

```bash
mkdir tienda-online && cd tienda-online
git init
```

```
Initialized empty Git repository in ~/tienda-online/.git/
```

Crea una carpeta oculta `.git/` en el directorio actual — a partir de ahí, ese directorio es un repositorio Git.

### Ver el estado actual

```bash
git status
```

```
On branch main
Changes not staged for commit:
	modified:   src/cart.js

Untracked files:
	src/validation.js
```

El objetivo de `git status` es ver el estado actual del repositorio **antes** de decidir el próximo paso — no modifica nada, es solo información. En el ejemplo: `cart.js` ya existía y cambió; `validation.js` es nuevo y todavía no se le dijo nada a Git sobre él. Conviene correrlo seguido, sobre todo justo antes de `add` o `commit`, para saber qué se está por confirmar.

### Agregar cambios al staging area

```bash
git add src/validation.js    # un archivo puntual
git add .                    # todos los cambios del directorio actual
```

### Confirmar un commit

```bash
git commit -m "Add user validation function"
```

El mensaje (`-m`) debería describir *qué* cambia y, si hace falta, *por qué* — no "cambios" o "fix" a secas (ver la sección de buenas prácticas más abajo).

### Ver el historial

```bash
git log
git log --oneline    # una línea por commit, más fácil de leer
```

```
$ git log --oneline
a3f9c21 Fix validation error on empty email field
7d1e8b4 Add user validation function
1c2a908 Initial commit
```

### Ignorar archivos

Un archivo `.gitignore` en la raíz del proyecto le dice a Git qué **no** versionar — típicamente `node_modules/`, archivos de build, credenciales locales. Ejemplo real (tomado de este mismo repositorio):

```text
node_modules/
dist/
.slidev/
*.log
.env
```

`.env` es particularmente importante: ahí van credenciales y claves — **nunca se commitea**.

En la práctica, agregar una entrada al `.gitignore` hace que ese archivo desaparezca de `git status`:

```
$ git status
Untracked files:
	.env

$ echo ".env" >> .gitignore
$ git status
# .env ya no aparece en la lista — Git lo ignora
```

## Ramas (branches)

Una **rama** es una línea de desarrollo independiente. Por defecto, un repositorio nuevo tiene una rama principal (`main`). Crear una rama nueva permite probar algo sin afectar el código que ya funciona en `main`.

```bash
git branch feature/login          # crea la rama
git switch feature/login          # se posiciona en esa rama
# (equivalente más viejo: git checkout feature/login)

git switch -c feature/login       # crea y se posiciona en un solo paso
```

Esto es lo que hace posible trabajar en equipo: cada persona (o cada feature) avanza en su propia rama, en paralelo, sin pisar el trabajo de las demás — y se integra todo a `main` recién cuando está listo.

### Varias ramas a la vez

Un repositorio real no tiene una sola rama activa — tiene varias, en distintos estados: algunas ya se fusionaron, otras siguen en curso, otras recién arrancaron.

<div class="branch-diagram-wrap">
<svg viewBox="0 0 720 300" class="branch-diagram" role="img" aria-label="Diagrama de tres ramas: feature/login ya fusionada, feature/cart en progreso, feature/payments recién creada">
  <line x1="40" y1="260" x2="680" y2="260" stroke="#3b82f6" stroke-width="3" />
  <circle cx="70" cy="260" r="7" fill="#3b82f6" />
  <circle cx="300" cy="260" r="7" fill="#3b82f6" />
  <circle cx="680" cy="260" r="7" fill="#3b82f6" />

  <path d="M 140 260 C 160 260, 160 170, 180 170 L 260 170 C 280 170, 280 260, 300 260" fill="none" stroke="#22c55e" stroke-width="3" />
  <circle cx="140" cy="260" r="6" fill="#22c55e" />
  <circle cx="200" cy="170" r="6" fill="#22c55e" />
  <circle cx="240" cy="170" r="6" fill="#22c55e" />

  <path d="M 340 260 C 360 260, 360 130, 380 130 L 520 130" fill="none" stroke="#8b5cf6" stroke-width="3" />
  <path d="M 520 130 L 650 130" fill="none" stroke="#8b5cf6" stroke-width="3" stroke-dasharray="6 6" />
  <circle cx="340" cy="260" r="6" fill="#8b5cf6" />
  <circle cx="420" cy="130" r="6" fill="#8b5cf6" />
  <circle cx="480" cy="130" r="6" fill="#8b5cf6" />

  <path d="M 560 260 C 575 260, 575 205, 590 205 L 610 205" fill="none" stroke="#f97316" stroke-width="3" />
  <path d="M 610 205 L 650 205" fill="none" stroke="#f97316" stroke-width="3" stroke-dasharray="6 6" />
  <circle cx="560" cy="260" r="6" fill="#f97316" />
  <circle cx="600" cy="205" r="6" fill="#f97316" />

  <text x="40" y="283" style="font-size:13px;font-family:monospace;fill:#374151">main</text>
  <text x="680" y="245" style="font-size:11px;font-family:sans-serif;fill:#6b7280" text-anchor="end">HEAD</text>
  <text x="180" y="158" style="font-size:12px;font-family:monospace;fill:#16a34a">feature/login</text>
  <text x="380" y="118" style="font-size:12px;font-family:monospace;fill:#7c3aed">feature/cart</text>
  <text x="560" y="195" style="font-size:12px;font-family:monospace;fill:#ea580c">feature/payments</text>
</svg>
</div>
<div class="diagram-legend">
<span><span class="dot" style="background:#22c55e"></span>fusionada</span>
<span><span class="dot" style="background:#8b5cf6"></span>en progreso</span>
<span><span class="dot" style="background:#f97316"></span>recién creada</span>
</div>

`main` sigue intacto mientras cada rama avanza en paralelo — se combinan recién en su propio merge.

### Merge

Cuando el trabajo en una rama está listo, se **combina** (merge) de vuelta a `main`:

```bash
git switch main
git merge feature/login
```

```
Updating 1c2a908..a3f9c21
Fast-forward
 src/validation.js | 12 ++++++++++++
 1 file changed, 12 insertions(+)
```

Si ambas ramas modificaron las mismas líneas de un mismo archivo, Git no puede decidir solo cuál versión es la correcta — eso es un **conflicto de merge**, y hay que resolverlo a mano editando el archivo. Los conflictos avanzados y `git rebase` quedan fuera de este apunte introductorio; se abordan en la práctica cuando aparecen en un caso real.

## Trabajando con GitHub

Un repositorio en GitHub es un repositorio Git alojado remotamente. La conexión entre nuestro repositorio local y el remoto se llama, por convención, `origin`.

```bash
# trae una copia local de un repo remoto
git clone https://github.com/tu-usuario/tienda-online.git

git push origin main   # sube nuestros commits locales al remoto
git pull origin main   # trae los commits nuevos del remoto
```

### Pull Requests

Cuando se trabaja en equipo, la práctica habitual **no** es hacer `push` directo a `main`. En cambio:

1. Se crea una rama con el cambio propuesto.
2. Se sube esa rama al remoto (`git push origin nombre-de-la-rama`).
3. En GitHub, se abre un **Pull Request (PR)**: una propuesta de "traer estos cambios a `main`".
4. Otra persona revisa, comenta, aprueba (o pide cambios).
5. Recién ahí se mezcla.

Este flujo es el que se va a usar en los trabajos prácticos de la materia de acá en adelante.

### El ciclo completo de una feature

<div class="flow-row">
<div class="flow-box tone-brand"><code>switch -c feature/x</code></div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-brand"><code>commits</code></div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-brand"><code>push</code></div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-yellow">Pull Request</div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-yellow">Revisión</div>
<div class="flow-arrow"><span class="arrow-glyph">→</span></div>
<div class="flow-box tone-green"><code>merge</code></div>
</div>

Y se repite con la próxima rama — cada feature nueva vuelve a arrancar desde `main` actualizado.

## Buenas prácticas de mensajes de commit

Un buen mensaje de commit:

- Describe **qué** cambia, en modo imperativo (`Add`, `Fix`, `Remove` — no `Added`, `Fixing`).
- Es corto en la primera línea (idealmente menos de 50-70 caracteres) y, si hace falta más detalle, lo agrega en líneas siguientes separadas por una línea en blanco.
- No dice simplemente `"cambios"`, `"fix"`, `"asdf"` — estos mensajes no ayudan a nadie (ni a uno mismo) a entender el historial más adelante.

```bash
# Mal
git commit -m "cambios"
git commit -m "fix"
git commit -m "asdf"

# Bien
git commit -m "Fix validation error on empty email field"
```

### Conventional Commits

**Conventional Commits** es un estándar (no obligatorio, pero muy usado en la industria) para el formato del mensaje:

```
<tipo>(<alcance opcional>): <descripción>
```

| Tipo | Se usa para |
|---|---|
| `feat` | una funcionalidad nueva |
| `fix` | corregir un bug |
| `docs` | solo documentación |
| `refactor` | cambio interno sin alterar comportamiento |
| `test` | agregar o corregir tests |

```bash
git commit -m "feat(auth): agregar validación de email"
git commit -m "fix(cart): corregir cálculo de totales con descuento"
```

Especificación completa: [conventionalcommits.org](https://www.conventionalcommits.org/es/).

## Cheat sheet

<div class="card-grid card-grid-2">
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

Referencia completa y siempre actualizada: [git-scm.com/docs](https://git-scm.com/docs).

## Referencias y recursos

- [git-scm.com](https://git-scm.com/) — sitio oficial de Git, documentación y el libro *Pro Git* gratis
- [git-scm.com/docs](https://git-scm.com/docs) — referencia completa de comandos
- [docs.github.com](https://docs.github.com/es/get-started) — documentación oficial de GitHub (Pull Requests, Issues, etc.)
- [GitHub Skills](https://skills.github.com/) — cursos interactivos oficiales de GitHub
- [learngitbranching.js.org](https://learngitbranching.js.org/) — practicar ramas y merges de forma visual e interactiva

## Cierre

El objetivo de este tema es que el flujo `git add` → `git commit` → `git push` sea automático, para no tener que pensar en la herramienta mientras se aprende el resto del contenido de la materia. Todo el trabajo práctico de acá en adelante se versiona con Git y se comparte por GitHub.
