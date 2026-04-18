---
title: Apunte teórico — Cálculo λ
description: Teoría de cálculo lambda (sintaxis, semántica, combinadores) y mapa de temas afines — Programación III, origen del paradigma funcional.
---

# Apunte teórico — Cálculo λ

Este apunte acompaña **Programación III** en la carrera de **Informática** (INSPT — UTN). El objetivo no es convertir al lector en lógico matemático, sino mostrar el **origen histórico y formal** del paradigma de **programación funcional**: qué es una función cuando se la piensa como regla de cálculo sobre expresiones, cómo se **ejecuta** un programa sin máquina de Von Neumann explícita, y por qué lenguajes como Lisp, Scheme, Haskell o Clojure heredan ideas del **$\lambda$-cálculo** (hoy con tipos, módulos, entrada/salida, etc., que aquí se dejan de lado).

## De Programación I y II a III: otro paradigma, otra cabeza

**Sí: es un cambio de *mindset*.** En **Programación I** (estructurada) uno suele pensar en *pasos*: leer, inicializar, repetir, contar, acumular en una variable, imprimir. El programa es una **secuencia de órdenes** a la máquina. En **Programación II** (orientada a objetos) el centro pasa a ser *quién tiene la responsabilidad*: objetos con **estado interno**, mensajes, polimorfismo; el flujo sigue siendo muy “imperativo” por detrás, solo que organizado en clases.

En **programación funcional** el centro es otro: **qué valor se obtiene** a partir de datos y funciones, sin que el foco principal sea *cómo mutar la memoria paso a paso*. No es que “no haya estado” en el mundo real (bases de datos, red, UI), sino que en el **núcleo del modelo mental** las piezas son **expresiones** y **funciones** que se **componen**, no tanto procedimientos que “hacen cosas” a variables globales.

**Analogía cotidiana.** El estilo imperativo se parece a una **receta con hornallas prendidas todo el tiempo** (subir el fuego, bajar, mezclar, volver a subir). El estilo funcional se parece más a **armar una cuenta de matemáticas o un presupuesto**: se va **simplificando** $((7+4)\times\cdots)$ hasta un resultado; si cambia un dato, se **rearma** el cálculo. Esa simplificación paso a paso es lo que aquí se llama **reducción**.

### Qué concepto del apunte se parece a qué cosa “de verdad” (FP moderna)

| En este apunte (λ puro) | En lenguajes funcionales (lo que suele encontrarse en la práctica) |
|-------------------------|--------------------------------------------------------------|
| $\lambda x.\,M$ — abstracción | Funciones anónimas, **lambdas**, `fn`, `lambda`; **bloques** que devuelven expresión. |
| $M\,N$ — aplicación | Llamar a una función; en estilo punto: `map(xs, f)` vs `map f xs`. |
| Currying — $\lambda x\,\lambda y.\,M$ | Funciones que “devuelven” funciones; APIs tipo `add(3)` que devuelve otra función; **partial application**. |
| Variables libres / ligadas | **Clausuras**: la función “recuerda” el entorno donde nació (variables del scope). |
| $\beta$-reducción | Sustituir argumento en el cuerpo: el modelo mental de **evaluar** una llamada. |
| Combinadores ($S$, $K$, …) | Patrones sin variables sueltas: se parece a **point-free style**, pipes, `compose`. |
| Church booleans / `If` | Condicionales como **expresiones** (con valor), no solo como ramas que “ejecutan” efectos. |
| Numerales de Church ($n\,f\,x$ = aplicar $n$ veces) | `fold`, `reduce`, `iterate`: **repetir una operación** una cantidad de veces. |
| Estrategias (CBN / CBV) | **Lazy** vs **strict**; si un argumento caro no se usa, ¿conviene calcularlo igual? |
| $Y$ — punto fijo | `rec`, **recursión** sin nombre global; trampolines en algunos runtimes. |

Ninguna fila es una identidad perfecta (los lenguajes tienen tipos, efectos, optimizaciones), pero sirve para orientarse: cada símbolo abstracto del apunte tiene un **paralelo** en el código que uno suele conocer o encontrará al programar.

### Sobre la curva de aprendizaje

- **No hace falta** imaginar memoria y PC para seguir el λ puro; hace falta **paciencia** con el símbolo. Es como aprender **otra gramática**: al principio incomoda, luego ordena el pensamiento.
- Lo que uno trae de orientación a objetos **no se descarta**: composición, nombres claros, tests y “responsabilidades” siguen valiendo; lo que cambia es **dónde se pone el centro** del diseño (funciones y datos inmutables frente a objetos que mutan).

## Introducción

En la década de 1930, varios matemáticos abordaron la pregunta: _¿cuándo una función $f:\mathbb{N}\to\mathbb{N}$ es computable?_ Una definición informal es que debe existir un método que permita calcular $f(n)$ para cualquier $n$ dado, usando lápiz y papel.

**Ejemplo (función sucesor).**

$$
\mathrm{succ}(x) = x + 1
$$

Donde $\mathrm{succ}(4) = 4 + 1 = 5$. En **notación de flecha** se omite el nombre de la función: $x \mapsto x+1$.

El inglés Alan Turing, el austríaco Kurt Gödel y el estadounidense Alonzo Church definieron la computabilidad mediante tres modelos equivalentes: cada uno define la misma clase de funciones computables (**tesis de Church-Turing**).

1. **Turing** (tesis doctoral dirigida por Church) definió una computadora idealizada, la **máquina de Turing**, y postuló que una función es computable si y solo si puede ser calculada por dicha máquina. Las computadoras actuales (modelo de Von Neumann) son, conceptualmente, máquinas de Turing con memoria de acceso aleatorio. Los lenguajes imperativos (C, Pascal, Fortran, ensamblador) se basan en instruir a una máquina de Turing mediante secuencias de sentencias.

2. **Gödel** definió las **funciones recursivas generales** como el menor conjunto de funciones parciales que contiene constantes y sucesor, y es cerrado bajo proyección, composición y recursión. Postuló que computable equivale a recursiva general.

3. **Church** definió el **cálculo lambda** y postuló que computable equivale a expresable como término $\lambda$. Es un lenguaje **mínimo** y, a la vez, **Turing-completo**: con variables, abstracción y aplicación basta para expresar lo mismo que con una máquina de Turing (salvo detalles de codificación). Lisp, Scheme, Haskell, Clojure y Scala **no son** el $\lambda$-cálculo puro, pero su noción central de **función como valor**, el **currying** y la **evaluación por reducción** vienen de ahí. Las **máquinas abstractas** y los intérpretes de estos lenguajes pueden verse como estrategias de reducción (más reglas prácticas) sobre términos.

