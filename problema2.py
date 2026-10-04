"""
Problema 2: el ciclo interno se rompe con break en su primera iteracion.
Complejidad: O(n)
"""

import os
import sys

import perfilador

# printf se manda a /dev/null para medir el algoritmo y no la velocidad de la terminal
salida = open(os.devnull, "w")


def funcion(n):
    if n <= 1:
        return
    i = 1
    while i <= n:                     # for (i = 1; i <= n; i++)
        j = 1
        while j <= n:                 # for (j = 1; j <= n; j++)
            print("Sequence", file=salida)
            break                     # sale del ciclo j en la primera vuelta
            j += 1                    # nunca se alcanza (igual que el j++ del for en C)
        i += 1


def conteo_teorico(n):
    """Veces que se ejecuta el printf."""
    return n if n > 1 else 0


def modelo(n):
    return n


def main(argumentos):
    global salida
    if "--demo" in argumentos:
        n = int(argumentos[argumentos.index("--demo") + 1])
        salida = sys.stdout
        funcion(n)
        print(f"(formula: {conteo_teorico(n)} impresiones)")
        return
    perfilador.ejecutar("problema2", "Problema 2: O(n)", funcion, conteo_teorico,
                        modelo, "n", perfilador.leer_limite(argumentos))


if __name__ == "__main__":
    main(sys.argv[1:])
