"""
Comprueba que las formulas exactas del analisis coinciden con lo que hacen los programas.
"""

import problema1
import problema2
import problema3
from problema5c import elementos_copiados


class ContadorDeLineas:
    """Sustituye a la salida: en vez de imprimir, cuenta cuantas lineas se escribieron."""
    def __init__(self):
        self.lineas = 0

    def write(self, texto):
        self.lineas += texto.count("\n")


def contar_impresiones(modulo, n):
    original = modulo.salida
    modulo.salida = ContadorDeLineas()
    modulo.funcion(n)
    lineas = modulo.salida.lineas
    modulo.salida = original
    return lineas


def revisar(nombre, valores, real, formula):
    fallos = [n for n in valores if real(n) != formula(n)]
    estado = "OK" if not fallos else f"FALLA en n = {fallos[:5]}"
    print(f"  {nombre:<32} {len(valores):>4} valores de n   {estado}")
    return not fallos


def main():
    pequenos = list(range(1, 201))
    del_lab = [1, 10, 100, 1000]
    todo_bien = all([
        revisar("Problema 1: counter", pequenos + del_lab, problema1.funcion, problema1.conteo_teorico),
        revisar("Problema 2: printf", pequenos + del_lab + [10000, 100000],
                lambda n: contar_impresiones(problema2, n), problema2.conteo_teorico),
        revisar("Problema 3: printf", pequenos + del_lab,
                lambda n: contar_impresiones(problema3, n), problema3.conteo_teorico),
        revisar("Problema 5c: elementos copiados", list(range(1, 61)),
                lambda n: sum(j - i for i in range(n) for j in range(i + 1, n)), elementos_copiados),
    ])
    print("\nTodas las formulas coinciden." if todo_bien else "\nHay diferencias, revisar.")


if __name__ == "__main__":
    main()
