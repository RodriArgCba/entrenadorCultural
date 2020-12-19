import threading

from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from controller.audiocontroller import AudioController, updatesound, contarpalabras
from controller.cvcontroller import CamaraController, updateimage
from view.widgetsmethods import WidgetCreator

camaracontroller = CamaraController()
miccontroller = AudioController()
backgroundColor = '6A3192'
subdivisionColor = [0.58, 0.337, 0.639]
padding = [75, 0, 75, 0]


class SimulacionScreen(Screen):
    def __init__(self, **kwargs):
        super(SimulacionScreen, self).__init__(**kwargs)
        self.add_widget(SimulacionScreenLayout())


class SimulacionScreenLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SimulacionScreenLayout, self).__init__(**kwargs)
        self.orientation='vertical'
        self.add_widget(WidgetCreator.newlabel("Fase 1: Saludos"))
        self.camara = Image()
        self.add_widget(self.camara)
        self.soundwave = FigureCanvasKivyAgg(AudioController().fig)
        self.add_widget(self.soundwave)
        self.threadcamara = threading.Thread(target=updateimage,args=(),daemon=True)
        self.threadcamara.start()
        self.threadsonido = threading.Thread(target=updatesound, args=(), daemon=True)
        self.threadsonido.start()
        self.threadcontadorpalabras = threading.Thread(target=contarpalabras, args=(), daemon=True)
        self.threadcontadorpalabras.start()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self,dt):
        buf = camaracontroller.capturepose()
        self.soundwave.draw()
        if buf is not False:
            texture1 = Texture.create(size=(640, 480), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camara.texture = texture1
