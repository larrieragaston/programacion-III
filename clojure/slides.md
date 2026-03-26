---
theme: bricks
title: Programación III - Clojure (In progress)
info: |
  Clojure - Programación III
  INSPT - UTN
author: Gastón Larriera
keywords: clojure, programación funcional, INSPT, UTN
transition: slide-left
mdc: true
---

# Clojure

<img src="/logos/clojure.svg" alt="Clojure" class="h-24 mx-auto mt-8" />

---
layout: center
---

# Surgimiento

---
layout: center
---

# Rich Hickey

<div class="mt-6 text-left max-w-md mx-auto">

- CTO Cognitect
- 2007
- Autor de Clojure

</div>

---
layout: center
---

# Fundamentos

---
layout: default
---

# Lenguaje

- Programación funcional (no puro)
- Multi-Thread
- Compilado
- Lisp
- Java

---
layout: default
---

# Características

- **Homoicónico**
- Datos persistentes — Inmutables
- Recursividad — Funciones de orden superior
- Lazy evaluation
- Entornos Java — JVM
- REPL: read-eval-print-loop

---
layout: default
---

# Ejemplos — REPL

<div class="text-sm">

```clojure
user=> (doc list)              ; Muestra la documentación de list
user=> (find-doc "trim")       ; Muestra las documentaciones que incluyan trim
user=> (apropos "?")           ; Muestra los nombres que incluyan ?
user=> (dir clojure.string)    ; Muestra los nombres definidos en clojure.string
user=> (source +)              ; Muestra la definición (código fuente) de +
user=> (load-file "op.clj")   ; Evalúa secuencialmente el contenido de op.clj
user=> (clojure-version)       ; Muestra la versión de Clojure
```

</div>

---
layout: center
---

# Elementos

---
layout: default
---

# Elementos

- Datos
- Evaluación de expresiones
- Formas especiales
- Funciones predefinidas
- Funciones de orden superior
- Macros predefinidas

---
layout: center
---

# Datos

---
layout: default
---

# Un dato puede ser...

- Un **escalar** (letras, cadenas, números), menos las palabras reservadas
- Una **colección** de datos
- Una **secuencia** (abstracción de una colección)

---
layout: default
---

# Escalares — Símbolos

- Nombre de: función, parámetro, variable, etc.
- Case sensitive
- Siempre comienzan con carácter
- `'` para evitar que se evalúe

```clojure
user=> a
CompilerException java.lang.RuntimeException:
  Unable to resolve symbol: a in this context

user=> 'a
a
```

---
layout: default
---

# Escalares — Valores literales

<div class="grid grid-cols-2 gap-8">
<div>

**Números:**
- Entero (long) → `42`
- Punto flotante (double) → `42.5`
- Racionales (fracción) → `1/3`

**Caracteres:**
- Valor → `\@`
- En octal → `\o100`
- En hexadecimal → `\u0040`
- Denominación → `\newline`

</div>
<div>

**Cadenas de caracteres:**
- Entre comillas → `"Hola \"mundo\"."`

**Booleanos:**
- `true` / `false`

**Nulo:**
- `nil` → `null` en Java

**Constantes simbólicas:**
- `##Inf` · `##-Inf` · `##NaN`

**Palabras clave:**
- En mapas `:` como key

</div>
</div>

---
layout: default
---

# Colecciones

<div class="text-sm">

| Tipo | Sintaxis | Ejemplo |
|---|---|---|
| **Listas** — código en Clojure | `()` | `(+ P 1)` |
| **Vectores** — datos (LIFO) | `[]` | `[0 1 1 2 3]` |
| **Colas** — datos (FIFO) | `PersistentQueue/EMPTY` | — |
| **Conjuntos** — datos no repetidos | `#{}` | `#{2 3 5 7}` |
| **Mapas** — entidades key-value | `{}` | `{:x 10, :y 15}` |

</div>

---
layout: default
---

# Colecciones — Comparación

<div class="text-xs">

| | Listas | Vectores | Colas | Conjuntos | Mapas |
|---|---|---|---|---|---|
| **Acceso** | Secuencial | Aleatorio | Secuencial | Secuencial | Aleatorio |
| **Repetidos** | Sí | Sí | Sí | No | No |
| **Contiene** | Operaciones | Datos | Datos | Datos | Entidades |
| **Orden** | Inserción | Inserción | Inserción | hash-set / sorted-set | Clave-valor |
| **Tipo** | LIFO | LIFO | FIFO | Por dato | Por clave |

</div>

---
layout: default
---

# Secuencias

- Interfaz **ISeq**
- Abstracción que representa una vista secuencial de una colección
- **Lazy evaluation**

---
layout: center
---

# Evaluación de expresiones

---
layout: default
---

# Sentencias vs Expresiones

Todo es una **expresión** a evaluar:

- **Dato** → dato
- **Expresión** → expresión o dato

Excepciones:

- **Símbolos** (valor al que se refieren)
- **Listas** (invocaciones)

---
layout: default
---

# Ejemplo

```clojure
user=> 1
1

user=> [1 2 3]
[1 2 3]

user=> (+ 3 4)
7

user=> (1 2 3)
ClassCastException java.lang.Long cannot be cast to clojure.lang.IFn

user=> '(1 2 3)
(1 2 3)
```

