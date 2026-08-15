# Git & GitHub

## Por qué versionar código

Antes de escribir la primera línea de código de un proyecto en equipo, necesitamos poder guardar el historial de nuestro trabajo, volver atrás cuando algo se rompe, y colaborar con otras personas sin pisarnos el código. Ese problema lo resuelve un **sistema de control de versiones (VCS)**: una herramienta que registra los cambios en un conjunto de archivos a lo largo del tiempo.

Un VCS no es exclusivo del código — se puede usar para versionar cualquier conjunto de archivos de texto (documentación, configuración, incluso texto plano) — pero es imprescindible para programar en equipo. Permite:

- Guardar el historial completo — quién cambió qué, y cuándo.
- Volver a cualquier versión anterior del proyecto.
- Comparar qué cambió entre dos versiones.
- Trabajar en equipo sobre los mismos archivos sin pisarse.

Sin uno, la alternativa habitual es algo así:

```
proyecto_final/
proyecto_final_v2/
proyecto_final_v2_ok/
proyecto_final_v2_ok_definitivo/
proyecto_final_v2_ok_definitivo_AHORA_SI/
```

Este esquema tiene varios problemas: no sabemos *qué* cambió entre una carpeta y la siguiente, no podemos combinar el trabajo de dos personas sobre el mismo archivo, y "volver atrás" significa buscar a mano la carpeta correcta. A medida que el proyecto crece y se suma gente, el costo de no tener un VCS crece con él.

## Antes de Git: generaciones de control de versiones

El control de versiones no arrancó con Git — pasó por varias generaciones, cada una resolviendo una limitación de la anterior:

- **Sin versionar**: copiar carpetas a mano (`_v2`, `_final`, `_ok`). No hay herramienta involucrada, solo disciplina personal — y falla apenas hay más de una persona escribiendo código.
- **Local**: el historial vive en la misma máquina — no sirve para trabajar en equipo (ej: RCS, 1982). Resuelve "puedo volver atrás", pero no "podemos trabajar juntos".
- **Centralizado**: un servidor central guarda el historial; hace falta estar conectado a él para casi cualquier operación (CVS, 1986 · Subversion/SVN, 2000). Ya permite equipos, pero todo pasa por un único servidor.
- **Distribuido**: cada copia tiene el historial completo, no solo el estado actual (Git, 2005 · Mercurial, 2005). Elimina la dependencia de un servidor único para trabajar.

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

En un sistema centralizado, si el servidor cae, nadie puede hacer commit, ni ver el historial, ni comparar versiones — solo pueden seguir editando archivos localmente, sin red de seguridad. En uno distribuido como Git, cada clon es un backup completo del proyecto: si el servidor remoto (por ejemplo, GitHub) desapareciera, cualquier copia local alcanza para reconstruir todo el historial.

## El origen de Git

- 2005 — el kernel de Linux pierde la licencia gratuita de **BitKeeper**, el sistema centralizado que usaba hasta entonces para coordinar a miles de colaboradores.
- **Linus Torvalds** (creador de Linux) escribe Git en un par de semanas para reemplazarlo, porque ninguna herramienta existente cumplía con lo que necesitaba el proyecto.
- Prioridades de diseño: velocidad, historial distribuido, integridad de los datos, y soportar el trabajo no lineal de miles de colaboradores simultáneos — la escala del propio kernel de Linux, que ningún otro proyecto de la época necesitaba manejar.

El nombre es jerga británica informal para "persona molesta" — el propio Torvalds bromeó con que, como ya había hecho con Linux, elegía nombrar sus proyectos en base a sí mismo.

Veinte años después, Git es el sistema de control de versiones más usado del mundo, tanto en proyectos open source como en empresas privadas — su diseño distribuido terminó siendo apropiado no solo para proyectos gigantes como el kernel, sino para equipos de cualquier tamaño.

## Qué es Git

