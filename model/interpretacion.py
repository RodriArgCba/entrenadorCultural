import copy

from model.captura import Captura


class Interpretacion(object):
    def __init__(self, lectura='', masinfo='', captura=None):
        self.lectura = lectura
        self.masInfo = masinfo
        self.captura = captura

    def _get_lectura(self):
        return self.__lectura

    def _set_lectura(self, value):
        if not isinstance(value, str):
            raise TypeError("lectura debe ser un string")
        self.__lectura = value

    def _set_masinfo(self, value):
        if not isinstance(value, str):
            raise TypeError("masinfo debe ser un string")
        self.__masinfo = value

    def _get_masinfo(self):
        return self.__masinfo

    def _set_captura(self, value: Captura):
        if isinstance(value, Captura) or (value is None):
            self.__captura = value
        else:
            raise Exception("El elemento no es una Captura")

    def _get_captura(self):
        return copy.deepcopy(self.__captura)

    lectura = property(_get_lectura, _set_lectura)
    masinfo = property(_get_masinfo, _set_masinfo)
    captura = property(_get_captura, _set_captura)
