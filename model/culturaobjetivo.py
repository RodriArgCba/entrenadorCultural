from model.interpretacion import Interpretacion
from model.captura import Captura
import copy


class CulturaObjetivo(object):
    def __init__(self, nombre='', descripcion=''):
        self.nombre = nombre
        self.descripcion = descripcion
        self.__interpretaciones = []

    def _get_nombre(self):
        return self.__nombre

    def _set_nombre(self, value):
        if not isinstance(value, str):
            raise TypeError("nombre debe ser un string")
        self.__nombre = value

    def _get_descripcion(self):
        return self.__descripcion

    def _set_descripcion(self, value):
        if not isinstance(value, str):
            raise TypeError("descripcion debe ser un string")
        self.__descripcion = value

    def _get_interpretaciones(self):
        return copy.deepcopy(self.__interpretaciones)

    def _set_interpretaciones(self, interpretaciones):
        if isinstance(interpretaciones, list):
            for x in interpretaciones:
                self._set_interpretaciones(x)
        elif isinstance(interpretaciones, Interpretacion):
            self.__interpretaciones.append(interpretaciones)
        else:
            raise Exception("El elemento no es una interpretación")

    nombre = property(_get_nombre, _set_nombre)
    descripcion = property(_get_descripcion, _set_descripcion)
    interpretaciones = property(_get_interpretaciones, _set_interpretaciones)

    def interpretar(self,captura):
        for interpretacion in self.interpretaciones:
            if interpretacion.captura.comparar(captura):
                return interpretacion
        capturavacia = Captura()
        capturavacia.id = 0
        interpretacion = Interpretacion("ERROR", "No se pudo interpretar", capturavacia)
        interpretacion.id = 0
        return interpretacion
