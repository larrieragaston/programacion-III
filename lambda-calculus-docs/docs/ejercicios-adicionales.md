---
title: Ejercicios adicionales — Cálculo λ
pageClass: ejercicios-adicionales
---

# Ejercicios adicionales

Ejercicios de cálculo λ. Las definiciones formales y los nombres canónicos de operadores siguen el **apunte** (`apunte.md`); en enunciados con notación abreviada (p. ej. `plus`, `iscero`), interpretar según las macros del apunte.

Enunciados

1. ¿Cuáles de las siguientes expresiones-λ son correctas según la gramática vista en clase? ¿Cuáles no lo son? Justificar cada respuesta.
   1. `(λx.2x)`
   2. `(λx.xλy.y)`
   3. `(λx.(λy.(xy)))`
   4. `(λx.x)`
   5. `(λx.(xy)z)`

2. ¿Cuáles de las siguientes representan expresiones-λ correctas según las convenciones sintácticas? ¿Cuáles no? En caso de responder negativamente, explicar por qué; en caso de responder afirmativamente, indicar a qué expresión-λ corresponde.
   1. `(λx.x)`
   2. `(λxx)`
   3. `λx.x`
   4. `λx.xy`
   5. `λx.xyλz.xz.y`

3. Indicar, para cada variable, cuáles de sus ocurrencias son libres y cuales acotadas, en las siguientes expresiones. Indicar a que abstracción-λ está ligada cada ocurrencia no libre.
   1. `(λy.y(λx.x)z)`
   2. `(λy.x(λx.x)z)`
   3. `(λy.y(λy.y)yx)`

4. Encontrar los subtérminos de las siguientes expresiones:
   1. `(λy.y(λx.x)z)`
   2. `(λy.x(λx.x)z)`

5. Realizar las siguientes sustituciones:
   1. `(λy.x(λx.x)z)[z := (λw.wt)]`
   2. `(λy.x(λx.x)z)[z := (λw.wy)]`
   3. `(λy.yz)[y := z]`
   4. `(λy.yz)[z := y]`

6. Indicar cuáles de los siguientes pares de expresiones-λ son α-equivalentes y cuáles no lo son. Justificar cada respuesta.
   1. `(λxyz.x(λy.yz)w)`, `(λtuv.t(λz.zv))w`
   2. `(λxyz.x(λy.yz)w)`, `(λxyw.x(λy.yw)z)`
   3. `(λxyz.x(λy.yz)w)`, `(λxtz.x(λu.tz))w`
   4. `(λxyz.x(λy.yz)w)(λx.xy)`, `(λxyw.x(λy.yz)w)(λz.zy)`

7. Determinar las redex-β de cada uno de los siguientes términos-λ -. De ser posible, β -reducirlos hasta obtener su forma normal.
   1. `(λx.λy.xy)(λy.yz)`
   2. `(λx.λy.xy)(λz.yz)z`
   3. `(λx.(λy.x)yλz.z)(λy.yz)`
   4. `(λf.(λx.f(xx))(λx.f(xx)))`

8. ¿Cuáles de los siguientes pares de términos-λ - son β -equivalentes? Justificar cada respuesta.
   1. `(λf.(λx.xx)(λx.f(xx)))`, `(λx.x)(λf.(λxy.xy)(λx.xx)((λz.z)(λx.f((λxy.xy)xx))))`
   2. `(λf.(λx.xx)(λx.f(xx)))`, `(λf.(λxy.xx)(λx.f(xx))(λx.xf(xx)))`

9. Determinar cuáles de las siguientes ecuaciones son ciertas (usar las definiciones de numerales de Church, `succ`, `plus`, etc., del apunte). Justificar cada respuesta.
   1. `and T F = F`
   2. `iscero 3 = F`
   3. `bic T T = T`
   4. `imp T F = F`
   5. `scc 4= 5`
   6. `2 succ 2 = 4`
   7. `pred 2 = 1`
   8. `prod 2 3 =6`
   9. `plus 2 0 = 2`
   10. `exp 2 3 = 8`
   11. `fst (2,1)=2`

10. Agregue 5 ejemplos y/o ejercicios vistos en clase que considere importantes.