## 1. Programas como expresiones
Un programa funcional consiste en una expresión E que representa tanto el algoritmo como los datos
de entrada. Para su ejecución, se le aplican a E ciertas reglas de conversión.

> **Lectura “humana”.** En imperativo el enfoque es “dar tantos pasos hasta obtener la respuesta”. En este modelo se dice: “esta **expresión grande** es la misma que esta **más chica**”, hasta llegar a algo que ya no se puede simplificar. Es el mismo espíritu que $(a+b)(a-b)=a^2-b^2$: **reglas que preservan el significado** y reducen el trabajo.

La reducción consiste en reemplazar una parte P de E por otra expresión P’ de acuerdo con las reglas
de conversión dadas. En notación esquemática:

E[P] → E[P’], siempre y cuando P → P’ esté de acuerdo con las reglas.

Este proceso de reducción se repetirá hasta que la expresión resultante no tenga más partes que
puedan convertirse (en este curso, sobre todo **$\beta$-redex**). Esa **forma normal** (cuando existe) se puede interpretar como la **salida** del programa funcional. Más adelante veremos que a veces interesa una noción más débil, la **forma normal de cabecera**, y que **no todo término** llega a una forma normal: eso modela también **bucles** o **recursión sin base** en lenguajes reales.

Por ejemplo:
(7 + 4) × (8 + 5 × 3)
→ 11 × (8 + 5 × 3)
→ 11 × (8 + 15)
→ 11 × 23
→ 253

En este caso, las reglas de reducción consisten en las tablas de sumar y multiplicar valores numéricos.

Mediante reglas de reducción también pueden convertirse datos simbólicos (no numéricos).

Por ejemplo:

primero (ordenar (unir ([“perro”, “conejo”], ordenar ([“ratón”, “gato”]))))
→ primero (ordenar (unir ([“perro”, “conejo”], [“gato”, “ratón”])))
→ primero (ordenar ([“perro”, “conejo”, “gato”, “ratón”]))
→ primero ([“conejo”, “gato”, “perro”, “ratón”])
→ “conejo”

Las funciones como primero, ordenar y unir se pueden programar fácilmente combinando
algunas reglas de conversión, por lo que se las denomina combinadores.

En el $\lambda$-cálculo (con $\beta$), la **propiedad de Church–Rosser** (confluencia) implica que si un término puede reducirse a dos resultados distintos, ambos pueden seguir reduciéndose hasta un término común. En particular, **si existe una forma normal**, es **única** (no depende del orden en que se elijan las redex). Eso **no** garantiza que toda secuencia de reducción termine: hay términos sin forma normal. El primer ejemplo aritmético, en cambio, sí termina y puede reducirse, por ejemplo, así:

**Transparencia referencial y efectos.** Esa “misma respuesta sin importar *cómo* simplifiqué” es la idea de la **transparencia referencial**: reemplazar una subexpresión por otra **equivalente** sin cambiar el resultado final. En **JavaScript** y **Clojure** suele priorizarse escribir funciones **puras** (sin efectos ocultos) para poder razonar así; el $\lambda$-cálculo puro es el caso donde eso vale *siempre*. En el navegador o la JVM hace falta delimitar dónde hay efectos (I/O, mutación, reloj).

Cambiando el orden de reducción:

(7 + 4) × (8 + 5 × 3)
→ (7 + 4) × (8 + 15)
→ 11 × (8 + 15)
→ 11 × 23
→ 253

Reduciendo varias expresiones al mismo tiempo:

(7 + 4) × (8 + 5 × 3)
→ 11 × (8 + 15)
→ 11 × 23
→ 253

## 2. Sintaxis del cálculo lambda

La sintaxis de una expresión lambda (término $\lambda$) en **BNF** es:

```text
<expresión λ> ::= <variable>
                | (λ <variable> . <expresión λ>)
                | (<expresión λ> <expresión λ>)
```

Es decir, un término puede ser: **(1)** una variable; **(2)** una abstracción (parámetro formal y cuerpo); **(3)** una aplicación (operador y operando).

En la jerga de programación funcional, **$\lambda x.\,M$** es una **función anónima** con argumento formal $x$ y cuerpo $M$; **$M\,N$** es **aplicar** la función $M$ al argumento $N$ (como escribir `(M N)` en un lenguaje con prefijo). No hay números ni booleanos en la gramática: más adelante los **codificaremos** con puro $\lambda$.

**Ejemplos:**

- $x$
- $(\lambda x.\,x)$
- $((\lambda x.\,x)\,y)$
- $(\lambda x.\,(x\,y))\,((\lambda y.\,(y\,y))\,z)$
- $((\lambda x.\,(x\,y))\,(\lambda y.\,(y\,y)))\,z$

En [Biwascheme](https://www.biwascheme.org) es posible evaluar en línea la siguiente aplicación escrita en Lisp / Scheme. Como se puede ver, la sintaxis de estos lenguajes (en especial el uso de los paréntesis)
es bastante similar a la sintaxis del cálculo lambda:

((lambda (x) (+ x 1)) 4)

**Ejemplos en Clojure y JavaScript.** La misma idea con otra sintaxis: en Clojure, `((fn [x] (+ x 1)) 4)` o `#(+ % 1)` aplicado a `4`; en JavaScript, `((x) => x + 1)(4)`. En ambos lenguajes la **función es un valor** que se puede pasar a otra función (orden superior), guardar o devolver: es lo que se llama **first-class functions**, heredado del modelo $\lambda$.

### 2.1 Convenciones
Para evitar tener que usar un número excesivo de paréntesis, se establecen ciertas convenciones al
escribir expresiones lambda.

Por ejemplo, para reducir el número de paréntesis de la expresión (((λx.(λy.(y x))) a) b):

1) Se omiten los paréntesis externos:

((λx.(λy.(y x))) a) b

2) Se asume que las aplicaciones se asocian a la izquierda:

(λx.(λy.(y x))) a b

3) Se asume que el cuerpo de las abstracciones se extiende hasta que se cierra un paréntesis o
se alcanza el final de la expresión:

(λx.λy.y x) a b

4) Opcionalmente (porque esto no disminuye el número de paréntesis), se pueden contraer
múltiples abstracciones lambda:

(λx y.y x) a b

Se obtiene de esta forma una expresión lambda que es equivalente a la original.

