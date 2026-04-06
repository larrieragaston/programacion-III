---
title: Ejercicios adicionales — Cálculo λ
aside: false
---

# Ejercicios adicionales

Ejercicios de Cálculo lambda
1. ¿Cuáles de las siguientes expresiones-λ son correctas según la gramática
vista en clase? ¿Cuáles no lo son? Justificar cada respuesta.
• (λx.2x)
• (λx.xλy.y)
• (λx.(λy.(xy)))
• (λx.x)
• (λx.(xy)z)
2. ¿Cuáles de las siguientes representan expresiones-λ correctas según las
convenciones sintácticas? ¿Cuáles no? En caso de responder negativamente, explicar porque; en caso de responder afirmativamente, indicar a
qué expresión-λ - corresponde.
• (λx.x)
• (λxx)
• λx.x
• λx.xy
• λx.xyλz.xz.y
3. Indicar, para cada variable, cuáles de sus ocurrencias son libres y cuales
acotadas, en las siguientes expresiones. Indicar a que abstracción-λ está
ligada cada ocurrencia no libre.
• (λy.y(λx.x)z)
• (λy.x(λx.x)z)
• (λy.y(λy.y)yx)
4. Encontrar los subtérminos de las siguientes expresiones:
• (λy.y(λx.x)z)
• (λy.x(λx.x)z)
5. Realizar las siguientes sustituciones:
• (λy.x(λx.x)z)[z := (λw.wt)]

• (λy.x(λx.x)z)[z := (λw.wy)]
• (λy.yz)[y := z]
• (λy.yz)[z := y]
6. Indicar cuáles de los siguientes pares de expresiones-λ son α-equivalentes
y cuáles no lo son. Justificar cada respuesta.
• (λxyz.x(λy.yz)w), (λtuv.t(λz.zv))w
• (λxyz.x(λy.yz)w), (λxyw.x(λy.yw)z)
• (λxyz.x(λy.yz)w), (λxtz.x(λu.tz))w
• (λxyz.x(λy.yz)w)(λx.xy), (λxyw.x(λy.yz)w)(λz.zy)
7. Determinar las redex-β de cada uno de los siguientes términos-λ -. De ser
posible, β -reducirlos hasta obtener su forma normal.
• (λx.λy.xy)(λy.yz)
• (λx.λy.xy)(λz.yz)z
• (λx.(λy.x)yλz.z)(λy.yz)
• (λf.(λx.f(xx))(λx.f(xx)))
8. ¿Cuáles de los siguientes pares de términos-λ - son β -equivalentes? Justificar cada respuesta.
• (λf.(λx.xx)(λx.f(xx))), (λx.x)(λf.(λxy.xy)(λx.xx)((λz.z)(λx.f((λxy.xy)xx))))
• (λf.(λx.xx)(λx.f(xx))), (λf.(λxy.xx)(λx.f(xx))(λx.xf(xx)))
9. Determinar cuáles de las siguientes ecuaciones son ciertas. Justificar cada
respuesta.
• and T F = F
• iscero 3 = F
• bic T T = T
• imp T F = F
• scc 4= 5
• 2 succ 2 = 4
• pred 2 = 1
• prod 2 3 =6
• plus 2 0 = 2
• exp 2 3 = 8
• fst (2,1)=2
10. Agregue 5 ejemplos y/o ejercicios vistos en clase que considere importantes.

