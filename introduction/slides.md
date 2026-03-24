---
theme: bricks
title: Programación III - Introducción
info: |
  Presentación introductoria de la materia Programación III.
  INSPT - UTN
author: Gastón Larriera
keywords: programación funcional, INSPT, UTN
transition: slide-left
mdc: true
---

# Programación III

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN
</div>

---
layout: center
---

# Profesor: Gastón A. Larriera

- Técnico Superior en Informática
- Profesor en Disciplinas Industriales
- Ingeniero en Informática
- Software Engineer ([MercadoLibre](https://www.mercadolibre.com.ar))

---
layout: default
---

# Presentación de alumnos

- Nombre
- ¿Profesorado?
- Conocimientos de programación
- Trabajo

---
layout: center
---

# Contenidos de la materia

---
layout: default
---

# Primera parte

1. **Cálculo Lambda**
2. **Clojure**

<div class="flex gap-6 items-center justify-center mt-8">
  <img src="/logos/lambda.svg" alt="Lambda" class="h-12" />
  <img src="/logos/clojure.svg" alt="Clojure" class="h-12" />
  <img src="/logos/lisp.svg" alt="Lisp" class="h-12" />
  <img src="/logos/haskell.svg" alt="Haskell" class="h-12" />
  <img src="/logos/scala.svg" alt="Scala" class="h-12" />
</div>

---
layout: default
---

# Segunda parte

<div class="grid grid-cols-2 gap-4">
<div>

1. **Programación Web FullStack**
   1. Mongo
   2. Express
   3. React
   4. Node
2. **API Rest**
3. **JSON**
4. **JavaScript**
5. **HTML**
6. **CSS**

</div>
<div class="flex flex-wrap gap-4 items-center justify-center content-center">
  <img src="/logos/mongodb.svg" alt="MongoDB" class="h-10" />
  <img src="/logos/express.svg" alt="Express" class="h-10" />
  <img src="/logos/react.svg" alt="React" class="h-10" />
  <img src="/logos/nodejs.svg" alt="Node.js" class="h-10" />
  <img src="/logos/javascript.svg" alt="JavaScript" class="h-10" />
  <img src="/logos/html5.svg" alt="HTML5" class="h-10" />
  <img src="/logos/css3.svg" alt="CSS3" class="h-10" />
</div>
</div>

---
layout: two-cols
---

# Condiciones de aprobación

::left::

<div class="pr-4">

### Regularidad

- 75% de asistencia
- 1er Parcial aprobado (6 o más)
- Actividades adicionales
- Proyecto web full stack JS (avance 40%)

**Final:** Proyecto web full stack JS - MERN (100%)

</div>

::right::

<div class="pl-4">

### Promoción

- 1er Parcial aprobado (8 o más)
- Proyecto web full stack JS (100%)

</div>

---
layout: center
---

# Vías de comunicación

<div class="grid grid-cols-2 gap-12 mt-8">
<div class="text-left">

### Mail institucional
gaston.larriera@inspt.utn.edu.ar

</div>
<div class="text-left">

### Aula virtual
[Programación III - 3.603](https://inspt.cvg.utn.edu.ar/course/view.php?id=2750)

</div>
</div>

---
layout: center
---

# Programación Funcional

---
layout: default
---

# Ejercicio

Dado un listado de colores, decir si el color `'red'` está en el listado.

**¿Cómo resolver el problema?**

---
layout: default
---

# Java - Forma Imperativa

```java {all|2|3|4-8|9}
List<String> colors = Arrays.asList("blue", "green", "red", "yellow");
boolean hasRed = false;
for (String color : colors) {
    if (color.equals("red")) {
        hasRed = true;
        break;
    }
}
System.out.println("Has color red? " + hasRed);
```

---
layout: default
---

# Java 8 - Forma Declarativa

```java
System.out.println("Has color red?: " + colors.contains("red"));
```

<br>

### ¿Cuál es el problema?

<v-click>

<!-- TODO: agregar problemas que resuelve la programación funcional -->

</v-click>