**Currying.** La convención $\lambda x\,y.\,M$ es azúcar para $\lambda x.\,\lambda y.\,M$: una función de **dos** argumentos es en realidad una función de un argumento que devuelve otra función. Así se hace en Haskell y en la API de colecciones de muchos lenguajes.

> **Analogía.** Un curried `f` es como un **dispenser** por etapas: primero se elige el sabor ($x$), y la máquina entrega **otro** dispenser que espera el tamaño ($y$). No es “más misterioso” que un método que devuelve un objeto con otro método; solo que aquí el objeto *es* otra función.

## 3. Variables libres y ligadas
Sean x, y, z variables y M, N, P expresiones lambda cualesquiera:

La variable x ocurre libre en la expresión N si y solo si:

1) N ≡ x

2) N ≡ λz.M  siendo x ≠ z y donde x ocurre libre en M

3) N ≡ M P
donde x ocurre libre en M **o** en P (equivalentemente: en al menos uno de los dos)

La variable x ocurre ligada en la expresión N si y solo si:

1) N ≡ λz.M  siendo x ≡ z o cuando x ocurre ligada en M

2) N ≡ M P
donde x ocurre ligada en M  y/o en P

Ejemplos:
- λz.x y

x libre, y libre

- λx.x y

x ligada, y libre

- λy.x y

x libre, y ligada

- λx y.x y

x ligada, y ligada

- (λz.z x y) (λx.x)     x libre (operador), x ligada (operando), y libre, z ligada

Aquí conviene el vocabulario de **ocurrencias**: la misma letra puede tener una ocurrencia **libre** y otra **ligada** en el mismo término (son “cosas distintas” ligadas a contextos distintos). En implementaciones reales, los nombres internos no importan: lo que cuenta es la **estructura** del término salvo $\alpha$ (renombre de parámetros).

> **Analogía lingüística.** “Cuando **Juan** dijo que **él** aprobaría…”: el segundo pronombre está **ligado** al sujeto de la oración; si se habla de **otro** Juan de la calle, ese nombre está **libre** del contexto de la frase. El $\lambda$ corresponde a “cuando se nombra *este* parámetro…”.

**Inmutabilidad en lenguajes reales.** En el $\lambda$-cálculo no hay “asignación” que pise un valor: al **reducir**, aparece un término **nuevo**. En **Clojure** encaja con colecciones **persistentes** y `let` para ligaduras locales, y con herramientas como átomos o refs cuando el estado debe cambiar de forma explícita. En **JavaScript** suele usarse `const`, evitar mutar argumentos y preferir que `map` o el *spread* devuelvan **estructuras nuevas** en lugar de alterar las originales.

## 4. Reglas de conversión
En el cálculo lambda existen tres reglas de conversión que permiten transformar una expresión en
otra. Como resultado, ambas expresiones denotan lo mismo y son, por lo tanto, equivalentes.

### 4.1 Regla de conversión Alfa (α)
Consiste en hacer un renombramiento de variable en una abstracción que tiene la forma λx.M.
Si la variable y no ocurre libre en M, es posible sustituir por y todas las ocurrencias libres de x en M:

λx.M =α λy.M[y/x]

Ejemplos:

1) λx.x sustituyendo queda λy.y

2) En $\lambda x.\,y\,x$ **sí** se puede aplicar $\alpha$ renombrando el parámetro a un nombre fresco (p. ej. $\lambda z.\,y\,z$). Lo que **no** es válido es renombrar $x$ a $y$, porque $y$ es libre en el cuerpo y quedaría **capturada** por el nuevo ligador.

Con cualquier variable $z$ que no ocurra libre en el cuerpo, se tiene $\lambda x.\,y\,x =_\alpha \lambda z.\,y\,z$.

3) $\lambda x.\,z\,x\,(\lambda u.\lambda v.\,u\,v)\,v\,x$ sustituyendo $x$ por $y$ fresco queda $\lambda y.\,z\,y\,(\lambda u.\lambda v.\,u\,v)\,v\,y$

4) Si se quiere renombrar el parámetro exterior de $\lambda x\,y.\,x\,z\,y$ a $y$, el $y$ interno **choca** con el nombre nuevo: primero se renombra el parámetro interno (p. ej. $\lambda x\,u.\,x\,z\,u$) y recién entonces el exterior ($\lambda y\,u.\,y\,z\,u$). Es el mismo problema que al compilar: evitar **sombreado** que confunda al lector o a la sustitución.

5) **Convención de Barendregt** (higiene de nombres): en un mismo término conviene que ninguna variable aparezca a la vez libre y ligada, y que **distintos** ligadores no reutilicen el mismo nombre si eso presta a confusión. A partir de $x\,(\lambda x.\,x\,y)\,(\lambda y.\,z\,y)$ son válidos, entre otros:

   - $x\,(\lambda t.\,t\,y)\,(\lambda u.\,z\,u)$ — todos los ligadores renombrados a nombres frescos;
   - $x\,(\lambda t.\,t\,y)\,(\lambda y.\,z\,y)$ — el $y$ libre del primer cuerpo sigue siendo el del contexto exterior.

   También aparecen variantes como $x\,(\lambda u.\,u\,y)\,(\lambda u.\,z\,u)$ o $x\,(\lambda x.\,x\,y)\,(\lambda x.\,z\,x)$ cuando se documentan **reglas** de renombre (no siempre son la forma más legible).

   **No** se puede llegar por $\alpha$ a algo como $z\,(\lambda z.\,z\,y)\,(\lambda y.\,z\,y)$: el $z$ más externo quedaría confundido con el parámetro $z$ (captura indebida del nombre).

### 4.2 Regla de conversión Beta (β)
Consiste en realizar la reducción de una β-redex (expresión reducible β), que es una aplicación cuyo
operador es una abstracción. Es decir, una β-redex es una aplicación que tiene la forma  (λx.M) N.

Ejemplos:
- (λx.(λu.u) (λv.x v)) ((λt.t t) w) Una β-redex que contiene otras dos

- (λx.x x) (λy.y y)

Una β-redex

- (λx.x) (λy.y y) z

Una β-redex

- x (λy.y y)

Ninguna β-redex

Una expresión lambda que no contiene ninguna β-redex está en forma normal. Mientras no se llegue
a la forma normal, puede seguir aplicándose la regla de conversión Beta, que consiste en sustituir por
$N$ todas las ocurrencias **libres** de $x$ en $M$, obteniendo $M[N/x]$ (**sustitución capturando-evitante**): si alguna variable libre de $N$ quedaría ligada por un $\lambda$ de $M$, antes se renombra ese $\lambda$ con $\alpha$.

