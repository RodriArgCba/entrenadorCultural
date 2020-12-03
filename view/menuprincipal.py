from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from view.widgetsmethods import WidgetCreator
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as getColor
from kivy.graphics import Color, Rectangle
from kivy.config import Config

backgroundColor = '6A3192'
subdivisionColor = [0.58,0.337,0.639]
padding = [75,0,75,0]

class MenuPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super(MenuPrincipal, self).__init__(**kwargs)
        Window.clearcolor = getColor(backgroundColor)
        Window.size = (800,600)
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
        self.add_widget(EstadoSensores())
        #Llenar pantalla hacia abajo
        self.add_widget(Label(size_hint=(1.0,1.0)))

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
            Color(subdivisionColor[0],subdivisionColor[1],subdivisionColor[2])
            self.rect = Rectangle(size=grid.size, pos=grid.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)


