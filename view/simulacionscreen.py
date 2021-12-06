from kivy.clock import Clock
from kivy.core.image import Texture
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout as BoxLayout, MDBoxLayout
from kivymd.uix.screen import MDScreen as Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle
from model.fase import Fase
from controller.audiocontroller import AudioController
from controller.cvcontroller import CamaraController
from model.rostro import Rostro
from view.widgetsmethods import WidgetCreator
from view.selectordeiconos import SelectorDeIconos
from kivymd.uix.label import MDLabel as Label

camaracontroller = CamaraController()
miccontroller = AudioController()
backgroundColor = '6A3192'
subdivisionColor = [1, 1, 1]
botmessagebubblecolor = [240 / 255, 240 / 255, 240 / 255]
usermessagebubblecolor = [230 / 255, 245 / 255, 255 / 255]
chatboxpadding = [10, 10, 10, 10]


class SimulacionScreen(Screen):
    def __init__(self, **kwargs):
        super(SimulacionScreen, self).__init__(**kwargs)
        self.layout = SimulacionScreenLayout()
        self.add_widget(self.layout)

    def restart_screen(self):
        self.remove_widget(self.layout)
        self.layout = SimulacionScreenLayout()
        self.add_widget(self.layout)

    def establecerfase(self, fase: Fase):
        self.layout.faselabel.text = fase.nombre
        new_box = MDBoxLayout(size_hint=(0.8, None), orientation='horizontal', height=50)
        new_box.add_widget(WidgetCreator.newlabel(fase.texto, size_hint=(1.0, None), valign='middle'))
        with new_box.canvas.before:
            Color(botmessagebubblecolor[0], botmessagebubblecolor[1], botmessagebubblecolor[2])
            new_box.rect = RoundedRectangle(size=new_box.size, pos=new_box.pos, radius=[0, 25, 25, 25])
        new_box.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        self.layout.chatbox.content.add_widget(new_box)

    def imprimiralchatbox(self, texto):
        new_box = MDBoxLayout(size_hint=(0.8, None), orientation='horizontal', height=50, pos_hint={'x': 0.2})
        new_box.text = WidgetCreator.newlabel(texto, valign='middle', halign='right', size_hint=(1.0, 1.0))
        new_box.add_widget(new_box.text)
        new_box.size = new_box.text.size
        with new_box.canvas.before:
            Color(usermessagebubblecolor[0], usermessagebubblecolor[1], usermessagebubblecolor[2])
            new_box.rect = RoundedRectangle(size=new_box.size, pos=new_box.pos, radius=[25, 0, 25, 25])
        new_box.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        self.layout.chatbox.content.add_widget(new_box)


class SimulacionScreenLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SimulacionScreenLayout, self).__init__(**kwargs)
        self.padding = [10, 10, 10, 10]
        self.orientation = 'vertical'
        self.faselabel = WidgetCreator.newlabel("Nombre de Fase", size_hint=(1.0, None))
        self.add_widget(self.faselabel)
        chat = BoxLayout(orientation="horizontal", size_hint=(1, 1), spacing=10)
        chat.add_widget(WidgetCreator.newimage('assets/BotFace.jpg'))
        self.chatbox = ChatBox(size_hint=(1, 1))
        chat.add_widget(self.chatbox)
        self.add_widget(chat)
        self.camara = Image(size_hint=(1, 1), pos_hint={'top': 1})
        self.soundwave = FigureCanvasKivyAgg(AudioController().fig)
        self.userinputbox = UserInputBox(self.camara, self.soundwave, padding=[10, 10, 10, 10], spacing=10)
        self.add_widget(self.userinputbox)
        self.add_widget(SimulacionScreenLowerButtonRow(size_hint=(1.0, None), height=30))
        self.simulacionfinalizada = False
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        pose = camaracontroller.capturepose()
        self.userinputbox.poselabel.text = "Brazos: " + pose.name
        rostro = camaracontroller.capturegesture()
        if rostro != Rostro.NOAPLICA:
            self.userinputbox.rostrolabel.text = "Rostro: " + rostro.name
            self.userinputbox.rostroimage.source = SelectorDeIconos.iconoderostro(rostro)
        buf = camaracontroller.captureposeimage()
        self.soundwave.draw()
        if buf is not False:
            texture1 = Texture.create(size=(640, 480), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camara.texture = texture1
        if self.simulacionfinalizada:
            return False


class ChatBox(ScrollView):
    def __init__(self, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.do_scroll_x = False
        self.do_scroll_y = True
        new_box = BoxLayout(size_hint_y=None, orientation='vertical', padding=chatboxpadding, spacing=10)
        new_box.bind(minimum_height=new_box.setter('height'))
        with self.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        # listen to size and position changes
        self.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        self.content = new_box
        self.add_widget(self.content)


class UserInputBox(BoxLayout):
    def __init__(self, camara, soundwave, **kwargs):
        super(UserInputBox, self).__init__(**kwargs)
        with self.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # listen to size and position changes
        self.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        self.orientation = "horizontal"
        leftbox = BoxLayout(orientation='vertical', size_hint=(0.5, 1))
        leftupbox = BoxLayout(orientation='horizontal')
        # leftupbox.add_widget(Image(source="assets/Camara.png", size_hint=(0.1, None), pos_hint={'top': 1}))
        leftupbox.add_widget(camara)
        leftbox.add_widget(leftupbox)
        leftdownbox = BoxLayout(orientation="horizontal", size_hint=(1, 0.3))
        self.poselabel = WidgetCreator.newlabel("Brazos: NULL", size_hint=(1.0, None))
        leftdownbox.add_widget(self.poselabel)
        self.rostroimage = Image(source=SelectorDeIconos.iconoderostro(Rostro.SERIO), size_hint=(1, 1))
        leftdownbox.add_widget(self.rostroimage)
        leftbox.add_widget(leftdownbox)
        self.add_widget(leftbox)
        rightbox = BoxLayout(orientation='vertical')
        rightupbox = BoxLayout(orientation='horizontal')
        # rightupbox.add_widget(Image(source="assets/Camara.png", size_hint=(0.1, 0.1)))
        rightupbox.add_widget(soundwave)
        rightbox.add_widget(rightupbox)
        rightdownbox = BoxLayout(orientation='horizontal')
        self.rostrolabel = WidgetCreator.newlabel("SERIO", size_hint=(1.0, None))
        rightdownbox.add_widget(self.rostrolabel)
        rightbox.add_widget(rightdownbox)
        self.add_widget(rightbox)


class SimulacionScreenLowerButtonRow(BoxLayout):
    def __init__(self, **kwargs):
        super(SimulacionScreenLowerButtonRow, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        btn1 = WidgetCreator.newiconbutton("close", "Error")
        btn1.bind(on_press=self.callback_cancelar)
        btn2 = WidgetCreator.newiconbutton("pause")
        btn2.bind(on_press=self.callback_pausar)
        btn3 = WidgetCreator.newiconbutton("skip-next")
        btn3.bind(on_press=self.callback_adelantar)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(btn3)

    def callback_cancelar(self, obj):
        print("Boton cancelar")
        from controller.controladorprincipal import ControladorPrincipal
        ControladorPrincipal().cancelarsimulacion()

    def callback_pausar(self, obj):
        print("Boton Pausar")
        from controller.controladorprincipal import ControladorPrincipal
        if ControladorPrincipal().pausardespausarsimulacion():
            obj.icon = 'play'
        else:
            obj.icon = 'pause'

    def callback_adelantar(self, obj):
        print("Boton forzar resultado")
        from controller.controladorprincipal import ControladorPrincipal
        ControladorPrincipal().avanzarfase()
