---
theme: bricks
title: "Programación III - FP (Backus) \U0001F6AB Deprecated"
info: |
  Lenguaje FP de John Backus - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: FP, Backus, programación funcional, INSPT, UTN
transition: slide-left
mdc: true
---

# FP

John Backus

---
layout: center
---

# Ideador

---
layout: center
---

# John Warner Backus

<div class="mt-6 text-left max-w-lg mx-auto">

- Científico de la Computación
- IBM
- FORTRAN
- Programación funcional — FP
- Premio Turing (1977)

</div>

<div class="mt-4 text-sm italic opacity-80 max-w-lg mx-auto">

"Can programming be liberated from the von Neumann style?: a functional style and its algebra of programs"

</div>

---
layout: center
---

# Fundamentos

---
layout: default
---

# Sistema

- Programación funcional
- Definición de funciones
- Átomos
- Aplicaciones

---
layout: default
---

# Programa funcional

- Expresión
  - Algoritmo
  - Entradas

---
layout: center
---

# Elementos

---
layout: default
---

# Elementos del sistema FP

- **Conjunto O** de objetos
- **Operación** → Aplicación
- **Conjunto F** de funciones, objetos → objetos
- **Conjunto FF** de formas funcionales, [funciones + objetos] → funciones
- **Conjunto D** de definiciones de funciones

---
layout: center
---

# Objetos

---
layout: default
---

# Un objeto puede ser...

- Un **átomo** (letras, cadenas, números), menos las palabras reservadas
- Una **secuencia** de objetos `<x1, x2, ..., xn>`
- **Indefinido** (`⊥`)

---
layout: default
---

# Aclaraciones

- El átomo `∅` representa la secuencia vacía, y es el único objeto que es a la vez átomo y secuencia
- Los átomos `T` y `F` se utilizan para booleanos
- Si una secuencia contiene `⊥`, está indefinida. Por ejemplo: `<5, A, 7, 4, ⊥, 3> = ⊥`

---
layout: default
---

# Ejemplos

```
⊥
3.2
∅
PEPE
<PEPE, 3.2, ⊥>
<A, <<B>, C>, D>
<>              Obs: <> equivale a ∅
```

---
layout: center
---

# Aplicación

---
layout: default
---

# Definición

Si **f** es una función y **x** es un objeto, entonces `f : x` es una **aplicación** y representa el objeto que resulta cuando se le aplica **f** a **x**.

---
layout: default
---

# Ejemplos

```
-  : <10, 7>                  resulta 3
1  : <JUAN, CARLOS, SOFIA>    resulta JUAN
3  : <PRIMERO, SEGUNDO>       resulta ∅
tl : <1, 2, 3>                resulta <2, 3>
```

---
layout: center
---

# Funciones (F)

---
layout: default
---

# Funciones

Todas las funciones **f** del conjunto F convierten objetos en otros objetos, y preservan el valor indefinido (`f : ⊥ = ⊥`).

Las **funciones primitivas** son las funciones básicas provistas por el sistema FP.

---
layout: default
---

# Selectores

```
Selector desde la izquierda
  3  : <34, 1, 25>                        resulta 25
  4  : <A, B, C>                           resulta ⊥

Selector desde la derecha
  3r : <PRIMERO, SEGUNDO, TERCERO>         resulta PRIMERO
  4r : <1, 2, 3>                           resulta ⊥

Cola desde la izquierda
  tl : <A, B, C>                           resulta <B, C>

Cola desde la derecha
  tlr : <A, B, C>                          resulta <A, B>

Identidad
  id : <A, B, C>                           resulta <A, B, C>
```

---
layout: default
---

# Predicados

```
¿Es átomo?
  atom : 5                resulta T
  atom : <A, B, C>        resulta F

¿Es igual?
  eq : <A, A>             resulta T
  eq : <A, 7>             resulta F
  eq : <A, B, C>          resulta ⊥

¿Es nulo?
  null : ∅                resulta T
  null : <A, 7>           resulta F
```

---
layout: default
---

# Funciones aritméticas

```
Suma
  + : <2, 7>          resulta 9
  + : <3, A, 7>       resulta ⊥

Resta
  - : <9, 7>          resulta 2
  - : <7, 9>          resulta -2

Producto
  × : <2, 7>          resulta 14
  × : <0, 5>          resulta 0

Cociente
  ÷ : <10, 2>         resulta 5
  ÷ : <10, 0>         resulta ⊥
```

---
layout: default
---

# Funciones lógicas

```
AND lógico
  and : <T, F>         resulta F
  and : <1, 0>         resulta ⊥

OR lógico
  or : <T, F>          resulta T
  or : <F, F>          resulta F

NOT lógico
  not : F              resulta T
  not : T              resulta F
```

---
layout: default
---

# Funciones para manipular secuencias

