# entrenadorCultural
Sistema de entrenamiento intérprete de comunicación no vebal

Este prototipo fue desarrollado como poryecto de mi Tesis de Ingeniería en Software.

Los empleados de la empresa multinacional CNH Industrial, deben comunicarse y trabajar constantemente con clientes de otros países y culturas. Esta situación acarrea contratiempos y malentendidos, generados por las diferencias culturales, que debilitan los resultados de dichas interacciones. De aquí en adelante, utilizamos el término choque cultural para referirnos a este fenómeno.
El objetivo de este trabajo fue desarrollar e implementar un sistema de entrenamiento cultural que ataque esta problemática. Esta aplicación interpreta las señales de comunicación no verbal que los empleados emiten durante la conversación, permitiéndoles obtener retroalimentación de su accionar con respecto a los códigos del lenguaje de la cultura en la que se evalúa dicha interacción. Se diseñó y desarrolló utilizando la metodología de desarrollo ágil Scrum y lenguaje Python. El sistema utiliza sensores de video, sonido, movimiento ocular, posición de cabeza y manos.

Palabras claves: comunicación no verbal, aprendizaje cultural, inteligencia artificial,  visión de computadora, comunicación intercultural


Instrucciones para modificar el proyecto:

1) Es necesario Python 3.7.9 para correr el proyecto, se recomienda crear un entorno virtual
2) Correr "pip install -r [Directorio del proyecto]/requirements.txt" para realizar la instalación en el entorno virtual de las librerias necesarias
3) Instalar PyAudio manualmente corriendo "pip install [Directorio del proyecto]/assets/PyAudio-0.2.11-cp37-cp37m-win_amd64.whl"
4) Ejecutar el código sql [Directorio del proyecto]/controller/dbinit.sql sobre [Directorio del proyecto]/sqlitedb.db para cargar los datos iniciales
