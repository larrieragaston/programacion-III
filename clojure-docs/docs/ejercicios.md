---
title: Guía de ejercicios — Clojure
description: Ejercicios de la guía del apunte de Clojure — Programación III, INSPT.
pageClass: ejercicios
---

# Guía de ejercicios

1. Definir la función `digs` que reciba un número y devuelva una lista con sus **dígitos**.

2. Definir la función `repartir` que, llamada sin argumentos, devuelva la cadena "Uno para vos, uno para mí". De lo contrario, se devolverá una lista, en la que habrá una cadena "Uno para X, uno para mí" por cada argumento X.

3. Definir una función para producir una lista con los elementos en las **posiciones pares** de dos listas dadas.

4. La **transcripción** es el proceso en el que la secuencia de **ADN** de un gen se copia (transcribe) para hacer una molécula de **ARN**. La cadena de ARN transcrita se forma reemplazando cada nucleótido del ADN por su complemento de ARN: G → C, C → G, T → A y, por último, A → U. Definir la función `adn2arn` que reciba una cadena de ADN y la devuelva transcrita en ARN.

5. Definir una función para eliminar las ocurrencias de un dato **escalar** en una lista (a todo nivel).

6. Definir una función para obtener el último símbolo de una lista (a todo nivel).

7. Definir una función para obtener el **elemento central** de una lista.

8. Definir una función para eliminar los **elementos repetidos** de una lista simple.

9. Definir una función para ordenar una lista de listas por **longitud creciente**.

10. Un **ISBN-10** es válido si sus 10 dígitos x1, x2, x3, ... x10 cumplen lo siguiente: (x1 * 10 + x2 * 9 + x3 * 8 + x4 * 7 + x5 * 6 + x6 * 5 + x7 * 4 + x8 * 3 + x9 * 2 + x10 * 1) mod 11 == 0. Un ISBN-10 está dividido en cuatro partes: el código de país o lengua de origen (de 1 a 5 dígitos), el editor, el número del artículo y un **dígito de control**. Opcionalmente, estas cuatro partes pueden estar separadas mediante espacios en blanco o guiones. El dígito de control puede valer X que representa el valor 10. Por ejemplo, 3-598-21507-X es un ISBN-10 válido. Escribir la función `isbn-10?` que devuelve `true` si la cadena recibida es un ISBN-10 válido; si no, `false`.

11. Definir una función para obtener la **matriz triangular superior** (incluyendo la diagonal principal) de una matriz cuadrada que está representada como una lista de listas.

12. Definir una función para obtener la **diagonal principal** de una matriz cuadrada que está representada como una lista de listas.

13. Definir una función para **transponer** una lista de listas.

14. Definir una función que cuente las apariciones de cada **nucleótido** en una cadena de ADN.

15. Definir una función que cuente las apariciones de cada **palabra** en una frase.

16. Definir una función que reciba un número *n* y devuelva el enésimo **número primo**.

17. Definir una función que determine si una palabra tiene o no **letras repetidas**.

18. Definir la función `b` que aplicada a una lista de funciones *f* y a un argumento *x* obtenga la lista de resultados de aplicar cada función *f* a *x*.

19. Definir una función que devuelva el **tipo de triángulo** que constituyen tres números que representan longitudes.

20. Definir la función `slice` que reciba una cadena *cad* y un número *n* y devuelva una lista con todas las subcadenas contiguas de *cad* cuyo tamaño sea *n*. Por ejemplo: `(slice "abcde" 3)` → `("abc" "bcd" "cde")`

21. Definir una función que reciba una palabra y un conjunto de sus posibles **anagramas**, y devuelva un conjunto que solo contenga las palabras que realmente son sus anagramas.

22. Definir una función que reciba una cadena y devuelva el **acrónimo** correspondiente.

23. Definir una función que devuelva `true` si una frase es un **pangrama** (es decir, si contiene todas las letras del alfabeto); si no, `false`. Por ejemplo: `(pangrama? "Fabio me exige, sin tapujos, que añada cerveza al whisky")` → `true`

24. Definir la función `narcissistic?` que devuelva `true` si un número dado es igual a la suma de cada uno de sus dígitos elevado a la cantidad de dígitos; si no, `false`. Por ej: `(narcissistic? 153)` → `true`