**Git** es un sistema de control de versiones **distribuido**: guarda el historial completo de un proyecto como una serie de *fotos* (snapshots) del estado de los archivos en cada momento, no como una lista de diferencias línea por línea. Cada snapshot se llama **commit**. Corre 100% local — no depende de estar conectado a internet para casi ninguna operación cotidiana (`commit`, `log`, `diff`, crear ramas...).

### Características de Git

- **Integridad**: cada commit se identifica con un hash (una huella digital calculada a partir de su contenido) — si el contenido cambia, aunque sea en un carácter, el hash cambia. Esto hace prácticamente imposible que el historial se corrompa sin que Git lo detecte.
- **Ramas livianas**: crear, cambiar y combinar ramas es rápido y casi no ocupa espacio — a diferencia de otros sistemas donde crear una rama es una operación costosa, en Git es casi instantánea.
- **Staging area**: hay un paso intermedio (`git add`) entre editar un archivo y confirmarlo — se elige explícitamente qué cambios entran en el próximo commit, no es todo o nada.
- **No lineal**: soporta miles de ramas y colaboradores trabajando en paralelo sin necesidad de coordinarse en tiempo real.
- **Gratuito, de código abierto y estándar de facto** de la industria — la inmensa mayoría de los proyectos de software, sean privados u open source, usan Git.

## Qué es GitHub

**GitHub** es un servicio que **aloja** repositorios Git en la nube y agrega funcionalidades de colaboración por encima de Git. Git es la herramienta; GitHub es *un lugar* donde alojar un repositorio Git — el concepto de Git es exactamente el mismo se use o no se use GitHub.

### Funcionalidades de GitHub

Más allá de alojar el repositorio, GitHub agrega:

- **Pull Requests**: la forma de proponer y revisar cambios antes de integrarlos (se ve en detalle más abajo).
- **Issues**: seguimiento de tareas pendientes, bugs y pedidos de funcionalidades.
- **Actions**: automatización y CI/CD (integración continua) integrados al repositorio — por ejemplo, correr los tests automáticamente en cada Pull Request.
- **Projects**: tableros tipo kanban para organizar el trabajo del equipo.
- **Pages**: hosting gratuito para sitios estáticos, publicado directamente desde un repositorio (así se despliega, de hecho, el sitio que estás leyendo).

### GitHub y sus competidores

GitHub es el más usado, pero no el único servicio que aloja repositorios Git. El concepto de Git es el mismo en los tres — lo que cambia es la plataforma de colaboración alrededor:

<div class="card-grid card-grid-3">
<div class="info-card">
<h4>GitHub</h4>

Pull Requests · el más usado · de Microsoft · Actions gratis en repos públicos

<div class="card-note"><a href="https://github.com" target="_blank" rel="noopener">github.com</a></div>
</div>
<div class="info-card">
<h4>GitLab</h4>

Merge Requests · fuerte en CI/CD integrado · se puede auto-alojar · todo-en-uno (registry, monitoreo)

<div class="card-note"><a href="https://gitlab.com" target="_blank" rel="noopener">gitlab.com</a></div>
</div>
<div class="info-card">
<h4>Bitbucket</h4>

Pull Requests · integrado con Jira/Trello · de Atlassian · gratis para equipos de hasta 5 personas

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

### Recomendaciones

- Elegir un usuario profesional y corto — va a acompañar el perfil de por vida, conviene evitar apodos.
- Usar el mismo usuario que en LinkedIn o un portfolio personal, para que sea fácil de encontrar.
- Completar el perfil: foto, nombre y una bio corta.
- Activar la verificación en dos pasos (2FA) en la configuración de seguridad de la cuenta.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Instalá Git en tu máquina, confirmá la versión con `git --version`, configurá tu identidad (`user.name` y `user.email`), y creá tu cuenta de GitHub siguiendo los pasos de arriba.
</div>

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

