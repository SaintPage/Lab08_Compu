"""
Problema 1: tres ciclos anidados, el mas interno duplica k.
Complejidad: O(n^2 log n)
"""

import math
import sys

import perfilador


def funcion(n):
    counter = 0
    i = n // 2
    while i <= n:                     # for (i = n/2; i <= n; i++)
        j = 1
        while j + n // 2 <= n:        # for (j = 1; j+n/2 <= n; j++)
            k = 1
            while k <= n:             # for (k = 1; k <= n; k = k*2)
                counter += 1
                k = k * 2
            j += 1
        i += 1
    return counter                    # se devuelve solo para poder verificarlo


def conteo_teorico(n):
    """Veces que se ejecuta counter++ (formula exacta del analisis de la parte a)."""
    ciclo_i = n - n // 2 + 1          # i = n/2, ..., n
    ciclo_j = n - n // 2              # j = 1, ..., n - n/2  (= techo de n/2)
    ciclo_k = n.bit_length()          # k = 1, 2, 4, ..., 2^piso(log2 n)  ->  piso(log2 n) + 1
    return ciclo_i * ciclo_j * ciclo_k


def modelo(n):
    return n * n * math.log2(n)


def main(argumentos):
    if "--demo" in argumentos:
        n = int(argumentos[argumentos.index("--demo") + 1])
        print(f"n = {n}: counter = {funcion(n)}, formula = {conteo_teorico(n)}")
        return
    perfilador.ejecutar("problema1", "Problema 1: O(n² log n)", funcion, conteo_teorico,
                        modelo, "n² log n", perfilador.leer_limite(argumentos))


if __name__ == "__main__":
    main(sys.argv[1:])
