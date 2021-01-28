import threading

from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle

from view.widgetsmethods import WidgetCreator

from controller.audiocontroller import AudioController, updatesound, contarpalabras
from controller.cvcontroller import CamaraController, updateimage, updategesture
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
        self.chatbox = BoxLayout(orientation="horizontal",size_hint=(1, 1))
        self.chatbox.add_widget(WidgetCreator.newimage('assets/customer-service-woman-16112201.jpg'))
        self.chatbox.add_widget(ChatBox(size_hint=(1,1)))
        self.add_widget(self.chatbox)
        self.camara = Image(size_hint=(1,None),pos_hint={'top': 1})
        self.soundwave = FigureCanvasKivyAgg(AudioController().fig)
        self.add_widget(UserInputBox(self.camara,self.soundwave))
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self,dt):
        buf = camaracontroller.capturepose()
        self.soundwave.draw()
        if buf is not False:
            texture1 = Texture.create(size=(640, 480), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camara.texture = texture1

class ChatBox(ScrollView):
    def __init__(self, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.do_scroll_x = False
        self.do_scroll_y = True
        content = BoxLayout(size_hint_y=None, orientation='vertical')
        content.add_widget(WidgetCreator.newlabel("Bienveniu mi buen usuariu!"))
        content.add_widget(WidgetCreator.newlabel("Bienveniu mi buen usuariu!"))
        content.add_widget(WidgetCreator.newlabel("Bienveniu mi buen usuariu!"))
        content.add_widget(WidgetCreator.newlabel("Bienveniu mi buen usuariu!"))
        content.add_widget(WidgetCreator.newlabel("Bienveniu mi buen usuariu!"))
        content.add_widget(WidgetCreator.newlabel("Bienveniu mi buen usuariu!"))
        content.add_widget(WidgetCreator.newlabel("Bienveniu mi buen usuariu!"))
        content.bind(minimum_height=content.setter('height'))
        with self.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)
        self.add_widget(content)

class UserInputBox(BoxLayout):
    def __init__(self, camara, soundwave, **kwargs):
        super(UserInputBox, self).__init__(**kwargs)
        with self.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = Rectangle(size=self.size, pos=self.pos)
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)
        self.orientation = "horizontal"
        rightbox = BoxLayout(orientation='vertical', size_hint=(0.3,1))
        rightupbox = BoxLayout(orientation='horizontal')
        rightupbox.add_widget(Image(source="assets/Camara.png",size_hint=(0.1,None),pos_hint={'top': 1}))
        rightupbox.add_widget(camara)
        rightbox.add_widget(rightupbox)
        rightbox.add_widget(WidgetCreator.newlabel("Brazos: Extendidos"))
        self.add_widget(rightbox)
        leftbox = BoxLayout(orientation='vertical')
        leftupbox = BoxLayout(orientation='horizontal')
        leftupbox.add_widget(Image(source="assets/Camara.png",size_hint=(0.1,1)))
        leftupbox.add_widget(soundwave)
        leftbox.add_widget(leftupbox)
        leftdownbox = BoxLayout(orientation='horizontal')
        leftdownbox.add_widget(Image(source="assets/green-emotion-smile.png",size_hint=(0.1,1)))
        leftdownbox.add_widget(WidgetCreator.newlabel("Sonriendo"))
        leftbox.add_widget(leftdownbox)
        self.add_widget(leftbox)