El flujo típico es: modificamos archivos en el *working directory* → los agregamos al *staging area* con `git add` → confirmamos ese conjunto de cambios como un commit con `git commit`. La staging area existe porque no siempre queremos confirmar *todo* lo que modificamos de una — puede que estemos trabajando en dos cosas a la vez, y querramos armar un commit prolijo que agrupe solo una de ellas.

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

Crea una carpeta oculta `.git/` en el directorio actual — a partir de ahí, ese directorio es un repositorio Git. Todo lo que Git necesita para funcionar vive adentro de esa carpeta; borrarla equivale a borrar todo el historial (los archivos de trabajo quedan intactos, pero dejan de estar versionados).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Creá una carpeta llamada `mi-primer-repo`, inicializala como repositorio Git con `git init`, y confirmá con `git status` que Git la reconoce como un repositorio nuevo, sin commits todavía.
</div>

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

<div class="practice-box">
<p class="practice-label">Practicá</p>

Dentro de `mi-primer-repo`, creá un archivo `notas.txt` con cualquier contenido y corré `git status`. Identificá en qué sección aparece listado, y por qué Git lo clasifica ahí.
</div>

### Agregar cambios al staging area

```bash
git add src/validation.js    # un archivo puntual
git add .                    # todos los cambios del directorio actual
```

<div class="practice-box">
<p class="practice-label">Practicá</p>

Agregá `notas.txt` al staging area con `git add notas.txt` y volvé a correr `git status`. Comparalo con el resultado anterior: ¿en qué cambió la sección donde aparece listado?
</div>

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

<div class="practice-box">
<p class="practice-label">Practicá</p>

Confirmá el `notas.txt` del ejercicio anterior con un mensaje descriptivo, agregale una línea más de contenido, y hacé un segundo commit. Corré `git log --oneline` y verificá que aparecen los dos commits, del más reciente al más viejo.
</div>

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

Es importante notar que `.gitignore` solo afecta archivos que **todavía no fueron agregados** a Git — si un archivo ya tiene commits previos, agregarlo al `.gitignore` no lo elimina del historial ni deja de trackearlo automáticamente.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Creá un archivo `secreto.env` en `mi-primer-repo`, agregá una línea `.env` al `.gitignore`, y confirmá con `git status` que `secreto.env` deja de aparecer como archivo sin trackear.
</div>

## Ramas (branches)

Una **rama** es una línea de desarrollo independiente. Por defecto, un repositorio nuevo tiene una rama principal (`main`). Crear una rama nueva permite probar algo sin afectar el código que ya funciona en `main`.

```bash
git branch feature/login          # crea la rama
git switch feature/login          # se posiciona en esa rama
# (equivalente más viejo: git checkout feature/login)

git switch -c feature/login       # crea y se posiciona en un solo paso
```

Esto es lo que hace posible trabajar en equipo: cada persona (o cada feature) avanza en su propia rama, en paralelo, sin pisar el trabajo de las demás — y se integra todo a `main` recién cuando está listo.

<div class="practice-box">
<p class="practice-label">Practicá</p>

En `mi-primer-repo`, creá una rama `feature/saludo` con `git switch -c feature/saludo`, y confirmá con `git branch` que aparece marcada como la rama actual.
</div>

### Convenciones para nombrar ramas

Un nombre de rama debería anticipar qué tipo de cambio contiene, siguiendo el mismo criterio que **Conventional Commits** (ver más abajo):

| Prefijo | Se usa para |
|---|---|
| `feature/` | una funcionalidad nueva |
| `fix/` | corregir un bug |
| `docs/` | solo documentación |
| `refactor/` | cambio interno sin alterar comportamiento |
| `test/` | agregar o corregir tests |
| `chore/` | mantenimiento (dependencias, configuración) |

Además del prefijo, conviene seguir estas buenas prácticas:

- `kebab-case`, corto y descriptivo: `feature/carrito-compras`, no `feature/JuanCambios`.
- El nombre describe **qué** se hace, no quién lo hace — evitar iniciales o nombres de persona.
- Una rama = un cambio lógico — no mezclar varias features en la misma rama.
- Borrarla después de mergearla — ya cumplió su función, y mantener ramas viejas solo agrega ruido.

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

