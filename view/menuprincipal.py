from typing import List, Any
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex as getcolor
from controller import dbcontroller
from view.widgetsmethods import WidgetCreator

backgroundColor = '6A3192'
subdivisionColor = [0.58, 0.337, 0.639]
padding = [45, 0, 45, 10]
culturas = dbcontroller.allculturas()
conversaciones: List[Any] = []


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
        self.add_widget(WidgetCreator.newlabel('Cultura Objetivo:', size_hint=(1.0, None)))
        values = []
        for x in culturas:
            values.append(x.nombre)
        self.culturaObjetivo = WidgetCreator.newspinner(
            'Elija la cultura objetivo...',
            values
        )
        self.culturaObjetivo.bind(text=self.callback_spinner_culturas)
        self.add_widget(self.culturaObjetivo)
        self.add_widget(WidgetCreator.newlabel('Conversación:', size_hint=(1.0, None)))
        self.conversación = WidgetCreator.newspinner(
            'Elija la conversación a simular...',
            ()
        )
        self.conversación.bind(text=self.callback_spinner_conversaciones)
        self.conversación.disabled = True
        self.add_widget(self.conversación)
        self.add_widget(WidgetCreator.newlabel('Estado Sensores:', size_hint=(1.0, None)))
        self.add_widget(EstadoSensores(
            height=176,
            size_hint_y=None
        ))
        # Llenar pantalla hacia abajo
        self.add_widget(Label(size_hint=(1.0, 1.0)))
        self.add_widget(LowerButtonsRow())

    def callback_spinner_culturas(self, obj, value):
        cultura = None
        for x in culturas:
            if x.nombre == value:
                cultura = x
                break;
        if cultura is not None:
            global conversaciones
            conversaciones = dbcontroller.conversacionesdecultura(cultura)
            values = []
            for x in conversaciones:
                values.append(x.nombre)
            self.conversación.values = values
            self.conversación.disabled = False
            from controller.controladorprincipal import ControladorPrincipal
            ControladorPrincipal().culturaseleccionada = cultura
        else:
            raise Exception("Valor de cultura incorrecto")

    def callback_spinner_conversaciones(self, obj, value):
        conversacion = None
        global conversaciones
        for x in conversaciones:
            if x.nombre == value:
                conversacion = x
                break;
        if conversacion is not None:
            from controller.controladorprincipal import ControladorPrincipal
            ControladorPrincipal().conversacionseleccionada = conversacion
        else:
            raise Exception("Valor de conversacion incorrecto")


class LowerButtonsRow(BoxLayout):
    def __init__(self, **kwargs):
        super(LowerButtonsRow, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        btn1 = WidgetCreator.newbutton("Iniciar conversación")
        btn1.bind(on_press=self.callback_iniciarconversacion)
        btn2 = WidgetCreator.newbutton("Historial")
        btn2.bind(on_press=self.callback_historial)
        btn3 = WidgetCreator.newbutton("Volver")
        btn3.bind(on_press=self.callback_volver)
        self.add_widget(btn1)
        self.add_widget(btn2)
        self.add_widget(btn3)

    def callback_volver(self, obj):
        print("Boton volver")

    def callback_historial(self, obj):
        print("Boton historial")
        from controller.controladorprincipal import ControladorPrincipal
        ControladorPrincipal().verhistorialusuario()

    def callback_iniciarconversacion(self, obj):
        print("Boton Simulacion")
        from controller.controladorprincipal import ControladorPrincipal
        ControladorPrincipal().iniciarsimulacion()


class EstadoSensores(GridLayout):
    def __init__(self, **kwargs):
        super(EstadoSensores, self).__init__(**kwargs)
        self.cols = 3
        self.add_widget(WidgetCreator.newlabel('Cámara:', valign='middle', size_hint=(1.0, None)))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/Sonriendo.png"))
        self.add_widget(WidgetCreator.newlabel('Micrófono:', valign='middle', size_hint=(1.0, None)))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/Sonriendo.png"))
        self.add_widget(WidgetCreator.newlabel('Casco de Realidad Virtual:', valign='middle', size_hint=(1.0, None)))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/Sonriendo.png"))
        self.add_widget(WidgetCreator.newlabel('Sensor Ocular:', valign='middle', size_hint=(1.0, None)))
        self.add_widget(WidgetCreator.newicon("assets/Camara.png"))
        self.add_widget(WidgetCreator.newicon("assets/Sonriendo.png"))
        grid = self
        with grid.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = Rectangle(size=grid.size, pos=grid.pos)

        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        # listen to size and position changes
        self.bind(pos=update_rect, size=update_rect)
        # print(self.rect)