(λx.M) N =β M[N/x]

**Pureza y efectos laterales.** La $\beta$ modela “sustituir el argumento en el cuerpo”. Si el cuerpo o el argumento **imprimieran**, **mutaran** estado global o **leyeran** la hora, el resultado puede depender del **orden** de evaluación o del mundo exterior: deja de valer el modelo de “solo reglas de reescritura”. Por eso conviene separar un **núcleo puro** (más fácil de probar y componer) de un **borde con efectos** (HTTP, DOM, `println`, etc.).

Ejemplos:
- (λu.u z u) a
   =β  a z a

- (λx y.y x) y a
   =α  (λx z.z x) y a  Obs:  Es obligatorio para evitar que  y  se ligue al entrar
   =β  (λz.z y) a
   =β  a y

- (λx.(λu.u) (λv.x v)) ((λt.t t) w)
   =β  (λu.u) (λv.(λt.t t) w v)
   =β  λv.(λt.t t) w v
   =β  λv.w w v

- (λt.z) ((λx.x x) (λy.y y))
   =β  z

- (λx.x x) (λy.y y)                    Obs: No termina nunca. No tiene forma normal.

### 4.3 Regla de conversión Eta (η)
Consiste en realizar la reducción de una η-redex (expresión reducible η), que es una abstracción que
tiene la forma  λv.M v  y en la cual v no ocurre libre en M.

La regla de conversión Eta establece que:

λv.M v =η M

Ejemplos:
- (λx v.x v) ((λt.t t) w) =β λv.((λt.t t) w) v =β λv.w w v =η w w

- (λv.w x y v) z =η w x y z     Obs:  También (λv.w x y v) z =β w x y z

- λx.x t x   Obs:  λx.M x  no es una η-redex con  M ≡ x t  porque x es libre en M

### 4.4 Equivalencia vs reducción · divergencia

Conviene separar dos ideas:

- **Reducción en un paso** ($\to_\beta$): se eligió **una** redex y se la contrajo. Una **cadena** de pasos se escribe $M \twoheadrightarrow_\beta N$ (cero o más pasos).
- **Equivalencia** ($=_\beta$): $M$ y $N$ son **$\beta$-convertibles** si se puede pasar de uno al otro usando $\beta$ en **cualquier** dirección (incluyendo “deshacer” un paso). Lo mismo con $=_\alpha$, $=_\eta$ y mezclas habituales ($=_{\beta\eta}$, etc.).

En la práctica de los ejercicios casi siempre se **reduce** en una dirección hasta una forma normal, pero las reglas $\alpha$/$\eta$ sirven para **reescribir** sin cambiar el significado.

**Término que no termina.** Ya apareció $(\lambda x.\,x\,x)\,(\lambda x.\,x\,x)$. Es habitual definir $\Omega$ exactamente así: no hay cadena de $\beta$ que llegue a forma normal; la reducción puede continuar **sin fin**. En un lenguaje real, algo análogo sería una recursión sin caso base o un ciclo que no produce valor.

### 4.5 Resumen de las tres reglas

| Regla | Forma típica | Idea en una frase |
|-------|----------------|-------------------|
| $\alpha$ | $\lambda x.\,M \;=_\alpha\; \lambda y.\,M[y/x]$ (con $y$ fresco) | Renombrar parámetros: “misma función, otro nombre de argumento”. |
| $\beta$ | $(\lambda x.\,M)\,N \to_\beta M[N/x]$ | **Aplicar** una función: sustitución en el cuerpo. |
| $\eta$ | $\lambda v.\,M\,v \to_\eta M$ si $v \notin FV(M)$ | Quitar un “envoltorio” que solo pasa el argumento a $M$. |

> **Tres gestos en lenguaje plano.** $\alpha$: “le cambié el nombre al parámetro, es la misma función”. $\beta$: “**metí** el argumento en la función y simplifiqué”. $\eta$: “saqué un envoltorio que solo pasaba el mismo valor al interior; era **redundante**”.

## 5. Estrategias de reducción
La reducción de una expresión lambda a su forma normal (si esta existe) puede realizarse de diversas
maneras. A continuación se describen cuatro de las estrategias más conocidas.

**Vínculo con lenguajes reales (idea general):** **call-by-name** y **orden normal** se parecen a la **evaluación perezosa** (no calcular un argumento hasta hacer falta; ej. Haskell en la práctica). **Call-by-value** y **orden aplicativo** se parecen a la **evaluación estricta** (evaluar argumentos antes de entrar al cuerpo; ej. la mayoría de los lenguajes de la familia ML, Scheme, etc.). La tabla del final resume **qué redex** se elige en cada paso; los ejemplos muestran que esa elección puede marcar la diferencia entre **terminar** o **diverger**.

> **Analogía.** **Call-by-value** es como **pagar al entrar** al cine: aunque uno se vaya a los cinco minutos, ya se pagó la entrada. **Call-by-name** es como “**cobramos solo si se usa** el servicio”: si la función ni mira el argumento, tal vez nunca haga falta calcularlo (y en ejemplos concretos eso puede ser la diferencia entre colgar o no).

### 5.1 Call-by-name
Consiste en ir reduciendo siempre la β-redex más externa desde la izquierda y que no esté ubicada
dentro de una abstracción lambda, hasta llegar a una expresión en forma normal de cabecera (head
normal form, una expresión sin β-redex en su inicio), que no siempre coincide con la forma normal.

Ejemplo:
- (λu.u (λt.t) ((λy.y) u)) ((λz.z) x)
   =β (λz.z) x (λt.t) ((λy.y) ((λz.z) x))
   =β x (λt.t) ((λy.y) ((λz.z) x))

### 5.2 Orden normal
Consiste en ir reduciendo siempre la β-redex más externa desde la izquierda.

Ejemplo:
- (λu.u (λt.t) ((λy.y) u)) ((λz.z) x)
   =β (λz.z) x (λt.t) ((λy.y) ((λz.z) x))
   =β x (λt.t) ((λy.y) ((λz.z) x))
   =β x (λt.t) ((λz.z) x)
   =β x (λt.t) x

Si existe la forma normal de una expresión lambda, esta estrategia siempre permite llegar a ella.

### 5.3 Call-by-value
Consiste en ir reduciendo siempre la β-redex más interna desde la izquierda y que no esté ubicada
dentro de una abstracción lambda.

