"""
Modulo compartido de profiling para los problemas 1, 2 y 3.

Mide cada funcion con cProfile, arma la tabla n vs tiempo y dibuja la grafica.
Cuando una corrida tardaria mas que `limite` segundos, no se ejecuta: su tiempo
se estima con el costo por operacion medido en la n mas grande que si corrio.
"""

import cProfile
import csv
import io
import math
import os
import pstats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

VALORES_N = [1, 10, 100, 1000, 10000, 100000, 1000000]
LIMITE_DEFAULT = 60.0          # segundos maximos por corrida
TIEMPO_MINIMO = 0.05           # para n pequenas se repite hasta juntar al menos esto

CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")

# Colores (paleta validada: azul = medido, naranja = estimado, gris = modelo)
AZUL = "#2a78d6"
NARANJA = "#eb6834"
GRIS = "#8a8983"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
FONDO = "#fcfcfb"


def medir(funcion, n, repeticiones=1):
    """Ejecuta funcion(n) bajo cProfile y devuelve (segundos por llamada, perfil)."""
    perfil = cProfile.Profile(builtins=False)
    perfil.enable()
    for _ in range(repeticiones):
        funcion(n)
    perfil.disable()

    estadisticas = pstats.Stats(perfil)
    for (archivo, linea, nombre), datos in estadisticas.stats.items():
        if nombre == funcion.__name__:
            llamadas, tiempo_acumulado = datos[1], datos[3]
            return tiempo_acumulado / llamadas, perfil
    raise RuntimeError("cProfile no registro la funcion " + funcion.__name__)


def medir_estable(funcion, n):
    """Para n pequenas una sola llamada dura microsegundos: se repite y se promedia."""
    t, perfil = medir(funcion, n)
    if t < TIEMPO_MINIMO:
        repeticiones = min(1000, math.ceil(TIEMPO_MINIMO / max(t, 1e-7)))
        t, perfil = medir(funcion, n, repeticiones)
    return t, perfil


def perfilar(funcion, conteo, limite=LIMITE_DEFAULT, valores_n=VALORES_N):
    """
    conteo(n) = numero exacto de veces que se ejecuta la operacion basica.
    Devuelve filas (n, operaciones, segundos, tipo) y el perfil de la n mas grande medida.
    """
    filas = []
    costo_por_operacion = None
    ultimo_perfil = None

    for n in valores_n:
        operaciones = conteo(n)
        prediccion = None
        if costo_por_operacion is not None:
            prediccion = costo_por_operacion * operaciones

        if prediccion is not None and prediccion > limite:
            filas.append((n, operaciones, prediccion, "estimado"))
            print(f"  n = {n:>9,}  estimado  {formato_tiempo(prediccion)}  (supera el limite de {limite:g} s)")
            continue

        t, ultimo_perfil = medir_estable(funcion, n)
        filas.append((n, operaciones, t, "medido"))
        if operaciones > 0:
            costo_por_operacion = t / operaciones
        print(f"  n = {n:>9,}  medido    {formato_tiempo(t)}")

    return filas, ultimo_perfil


def formato_tiempo(segundos):
    if segundos < 1e-3:
        return f"{segundos * 1e6:10.2f} us "
    if segundos < 1:
        return f"{segundos * 1e3:10.2f} ms "
    if segundos < 60:
        return f"{segundos:10.2f} s  "
    if segundos < 3600:
        return f"{segundos / 60:10.2f} min"
    if segundos < 86400:
        return f"{segundos / 3600:10.2f} h  "
    return f"{segundos / 86400:10.2f} d  "


def imprimir_tabla(nombre, filas):
    print(f"\n{nombre}")
    print(f"  {'n':>9} | {'operaciones':>19} | {'tiempo':>14} | tipo")
    print("  " + "-" * 60)
    for n, operaciones, t, tipo in filas:
        print(f"  {n:>9,} | {operaciones:>19,} | {formato_tiempo(t)} | {tipo}")


