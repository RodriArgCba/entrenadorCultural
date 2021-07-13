from model.direccionmirada import DireccionMirada
from model.movimientocabeza import MovimientoCabeza
from model.posicionbrazos import PosicionBrazos
from model.rostro import Rostro


class Captura(object):
    def __init__(
            self,
            volumendevoz=0.0,
            palabrasporsegundo=0.0,
            posicionbrazos=PosicionBrazos.NOAPLICA,
            mirada=DireccionMirada.NOAPLICA,
            rostro=Rostro.NOAPLICA,
            cabeza=MovimientoCabeza.NOAPLICA
    ):
        self.volumendevoz = volumendevoz
        self.palabrasporsegundo = palabrasporsegundo
        self.posicionbrazos = posicionbrazos
        self.mirada = mirada
        self.rostro = rostro
        self.cabeza = cabeza

    def _get_volumendevoz(self):
        return self.__volumendevoz

    def _set_volumendevoz(self, value):
        if not isinstance(value, float):
            raise TypeError("volumendevoz debe ser un punto flotante")
        self.__volumendevoz = value

    def _get_palabrasporsegundo(self):
        return self.__palabrasporsegundo

    def _set_palabrasporsegundo(self, value):
        if not isinstance(value, float):
            raise TypeError("palabrasporsegundo debe ser un string")
        self.__palabrasporsegundo = value

    def _get_posicionbrazos(self):
        return self.__posicionbrazos

    def _set_posicionbrazos(self, value):
        if isinstance(value, PosicionBrazos):
            self.__posicionbrazos = value
        else:
            raise TypeError("posicionbrazos debe ser miembro del enum PosicionBrrazos")

    def _get_mirada(self):
        return self.__mirada

    def _set_mirada(self, value):
        if isinstance(value, DireccionMirada):
            self.__mirada = value
        else:
            raise TypeError("mirada debe ser miembro del enum DireccionMirada")

    def _get_rostro(self):
        return self.__rostro

    def _set_rostro(self, value):
        if isinstance(value, Rostro):
            self.__rostro = value
        else:
            raise TypeError("rostro debe ser miembro del enum Rostro")

    def _get_cabeza(self):
        return self.__cabeza

    def _set_cabeza(self, value):
        if isinstance(value, MovimientoCabeza):
            self.__cabeza = value
        else:
            raise TypeError("cabeza debe ser miembro del enum MovimientoCabeza")

    volumendevoz = property(_get_volumendevoz, _set_volumendevoz)
    palabrasporsegundo = property(_get_palabrasporsegundo, _set_palabrasporsegundo)
    posicionbrazos = property(_get_posicionbrazos, _set_posicionbrazos)
    mirada = property(_get_mirada, _set_mirada)
    rostro = property(_get_rostro, _set_rostro)
    cabeza = property(_get_cabeza, _set_cabeza)

    def comparar(self, captura):
        # Comparando volúmen de voz
        if not ((self.volumendevoz - 15) <= captura.volumendevoz <= (self.volumendevoz + 15)):
            return False
        # Comparando velocidad del hábla
        if not ((self.palabrasporsegundo - 0.5) <= captura.palabrasporsegundo <= (self.palabrasporsegundo + 0.5)):
            return False
        # Comparando posición de brazos
        if not ((self.posicionbrazos == PosicionBrazos.NOAPLICA) or (self.posicionbrazos == captura.posicionbrazos)):
            return False
        # Comparando dirección de la mirada
        if not ((self.mirada == DireccionMirada.NOAPLICA) or (self.mirada == captura.mirada)):
            return False
        # Comparando rostro
        if not ((self.rostro == Rostro.NOAPLICA) or (self.rostro == captura.rostro)):
            return False
        # Comparando movimiento de la cabeza
        if not ((self.cabeza == MovimientoCabeza.NOAPLICA) or (self.cabeza == captura.cabeza)):
            return False
        return True

    def similitud(self, captura):
        result = 0.0
        # Comparando volúmen de voz
        if (self.volumendevoz - 300) <= captura.volumendevoz <= (self.volumendevoz + 300):
            result += 1 / 6
        # Comparando velocidad del hábla
        if (self.palabrasporsegundo - 0.5) <= captura.palabrasporsegundo <= (self.palabrasporsegundo + 0.5):
            result += 1 / 6
        # Comparando posición de brazos
        if (self.posicionbrazos == PosicionBrazos.NOAPLICA) or (self.posicionbrazos == captura.posicionbrazos):
            result += 1 / 6
        # Comparando dirección de la mirada
        if (self.mirada == DireccionMirada.NOAPLICA) or (self.mirada == captura.mirada):
            result += 1 / 6
        # Comparando rostro
        if (self.rostro == Rostro.NOAPLICA) or (self.rostro == captura.rostro):
            result += 1 / 6
        # Comparando movimiento de la cabeza
        if (self.cabeza == MovimientoCabeza.NOAPLICA) or (self.cabeza == captura.cabeza):
            result += 1 / 6
        return result
