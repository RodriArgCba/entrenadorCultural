import threading
import kivy
from kivy.uix.screenmanager import ScreenManager
from controller.audiocontroller import updatesound, contarpalabras
from controller.cvcontroller import updateimage, updategesture
from model.conversacion import Conversacion
from model.culturaobjetivo import CulturaObjetivo
from model.simulacion import Simulacion
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
                    cls._instance.culturaseleccionada: CulturaObjetivo = None
                    cls._instance.conversacionseleccionada: Conversacion = None
                    cls._instance.iteradordefase = None
                    cls._instance.threadcamara = threading.Thread(target=updateimage, args=(), daemon=True)
                    cls._instance.threadsonido = threading.Thread(target=updatesound, args=(), daemon=True)
                    cls._instance.threadcontadorpalabras = threading.Thread(target=contarpalabras, args=(), daemon=True)
                    cls._instance.threadgestos = threading.Thread(target=updategesture, args=(), daemon=True)
                    cls._instance.simulacion = Simulacion()
        return cls._instance

    def logearusuario(self):
        pass

    def verificarsensores(self):
        pass

    def iniciarsimulacion(self):
        if (self.culturaseleccionada is not None) and (self.conversacionseleccionada is not None):
            self.threadcamara.start()
            self.threadsonido.start()
            self.threadcontadorpalabras.start()
            self.threadgestos.start()
            self.iteradordefase = iter(self.conversacionseleccionada.fases)
            app = App.get_running_app()
            pantallasimulacion = SimulacionScreen(self, name="simulacion")
            app.root.add_widget(pantallasimulacion)
            app.root.current = 'simulacion'
            self.simulacion.conversacion = self.conversacionseleccionada
        else:
            raise Exception("Se intentó iniciar simulación sin haber seleccionado una cultura y/o conversación")

    def avanzarfase(self):
        pass

    def verhistorialusuario(self):
        pass

    def listarhistorialtodoslosusuarios(self):
        pass

    def nuevaculturaobjetivo(self):
        pass

    def nuevaconversacion(self):
        pass


class EntrenadorCulturalApp(App):
    def __init__(self, controladorprincipal, **kwargs):
        super(EntrenadorCulturalApp, self).__init__(**kwargs)
        self.controladorprincipal = controladorprincipal

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(self.controladorprincipal, name="menu"))
        return sm
