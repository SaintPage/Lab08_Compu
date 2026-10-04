"""
Problema 5c: se mide A(n) para ver si su tiempo crece como n^2 o como n^3.
Si fuera Theta(n^2), al duplicar n el tiempo se multiplicaria por ~4; si es Theta(n^3), por ~8.
"""

import gc
import math
import os
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import perfilador as p


def A(n):
    atupla = tuple(range(0, n))
    S = set()
    for i in range(0, n):
        for j in range(i + 1, n):
            S.add(atupla[i:j])


def elementos_copiados(n):
    """Suma de (j - i) sobre todos los pares i < j = (n^3 - n) / 6."""
    return (n ** 3 - n) // 6


def main():
    valores = [25, 50, 100, 200, 400]     # n mas grandes necesitan varios GB de RAM (el set guarda Theta(n^3) referencias)
    tiempos = []
    print(f"  {'n':>5} | {'llamadas a add':>14} | {'elementos copiados':>18} | {'tiempo':>14} | t(n)/t(n/2)")
    for n in valores:
        mejor = math.inf
        for _ in range(15):             # se toma la mejor de 15 corridas, sin el recolector de basura
            gc.disable()
            inicio = time.perf_counter()
            A(n)
            mejor = min(mejor, time.perf_counter() - inicio)
            gc.enable()
        tiempos.append(mejor)
        razon = f"{mejor / tiempos[-2]:.2f}" if len(tiempos) > 1 else "-"
        print(f"  {n:>5} | {n * (n - 1) // 2:>14,} | {elementos_copiados(n):>18,} | {p.formato_tiempo(mejor)} | {razon}")

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    figura, eje = plt.subplots(figsize=(7, 4.6), facecolor=p.FONDO)
    n_ref, t_ref = valores[-1], tiempos[-1]
    eje.plot(valores, [t_ref * (n / n_ref) ** 2 for n in valores], color=p.GRIS, linestyle=":",
             linewidth=2, label="pendiente de n² (lo que diria el enunciado)")
    eje.plot(valores, [t_ref * (n / n_ref) ** 3 for n in valores], color=p.NARANJA, linestyle="--",
             linewidth=2, label="pendiente de n³")
    eje.plot(valores, tiempos, color=p.AZUL, linewidth=2, marker="o", markersize=8,
             markeredgecolor=p.FONDO, markeredgewidth=2, label="A(n) medido")
    eje.set_xscale("log")
    eje.set_yscale("log")
    eje.set_xticks(valores)
    eje.set_xticklabels([str(v) for v in valores])
    eje.minorticks_off()
    eje.set_facecolor(p.FONDO)
    eje.set_xlabel("tamaño del input n", color=p.TINTA_2)
    eje.set_ylabel("tiempo (s)", color=p.TINTA_2)
    eje.set_title("Problema 5c: tiempo de A(n)", color=p.TINTA)
    eje.grid(True, which="major", color="#e4e3df", linewidth=0.8)
    eje.tick_params(colors=p.TINTA_2)
    for lado in ("top", "right"):
        eje.spines[lado].set_visible(False)
    eje.legend(frameon=False, loc="upper left", labelcolor=p.TINTA_2)
    figura.tight_layout()
    os.makedirs(p.CARPETA, exist_ok=True)
    with open(os.path.join(p.CARPETA, "problema5c_tabla.csv"), "w") as archivo:
        archivo.write("n,llamadas_add,elementos_copiados,segundos\n")
        for n, t in zip(valores, tiempos):
            archivo.write(f"{n},{n * (n - 1) // 2},{elementos_copiados(n)},{t:.6e}\n")
    figura.savefig(os.path.join(p.CARPETA, "problema5c_grafica.png"), dpi=150, facecolor=p.FONDO)
    plt.close(figura)
    print("  grafica guardada en resultados/problema5c_grafica.png")


if __name__ == "__main__":
    main()
