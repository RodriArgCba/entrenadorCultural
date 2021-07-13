from model.direccionmirada import DireccionMirada
from model.movimientocabeza import MovimientoCabeza
from model.posicionbrazos import PosicionBrazos
from model.rostro import Rostro

selectorderostro = {
    Rostro.NOAPLICA: "assets/Invalid.png",
    Rostro.SONRIENDO: "assets/rostros/Sonriendo.png",
    Rostro.SERIO: "assets/rostros/Serio.png",
    Rostro.IRRITADO: "assets/rostros/Irritado.png",
    Rostro.PREOCUPADO: "assets/rostros/Preocupado.png"
}
selectordemirada = {
    DireccionMirada.NOAPLICA: "assets/Invalid.png",
    DireccionMirada.SUELO: "assets/miradas/AlSuelo.png",
    DireccionMirada.OJOS: "assets/miradas/ALosOjos.png",
    DireccionMirada.ARRIBA: "assets/miradas/HaciaArriba.png",
    DireccionMirada.ENMOVIMIENTOCONSTANTE: "assets/miradas/EnMovimientoConstante.png",
    DireccionMirada.ENOTRAPARTEDELCUERPO: "assets/miradas/EnOtraParteDelCuerpo.png"
}

selectordecabeza = {
    MovimientoCabeza.NOAPLICA: "assets/Invalid.png",
    MovimientoCabeza.ENMOVIMIENTOCONSTANTE: "assets/cabezas/MovimientoConstante.png",
    MovimientoCabeza.QUIETA: "assets/cabezas/Quieta.png",
    MovimientoCabeza.DEARRIBAABAJO: "assets/cabezas/ArribaAbajo.png",
    MovimientoCabeza.DEIZQUIERDAADERECHA: "assets/cabezas/IzquierdaDerecha.png"
}

selectordebrazos = {
    PosicionBrazos.NOAPLICA: "assets/Invalid.png",
    PosicionBrazos.CRUZADOS: "assets/brazos/Cruzados.png",
    PosicionBrazos.TRASLAESPALDA: "assets/brazos/TrasLaEspalda.png",
    PosicionBrazos.EXTENDIDOS: "assets/brazos/Extendidos.png",
    PosicionBrazos.NEUTRALES: "assets/brazos/Neutrales.png"
}

selectordevolumen = {
    "bajo": "assets/volumenes/Bajo.png",
    "medio": "assets/volumenes/Medio.png",
    "alto": "assets/volumenes/Alto.png",
}

selectordevelocidad = {
    "lento": "assets/velocidades/Lento.png",
    "medio": "assets/velocidades/Medio.png",
    "rapido": "assets/velocidades/Rapido.png",
}

selectordecolorbarra = {
    "baja": [237/255, 35/255, 18/255, 1.0],
    "media": [250/255, 249/255, 4/255, 1.0],
    "alta": [61/255, 171/255, 21/255, 1.0]
}


class SelectorDeIconos:

    @staticmethod
    def iconoderostro(rostro: Rostro):
        return selectorderostro.get(rostro, None)

    @staticmethod
    def iconodemirada(mirada: DireccionMirada):
        return selectordemirada.get(mirada, None)

    @staticmethod
    def iconodecabeza(cabeza: MovimientoCabeza):
        return selectordecabeza.get(cabeza, None)

    @staticmethod
    def iconodebrazos(brazos: PosicionBrazos):
        return selectordebrazos.get(brazos, None)

    @staticmethod
    def iconodevolumen(volumen):
        if volumen <= 35:
            return selectordevolumen.get("bajo")
        elif 35 < volumen <= 60:
            return selectordevolumen.get("medio")
        else:
            return selectordevolumen.get("alto")

    @staticmethod
    def iconodevelocidad(velocidad):
        if velocidad <= 0.8:
            return selectordevelocidad.get("lento")
        elif 0.8 < velocidad <= 1.6:
            return selectordevelocidad.get("medio")
        else:
            return selectordevelocidad.get("rapido")

    @staticmethod
    def progressbarcolor(calificacion):
        if calificacion <= 35:
            return selectordecolorbarra.get("baja")
        elif 35 < calificacion < 70:
            return selectordecolorbarra.get("media")
        elif calificacion >= 70:
            return selectordecolorbarra.get("alta")