---
layout: default
---

# Adicionalmente

En una lista, el **primer elemento** es lo que va a ser evaluado y lo que lo prosigue, son sus **argumentos**.

```clojure
;; Macro en la primera posición
user=> (defn suma [a b] (+ a b))
#'user/suma

;; Función en la primera posición
user=> (suma 5 6)
11

;; Palabra clave en la primera posición
user=> (:v1 '{:v2 b, :v1 a, :v3 c})
a

;; Vector en la primera posición
user=> ([0 10 20 30 40] 3)
30
```

---
layout: default
---

# Adicionalmente

El orden de los argumentos depende del tipo de elemento y el tipo de operación.

```clojure
;; Operación sobre una colección
user=> (conj [1 2 3] 4)
[1 2 3 4]

;; Operación sobre una secuencia
user=> (cons 1 [2 3 4])
(1 2 3 4)

;; Otras no toman argumentos
user=> (do (print "Nombre: ")
           (flush)
           (let [n (read)] (print (str "Hola ")) n))
```

---
layout: center
---

# Formas especiales

---
layout: default
---

# if · quote

```clojure
;; IF => condicional => (if a b c) o (if a b)
user=> (if (= 3 4) ([10 20 30] 2) ([40 50 60] 1))
50

user=> (if (= 3 4) ([10 20 30] 2))
nil
```

```clojure
;; QUOTE => no evalúa => (quote expresion) o 'expresion
user=> (quote (+ 3 2))
(+ 3 2)

user=> '(+ 3 2)
(+ 3 2)
```

---
layout: default
---

# fn

<div class="text-sm">

Sin sobrecarga por aridad:

```clojure
(fn name? [params*] condition-map? expr*)
```

Con sobrecarga por aridad:

```clojure
(fn name? ([params*] condition-map? expr*)+)
```

- `name?` — nombre, permite llamadas recursivas
- `params*` — parámetros de la función
- `condition-map?` — pre- y postcondiciones
- `expr*` — son evaluadas, pero solo devuelve el valor de la última

</div>

---
layout: default
---

# fn — Ejemplos

<div class="text-sm">

```clojure
user=> ((fn [a b] (+ a b)) 3 5)
8

user=> ((fn fact [n] (if (zero? n) 1 (* n (fact (- n 1))))) 5)
120

user=> ((fn ([] 0)
            ([x] x)
            ([x y] (+ x y))
            ([x y & more] (+ x y (reduce + more)))) 2 3 5 2)
12

;; Funciones anónimas abreviadas
user=> (#(* % %) 3)
9

user=> (#(+ (* %1 %1) (* %2 %2)) 3 4)
25
```

</div>

---
layout: default
---

# def

<div class="text-sm">

Crea y devuelve una **Var** (referencia) y registra en el namespace.

```clojure
user=> x
CompilerException java.lang.RuntimeException:
  Unable to resolve symbol x in this context

user=> (def x)
#'user/x

user=> x
#object[clojure.lang.Var$Unbound 0xb07f29 "Unbound: #'user/x"]

user=> (def x 1)
#'user/x

user=> x
1

user=> (class x)
java.lang.Long
```

</div>

---
layout: default
---

# var · do

```clojure
;; VAR => definición
user=> (var x)
#'user/x

user=> (class (var x))
clojure.lang.Var
```

```clojure
;; DO => evalúa grupo de expresiones, devuelve la última
user=> (do)
nil

user=> (if (= 2 (+ 1 1)) (do 1 2 3) 4)
3

user=> (if (= 2 (+ 1 1)) (do (println 1) (println 2) 3) 4)
1
2
3
```

---
layout: default
---

# let · try-catch-finally

<div class="text-sm">

```clojure
;; LET => evalúa expresiones con constantes locales
;; (let [binding*] expr*)
user=> (let [a [1 2 3], b 4]
         (println (list a b b a))
         (list b a a b))
([1 2 3] 4 4 [1 2 3])
(4 [1 2 3] [1 2 3] 4)
```

```clojure
;; TRY-CATCH-FINALLY => ídem que en Java
;; (try expreT* (catch classname name expreC*)* (finally expreF*)?)
user=> (try (/ 1 0)
         (catch Exception e
           (println "Exception:" (.getMessage e)))
         (finally (println "Good bye.")))
Exception: Divide by zero
Good bye.
nil
```

</div>

---
layout: default
---

# . (punto) — Interop con Java

<div class="text-sm">

Permite acceder a las funciones de Java. 1er argumento: nombre de clase. 2do argumento: símbolo (atributo) o lista (método).

```clojure
;; Acceso a atributo
user=> (. Math PI)
3.141592653589793

;; Llamada a método
user=> (. (. System (getProperties)) (get "java.runtime.version"))
"1.8.0_60-b27"

;; Lo más común es usar macros
user=> (.toUpperCase "Hola")
"HOLA"

user=> (.indexOf '(a b c d) 'c)
2
```

</div>

---
layout: center
---

# Funciones predefinidas

<div class="mt-4 opacity-60">

*Ver documentación oficial: [clojure.org/api](https://clojure.org/api/api)*

</div>

---
layout: center
---

# ¡Muchas Gracias!
