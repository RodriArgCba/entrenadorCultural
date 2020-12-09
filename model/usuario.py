import copy

from model.simulacion import Simulacion


class Usuario(object):
    def __init__(self, nrodeempleado=0, nombre='', email='', administrador=False):
        self.nrodeempleado = nrodeempleado
        self.nombre = nombre
        self.email = email
        self.administrador = administrador
        self.__historial = []
        
    def _get_nrodeempleado(self):
        return self.__nrodeempleado

    def _set_nrodeempleado(self, value):
        if not isinstance(value, int):
            raise TypeError("nrodeempleado debe ser un int")
        self.__nrodeempleado = value
        
    def _get_nombre(self):
        return self.__nombre

    def _set_nombre(self, value):
        if not isinstance(value, str):
            raise TypeError("nombre debe ser un string")
        self.__nombre = value
        
    def _get_email(self):
        return self.__email

    def _set_email(self, value):
        if not isinstance(value, str):
            raise TypeError("email debe ser un string")
        self.__email = value
        
    def _get_administrador(self):
        return self.__administrador

    def _set_administrador(self, value):
        if not isinstance(value, bool):
            raise TypeError("administrador debe ser un booleano")
        self.__administrador = value

    def _get_historial(self):
        return copy.deepcopy(self.__historial)
    
    def _set_historial(self, historial):
        if isinstance(historial, list):
            for x in historial:
                self._set_historial(x)
        elif isinstance(historial, Simulacion):
            self.__historial.append(historial)
        else:
            raise Exception("El elemento no es una Simulacion")

    nombre = property(_get_nombre, _set_nombre)
    email = property(_get_email, _set_email)
    nrodeempleado = property(_get_nrodeempleado, _set_nrodeempleado)
    administrador = property(_get_administrador, _set_administrador)
    historial = property(_get_historial, _set_historial)