Ejemplo:
- (λu.u (λt.t) ((λy.y) u)) ((λz.z) x)
   =β (λu.u (λt.t) ((λy.y) u)) x
   =β x (λt.t) ((λy.y) x)
   =β x (λt.t) x

Aunque una expresión lambda tenga forma normal, esta estrategia no siempre permite llegar a ella.

### 5.4 Orden aplicativo
Consiste en ir reduciendo siempre la β-redex más interna desde la izquierda.

Ejemplo:
- (λu.u (λt.t) ((λy.y) u)) ((λz.z) x)
   =β (λu.u (λt.t) u) ((λz.z) x)
   =β (λu.u (λt.t) u) x
   =β x (λt.t) x

Aunque una expresión lambda tenga forma normal, esta estrategia no siempre permite llegar a ella.

### 5.5 Comparación de estrategias
Mediante algunos ejemplos se muestran a continuación las características de las estrategias vistas.

La siguiente expresión lambda no tiene forma normal:

(λu.(λt.t) ((λy.y) w)) ((λv.v) r) ((λz.z z) (λx.x x))

Call-by-name

(λu.(λt.t) ((λy.y) w)) ((λv.v) r) ((λz.z z) (λx.x x))
=β  (λt.t) ((λy.y) w) ((λz.z z) (λx.x x))
=β  (λy.y) w ((λz.z z) (λx.x x))
=β  w ((λz.z z) (λx.x x))

Se llega a la forma normal de cabecera
Orden normal

(λu.(λt.t) ((λy.y) w)) ((λv.v) r) ((λz.z z) (λx.x x))
=β  (λt.t) ((λy.y) w) ((λz.z z) (λx.x x))
=β  (λy.y) w ((λz.z z) (λx.x x))
=β  w ((λz.z z) (λx.x x))
=β  w ((λx.x x) (λx.x x)) ...

Se produce un ciclo infinito

Call-by-value

(λu.(λt.t) ((λy.y) w)) ((λv.v) r) ((λz.z z) (λx.x x))
=β  (λu.(λt.t) ((λy.y) w)) r ((λz.z z) (λx.x x))
=β  (λt.t) ((λy.y) w) ((λz.z z) (λx.x x))
=β  (λt.t) w ((λz.z z) (λx.x x))
=β  w ((λz.z z) (λx.x x))
=β  w ((λx.x x) (λx.x x)) ...

Se produce un ciclo infinito

Orden aplicativo

(λu.(λt.t) ((λy.y) (w))) ((λv.v) r) ((λz.z z) (λx.x x))
=β  (λu.(λt.t) w) ((λv.v) r) ((λz.z z) (λx.x x))
=β  (λu.w) ((λv.v) r) ((λz.z z) (λx.x x))
=β  (λu.w) r ((λz.z z) (λx.x x))
=β  w ((λz.z z) (λx.x x))
=β  w ((λx.x x) (λx.x x)) ...

Se produce un ciclo infinito

La siguiente expresión lambda sí tiene forma normal:

(λu.w ((λy.y) t)) ((λz.z z) (λx.x x))

Call-by-name

(λu.w ((λy.y) t)) ((λz.z z) (λx.x x))
=β  w ((λy.y) t)

Se llega a la forma normal de cabecera
Orden normal

(λu.w ((λy.y) t)) ((λz.z z) (λx.x x))
=β  w ((λy.y) t)
=β  w t

Se llega a la forma normal

Call-by-value

(λu.w ((λy.y) t)) ((λz.z z) (λx.x x))
=β  (λu.w ((λy.y) t)) ((λx.x x) (λx.x x)) ...

Se produce un ciclo infinito

Orden aplicativo

(λu.w ((λy.y) t)) ((λz.z z) (λx.x x))
=β  (λu.w t) ((λz.z z) (λx.x x))
=β  (λu.w t) ((λx.x x) (λx.x x)) ...

Se produce un ciclo infinito

Conclusiones: El **orden normal** (elegir siempre la $\beta$-redex **más externa** a la **izquierda**, aunque esté bajo un $\lambda$) tiene la propiedad clave: **si el término tiene forma normal**, esta estrategia **llega** a ella (no se “pierde” en un camino que solo diverge). Eso **no** dice que todo término termine: en el $\lambda$-cálculo no tipado hay términos **sin** forma normal. **Call-by-name** y **call-by-value** añaden restricciones que modelan implementaciones; **call-by-name** suele relacionarse con hallar **forma normal de cabecera** cuando corresponde, mientras que **call-by-value** puede **no** encontrar la forma normal aun existiendo. **Orden aplicativo** es el “hermano” interno de call-by-value (permite redex bajo $\lambda$) y comparte muchas de sus limitaciones. En la práctica, los lenguajes añaden **tipos**, **constantes** y reglas para que la evaluación sea predecible y eficiente.

**Cortocircuito en JavaScript.** Los operadores `&&` y `||` son **perezosos** en la segunda expresión (no la evalúan si ya tienen el resultado): la intuición es parecida a `And`/`Or` de Church, donde una rama puede no usarse. No confundir con `&` y `|` *bitwise*, que se comportan distinto.

## 6. Representación de valores de verdad · Funciones lógicas
Mediante abstracciones es posible definir representaciones de los valores verdadero y falso,
y funciones lógicas aplicables sobre ellos. Es la idea de **codificación de datos como comportamiento**: un booleano no es un bit en memoria, sino una función que **elige** entre dos alternativas (como un `if` que recibe dos continuaciones).

> **Analogía.** Puede imaginarse un **cruce de ferrocarril** con dos rieles: el booleano no “es un palito”; es el **mecanismo** que manda el tren por la rama A o por la rama B. En programación funcional moderna, los `if`/`match` suelen ser **expresiones con valor** (como el operador ternario `?:` en varios lenguajes), no solo “sentencias” que alteran el flujo imperativo.

Una condición de la forma  si p entonces q; si no r  se representa en cálculo lambda de la siguiente
manera:
If = λp.λq.λr.p q r

Al utilizar la regla de conversión Beta en una aplicación que tenga If como operador y tres
operandos (por ejemplo, a, b y c), se obtendrá otra aplicación que tendrá a como operador y dos
operandos (b y c). Si a representa el valor verdadero, al aplicar nuevamente la regla de conversión
Beta, deberá obtenerse b. En cambio, si a representa el valor falso, deberá obtenerse c. Para ello, se
adoptan las siguientes representaciones de los valores de verdad:

