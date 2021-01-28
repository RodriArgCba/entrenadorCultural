from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from view.widgetsmethods import WidgetCreator
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as getcolor
from kivy.graphics import Color, Rectangle

backgroundColor = '6A3192'
subdivisionColor = [0.58, 0.337, 0.639]
padding = [45, 0, 45, 10]


def callback_volver(instance):
    print("Boton volver")


def callback_historial(instance):
    print("Boton historial")


def callback_iniciarconversacion(instance):
    print("Boton Simulacion")
    from controller.controladorprincipal import ControladorPrincipal
    ControladorPrincipal().iniciarsimulacion()


class MenuPrincipal(Screen):
    def __init__(self, **kwargs):
        super(MenuPrincipal, self).__init__(**kwargs)
        self.add_widget(MenuPrincipalLayout())


class MenuPrincipalLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MenuPrincipalLayout, self).__init__(**kwargs)
        Window.clearcolor = getcolor(backgroundColor)
        Window.size = (800, 600)
        Window.minimum_width, Window.minimum_height = Window.size
        self.orientation = 'vertical'
        self.padding = padding
        self.add_widget(WidgetCreator.newlabel('Cultura Objetivo:'))
        self.culturaObjetivo = WidgetCreator.newspinner(
            'Elija la cultura objetivo...',
            ('Japonesa', 'Finlandesa')
        )
        self.add_widget(self.culturaObjetivo)
        self.add_widget(WidgetCreator.newlabel('Conversación:'))
        self.conversación = WidgetCreator.newspinner(
            'Elija la conversación a simular...',
            ('Saludo y presentaciones', 'Calmando al cliente', 'Explicando el producto')
        )
        self.add_widget(self.conversación)
        self.add_widget(WidgetCreator.newlabel('Estado Sensores:'))
        self.add_widget(EstadoSensores(
            height=176,
            size_hint_y=None
        ))
        # Llenar pantalla hacia abajo
        self.add_widget(Label(size_hint=(1.0, 1.0)))
        self.add_widget(LowerButtonsRow())



class LowerButtonsRow(BoxLayout):
    def __init__(self, **kwargs):
        super(LowerButtonsRow, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        btn1 = WidgetCreator.newbutton("Iniciar conversación")
        btn1.bind(on_press=callback_iniciarconversacion)
        btn2 = WidgetCreator.newbutton("Historial")
        btn2.bind(on_press=callback_historial)
        btn3 = WidgetCreator.newbutton("Volver")
        btn3.bind(on_press=callback_volver)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(btn3)


class EstadoSensores(GridLayout):
    def __init__(self, **kwargs):
        super(EstadoSensores, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(WidgetCreator.newlabel('Cámara:', 'middle'))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/green-emotion-smile.png"))
        self.add_widget(WidgetCreator.newlabel('Micrófono:', 'middle'))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/green-emotion-smile.png"))
        self.add_widget(WidgetCreator.newlabel('Casco de Realidad Virtual:', 'middle'))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/green-emotion-smile.png"))
        self.add_widget(WidgetCreator.newlabel('Sensor Ocular:', 'middle'))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/green-emotion-smile.png"))
        grid = self
        with grid.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = Rectangle(size=grid.size, pos=grid.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)
        #print(self.rect)
