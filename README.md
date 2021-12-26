# entrenadorCultural
Sistema de entrenamiento intérprete de comunicación no vebal

Este prototipo fue desarrollado como poryecto de mi Tesis de Ingeniería en Software.

Los empleados de la empresa multinacional CNH Industrial, deben comunicarse y trabajar constantemente con clientes de otros países y culturas. Esta situación acarrea contratiempos y malentendidos, generados por las diferencias culturales, que debilitan los resultados de dichas interacciones. De aquí en adelante, utilizamos el término choque cultural para referirnos a este fenómeno.
El objetivo de este trabajo fue desarrollar e implementar un sistema de entrenamiento cultural que ataque esta problemática. Esta aplicación interpreta las señales de comunicación no verbal que los empleados emiten durante la conversación, permitiéndoles obtener retroalimentación de su accionar con respecto a los códigos del lenguaje de la cultura en la que se evalúa dicha interacción. Se diseñó y desarrolló utilizando la metodología de desarrollo ágil Scrum y lenguaje Python. El sistema utiliza sensores de video, sonido, movimiento ocular, posición de cabeza y manos.

Palabras claves: comunicación no verbal, aprendizaje cultural, inteligencia artificial,  visión de computadora, comunicación intercultural


Instrucciones para modificar el proyecto:

1) Es necesario Python 3.7.9 para correr el proyecto, se recomienda crear un entorno virtual
2) Descargar e instalar visual studio con Visual C++
3) Descargar e instalar CMake
4) Correr "pip install -r [Directorio del proyecto]/requirements.txt" para realizar la instalación de las dependencias
5) En caso de que surja un error con numpy, desinstalar el paquete con "pip uninstall numpy" y reinstalarlo con "pip install numpy"
6) Correr "garden install matplotlib"
7) Ejecutar el código sql [Directorio del proyecto]/controller/dbinit.sql sobre [Directorio del proyecto]/sqlitedb.db para inicializar la base de datos. Alternativamente puede hacer una copia del archivo "sqlitedb - estado inicial.db" y renombrarlo a "sqlitedb.db"
