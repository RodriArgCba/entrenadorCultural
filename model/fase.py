import copy

from model.captura import Captura


class Fase(object):
    def __init__(self, nombre='', tema='', inicio=0.0, duracion=0.0, capturaesperada=None):
        self.nombre = nombre
        self.tema = tema
        self.inicio = inicio
        self.duracion = duracion
        self.capturaesperada = capturaesperada

    def _get_nombre(self):
        return self.__nombre

    def _set_nombre(self, value):
        if not isinstance(value, str):
            raise TypeError("nombre debe ser un string")
        self.__nombre = value

    def _get_tema(self):
        return self.__tema

    def _set_tema(self, value):
        if not isinstance(value, str):
            raise TypeError("nombre debe ser un string")
        self.__tema = value

    def _get_duracion(self):
        return self.__duracion

    def _set_duracion(self, value):
        if not isinstance(value, float):
            raise TypeError("duracion debe ser un numero con punto flotante")
        self.__duracion = value

    def _get_inicio(self):
        return self.__duracion

    def _set_inicio(self, value):
        if not isinstance(value, float):
            raise TypeError("inicio debe ser un numero con punto flotante")
        self.__inicio = value

    def _get_capturaesperada(self):
        return copy.deepcopy(self.__capturaesperada)

    def _set_capturaesperada(self, value: Captura):
        if isinstance(value, Captura) or (value is None):
            self.__capturaesperada = value
        else:
            raise Exception("El elemento no es una Captura")

    nombre = property(_get_nombre, _set_nombre)
    tema = property(_get_tema, _set_tema)
    duracion = property(_get_duracion, _set_duracion)
    inicio = property(_get_inicio, _set_inicio)
    capturaesperada = property(_get_capturaesperada, _set_capturaesperada)
