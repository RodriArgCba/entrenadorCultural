import threading
import kivy
from kivy.uix.screenmanager import ScreenManager
from controller.audiocontroller import updatesound, contarpalabras
from controller.cvcontroller import updateimage, updategesture
from model.conversacion import Conversacion
from model.culturaobjetivo import CulturaObjetivo
from view.menuprincipal import MenuPrincipal
from kivy.app import App
from view.simulacionscreen import SimulacionScreen

kivy.require('1.11.1')


class ControladorPrincipal(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    cls._instance = super(ControladorPrincipal, cls).__new__(cls)
                    print('Creating the object')
                    cls._instance.culturaseleccionada = CulturaObjetivo(nombre="Japonesa")
                    cls._instance.conversacionseleccionada = Conversacion(
                        nombre="Saludo y Presentaciones",
                        duracion=120.0,
                        culturaobjetivo=cls._instance.culturaseleccionada
                    )
                    cls._instance.threadcamara = threading.Thread(target=updateimage, args=(), daemon=True)
                    cls._instance.threadsonido = threading.Thread(target=updatesound, args=(), daemon=True)
                    cls._instance.threadcontadorpalabras = threading.Thread(target=contarpalabras, args=(), daemon=True)
                    cls._instance.threadgestos = threading.Thread(target=updategesture, args=(), daemon=True)
        return cls._instance

    def logearusuario(self):
        pass

    def verificarsensores(self):
        pass

    def iniciarsimulacion(self):
        self.threadcamara.start()
        self.threadsonido.start()
        self.threadcontadorpalabras.start()
        self.threadgestos.start()
        app = App.get_running_app()
        app.root.add_widget(SimulacionScreen(name="simulacion"))
        app.root.current = 'simulacion'

    def verhistorialusuario(self):
        pass

    def listarhistorialtodoslosusuarios(self):
        pass

    def nuevaculturaobjetivo(self):
        pass

    def nuevaconversacion(self):
        pass


class EntrenadorCulturalApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(name="menu"))
        return sm