```
Longitud
  length : <2, A, 7>                          resulta 3
  length : ∅                                   resulta 0

Invertir
  reverse : <2, A, 7>                         resulta <7, A, 2>
  reverse : ∅                                  resulta ∅

Transponer
  trans : <<1, 2, 3>, <A, B, C>>              resulta <<1, A>, <2, B>, <3, C>>

Distribuir desde la izquierda
  distl : <A, <1, 2, 3>>                      resulta <<A, 1>, <A, 2>, <A, 3>>
```

---
layout: default
---

# Funciones para manipular secuencias (cont.)

```
Distribuir desde la derecha
  distr : <<1, 2, 3>, A>                      resulta <<1, A>, <2, A>, <3, A>>

Concatenar a la izquierda
  apndl : <<A, B>, <C, D>>                    resulta <<A, B>, C, D>

Concatenar a la derecha
  apndr : <<A, B>, <C, D>>                    resulta <A, B, <C, D>>

Rotar hacia la izquierda
  rotl : <A, B, C, D>                         resulta <B, C, D, A>

Rotar hacia la derecha
  rotr : <A, B, C, D>                         resulta <D, A, B, C>
```

---
layout: center
---

# Formas funcionales (FF)

---
layout: default
---

# Composición

$$f \circ g : x \equiv f : (g : x)$$

**Ejemplo:**

```
1 o tl : <A, B, C>    resulta B
```

---
layout: default
---

# Construcción

$$[f_1, \ldots, f_n] : x \equiv \langle f_1 : x,\ f_2 : x,\ \ldots,\ f_n : x \rangle$$

**Ejemplo:**

```
[tl, tlr] : <A, B, C>    resulta <<B, C>, <A, B>>
```

---
layout: default
---

# Condición

$$(p \to f;\ g) : x \equiv (p : x) = T \to f : x\ ;\ (p : x) = F \to g : x\ ;\ \bot$$

**Ejemplo:**

```
(not o atom → 1; id) : <A, B, C>    resulta A
```

---
layout: default
---

# Constante

$$\overline{X} : y \equiv y = \bot \to \bot\ ;\ X$$

**Ejemplo:**

```
+ o [id, 1̄] : 3    resulta 4
```

---
layout: default
---

# Inserción

$$/f : x \equiv x = \langle x_1 \rangle \to x_1\ ;\ x = \langle x_1, \ldots, x_n \rangle \to f : \langle x_1,\ /f : \langle x_2, \ldots, x_n \rangle \rangle\ ;\ \bot$$

**Ejemplo:**

```
/+ : <1, 2, 3>
  ≡ + : <1, /+ : <2, 3>>
  ≡ + : <1, + : <2, 3>>
  resulta 6
```

---
layout: default
---

# Aplicación a todos

$$\alpha f : x \equiv x = \emptyset \to \emptyset\ ;\ x = \langle x_1, \ldots, x_n \rangle \to \langle f : x_1, \ldots, f : x_n \rangle\ ;\ \bot$$

**Ejemplo:**

```
α 1 : <<A, B, C>, <4, 5, 6>>    resulta <A, 4>
```

---
layout: default
---

# Binario a unario

$$(bu\ f\ x) : y \equiv f : \langle x, y \rangle$$

**Ejemplo:**

```
(bu + 1) : 2  ≡  + : <1, 2>    resulta 3
```

---
layout: default
---

# While

$$(while\ p\ f) : x \equiv p : x = F \to x\ ;\ p : x = T \to (while\ p\ f) : (f : x)\ ;\ \bot$$

**Ejemplo:**

```
(while (not o null o tl) tl) : <A, B, C, D, E, F, G, H>
  resulta <H>
```

---
layout: center
---

# Definición de funciones (D)

---
layout: default
---

# Función iota

```
Def iota ≡ funrec o [id, <>]
Def funrec ≡ < o [1, 1] → 2; funrec o [- o [1, 1], apndl]
```

**Ejemplo:**

```
iota : 5    resulta <1, 2, 3, 4, 5>
```

---
layout: default
---

# Función factorial

```
Def !    ≡ eq0 → 1̄; × o [id, ! o sub1]
Def eq0  ≡ eq o [id, 0̄]
Def sub1 ≡ - o [id, 1̄]
```

Definición más funcional:

```
Def fact ≡ eq0 → 1̄; (/×) o iota
```

**Ejemplo:**

```
! : 4       resulta 24
fact : 4    resulta 24
```

---
layout: default
---

# Función producto interno

```
Def IP ≡ (/+) o (α×) o trans
```

**Ejemplo:**

```
IP : <<1, 2, 3>, <4, 5, 6>>    resulta 32
```

---
layout: default
---

# Función producto matricial

```
Def MM ≡ (α α IP) o (α distl) o distr o [1, trans o 2]
```

**Ejemplo:**

```
MM : <<<1, 2, 3>, <4, 5, 6>, <7, 8, 9>>,
      <<1, 1, 1>, <0, 0, 0>, <0, 1, 0>>>

resulta <<1, 4, 1>, <4, 10, 4>, <7, 16, 7>>
```

---
layout: center
---

# ¡Muchas Gracias!
