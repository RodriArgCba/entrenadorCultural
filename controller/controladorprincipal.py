import threading
import kivy
from kivy.clock import Clock
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
                    cls._instance.simulacion = None
        return cls._instance

    def logearusuario(self):
        pass

    def verificarsensores(self):
        pass

    def iniciarsimulacion(self):
        if (self.culturaseleccionada is not None) and (self.conversacionseleccionada is not None):
            self.simulacion = Simulacion()
            self.iteradordefase = iter(self.conversacionseleccionada.fases)
            self.faseactual = next(self.iteradordefase)
            app = MDApp.get_running_app()
            if app.root.has_screen("simulacion"):
                self.pantallasimulacion = app.root.get_screen("simulacion")
                self.pantallasimulacion.restart_screen()
            else:
                self.pantallasimulacion = SimulacionScreen(name="simulacion")
                app.root.add_widget(self.pantallasimulacion)
            self.pantallasimulacion.establecerfase(self.faseactual)
            CamaraController().killthread = False
            self.threadcamara.start()
            self.threadgestos.start()
            AudioController().killthread = False
            self.threadsonido.start()
            ContadorDePalabras().killthread = False
            self.threadcontadorpalabras.start()

            app.root.current = 'simulacion'
            self.simulacion.conversacion = self.conversacionseleccionada
            self.nohaymasfases = False
            Clock.schedule_interval(self.simulacionupdate, 5.0)
        else:
            raise Exception("Se intentó iniciar simulación sin haber seleccionado una cultura y/o conversación")

    def pausardespausarsimulacion(self):
        contador = ContadorDePalabras()
        contador.paused = not contador.paused
        return contador.paused

    def cancelarsimulacion(self):
        CamaraController().killthread = True
        AudioController().killthread = True
        ContadorDePalabras().killthread = True
        self.resetthreads()
        self.pantallasimulacion.layout.simulacionfinalizada = True
        self.volveramenu()

    def simulacionupdate(self, dt):
        if self.nohaymasfases:
            self.finalizarsimulacion()
            return False

    def avanzarfase(self):
        if self.pantallasimulacion.layout.simulacionfinalizada:
            return
        captura = Captura()
        contadordepalabras = ContadorDePalabras()
        if contadordepalabras.duracionacumulada != 0:
            captura.palabrasporsegundo = contadordepalabras.acumulado / contadordepalabras.duracionacumulada
        else:
            captura.palabrasporsegundo = 0.0
        contadordepalabras.resetearcuenta()
        audiocontroller = AudioController()
        captura.volumendevoz = audiocontroller.volumenpromedio
        audiocontroller.reset = True
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
            self.nohaymasfases = True

    def interpretarcapturas(self):
        resultados = self.simulacion.resultados
        for linearesultado in resultados:
            linearesultado.interpretacion = self.culturaseleccionada.interpretar(linearesultado.captura)
        self.simulacion.limpiarresultados()
        self.simulacion.resultados = resultados
        self.simulacion.calcularcalificacion()

    def verhistorialusuario(self):
        app = MDApp.get_running_app()
        if app.root.has_screen("historialusuario"):
            historialscreen = app.root.get_screen("historialusuario")
            historialscreen.updatedata(obtenerhistorialdeusuario())
        else:
            app.root.add_widget(HistorialDeUsuario(obtenerhistorialdeusuario(), name="historialusuario"))
        app.root.current = 'historialusuario'

    def detallesdesimulacion(self, simulacion: Simulacion):
        app = MDApp.get_running_app()
        if app.root.has_screen("resultado"):
            resultadoscreen = app.root.get_screen("resultado")
            resultadoscreen.updatedata(simulacion)
        else:
            resultadoscreen = ResultadoScreen(simulacion, name="resultado")
            app.root.add_widget(resultadoscreen)
        resultadoscreen.layout.guardarsimulacionalsalir = False
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
        self.resetthreads()
        self.interpretarcapturas()
        self.pantallasimulacion.layout.simulacionfinalizada = True
        app = MDApp.get_running_app()
        if app.root.has_screen("resultado"):
            resultadoscreen = app.root.get_screen("resultado")
            resultadoscreen.updatedata(self.simulacion)
        else:
            resultadoscreen = ResultadoScreen(self.simulacion, name="resultado")
            app.root.add_widget(resultadoscreen)
        resultadoscreen.layout.guardarsimulacionalsalir = True
        app.root.current = 'resultado'

    def resetthreads(self):
        self.threadcamara = threading.Thread(target=updateimage, args=(), daemon=True)
        self.threadsonido = threading.Thread(target=updatesound, args=(), daemon=True)
        self.threadcontadorpalabras = threading.Thread(target=contarpalabras, args=(), daemon=True)
        self.threadgestos = threading.Thread(target=updategesture, args=(), daemon=True)

    def guardarsimulacion(self):
        guardarresultado(self.simulacion)

    def volveramenu(self):
        app = MDApp.get_running_app()
        app.root.current = 'menu'


class EntrenadorCulturalApp(MDApp):
    def __init__(self, **kwargs):
        super(EntrenadorCulturalApp, self).__init__(**kwargs)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(name="menu"))
        return sm
