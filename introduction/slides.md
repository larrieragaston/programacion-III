---
theme: bricks
title: Programación III - Introducción
download: true
info: |
  Presentación introductoria de la materia Programación III.
  INSPT - UTN
author: Gastón Larriera
keywords: programación funcional, INSPT, UTN
transition: slide-left
mdc: true
---

# Programación III

Programación Funcional & Desarrollo Web Full-Stack

<div class="abs-b mb-8 text-sm opacity-60">
INSPT - UTN · Ciclo Lectivo 2026
</div>

---
layout: center
---

# Prof. Ing. Gastón A. Larriera

<div class="mt-4">

**Formación**

- Ingeniero en Informática
- Técnico Superior en Informática
- Profesor en Disciplinas Industriales

</div>

<div class="mt-4">

**Experiencia**

- Software Engineer en [MercadoLibre](https://www.mercadolibre.com.ar)

</div>

<div class="flex gap-6 items-center justify-center mt-8">
  <a href="https://github.com/larrieragaston" target="_blank" class="flex items-center gap-2 opacity-70 hover:opacity-100">
    <img src="/logos/github.svg" alt="GitHub" class="h-6" /> GitHub
  </a>
  <a href="https://www.linkedin.com/in/gaston-ariel-larriera/" target="_blank" class="flex items-center gap-2 opacity-70 hover:opacity-100">
    <img src="/logos/linkedin.svg" alt="LinkedIn" class="h-6" /> LinkedIn
  </a>
</div>

---
layout: center
---

# Presentación de alumnos

<div class="mt-6 text-left max-w-md mx-auto">

- ¿Cómo te llamás?
- ¿Estás haciendo el profesorado?
- ¿Qué conocimientos de programación tenés?
- ¿Trabajás en algo relacionado?

</div>

---
layout: center
---

# Contenidos de la materia

Lo que vamos a ver este año

---
layout: default
---

# 1er Cuatrimestre

<div class="grid grid-cols-2 gap-4">
<div>

1. **Unidad 1** — Cálculo Lambda
2. **Unidad 2** — Programación Funcional
   - Funciones puras y de orden superior
   - Inmutabilidad y transparencia referencial
   - Recursividad
3. **Unidad 3** — Clojure

</div>
<div class="relative h-64">
  <img src="/logos/lambda.svg" alt="Lambda" class="absolute h-16" style="top: 5%; left: 8%;" />
  <img src="/logos/clojure.svg" alt="Clojure" class="absolute h-14" style="top: 10%; left: 55%;" />
  <img src="/logos/lisp.svg" alt="Lisp" class="absolute h-14" style="top: 50%; left: 60%;" />
  <img src="/logos/haskell.svg" alt="Haskell" class="absolute h-12" style="top: 55%; left: 15%;" />
  <img src="/logos/scala.svg" alt="Scala" class="absolute h-14" style="top: 30%; left: 35%;" />
</div>
</div>

---
layout: default
---

# 2do Cuatrimestre

<div class="grid grid-cols-2 gap-4">
<div>

4. **Unidad 4** — Desarrollo Web Full-Stack
   - MongoDB
   - Express
   - React
   - Node.js
   - API Rest · JSON
   - HTML · CSS · JavaScript

</div>
<div class="relative h-64">
  <img src="/logos/mongodb.svg" alt="MongoDB" class="absolute h-16" style="top: 2%; left: 10%;" />
  <img src="/logos/express.svg" alt="Express" class="absolute h-14" style="top: 8%; left: 60%;" />
  <img src="/logos/react.svg" alt="React" class="absolute h-16" style="top: 32%; left: 35%;" />
  <img src="/logos/nodejs.svg" alt="Node.js" class="absolute h-16" style="top: 28%; left: 75%;" />
  <img src="/logos/javascript.svg" alt="JavaScript" class="absolute h-14" style="top: 58%; left: 15%;" />
  <img src="/logos/html5.svg" alt="HTML5" class="absolute h-16" style="top: 62%; left: 55%;" />
  <img src="/logos/css3.svg" alt="CSS3" class="absolute h-14" style="top: 82%; left: 35%;" />
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

Un vistazo a por qué importa

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

<v-click>

**¿Qué problemas sugiere este enfoque?**

</v-click>

---
layout: default
---

# Java 8 - Forma Declarativa

```java
System.out.println("Has color red?: " + colors.contains("red"));
```
