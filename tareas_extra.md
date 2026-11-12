# Tareas extra — Laboratorio MapReduce

## 1. Librerías de Python

Conocía casi que todas, excepto la de multiprocessing.

**csv:** Permite leer y escribir archivos CSV.
**os:** Permite interactuar con el sistema operativo y trabajar con archivos y directorios.
**multiprocessing:** Permite ejecutar tareas en diferentes procesos y aprovechar varios núcleos del procesador. En el laboratorio utilizamos `multiprocessing.Pool()` para distribuir el trabajo entre procesos y `multiprocessing.cpu_count()` para conocer la cantidad de procesadores lógicos disponibles.
**itertools:** Contiene herramientas para trabajar con iteradores de manera eficiente.

## 2. Funciones/métodos de Python

**chain.from_iterable():** Permite unir varios iterables en una sola secuencia. En el laboratorio la utilizamos para aplanar las listas de resultados.
**sorted():** Ordena los elementos de un iterable según un criterio. La utilizamos para ordenar las tuplas por la clave del partido antes de agruparlas.
**groupby():** Agrupa elementos consecutivos que comparten una misma clave. La utilizamos para reunir todos los touchdowns correspondientes a un mismo partido.
**multiprocessing.Pool():** Crea un conjunto de procesos que pueden ejecutar tareas en paralelo. En el laboratorio permitió distribuir el procesamiento de los archivos CSV y la generación de resultados entre diferentes procesos.
**f.write():** Escribe texto dentro de un archivo abierto. La utilizamos en REDUCE para guardar los touchdowns de cada partido en su respectivo archivo `.txt`.

## 3. Hilos (threads) y candados de memoria (locks)

**Threads:** Son unidades de ejecución dentro de un proceso que permiten realizar varias tareas de manera concurrente. Los hilos de un mismo proceso comparten memoria, por lo que pueden existir conflictos cuando intentan modificar los mismos datos simultáneamente.

**Locks:** Son mecanismos de sincronización que controlan el acceso a recursos compartidos. Permiten evitar condiciones de carrera, que ocurren cuando varios hilos acceden o modifican información al mismo tiempo y el resultado depende del orden de ejecución.

**Diferencia en el laboratorio:** Al utilizar `multiprocessing.Pool()` y `pool.map()`, Python se encarga de distribuir las tareas entre diferentes procesos, sin necesidad de programar manualmente hilos o locks. A diferencia de los threads, los procesos tienen espacios de memoria independientes, lo que reduce los conflictos por memoria compartida. Esto permite concentrarnos en definir las operaciones de MAP y REDUCE, mientras que el framework administra la ejecución paralela.

## 4. Comparación de rendimiento: MapReduce vs. programación tradicional

### Resultados

| Implementación           | Tiempo de ejecución |
| ------------------------ | ------------------- |
| MapReduce                | 1.7572 segundos     |
| Programación tradicional | 4.1658 segundos     |

### Análisis

En la prueba realizada, MapReduce fue aproximadamente 2.37 veces más rápido que la programación tradicional, con una diferencia de 2.4086 segundos.

Esto puede explicarse porque MapReduce utiliza `multiprocessing.Pool()` para distribuir el procesamiento entre varios procesos, mientras que la implementación tradicional recorre los archivos de manera secuencial.

### Conclusión

En este laboratorio, MapReduce presentó un mejor rendimiento que la programación tradicional. El procesamiento paralelo permitió reducir el tiempo de ejecución al trabajar con los archivos CSV de la NFL.