def guardar_tabla(clave, filas):
    os.makedirs(CARPETA, exist_ok=True)
    ruta_csv = os.path.join(CARPETA, f"{clave}_tabla.csv")
    with open(ruta_csv, "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["n", "operaciones", "segundos", "tipo"])
        for n, operaciones, t, tipo in filas:
            escritor.writerow([n, operaciones, f"{t:.6e}", tipo])

    ruta_md = os.path.join(CARPETA, f"{clave}_tabla.md")
    with open(ruta_md, "w") as archivo:
        archivo.write("| n | operaciones | tiempo | tipo |\n|---:|---:|---:|---|\n")
        for n, operaciones, t, tipo in filas:
            archivo.write(f"| {n:,} | {operaciones:,} | {formato_tiempo(t).strip()} | {tipo} |\n")
    return ruta_csv


def guardar_perfil(clave, perfil):
    """Guarda el reporte de cProfile de la n mas grande que se midio."""
    if perfil is None:
        return
    salida = io.StringIO()
    pstats.Stats(perfil, stream=salida).sort_stats("cumulative").print_stats(8)
    with open(os.path.join(CARPETA, f"{clave}_cprofile.txt"), "w") as archivo:
        archivo.write(salida.getvalue())


def graficar(clave, titulo, filas, modelo, etiqueta_modelo):
    """
    Izquierda: n vs tiempo en escala log-log, con todas las n (medidas y estimadas).
    Derecha: tiempo / operaciones, para ver que el costo por operacion basica es constante.
    modelo(n) es la funcion de la cota (n**2, n, ...), escalada al punto medido mas grande.
    """
    medidos = [(n, t) for n, _, t, tipo in filas if tipo == "medido"]
    estimados = [(n, t) for n, _, t, tipo in filas if tipo == "estimado"]
    por_operacion = [(n, t / ops * 1e9) for n, ops, t, tipo in filas if tipo == "medido" and ops > 0]

    n_ref, t_ref = max(medidos)
    escala = t_ref / modelo(n_ref)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    figura, (izq, der) = plt.subplots(1, 2, figsize=(12, 4.8), facecolor=FONDO)

    xs = np.logspace(math.log10(2), math.log10(max(n for n, *_ in filas)), 300)
    izq.plot(xs, [escala * modelo(x) for x in xs], color=GRIS, linestyle=":", linewidth=2,
             label=f"modelo {etiqueta_modelo} (ajustado)", zorder=1)
    izq.plot(*zip(*medidos), color=AZUL, linewidth=2, marker="o", markersize=8,
             markeredgecolor=FONDO, markeredgewidth=2, label="medido (cProfile)", zorder=3)
    if estimados:
        puente = [medidos[-1]] + estimados
        izq.plot(*zip(*puente), color=NARANJA, linewidth=2, linestyle="--", zorder=2)
        izq.plot(*zip(*estimados), linestyle="none", marker="o", markersize=8,
                 markerfacecolor=FONDO, markeredgecolor=NARANJA, markeredgewidth=2,
                 label="estimado (no se ejecutó)", zorder=3)
    izq.set_xscale("log")
    izq.set_yscale("log")
    izq.set_ylabel("tiempo (s)", color=TINTA_2)
    izq.set_title("Tamaño del input vs tiempo (log-log)", color=TINTA)
    izq.legend(frameon=False, loc="upper left", labelcolor=TINTA_2)

    der.plot(*zip(*por_operacion), color=AZUL, linewidth=2, marker="o", markersize=8,
             markeredgecolor=FONDO, markeredgewidth=2, label="tiempo / operaciones", zorder=3)
    if estimados:
        costo = por_operacion[-1][1]
        der.axhline(costo, color=NARANJA, linestyle="--", linewidth=2, zorder=2,
                    label=f"costo usado para estimar ({costo:.1f} ns)")
    der.set_xscale("log")
    der.set_ylim(0, max(v for _, v in por_operacion) * 1.25)
    der.set_ylabel("nanosegundos por operación", color=TINTA_2)
    der.set_title("Costo por operación básica", color=TINTA)
    der.legend(frameon=False, loc="upper right", labelcolor=TINTA_2)

    for eje in (izq, der):
        eje.set_facecolor(FONDO)
        eje.set_xlabel("tamaño del input n", color=TINTA_2)
        eje.grid(True, which="major", color="#e4e3df", linewidth=0.8)
        eje.tick_params(colors=TINTA_2)
        for lado in ("top", "right"):
            eje.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            eje.spines[lado].set_color("#c9c8c3")

    figura.suptitle(titulo, color=TINTA, fontsize=13)
    figura.tight_layout()
    ruta = os.path.join(CARPETA, f"{clave}_grafica.png")
    figura.savefig(ruta, dpi=150, facecolor=FONDO)
    plt.close(figura)
    return ruta


def ejecutar(clave, titulo, funcion, conteo, modelo, etiqueta_modelo, limite=LIMITE_DEFAULT):
    print(f"\n{titulo}  (limite por corrida: {limite:g} s)")
    filas, perfil = perfilar(funcion, conteo, limite)
    imprimir_tabla(titulo, filas)
    guardar_tabla(clave, filas)
    guardar_perfil(clave, perfil)
    ruta = graficar(clave, titulo, filas, modelo, etiqueta_modelo)
    print(f"  tabla y grafica guardadas en resultados/ ({os.path.basename(ruta)})")
    return filas


def leer_limite(argumentos):
    """Permite: python problemaX.py --limite 30"""
    if "--limite" in argumentos:
        return float(argumentos[argumentos.index("--limite") + 1])
    return LIMITE_DEFAULT
