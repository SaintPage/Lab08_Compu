"""
Problema 3: el ciclo externo da n/3 vueltas y el interno avanza de 4 en 4.
Complejidad: O(n^2)
"""

import os
import sys

import perfilador

# printf se manda a /dev/null para medir el algoritmo y no la velocidad de la terminal
salida = open(os.devnull, "w")


def funcion(n):
    i = 1
    while i <= n // 3:                # for (i = 1; i <= n/3; i++)
        j = 1
        while j <= n:                 # for (j = 1; j <= n; j += 4)
            print("Sequence", file=salida)
            j += 4
        i += 1


def conteo_teorico(n):
    """Veces que se ejecuta el printf: piso(n/3) * techo(n/4)."""
    return (n // 3) * ((n + 3) // 4)


def modelo(n):
    return n * n


def main(argumentos):
    global salida
    if "--demo" in argumentos:
        n = int(argumentos[argumentos.index("--demo") + 1])
        salida = sys.stdout
        funcion(n)
        print(f"(formula: {conteo_teorico(n)} impresiones)")
        return
    perfilador.ejecutar("problema3", "Problema 3: O(n²)", funcion, conteo_teorico,
                        modelo, "n²", perfilador.leer_limite(argumentos))


if __name__ == "__main__":
    main(sys.argv[1:])
