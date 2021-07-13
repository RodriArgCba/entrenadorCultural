import copy

from model.captura import Captura
from model.fase import Fase
from model.interpretacion import Interpretacion


class LineaResultado(object):
    def __init__(self, fase=None, captura=None, interpretacion=None):
        self.fase = fase
        self.captura = captura
        self.interpretacion = interpretacion

    def _set_captura(self, value: Captura):
        if isinstance(value, Captura) or (value is None):
            self.__captura = value
        else:
            raise Exception("El elemento no es una Captura")

    def _get_captura(self):
        return copy.deepcopy(self.__captura)

    def _set_fase(self, value: Fase):
        if isinstance(value, Fase) or (value is None):
            self.__fase = value
        else:
            raise Exception("El elemento no es una Fase")

    def _get_fase(self):
        return copy.deepcopy(self.__fase)

    def _set_interpretacion(self, value: Interpretacion):
        if isinstance(value, Interpretacion) or (value is None):
            self.__interpretacion = value
        else:
            raise Exception("El elemento no es una interpretacion")

    def _get_interpretacion(self):
        return copy.deepcopy(self.__interpretacion)

    fase = property(_get_fase, _set_fase)
    captura = property(_get_captura, _set_captura)
    interpretacion = property(_get_interpretacion, _set_interpretacion)

    def precisiondeusuario(self):
        return self.fase.capturaesperada.similitud(self.captura)