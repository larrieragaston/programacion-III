---
title: Guía de ejercicios — Cálculo λ
description: Ejercicios de la guía del apunte e intérpretes en línea.
aside: false
---

# Guía de ejercicios

## Intérpretes en línea

- [kdlcj.gitlab.io/lambda](http://kdlcj.gitlab.io/lambda)
- [projectultimatum.org/cgi-bin/lambda](http://projectultimatum.org/cgi-bin/lambda)
- [cburch.com/dev/lambda](http://www.cburch.com/dev/lambda/index.html)
- [math.cmu.edu/~wgunther/lamred](http://www.math.cmu.edu/~wgunther/lamred.html)

## Enunciados

1. Escribir las siguientes expresiones con el menor número de paréntesis posible:
a) (λx.(λy.(λz.((x z) (y z)))))
b) (((a b) (c d)) ((e f) (g h)))
c) (λx.((λy.(y x)) (λv.v) z) u) (λw.w)

2. Restaurar todos los paréntesis descartados en las siguientes expresiones:
a) x x x x
b) λx.x λy.y
c) λx.(x λy.y x x) x

3. Para las siguientes expresiones lambda:
a) Identificar las ocurrencias de variables libres y ligadas.
b) Reducir a su forma normal aplicando las reglas alfa, beta y eta, utilizando
orden normal y orden aplicativo, y comparar los resultados.

1) ( λx.( ( λy.y ) x ) ) z
2) ( λx.λy.x y ) ( z y )
3) ( λx.λy.x ) x y
4) ( λx.( ( λz.z x ) ( λx.x ) ) ) y
5) ( λx.( ( λy.x y ) z ) ) ( λx.x y )
6) ( ( λy.( λx.( ( λx.λy.x ) x ) ) y ) M ) N
7) ( λx.λy.λx.x y z ) (λx.λy.y) M N
8) ( ( λx.( λy.λz.z ) x ) ( ( λx.x x x ) ( λx.x x x ) ) ) x

4. Probar que:

a) C I = λy z.z y

b) K I = O

c) S (K S) K = B

5. Definir en Cálculo Lambda las siguientes operaciones lógicas: NOR, NAND,
XNOR, y verificar para cada una su tabla de verdad.

6. Verificar que:

a) Pred 5 = 4

b) IsZero 2 = False

c) Add 2 3 = 5

d) Sub 3 1 = 2

e) Mul 2 3 = 6

f) Div 6 2 = 3

g) Pow 2 3 = 8

h) Fibo 6 = 8

i) Fact 3 = 6

7. ¿Por qué a (Y K) se lo conoce como el Pac-Man? Reducir (Y K) a b c d usando la
estrategia Call-by-name.

8. Reducir YO y confirmar que se haya traducido al inglés.
