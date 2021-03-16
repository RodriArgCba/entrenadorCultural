from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from model.fase import Fase
from controller.audiocontroller import AudioController
from controller.cvcontroller import CamaraController
from view.widgetsmethods import WidgetCreator

camaracontroller = CamaraController()
miccontroller = AudioController()
backgroundColor = '6A3192'
subdivisionColor = [0.58, 0.337, 0.639]
padding = [75, 0, 75, 0]


class SimulacionScreen(Screen):
    def __init__(self, **kwargs):
        super(SimulacionScreen, self).__init__(**kwargs)
        self.layout = SimulacionScreenLayout()
        self.add_widget(self.layout)

    def establecerfase(self, fase: Fase):
        self.layout.faselabel.text = fase.nombre
        self.layout.chatbox.content.add_widget(WidgetCreator.newlabel(fase.texto, size_hint=(1.0, None)))

    def imprimiralchatbox(self,texto):
        self.layout.chatbox.content.add_widget(WidgetCreator.newlabel(texto, valign='bottom', halign='right', size_hint=(1.0, None)))


class SimulacionScreenLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SimulacionScreenLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.faselabel = WidgetCreator.newlabel("Nombre de Fase", size_hint=(1.0, None))
        self.add_widget(self.faselabel)
        chat = BoxLayout(orientation="horizontal", size_hint=(1, 1))
        chat.add_widget(WidgetCreator.newimage('assets/BotFace.jpg'))
        self.chatbox = ChatBox(size_hint=(1, 1))
        chat.add_widget(self.chatbox)
        self.add_widget(chat)
        self.camara = Image(size_hint=(1, None), pos_hint={'top': 1})
        self.soundwave = FigureCanvasKivyAgg(AudioController().fig)
        self.userinputbox = UserInputBox(self.camara, self.soundwave)
        self.add_widget(self.userinputbox)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        pose = camaracontroller.capturepose()
        self.userinputbox.poselabel.text = "Brazos: " + pose.name
        rostro = camaracontroller.capturegesture()
        self.userinputbox.rostrolabel.text = "Rostro: " + rostro.name
        if rostro.value == 1:
            self.userinputbox.rostroimage.source = "assets/Sonriendo.png"
        elif rostro.value == 2:
            self.userinputbox.rostroimage.source = "assets/Serio.png"
        elif rostro.value == 3:
            self.userinputbox.rostroimage.source = "assets/Irritado.png"
        elif rostro.value == 4:
            self.userinputbox.rostroimage.source = "assets/Preocupado.png"
        buf = camaracontroller.captureposeimage()
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
        self.content = BoxLayout(size_hint_y=None, orientation='vertical')
        self.content.bind(minimum_height=self.content.setter('height'))
        with self.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = Rectangle(size=self.size, pos=self.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)
        self.add_widget(self.content)


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
        rightbox = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        rightupbox = BoxLayout(orientation='horizontal')
        rightupbox.add_widget(Image(source="assets/Camara.png", size_hint=(0.1, None), pos_hint={'top': 1}))
        rightupbox.add_widget(camara)
        rightbox.add_widget(rightupbox)
        self.poselabel = WidgetCreator.newlabel("Brazos: NULL", size_hint=(1.0, None))
        rightbox.add_widget(self.poselabel)
        self.add_widget(rightbox)
        leftbox = BoxLayout(orientation='vertical')
        leftupbox = BoxLayout(orientation='horizontal')
        leftupbox.add_widget(Image(source="assets/Camara.png", size_hint=(0.1, 1)))
        leftupbox.add_widget(soundwave)
        leftbox.add_widget(leftupbox)
        leftdownbox = BoxLayout(orientation='horizontal')
        self.rostroimage = Image(source="assets/Serio.png", size_hint=(0.1, 1))
        leftdownbox.add_widget(self.rostroimage)
        self.rostrolabel = WidgetCreator.newlabel("SERIO", size_hint=(1.0, None))
        leftdownbox.add_widget(self.rostrolabel)
        leftbox.add_widget(leftdownbox)
        self.add_widget(leftbox)
