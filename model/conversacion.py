import string

from model.culturaobjetivo import CulturaObjetivo
from model.fase import Fase
import copy


class Conversacion(object):
    def __init__(self, nombre='', descripcion='', duracion=0.0, culturaobjetivo=None, ubicacionmp3=''):
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion = duracion
        self.ubicacionmp3 = ubicacionmp3
        self.__fases = []
        if (culturaobjetivo is None) or isinstance(culturaobjetivo,CulturaObjetivo):
            self.__culturaobjetivo = culturaobjetivo
        else:
            raise Exception("El elemento no es una CulturaObjetivo")

    def _get_nombre(self):
        return self.__nombre

    def _set_nombre(self, value):
        if not isinstance(value, string):
            raise TypeError("nombre debe ser un string")
        self.__nombre = value

    def _get_descripcion(self):
        return self.__descripcion

    def _set_descripcion(self, value):
        if not isinstance(value, string):
            raise TypeError("nombre debe ser un string")
        self.__descripcion = value

    def _get_duracion(self):
        return self.__duracion

    def _set_duracion(self, value):
        if not isinstance(value, float):
            raise TypeError("duracion debe ser un numero con punto flotante")
        self.__duracion = value

    def _get_ubicacionmp3(self):
        return self.__ubicacionmp3

    def _set_ubicacionmp3(self, value):
        if not isinstance(value, string):
            raise TypeError("ubicacionmp3 debe ser un string")
        self.__ubicacionmp3 = value

    def _get_fases(self):
        return copy.deepcopy(self.__fases)

    def _set_fases(self, fases):
        if isinstance(fases, list):
            for x in fases:
                self._set_fases(x)
        elif isinstance(fases, Fase):
            self.__fases.append(fases)
        else:
            raise Exception("El elemento no es una Fase")

    def _get_culturaobjetivo(self):
        return copy.deepcopy(self.__culturaobjetivo)

    def _set_culturaobjetivo(self, value):
        if isinstance(value, CulturaObjetivo):
            self.__fases.append(value)
        else:
            raise Exception("El elemento no es una CulturaObjetivo")

    nombre = property(_get_nombre, _set_nombre)
    descripcion = property(_get_nombre, _set_nombre)
    duracion = property(_get_duracion, _set_duracion)
    ubicacionmp3 = property(_get_ubicacionmp3, _set_ubicacionmp3)
    culturaobjetivo = property(_get_culturaobjetivo, _set_culturaobjetivo)
    fases = property(_get_fases, _set_fases)