<div class="practice-box">
<p class="practice-label">Practicá</p>

Con la rama `feature/saludo` creada antes, hacé un commit en ella (por ejemplo, un archivo nuevo `saludo.txt`), volvé a `main` con `git switch main`, y fusioná la rama con `git merge feature/saludo`. Confirmá con `git log --oneline` que el commit ya forma parte de `main`.
</div>

## Trabajando con GitHub

Un repositorio en GitHub es un repositorio Git alojado remotamente. La conexión entre nuestro repositorio local y el remoto se llama, por convención, `origin`.

Si el repositorio ya existe en GitHub y todavía no tenemos una copia local, se clona directamente:

```bash
# trae una copia local de un repo remoto
git clone https://github.com/tu-usuario/tienda-online.git
```

Si en cambio ya tenemos un repositorio local (como `mi-primer-repo`) y queremos conectarlo a uno vacío recién creado en GitHub, hace falta indicarle cuál es su remoto antes de poder subir nada:

```bash
git remote add origin https://github.com/tu-usuario/mi-primer-repo.git
git push -u origin main   # -u deja main "enlazada" con origin/main
```

Una vez conectado el remoto, el trabajo del día a día es:

```bash
git push origin main   # sube nuestros commits locales al remoto
git pull origin main   # trae los commits nuevos del remoto
```

<div class="practice-box">
<p class="practice-label">Practicá</p>

Creá un repositorio vacío en GitHub (sin README), conectalo como `origin` de `mi-primer-repo`, y subí tu historial con `git push -u origin main`. Refrescá la página del repositorio en GitHub y confirmá que tus commits aparecen ahí.
</div>

### Pull Requests

Cuando se trabaja en equipo, la práctica habitual **no** es hacer `push` directo a `main`. En cambio:

1. Se crea una rama con el cambio propuesto.
2. Se sube esa rama al remoto (`git push origin nombre-de-la-rama`).
3. En GitHub, se abre un **Pull Request (PR)**: una propuesta de "traer estos cambios a `main`".
4. Otra persona revisa, comenta, aprueba (o pide cambios).
5. Recién ahí se mezcla.

Este flujo es el que se va a usar en los trabajos prácticos de la materia de acá en adelante.

<div class="practice-box">
<p class="practice-label">Practicá</p>

Creá una rama nueva en tu repo de GitHub, hacé algún cambio y subila con `git push origin nombre-de-la-rama`. Desde la web de GitHub, abrí un Pull Request de esa rama contra `main` (no hace falta mergearlo todavía — el objetivo es solo ver cómo se abre uno).
</div>

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

Un ejemplo concreto, de punta a punta:

```text
feature/agregar-favoritos → 4 commits → push → PR #23 → 2 comentarios → merge a main
```

Cuatro commits pequeños documentan el progreso de la feature; el Pull Request #23 agrupa esos commits en una propuesta de cambio revisable; dos comentarios de otra persona del equipo piden un ajuste antes de aprobarlo; y recién entonces se mezcla a `main`.

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

Más allá de estandarizar el mensaje, seguir esta convención tiene una ventaja práctica: herramientas automáticas pueden leer el historial de commits y generar un *changelog* (lista de cambios por versión) sin intervención manual, agrupando automáticamente todos los `feat` como funcionalidades nuevas y todos los `fix` como correcciones.

Especificación completa: [conventionalcommits.org](https://www.conventionalcommits.org/es/).

<div class="practice-box">
<p class="practice-label">Practicá</p>

Reescribí estos tres mensajes de commit usando Conventional Commits: "arreglos varios en el carrito", "nueva sección de contacto en la home", "actualizar el README con instrucciones de instalación".
</div>

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
| `git remote add origin <url>` | Conecta un repo local a uno remoto |
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
