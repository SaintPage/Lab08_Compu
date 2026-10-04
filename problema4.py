"""
Problema 4 (verificacion empirica, el analisis esta en respuestas/).
Cuenta comparaciones de Busqueda Lineal, Busqueda Binaria y Quicksort y las
compara con las formulas de mejor, promedio y peor caso.
"""

import math
import os
import random
import sys


def busqueda_lineal(arreglo, objetivo):
    comparaciones = 0
    for i in range(len(arreglo)):
        comparaciones += 1
        if arreglo[i] == objetivo:
            return i, comparaciones
    return -1, comparaciones


def busqueda_binaria(arreglo, objetivo):
    """Cada vuelta del while cuenta como una comparacion (de tres vias) contra arreglo[medio]."""
    comparaciones = 0
    bajo, alto = 0, len(arreglo) - 1
    while bajo <= alto:
        medio = (bajo + alto) // 2
        comparaciones += 1
        if arreglo[medio] == objetivo:
            return medio, comparaciones
        if arreglo[medio] < objetivo:
            bajo = medio + 1
        else:
            alto = medio - 1
    return -1, comparaciones


def quicksort(arreglo):
    """Quicksort con particion de Lomuto (pivote = ultimo). Devuelve comparaciones."""
    a = list(arreglo)
    comparaciones = 0
    pila = [(0, len(a) - 1)]          # iterativo para no chocar con el limite de recursion
    while pila:
        bajo, alto = pila.pop()
        if bajo >= alto:
            continue
        pivote = a[alto]
        i = bajo - 1
        for j in range(bajo, alto):
            comparaciones += 1
            if a[j] <= pivote:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[alto] = a[alto], a[i + 1]
        pila.append((bajo, i))
        pila.append((i + 2, alto))
    return comparaciones


def armonico(n):
    return sum(1 / k for k in range(1, n + 1))


def quicksort_mejor_teorico(n):
    """C(n) = C(piso((n-1)/2)) + C(techo((n-1)/2)) + (n - 1): pivote siempre en la mitad."""
    memo = {0: 0, 1: 0}
    def c(m):
        if m not in memo:
            memo[m] = c((m - 1) // 2) + c(m // 2) + (m - 1)
        return memo[m]
    return c(n)


def main():
    random.seed(8)
    lineas = []

    def escribir(texto=""):
        print(texto)
        lineas.append(texto)

    escribir("Busqueda lineal (comparaciones)")
    escribir(f"  {'n':>6} | {'mejor':>6} | {'promedio medido':>15} | {'(n+1)/2':>8} | {'peor':>6}")
    for n in (10, 100, 1000):
        arreglo = list(range(n))
        mejor = busqueda_lineal(arreglo, 0)[1]
        promedio = sum(busqueda_lineal(arreglo, x)[1] for x in arreglo) / n
        peor = busqueda_lineal(arreglo, -1)[1]
        escribir(f"  {n:>6} | {mejor:>6} | {promedio:>15.2f} | {(n + 1) / 2:>8.2f} | {peor:>6}")

    escribir()
    escribir("Busqueda binaria (comparaciones)")
    escribir(f"  {'n':>6} | {'mejor':>6} | {'promedio medido':>15} | {'formula':>8} | {'peor':>6} | {'piso(log2 n)+1':>14}")
    for k in (4, 7, 10, 14):
        n = 2 ** k - 1                # arbol de decision completo
        arreglo = list(range(n))
        mejor = busqueda_binaria(arreglo, arreglo[(n - 1) // 2])[1]
        conteos = [busqueda_binaria(arreglo, x)[1] for x in arreglo]
        conteos.append(busqueda_binaria(arreglo, n + 5)[1])
        promedio = sum(conteos[:-1]) / n
        formula = ((k - 1) * 2 ** k + 1) / n
        escribir(f"  {n:>6} | {mejor:>6} | {promedio:>15.3f} | {formula:>8.3f} | {max(conteos):>6} | {int(math.log2(n)) + 1:>14}")

    escribir()
    escribir("Quicksort, pivote = ultimo elemento (comparaciones)")
    escribir(f"  {'n':>6} | {'mejor (recurrencia)':>19} | {'promedio medido':>15} | {'2(n+1)H_n-4n':>12} | {'peor medido':>11} | {'n(n-1)/2':>9}")
    for n in (10, 100, 1000):
        pruebas = 2000 if n <= 100 else 300
        promedio = sum(quicksort(random.sample(range(n), n)) for _ in range(pruebas)) / pruebas
        formula = 2 * (n + 1) * armonico(n) - 4 * n
        peor = quicksort(list(range(n)))            # arreglo ya ordenado
        escribir(f"  {n:>6} | {quicksort_mejor_teorico(n):>19} | {promedio:>15.1f} | {formula:>12.1f} | {peor:>11} | {n * (n - 1) // 2:>9}")

    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    os.makedirs(carpeta, exist_ok=True)
    with open(os.path.join(carpeta, "problema4_verificacion.txt"), "w") as archivo:
        archivo.write("\n".join(lineas) + "\n")


if __name__ == "__main__":
    main()
