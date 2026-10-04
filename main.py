"""
Ejecuta todo el laboratorio: verificacion de formulas, profiling de los problemas 1-3,
verificacion del problema 4 y medicion del problema 5c.

Uso:  python main.py              (limite de 60 s por corrida)
      python main.py --limite 20  (limite distinto)
"""

import sys

import perfilador
import problema1
import problema2
import problema3
import problema4
import problema5c
import verificar


def seccion(titulo):
    print("\n" + titulo)
    print("-" * len(titulo))


def main(argumentos):
    limite = perfilador.leer_limite(argumentos)

    seccion("Verificacion de formulas")
    verificar.main()

    seccion("Profiling")
    problema1.main(["--limite", str(limite)])
    problema2.main(["--limite", str(limite)])
    problema3.main(["--limite", str(limite)])

    seccion("Problema 4: conteo de comparaciones")
    problema4.main()

    seccion("Problema 5c: tiempo de A(n)")
    problema5c.main()


if __name__ == "__main__":
    main(sys.argv[1:])