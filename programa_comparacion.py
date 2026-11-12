import csv
import os
from datetime import datetime

inicio = datetime.now()

annos = range(1999, 2004)

resultados = {}

for anno in annos:
    archivo = f"play_by_play_{anno}.csv"

    if not os.path.exists(archivo):
        continue

    print(f"Procesando: {archivo}")

    with open(archivo, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for fila in reader:
            if fila.get("touchdown") == "1" and fila.get("posteam"):
                nombre_partido = (
                    f"{fila['home_team']}_vs_"
                    f"{fila['away_team']}_{fila['game_date']}"
                )
                descripcion = (
                    f"Equipo: {fila['posteam']} | "
                    f"Serie {fila['drive']}: {fila['desc']}"
                )
                if nombre_partido not in resultados:
                    resultados[nombre_partido] = []

                resultados[nombre_partido].append(descripcion)

carpeta = "resultados_tradicional"
os.makedirs(carpeta, exist_ok=True)

for nombre_partido, lista_series in resultados.items():
    ruta_archivo = os.path.join(
        carpeta, f"{nombre_partido}.txt"
    )
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        for serie in lista_series:
            f.write(f"- {serie}\n")


fin = datetime.now()

tiempo_total = fin - inicio

print("\n---RESULTADOS DEL PROCESAMIENTO TRADICIONAL---")
print(f"Total de partidos procesados: {len(resultados)}")
print(f"Tiempo de ejecucion: {tiempo_total.total_seconds():.4f} segundos")