True = λx.λy.x         (Selección del primero de dos operandos)

False = λx.λy.y         (Selección del segundo de dos operandos)

*(Estas son las codificaciones clásicas de **Church** para los booleanos.)*

En efecto, la reducción de  If True b c  da  b,  y la de  If False b c  da  c:

(λp.λq.λr.p q r) (λx.λy.x) b c
=β (λq.λr.(λx.λy.x) q r) b c
=β (λr.(λx.λy.x) b r) c
=β (λx.λy.x) b c
=β (λy.b) c
=β b
(λp.λq.λr.p q r) (λx.λy.y) b c
=β (λq.λr.(λx.λy.y) q r) b c
=β (λr.(λx.λy.y) b r) c
=β (λx.λy.y) b c
=β (λy.y) c
=β c

La negación se representa mediante la siguiente abstracción:

Not = λp.p False True

Es sencillo verificar que **Not True** se reduce a **False** y **Not False** a **True** (con True $= \lambda x.\lambda y.\,x$ y False $= \lambda x.\lambda y.\,y$):

(λp.p False True) True
=β True False True
=β (λx.λy.x) False True
=β (λy.False) True
=β False

(λp.p False True) False
=β False False True
=β (λx.λy.y) False True
=β (λy.y) True
=β True

Las 16 posibles funciones lógicas diádicas (conectivos) se pueden definir mediante abstracciones.
Por ejemplo, la conjunción, la disyunción y la disyunción exclusiva se definen así:

Conjunción:
And = λp.λq.p q False

(*Si $p$ es True, se devuelve $q$; si $p$ es False, se ignora $q$ y se devuelve False.*)

Disyunción:
Or = λp.λq.p True q

(*Si $p$ es True, se devuelve True sin evaluar $q$ en esta codificación; si $p$ es False, se devuelve $q$.*)

Disyunción exclusiva:
Xor = λp.λq.p (q False True) q

**Condicionales en Clojure.** Allí `if` es una **expresión** con valor (como en este formalismo), no solo una sentencia. Los booleanos (`true`/`false`) no son codificación de Church, pero la idea es parecida: `and` y `or` son **macros** con **cortocircuito** (pueden no evaluar una rama), en la misma línea que no reducir un ramal que no corresponde.

## 7. Representación de números · Funciones numéricas y relacionales
También mediante abstracciones se pueden definir numerales (representaciones de números) y
funciones numéricas y relacionales aplicables sobre ellos.

**Numerales de Church.** La idea es que el natural $n$ sea una función que **aplica** $f$ exactamente $n$ veces sobre $x$: así el “contenido” del número es **iteración**. No es una representación eficiente en una computadora real, pero es compacta para razonar y conecta con **fold** / `reduce` en lenguajes funcionales.

> **Analogía.** El número no es “la etiqueta del cajón”; es **cuántas veces se repite una acción**: “dar **tres** vueltas a la manzana”, “picar el ajo **dos** veces”. Por eso el numeral de Church “habla” con un $f$ y un $x$: *repetir esta transformación tantas veces sobre este valor inicial*.

**`reduce` en Clojure y JavaScript.** En ambos entornos aparece la misma idea: función de acumulación, valor inicial y recorrido de una colección. En estilo funcional conviene que cada paso produzca el **siguiente** acumulado sin depender de mutar un objeto compartido; en JavaScript a veces se usa un objeto mutable como acumulador, lo cual exige más cuidado.

El número  0  se representa así:

0 = λf.λx.x

La función  Succ  se define de la siguiente manera:

Succ = λn.λf.λx.f (n f x)

La representación del número  1  se obtiene reduciendo la aplicación  Succ 0:

(λn.λf.λx.f (n f x)) (λf.λx.x)
=β λf.λx.f ((λf.λx.x) f x)
=β λf.λx.f ((λx.x) x)
=β λf.λx.f x

El numeral  2  se obtiene reduciendo  la aplicación Succ (Succ 0) o  Succ 1, y así sucesivamente:

0 = λf.λx.x
1 = λf.λx.f x
2 = λf.λx.f (f x)
3 = λf.λx.f (f (f x))
4 = λf.λx.f (f (f (f x)))
5 = λf.λx.f (f (f (f (f x))))

Puede verificarse que al reducir la aplicación  Succ 3  se obtiene el numeral  4:

(λn.λf.λx.f (n f x)) (λf.λx.f (f (f x)))
=β λf.λx.f ((λf.λx.f (f (f x))) (f) x)
=β λf.λx.f ((λx.f (f (f x))) (x))
=β λf.λx.f (f (f (f x)))

Algunas funciones numéricas que se pueden utilizar con los numerales son las siguientes:

Predecesor de un número:
Pred = λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)

Suma de dos números:
Add = λm.λn.λf.λx.m f (n f x)

Resta de dos números (convención de este apunte: **$m - n$**, es decir, aplicar $\mathrm{Pred}$ $n$ veces a $m$):
 Sub = λm.λn.n Pred m

Producto de dos números:
 Mul = λm.λn.λf.λx.m (n f) x

Potencia de dos números (base $m$, exponente $n$):
 Pow = λm.λn.λf.λx.n m f x

(Nota: con numerales de Church suele escribirse también la forma corta **$\lambda m.\lambda n.\,n\,m$**; al aplicarla a numerales coincide con la versión que explicita $f$ y $x$.)

Enésimo término de la sucesión de Fibonacci (con $F(0)=0$, $F(1)=1$, …; el término itera un paso sobre un par de valores acumulados):
Fibo = λn.n (λf.λa.λb.f b (Add a b)) (λx.λy.x) (λf.λx.x) (λf.λx.f x)

Las funciones relacionales que se pueden utilizar con los numerales son las siguientes:

Evaluar si un número es igual a cero:

IsZero = λn.n (λz.(λx.λy.y)) (λx.λy.x)

Por ejemplo, la reducción de  IsZero 4  da  False:

(λn.n (λz.λx.λy.y) (λx.λy.x)) (λf.λx.f (f (f (f x))))

=β (λf.λx.f (f (f (f x)))) (λz.λx.λy.y) (λx.λy.x)

=β (λx.(λz.λx.λy.y) ((λz.λx.λy.y) ((λz.λx.λy.y) ((λz.λx.λy.y) x)))) (λx.λy.x)

=β (λz.λx.λy.y) ((λz.λx.λy.y) ((λz.λx.λy.y) ((λz.λx.λy.y) (λx.λy.x))))

=β λx.λy.y

