# Practica 2: Puente de Ambite

Autor: Abdelaziz el Kadi Lachehab

Asignatura: PRPA

El problema consiste en sincronizar el uso del puente por parte de: coches dirección sur, coches dirección norte y peatones. Donde son excluyentes los coches en direcciones contrarias y los peatones, puesto que es un puente estrecho de una sola dirección (los peatones si pueden ir en direcciones contrarias).

Primero se propone una solución segura (fichero `solucion_segura.py`), luego esta se mejora llegando a una solución segura y sin inanición ( fichero `solucion_sin_inanicion.py`). La demostración de estas propiedades viene dada en el fichero `practica_2_cuestiones.txt`.

### Ejecutar solución

Para ejecutar y probar una solución debemos:

1. Dirigirnos a la directorio donde se encuentre el fichero de python que deseamos probar.

2. Abrir el fichero y modificar las variables globales (como el número de peatones, delay para generar un coche...) a nuestro gusto. (No modificar si queremos dejar valores por defecto)

3. Ejecutamos el fichero de la solución a probar. Por ejemplo: `python solucion_sin_inanicion.py`

4. Durante la ejecución podemos ver por pantalla los logs, indicando cuando ha entrado un coche en el puente, cuando ha salido un peaton... Podemos usar estos logs para comprobar que el algoritmo funciona correctamente.

4. Cuando observemos por pantalla la señal `FIN` significa que la ejecución ya ha acabado y que todos los procesos han finalizado.
