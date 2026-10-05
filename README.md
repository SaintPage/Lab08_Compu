Laboratorio 8 - Teoría de la Computación

Ángel Mérida - 23661

Video: [https://youtu.be/25fEHStRg-g]


Contenido

- `problema1.py`, `problema2.py`, `problema3.py`: los programas del enunciado traducidos a Python, con su fórmula exacta de operaciones.
- `perfilador.py`: profiling con cProfile, tabla y gráfica (módulo compartido por los problemas 1 a 3).
- `problema4.py`: cuenta comparaciones de búsqueda lineal, búsqueda binaria y Quicksort para comprobar el análisis.
- `problema5c.py`: mide el tiempo de A(n) del inciso 5c.
- `verificar.py`: comprueba que las fórmulas del análisis coinciden con lo que hacen los programas.
- `main.py`: corre todo lo anterior.
- `resultados/`: tablas (.csv y .md), gráficas (.png) y reportes de cProfile.
- `procedimiento/Laboratorio 8.pdf`: Procedimiento de los incisos.

Ejecución

Todo el laboratorio (tarda alrededor de un minuto):

    python main.py

Un problema a la vez:

    python problema1.py
    python problema2.py
    python problema3.py
    python problema4.py
    python problema5c.py
    python verificar.py

Ver la salida real de un programa con una n pequeña:

    python problema1.py --demo 10
    python problema2.py --demo 5
    python problema3.py --demo 10



Notas sobre el profiling

- Cada for de C se tradujo a un while con la misma condición e incremento, para que las vueltas sean exactamente las mismas.
- El tiempo se mide con cProfile. Para n pequeñas la función se llama varias veces y se promedia, porque una sola llamada dura microsegundos.
- El printf se manda a /dev/null para medir el algoritmo y no la velocidad de la terminal.
- Si una corrida tardaría más de 60 s, no se ejecuta: su tiempo se estima como operaciones exactas por costo por operación medido en la n más grande que sí corrió. En la tabla aparece como "estimado". El límite se cambia con `--limite`, por ejemplo `python main.py --limite 120`.
