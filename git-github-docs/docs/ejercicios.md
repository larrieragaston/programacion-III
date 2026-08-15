# Git & GitHub — Guía de ejercicios

Ejercicios progresivos, de lo más simple a lo más completo. Se recomienda resolverlos en orden — cada uno se apoya en el resultado del anterior.

## 1. Primer repositorio local

1. Crear una carpeta nueva llamada `git-practica`.
2. Inicializar un repositorio Git dentro de esa carpeta.
3. Crear un archivo `README.md` con un título y una línea de descripción.
4. Verificar con `git status` que Git detecta el archivo como no rastreado (*untracked*).
5. Agregar el archivo al staging area y confirmar el primer commit, con un mensaje descriptivo.
6. Confirmar con `git log --oneline` que el commit quedó registrado.

## 2. Historial y buenas prácticas de commit

1. Sobre el mismo repositorio, agregar un archivo `notas.txt` con al menos tres líneas de texto.
2. Confirmarlo en un commit aparte (no junto con el `README.md`).
3. Modificar una línea de `notas.txt` y confirmar el cambio en un tercer commit.
4. Revisar `git log --oneline`: debería haber tres commits. Escribir, para cada uno, qué mensaje de commit usaron y por qué es (o no es) un buen mensaje según los criterios del apunte.

## 3. Conventional Commits

1. Agregar un archivo `changelog.md` vacío al repositorio y confirmarlo con un mensaje que siga el formato de Conventional Commits (`docs: ...`).
2. Modificar `notas.txt` agregando una línea nueva y confirmar el cambio con tipo `feat`.
3. Introducir a propósito un error de tipeo en `notas.txt`, confirmarlo, y después corregirlo en un commit separado con tipo `fix`.
4. Revisar `git log --oneline`: cada mensaje debería poder leerse y clasificarse de un vistazo por su prefijo (`feat`, `fix`, `docs`).

## 4. `.gitignore`

1. Crear, dentro del mismo repositorio, una carpeta `node_modules/` con un archivo cualquiera adentro (puede estar vacío) y un archivo `secreto.env` en la raíz.
2. Correr `git status` y observar que Git los detecta como archivos nuevos.
3. Crear un archivo `.gitignore` que excluya `node_modules/` y `*.env`.
4. Verificar con `git status` que esos archivos ya no aparecen como pendientes.
5. Confirmar el `.gitignore` en un commit.

## 5. Ramas y merge sin conflicto

1. Crear una rama llamada `feature/saludo`.
2. Sobre esa rama, agregar una función a un archivo `saludo.js`:

   ```js
   function greet(name) {
     return `Hola, ${name}!`;
   }
   ```

3. Confirmar el cambio en un commit dentro de la rama `feature/saludo`.
4. Volver a la rama `main` y confirmar (con `cat saludo.js` o abriendo el archivo) que el archivo **no** existe ahí todavía.
5. Hacer merge de `feature/saludo` a `main`.
6. Verificar que ahora sí existe `saludo.js` en `main`.

## 6. Varias ramas en paralelo

El objetivo de este ejercicio es reproducir, en un repo propio, una situación real: varias ramas activas al mismo tiempo, cada una en un estado distinto (igual que el diagrama "Varias ramas a la vez" del apunte).

1. Desde `main`, crear una rama `feature/uno`, agregar un archivo `uno.txt` con una línea de texto, confirmarlo, volver a `main` y mezclarla — esta rama queda **fusionada**.
2. Crear una rama `feature/dos`, agregar dos commits con cambios en un archivo `dos.txt`, pero **no** mezclarla todavía — esta rama queda **en progreso**.
3. Crear una tercera rama `feature/tres` y hacer un único commit mínimo (por ejemplo, un archivo `tres.txt` vacío) — esta rama queda **recién creada**.
4. Correr `git log --oneline --graph --all` y comparar la salida con el diagrama del apunte: ¿se distingue a simple vista cuál rama está fusionada, cuál en progreso y cuál recién creada?
5. Correr `git branch` (sin mezclar `feature/dos` ni `feature/tres`) y confirmar que las tres ramas conviven en el mismo repositorio.

## 7. Provocar y resolver un conflicto

1. Desde `main`, crear una rama `feature/version-a`. Modificar la primera línea de `saludo.js` a:

   ```js
   function greet(name) {
     return `¡Hola, ${name}! Bienvenido/a.`;
   }
   ```

   Confirmar el cambio.

2. Volver a `main` y crear otra rama, `feature/version-b`, a partir de ahí. Modificar la misma línea de `saludo.js` a:

   ```js
   function greet(name) {
     return `Hey ${name}, ¿cómo estás?`;
   }
   ```

   Confirmar el cambio.

3. Mezclar `feature/version-a` a `main` (sin conflicto, porque `main` no cambió esa línea todavía).
4. Intentar mezclar `feature/version-b` a `main`. Git debería reportar un conflicto en `saludo.js`.
5. Abrir el archivo, identificar las marcas de conflicto (`<<<<<<<`, `=======`, `>>>>>>>`), decidir qué versión final dejar (puede ser una, la otra, o una combinación), y completar el merge con un commit.

## 8. Trabajar con un repositorio remoto en GitHub

1. Crear una cuenta en GitHub si todavía no se tiene una ([github.com/join](https://github.com/join)).
2. Crear un repositorio nuevo, vacío, en GitHub (sin README inicial).
3. Conectar el repositorio local de los ejercicios anteriores a ese remoto (`git remote add origin <url>`).
4. Subir la rama `main` al remoto.
5. Verificar en la interfaz web de GitHub que el historial de commits aparece completo.

## 9. Pull Request

1. Sobre el repositorio ya subido a GitHub, crear una rama nueva `feature/despedida` y agregar una función `farewell` a `saludo.js`.
2. Subir esa rama al remoto.
3. Desde la interfaz de GitHub, abrir un Pull Request de `feature/despedida` hacia `main`.
4. Escribir una descripción breve de qué hace el cambio, siguiendo el formato de Conventional Commits en el título (por ejemplo, `feat: agregar función de despedida`).
5. (Si están trabajando en pareja) Pedirle a un compañero o compañera que revise el PR y lo apruebe antes de mezclarlo. Si están solos, mezclarlo ustedes mismos y observar cómo queda reflejado en el historial de GitHub.

## Para pensar

- ¿Qué pasaría si dos personas hacen `git push` al mismo tiempo sobre la misma rama? Investigar qué error tira Git y cómo se resuelve (`git pull` antes de `git push`).
- ¿Por qué `node_modules/` no se versiona nunca, a pesar de ser necesario para correr el proyecto?
- Un formato de commit estandarizado como Conventional Commits lo termina leyendo, casi siempre, otra persona. ¿Qué se gana con eso además de prolijidad? (pensar en herramientas que generan un *changelog* automático a partir del historial).