En cambio, la reducción de  IsZero 0  da  True:

(λn.n (λz.λx.λy.y) (λx.λy.x)) (λf.λx.x)

=β (λf.λx.x) (λz.λx.λy.y) (λx.λy.x)

=β (λx.x) (λx.λy.x)

=β λx.λy.x

Evaluar si un número es menor o igual que otro:

Lte = λx.λy.IsZero (Sub x y)

Evaluar si un número es mayor o igual que otro:

Gte = λx.λy.Lte y x

Evaluar si un número es menor que otro:

Lt = λx.λy.Not (Gte x y)

Evaluar si un número es mayor que otro:

Gt = λx.λy.Not (Lte x y)

Evaluar si dos números son iguales:

Eq = λx.λy.And (Lte x y) (Gte x y)

Evaluar si dos números son distintos:

Ne = λx.λy.Not (Eq x y)

## 8. Combinadores
Las expresiones lambda que no contienen ninguna variable libre se denominan combinadores.
Algunos combinadores de uso frecuente tienen designaciones propias, por ejemplo los tres que dan
nombre al cálculo de combinadores  SKI (el cual es un tipo de lógica combinatoria):

S = λx.λy.λz.x z (y z)     Función de fusión (Verschmelzungsfunktion)

K = λx.λy.x                Función de constancia (Konstanzfunktion)

I = λx.x                   Función de identidad (Identitätsfunktion)

Todo el cálculo lambda puede reformularse en el cálculo de combinadores SKI, que tiene una
sola operación básica: la aplicación. Al ser equivalente al cálculo lambda, el cálculo de combinadores
SKI es lo suficientemente potente como para codificar cualquier función computable. Los
combinadores S y K se denominan combinadores estándar, ya que con ellos es posible representar
todos los demás. Por ejemplo, I = S K K.

> **Analogía.** $S$ y $K$ son como **dos ladrillos** de LEGO con los que, repitiendo y encajando, se puede armar cualquier figura (cualquier función). En código, la idea se parece a construir todo con **composición** y pocos primitivos, aunque en la práctica se usan más piezas con nombre (`map`, `filter`, etc.) por legibilidad.

**Composición y orden superior.** En Clojure, `comp` arma “$f$ después de $g$”: `(comp f g)`. En JavaScript suele escribirse `x => f(g(x))` o con utilidades de estilo *lodash/fp*. Los combinadores $B$ (composición) y $C$ (intercambio de argumentos) son antecedentes de esos patrones; `map`, `filter` y `partial` son ejemplos cotidianos de **orden superior** cuando las funciones son valores.

En efecto, al reducir S K K se obtiene I:

(λx.λy.λz.x z (y z)) (λx.λy.x) (λx.λy.x)
=β  (λy.λz.(λx.λy.x) z (y z)) (λx.λy.x)
=β  λz.(λx.λy.x) (z) ((λx.λy.x) z)
=β  λz.(λy.z) ((λx.λy.x) z)
=β  λz.z

Otros combinadores muy conocidos son los siguientes:

B = λx.λy.λz.x (y z)

C = λx.λy.λz.x z y

D = λx.λy.λz.λv.x y (z v)

J = λx.λy.λz.λv.x y (x v z)

M = λx.x x

O = λx.λy.y

Q = λx.λy.λz.y (x z)

R = λx.λy.λz.y z x

V = λx.λy.λz.z x y

W = λx.λy.x y y

Y = λf.(λx.f (x x)) (λx.f (x x))              Obs: Definido por Curry

Θ = (λx.λy.y (x x y)) (λx.λy.y (x x y))       Obs: Definido por Turing

Ω = (λx.x x) (λx.x x)

Las funciones recursivas se suelen expresar con un **combinador de punto fijo** como $Y$ o $\Theta$ (definidos arriba).

En el $\lambda$-cálculo **no tipado**, el combinador $Y$ cumple $Y\,g =_\beta g\,(Y\,g)$ para cualquier $g$, lo que permite expresar recursión sin un nombre global. En lenguajes **estrictos** (evaluación estilo call-by-value), esta $Y$ **no** puede usarse tal cual: hace falta una variante (combinador de punto fijo para CBV) o mecanismos del lenguaje (`let rec`, evaluación lazy). A nivel de este apunte basta con captar la idea: la recursión aparece como **punto fijo** de un funcional.

> **Analogía.** Es como definir “el factorial es: si $n=0$ se devuelve 1; si no, $n$ por **el factorial** de $n-1$”: la palabra “factorial” vuelve a aparecer en su propia definición. $Y$ es el truco formal que permite **nombrar** esa autorreferencia cuando no existe `def factorial` en el lenguaje minimal.

Por ejemplo, el factorial y un esquema de **división** (la división entera completa en numerales de Church es extensa; lo siguiente **ilustra** el patrón con $Y$ e `If`):

Fact = Y (λf.λx.If (IsZero x) 1 (Mul x (f (Pred x))))

Div = λn.(Y (λc.λn.λm.λf.λx.(λd.If (IsZero d) (0 f x)
       (f (c d m f x))) (Sub n m))) (Succ n)

## 9. Pares y listas
Las abstracciones permiten definir pares ordenados y listas. Un par ordenado está compuesto de dos
elementos, denominados primero y segundo.

El par ordenado  (a . b)  se representa así:

(a . b) = λs.s a b

La función  Pair  utilizada para construir pares ordenados se define de la siguiente manera:

Pair = λx.λy.λs.s x y

Las funciones  First  y  Second  devuelven, respectivamente, los elementos primero y segundo de
un par ordenado:
First = λp.p True

Second = λp.p False
Por ejemplo:

First (Pair p q)
(λp.p (λx.λy.x)) ((λx.λy.λs.s x y) p q)
=β (λp.p (λx.λy.x)) ((λy.λs.s p y) q)
=β (λp.p (λx.λy.x)) (λs.s p q)
=β (λs.s p q) (λx.λy.x)
=β (λx.λy.x) p q
=β (λy.p) q
=β p
Second (Pair p q)
(λp.p (λx.λy.y)) ((λx.λy.λs.s x y) p q)
=β (λp.p (λx.λy.y)) ((λy.λs.s p y) q)
=β (λp.p (λx.λy.y)) (λs.s p q)
=β (λs.s p q) (λx.λy.y)
=β (λx.λy.y) p q
=β (λy.y) q
=β q

