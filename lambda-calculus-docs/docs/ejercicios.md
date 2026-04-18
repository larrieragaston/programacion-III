---
title: Guía de ejercicios — Cálculo λ
description: Ejercicios de la guía del apunte e intérpretes en línea.
---

# Guía de ejercicios

## Intérpretes en línea

- [Lambda Calculus Interpreter](https://lambda-calculus-interpreter.vercel.app/) — reducción paso a paso
- [Lambda Calculator (Burch)](https://cburch.com/lambda/) — orden eager/lazy
- [λ-Calculus Playground](https://sshwy.github.io/lamcalc/en/playground.html) — numerales de Church y combinadores
- [kdlcj.gitlab.io/lambda](https://kdlcj.gitlab.io/lambda)

## Enunciados

1. Escribir las siguientes expresiones con el menor número de paréntesis posible:
   1. `(λx.(λy.(λz.((x z) (y z)))))`
   2. `(((a b) (c d)) ((e f) (g h)))`
   3. `(λx.((λy.(y x)) (λv.v) z) u) (λw.w)`

2. Restaurar todos los paréntesis descartados en las siguientes expresiones:
   1. `x x x x`
   2. `λx.x λy.y`
   3. `λx.(x λy.y x x) x`

3. Para las siguientes expresiones lambda:
   - Identificar las ocurrencias de variables libres y ligadas.
   - Reducir a su forma normal aplicando las reglas alfa, beta y eta, utilizando orden normal y orden aplicativo, y comparar los resultados.
   1. `(λx.((λy.y) x)) z`
   2. `(λx.λy.x y) (z y)`
   3. `(λx.λy.x) x y`
   4. `(λx.((λz.z x) (λx.x))) y`
   5. `(λx.((λy.x y) z)) (λx.x y)`
   6. `((λy.(λx.((λx.λy.x) x)) y) M) N`
   7. `(λx.λy.λx.x y z) (λx.λy.y) M N`
   8. `((λx.(λy.λz.z) x) ((λx.x x x) (λx.x x x))) x`

4. Probar que:
   1. `C I = λy.λz.z y` (con `C = λx.λy.λz.x z y` e `I = λx.x`)
   2. `K I = 0` (combinadores `S` y `K` como en el apunte)
   3. `S (K S) K = B`

5. Definir en Cálculo Lambda las siguientes operaciones lógicas: `NOR`, `NAND`, `XNOR`, y verificar para cada una su tabla de verdad.

6. Verificar que:
   1. `Pred 5 = 4`
   2. `IsZero 2 = False`
   3. `Add 2 3 = 5`
   4. `Sub 3 1 = 2`
   5. `Mul 2 3 = 6`
   6. `Div 6 2 = 3`
   7. `Pow 2 3 = 8`
   8. `Fibo 6 = 8`
   9. `Fact 3 = 6`

7. ¿Por qué a `(Y K)` se lo conoce como el Pac-Man? Reducir `(Y K) a b c d` usando la estrategia Call-by-name.

8. Reducir `YO` y confirmar que se haya traducido al inglés.
