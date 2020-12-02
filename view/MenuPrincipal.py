from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from view.widgetsMethods import WidgetCreator
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as getColor

backgroundColor = '6A3192'
padding = [25,0,25,0]

class MenuPrincipal(BoxLayout):
    def __init__(self, **kwargs):
        super(MenuPrincipal, self).__init__(**kwargs)
        Window.clearcolor = getColor(backgroundColor)
        self.orientation = 'vertical'
        self.padding = padding
        self.add_widget(WidgetCreator.newLabel('Cultura Objetivo:'))
        self.culturaObjetivo = WidgetCreator.newSpinner('Elija la cultura objetivo...', ('Saludo y presentaciones', 'Calmando al cliente', 'Explicando el producto'))
        self.add_widget(self.culturaObjetivo)
        #Llenar pantalla hacia abajo
        self.add_widget(Label(size_hint=(1.0,1.0)))


