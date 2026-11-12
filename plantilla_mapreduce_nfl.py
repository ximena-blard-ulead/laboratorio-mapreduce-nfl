import csv
import os
import multiprocessing
from itertools import chain, groupby
from datetime import datetime #para la comparación

# ==========================================
# 1. FASE MAP (Filtrado y Extracción)
# ==========================================
def mapper(ruta_archivo):
    """
    Entrada: Ruta del archivo CSV.
    Salida: Lista de tuplas (Clave, Valor).
    Regla: Usar filter() y map(). Evitar bucles for mutables.
    """
    print(f"   [Mapper PID {os.getpid()}] Extrayendo TD de: {ruta_archivo}")
    
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # TODO 1: Filtrar jugadas con touchdown
        jugadas_td = filter(
            lambda fila: fila.get('touchdown') == '1' and fila.get('posteam'),
            reader
        )

        # TODO 2: Transformar jugadas en tuplas
        tuplas_mapeadas = map(
            lambda fila: (
                f"{fila['home_team']}_vs_{fila['away_team']}_{fila['game_date']}",
                f"Equipo: {fila['posteam']} | Serie {fila['drive']}: {fila['desc']}"
            ),
            jugadas_td
        )
        
        # TODO 3: Retornar list(tuplas_mapeadas)
        return list(tuplas_mapeadas)

# ==========================================
# 2. FASE SHUFFLE & SORT (Preparación pura)
# ==========================================
def shuffle_and_sort(resultados_mappers):
    """
    Entrada: Lista de listas con tuplas. Ej: [[(KC, Serie1), (DET, Serie2)], [(KC, Serie3)]]
    Salida: Lista de tuplas agrupadas. Ej: [(KC, [Serie1, Serie3]), (DET, [Serie2])]
    """
    # TODO 1:Aplanar resultados
    lista_plana = chain.from_iterable(resultados_mappers)

    # TODO 2:Ordenar por clave
    lista_ordenada = sorted(lista_plana, key=lambda item: item[0])

    # TODO 3: Agrupar por partido
    datos_agrupados = [
        (clave, [v[1] for v in grupo])
        for clave, grupo in groupby(lista_ordenada, key=lambda item: item[0])
    ]

    return datos_agrupados

# ==========================================
# 3. FASE REDUCE (Agregación matemática)
# ==========================================
def reducer(item_agrupado):
    """
    Entrada: Tupla con Clave (Partido) y Lista de Series. Ej: ('PHI_vs_DAL_2000-10-01', ['Serie 1...', 'Serie 4...'])
    Salida: Tupla con Partido y Resumen. Adicionalmente, escribe un archivo de texto.
    """
    nombre_archivo, lista_series = item_agrupado #desempaquetamiento de tuplas
    
    # TODO 1: Crea la ruta del archivo uniendo la carpeta "resultados_series" y f"{nombre_archivo}.txt" usando os.path.join
    ruta_archivo = os.path.join(
        "resultados_series", 
        f"{nombre_archivo}.txt"
    )
    
    # TODO 2: Abre el archivo en modo escritura ('w') usando la estructura `with open(...)`
    with open(ruta_archivo, 'w', encoding='utf-8') as f:

        # TODO 3: Escribe todas las jugadas de `lista_series` dentro del archivo
        for serie in lista_series:
            f.write(f"- {serie}\n")

    # TODO 4: Retorna una tupla resumen para el orquestador: (nombre_archivo, {"total_td": len(lista_series), "archivo": ruta_archivo})
    resumen = {
        "total_td": len(lista_series),
        "archivo": ruta_archivo
    }

    return (nombre_archivo, resumen)

# ==========================================
# ORQUESTADOR (Framework) - NO MODIFICAR
# ==========================================
def ejecutar_motor():
    archivos = [f"play_by_play_{year}.csv" for year in range(1999, 2004)]
    archivos_disponibles = [f for f in archivos if os.path.exists(f)]
    
    # Contingencia: Usar el archivo de muestra si no están los datasets completos
    if not archivos_disponibles and os.path.exists("play_by_play_2000-sample_2.csv"):
        archivos_disponibles = ["play_by_play_2000-sample_2.csv"]
        
    if not archivos_disponibles:
        print("[!] Error: No se encontraron los archivos CSV para procesar.")
        return

    # Crear directorio de salida para los archivos de las series
    os.makedirs("resultados_series", exist_ok=True)

    num_nucleos = multiprocessing.cpu_count()
    print(f"\n[*] Iniciando MapReduce Funcional ({num_nucleos} núcleos)...")

    # Usamos map nativo del Pool de Multiprocessing para paralelizar puramente
    with multiprocessing.Pool(processes=num_nucleos) as pool:
        
        print("\n>> 1. Ejecutando Fase MAP...")
        # Paraleliza la ejecución del mapper
        resultados_map = pool.map(mapper, archivos_disponibles)
        
        print("\n>> 2. Ejecutando Fase SHUFFLE...")
        # Se ejecuta secuencialmente en el nodo maestro
        datos_agrupados = shuffle_and_sort(resultados_map)
        
        print("\n>> 3. Ejecutando Fase REDUCE...")
        # Paraleliza la ejecución del reducer
        resultados_finales = pool.map(reducer, datos_agrupados)

    # Ordenar y mostrar resultados
    print("\n" + "="*50)
    print(" RESULTADOS: ARCHIVOS GENERADOS ")
    print("="*50)
    
    # Ordenamos por cantidad de TD descendente
    resultados_finales.sort(key=lambda x: x[1]['total_td'], reverse=True)
    
    for partido, info in resultados_finales:
        print(f"🏈 {partido}: {info['total_td']} Series registradas en '{info['archivo']}'")

if __name__ == '__main__':
    inicio = datetime.now()

    ejecutar_motor()

    fin = datetime.now()

    tiempo_total = fin - inicio

    print(f"\n Tiempo de ejecución: {tiempo_total.total_seconds():.4f} segundos")