Una lista puede estar vacía o no. En esta codificación, un nodo de lista es un **par**: la **primera** componente del par actúa como **etiqueta** (`True` = lista vacía, `False` = nodo con cabeza y cola). Por eso `Null = First`: lee la etiqueta y distingue vacío de no vacío.

> **Analogía.** Una lista encadenada es como un **tren**: cada vagón (`Cons`) dice “acá va un pasajero (cabeza) y el resto del tren (cola)”. El **vagón fantasma** inicial que marca “no hay más formación” es `Nil`. En lenguajes con listas nativas (`[]` y `::`) no se razona así en el día a día, pero la idea de **cabeza + cola** es la misma que en recursión sobre listas en Programación I.

La lista vacía se define así:

Nil = Pair True True    Obs: Es más recomendable usar  Nil = λz.z

*(Con `Nil = Pair True True`, se tiene `First Nil = True`. Con `Cons`, la cabeza va en un par interno y la etiqueta externa es `False`, así `First (Cons …) = False`.)*

La lista (a b c) se representa así (notación informal “estilo Lisp” para leer la anidación de pares):

(False . (a . (False . (b . (False . (c . (λz.z)))))))

La función para verificar si una lista está vacía es la siguiente:

Null = First

Una aplicación cuyo operador sea la función Null se reduce a True si el operando es Nil o a False
si el operando es un nodo `Cons` (etiqueta False).

Para construir un nodo de una lista, indicando la cabeza  x  y la cola  y, se define la función Cons:

Cons = λx.λy.Pair False (Pair x y)

**Listas persistentes.** En Clojure, listas y `cons` permiten **compartir estructura**: por ejemplo, `conj` no invalida la lista anterior para quien aún la referencia. En JavaScript, `[...xs, x]` o `.concat` siguen una idea parecida si no se muta `xs` *in-place*.

Las funciones  Head  y  Tail  devuelven, respectivamente, los elementos cabeza y cola de una lista:

Head = λz.First (Second z)

Tail = λz.Second (Second z)
Por ejemplo:
(Head (Tail (Tail (Cons a (Cons b (Cons c Nil))))))  da  c.

## 10. Temas que este apunte no desarrolla (y por qué importan)

Este apunte centra el **$\lambda$-cálculo no tipado** como historia y como lenguaje mínimo. Lo que sigue es un mapa breve del paradigma y de la teoría de lenguajes; los detalles quedan para lectura u otras asignaturas.

### 10.1 Azúcar sintáctico: `let`, nombres locales y clausuras

En texto y en pizarra se escribe a menudo **$\texttt{let}\; x = N \;\texttt{in}\; M$** (o definiciones con nombre). En $\lambda$ puro eso es azúcar de **$(\lambda x.\,M)\,N$**: el nombre $x$ es el parámetro de una función aplicada al valor $N$. En una implementación real, el **entorno** guarda qué valor tiene cada variable libre en el cuerpo: eso es la **clausura** cuando una función “recuerda” variables del contexto donde se creó.

> **Quienes vienen de orientación a objetos.** La imagen es parecida a un objeto que guarda datos y expone un método que los usa; aquí el encapsulado suele ser **otra función**. En Java, las lambdas que capturan variables **efectivamente finales** ilustran la misma idea de entorno capturado.

### 10.2 Call-by-need (evaluación perezosa con memoria)

**Call-by-name** no vuelve a calcular un argumento si se usa dos veces… pero **sí** puede recalcularlo cada vez. **Call-by-need** (idea central de Haskell) es como CBN, pero **memoiza** el resultado de la primera demanda del argumento. Así se evita trabajo duplicado sin perder la semántica perezosa en muchos casos.

**Evaluación diferida en Clojure.** Las *lazy seqs* y formas como `lazy-seq` o `delay` retrasan el trabajo hasta **consumir** el siguiente valor (salvo detalles del lenguaje: *chunking*, efectos en el cuerpo, etc.).

### 10.3 $\lambda$-cálculo simplemente tipado y más allá

En el $\lambda$-cálculo **no tipado** se pueden escribir términos “locos” que **no tienen** interpretación razonable como programa (p. ej. aplicar un número como si fuera función). Los lenguajes de producción usan **sistemas de tipos** que descartan esos términos **antes** de ejecutar. El **$\lambda$-cálculo simplemente tipado** es el primer paso: cada variable tiene un tipo, las aplicaciones están restringidas y, crucialmente, **toda** reducción termina (no hay $\Omega$). A partir de ahí se construyen sistemas más ricos (polimorfismo, tipos dependientes, etc.). Una curiosidad histórica: el **isomorfismo de Curry–Howard** relaciona pruebas y programas (“proposiciones como tipos”); queda fuera del alcance de este apunte, pero explica por qué el $\lambda$-cálculo tipado es central en fundamentos.

### 10.4 Constantes, $\delta$-reglas y “$\lambda$ más aritmética”

Aquí los números y booleanos son **codificaciones**. Los intérpretes reales suelen tener **literales** y primitivas (`+`, `if`, etc.) con reglas extra ($\delta$-reducción). Eso acerca el modelo a la implementación sin reemplazar la lección sobre **codificación** y **combinadores**.

### 10.5 Otras codificaciones de datos

Los **numerales de Church** no son la única opción. Por ejemplo, los **numerales de Scott** representan un natural como “caso cero o sucesor de otro”, alineados con **tipos inductivos** (como `data Nat = Z | S Nat` en Haskell). Para listas y árboles existen codificaciones análogas. Sirven para comparar estilos de razonamiento y eficiencia teórica.

### 10.6 Máquinas abstractas

La reducción en papel no es cómo ejecuta la máquina. Modelos como la **SECD** o la **máquina de Krivine** traducen estrategias de evaluación a **estados** (código + pila + entorno). Conectan este apunte con compiladores e intérpretes reales.

### 10.7 Lecturas posibles (opcional)

- H. P. Barendregt, *The Lambda Calculus: Its Syntax and Semantics* — referencia clásica (exigente).
- B. C. Pierce, *Types and Programming Languages* — $\lambda$ tipado y fundamentos orientados a informática.

---

**Cierre.** El hilo conductor es: **expresión**, **reducción**, **estrategia**, **datos codificados**, **recursión por punto fijo** y **combinadores**. El resto del paradigma funcional (módulos, efectos, concurrencia, ecosistemas concretos) se apoya en estas ideas, pero ya no en el $\lambda$-cálculo puro de los años 30. Los apartados que relacionan el texto con **JavaScript** y **Clojure** sirven como puente hacia la práctica con lenguajes reales.