25. Definir las funciones `filas-max-V` y `mas-V-o-F` que, aplicadas a una **matriz de V y F** (una lista de listas con los valores V y F), devuelvan, respectivamente:

    **a)** El/los número/s de la/s fila/s en la/s que la cantidad de V es máxima, por ejemplo: `(filas-max-V '((V F V V F)(V V F V V)(F F F V F)(V V V F V)))` → `(2 4)`

    **b)** V si en la mayoría de las filas hay más V que F o, de lo contrario, F, por ejemplo: `(mas-V-o-F '((V F V V F)(F F F V F)(V V F F V)))` → `V`

26. Definir la función `sublist` que devuelva la **sublista** correspondiente a una lista, una posición inicial y una longitud dadas. Por ejemplo: `(sublist '(A B C D E F G) 3 2)` → `(C D)`

27. Definir la función `pos-inicial` que, dadas dos listas simples, devuelva la **posición inicial** en la cual la primera lista se encuentra contenida en la segunda. Si no se encuentra contenida, la función devolverá cero. Por ejemplo: `(pos-inicial '(C D) '(A B C D E F))` → `3` · `(pos-inicial '(A C) '(A B C D E F))` → `0`

28. Definir una función que actúe como la instrucción `distl` de **FP**. Por ejemplo: `(distl 'a '(b c d))` → `((a b)(a c)(a d))`

29. Definir la función `col-par-fil-imp` que devuelva la matriz resultante de tomar de una matriz las **columnas pares** y, de estas, las **filas impares**. Por ejemplo: `(col-par-fil-imp '((1 5 7 9)(2 4 8 4)(3 6 7 8)(6 8 7 3)))` → `((5 9)(6 8))`

30. Definir la función `dif-sumas` que devuelva la sumatoria de los números de las **filas impares** menos la sumatoria de los números de las **filas pares** de una matriz representada mediante listas. Por ejemplo: `(dif-sumas '((1 5 7)(2 4 8)(3 6 7)))` → (1+5+7+3+6+7)-(2+4+8) → 15

31. Definir una función que devuelva la lista que resulta al **intercalar** los elementos de otras dos listas que recibe como parámetros. Por ejemplo: `(intercalar '(1 2 3) '(4 5 6))` → `(1 4 2 5 3 6)`

32. Definir una función que calcule la **profundidad** de una lista. Por ejemplo: `(profundidad '((2 3)(3 ((7))) 5))` → `4`

33. Definir una función que devuelva un vector con los **números primos** menores que 100.

34. Definir una función que reciba un número *n* y devuelva un vector de vectores que tenga la siguiente forma: `[[1] [1 2] [1 2 3] [1 2 3 4] ... [1 2 3 4 ... n]]`

35. Definir una función que reciba una lista de pares ordenados, en los cuales la primera componente indica el equipo que resultó ganador de un partido y la segunda indica el perdedor (no hay empates), y que devuelva una lista con los equipos **invictos**.

36. Definir una función que reciba una lista de pares ordenados, en los cuales la primera componente indica el equipo que resultó ganador de un partido y la segunda indica el perdedor (no hay empates), y devuelva una lista con los equipos que **solo perdieron**.

37. Definir una función que reciba una lista de pares ordenados, en los cuales la primera componente indica el equipo que resultó ganador de un partido y la segunda indica el perdedor (no hay empates), y que devuelva una lista que contenga tres sublistas: en la primera aparecerán los equipos que **ganaron más** veces de las que perdieron; en la segunda, los equipos que **perdieron más** veces de las que ganaron y, en la tercera, los equipos que ganaron y perdieron la misma cantidad de veces.

38. Definir una función que devuelva `true` si una frase es un **palíndromo** (es decir, si se lee igual al derecho o al revés); si no, `false`. No se debe distinguir entre mayúsculas y minúsculas, ni considerar los acentos. Los espacios y los signos de puntuación deben ignorarse. Por ejemplo: `(palindromo? "La ruta nos aportó otro paso natural.")` → `true`

39. Definir las funciones `ieee-754` que reciba un número y devuelva una lista con los 32 bits correspondientes a su representación en notación de **punto flotante** según la norma **IEEE-754** (*single*) y `bin2hex` que reciba una lista de bits y devuelva una cadena con su representación en hexadecimal.

40. Definir una función que reciba un número entero y devuelva una cadena con su representación en **números romanos**.
