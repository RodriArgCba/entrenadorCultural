import copy
from datetime import datetime

from model.conversacion import Conversacion
from model.linearesultado import LineaResultado


class Simulacion(object):
    def __init__(self, fecha=datetime.now(), conversacion=None, calificaciondeusuario=0):
        self.fecha = fecha
        self.conversacion = conversacion
        self.__resultados = []
        self.calificaciondeusuario = calificaciondeusuario

    def _get_fecha(self):
        return self.__fecha

    def _set_fecha(self, value):
        if not isinstance(value, datetime):
            raise TypeError("fecha debe ser un datetime")
        self.__fecha = value

    def _get_conversacion(self):
        return self.__conversacion

    def _set_conversacion(self, value):
        if (not isinstance(value, Conversacion)) or (not (value is None)):
            raise TypeError("conversacion debe ser una Conversacion")
        self.__conversacion = value

    def _get_calificaciondeusuario(self):
        return self.__calificaciondeusuario

    def _set_calificaciondeusuario(self, value):
        if not isinstance(value, int):
            raise TypeError("calificacion debe ser un int")
        elif value > 1 or value < 0:
            raise TypeError("calificacion debe ser un int entre 0 y 1")
        self.__calificaciondeusuario= value

    def _get_resultados(self):
        return copy.deepcopy(self.__resultados)

    def _set_resultados(self, resultados):
        if isinstance(resultados, list):
            for x in resultados:
                self._set_resultados(x)
        elif isinstance(resultados, LineaResultado):
            self.__resultados.append(resultados)
        else:
            raise Exception("El elemento no es un Resultado")

    resultados = property(_get_resultados,_set_resultados)
    calificaciondeusuario = property(_get_calificaciondeusuario,_set_calificaciondeusuario)
    conversacion = property(_get_conversacion,_set_conversacion)
    fecha = property(_get_fecha,_set_fecha)