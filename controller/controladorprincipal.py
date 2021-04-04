import threading
import kivy
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from controller.audiocontroller import updatesound, contarpalabras, AudioController, ContadorDePalabras
from controller.cvcontroller import CamaraController, updateimage, updategesture
from model.captura import Captura
from model.conversacion import Conversacion
from model.culturaobjetivo import CulturaObjetivo
from model.direccionmirada import DireccionMirada
from model.linearesultado import LineaResultado
from model.movimientocabeza import MovimientoCabeza
from model.simulacion import Simulacion
from view.historialdeusuarioscreen import HistorialDeUsuario
from view.menuprincipal import MenuPrincipal

from view.resultadoscreen import ResultadoScreen
from view.simulacionscreen import SimulacionScreen
from controller.dbcontroller import guardarresultado, obtenerhistorialdeusuario

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
            self.iteradordefase = iter(self.conversacionseleccionada.fases)
            self.faseactual = next(self.iteradordefase)
            self.pantallasimulacion = SimulacionScreen(name="simulacion")
            self.pantallasimulacion.establecerfase(self.faseactual)
            CamaraController().killthread = False
            self.threadcamara.start()
            self.threadgestos.start()
            AudioController().killthread = False
            self.threadsonido.start()
            ContadorDePalabras().killthread = False
            self.threadcontadorpalabras.start()
            app = MDApp.get_running_app()
            app.root.add_widget(self.pantallasimulacion)
            app.root.current = 'simulacion'
            self.simulacion.conversacion = self.conversacionseleccionada
        else:
            raise Exception("Se intentó iniciar simulación sin haber seleccionado una cultura y/o conversación")

    def avanzarfase(self):
        captura = Captura()
        contadordepalabras = ContadorDePalabras()
        captura.palabrasporsegundo = contadordepalabras.acumulado / contadordepalabras.duracionacumulada
        audiocontroller = AudioController()
        captura.volumendevoz = audiocontroller.volumenpromedio
        camaracontroller = CamaraController()
        captura.rostro = camaracontroller.capturegesture()
        captura.posicionbrazos = camaracontroller.capturepose()
        captura.mirada = DireccionMirada.OJOS
        captura.cabeza = MovimientoCabeza.QUIETA
        self.simulacion.resultados = LineaResultado(self.faseactual, captura)
        try:
            self.faseactual = next(self.iteradordefase)
            self.pantallasimulacion.establecerfase(self.faseactual)
        except:
            self.finalizarsimulacion()

    def interpretarcapturas(self):
        resultados = self.simulacion.resultados
        for linearesultado in resultados:
            linearesultado.interpretacion = self.culturaseleccionada.interpretar(linearesultado.captura)
        self.simulacion.limpiarresultados()
        self.simulacion.resultados = resultados

    def verhistorialusuario(self):
        app = MDApp.get_running_app()
        screenexists = False
        for child in app.root.children:
            if child.name == 'historialusuario':
                screenexists = True
                historialscreen = child
        if not screenexists:
            app.root.add_widget(HistorialDeUsuario(obtenerhistorialdeusuario(), name="historialusuario"))
        else:
            historialscreen.updatedata(obtenerhistorialdeusuario())
        app.root.current = 'historialusuario'

    def detallesdesimulacion(self, simulacion: Simulacion):
        app = MDApp.get_running_app()
        screenexists = False
        for child in app.root.children:
            if child.name == 'resultado':
                screenexists = True
                resultadoscreen = child
        if not screenexists:
            app.root.add_widget(ResultadoScreen(simulacion, name="resultado"))
        else:
            resultadoscreen.updatedata(simulacion)
        app.root.current = 'resultado'

    def listarhistorialtodoslosusuarios(self):
        pass

    def nuevaculturaobjetivo(self):
        pass

    def nuevaconversacion(self):
        pass

    def printtochatbox(self, texto):
        self.pantallasimulacion.imprimiralchatbox(texto)
        self.avanzarfase()

    def finalizarsimulacion(self):
        CamaraController().killthread = True
        AudioController().killthread = True
        ContadorDePalabras().killthread = True
        self.interpretarcapturas()
        app = MDApp.get_running_app()
        app.root.add_widget(ResultadoScreen(self.simulacion, name="resultado"))
        app.root.current = 'resultado'

    def guardarsimulacion(self):
        guardarresultado(self.simulacion)

    def volveramenu(self):
        app = MDApp.get_running_app()
        app.root.current = 'menu'


class EntrenadorCulturalApp(MDApp):
    def __init__(self, **kwargs):
        super(EntrenadorCulturalApp, self).__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(name="menu"))
        return sm
