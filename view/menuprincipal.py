from typing import List, Any
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import RoundedRectangle
from kivymd.uix.boxlayout import MDBoxLayout as BoxLayout
from kivymd.uix.gridlayout import MDGridLayout as GridLayout
from kivymd.uix.label import MDLabel as Label, MDIcon
from kivymd.uix.screen import MDScreen as Screen
from kivy.utils import get_color_from_hex as getcolor
from controller import dbcontroller
from view.widgetsmethods import WidgetCreator

backgroundColor = '6A3192'
subdivisionColor = [0.91, 0.91, 0.91]
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
            self.conversación
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
        self.add_widget(WidgetCreator.newmdicon('camera'))
        self.add_widget(WidgetCreator.newmdicon('checkbox-marked-outline', text_color=getcolor("#008000"), theme_text_color="Custom"))
        self.add_widget(WidgetCreator.newlabel('Micrófono:', valign='middle', size_hint=(1.0, None)))
        self.add_widget(WidgetCreator.newmdicon('microphone'))
        self.add_widget(WidgetCreator.newmdicon('checkbox-marked-outline', text_color=getcolor("#008000"), theme_text_color="Custom"))
        self.add_widget(WidgetCreator.newlabel('Casco de Realidad Virtual:', valign='middle', size_hint=(1.0, None)))
        self.add_widget(WidgetCreator.newmdicon('racing-helmet'))
        self.add_widget(WidgetCreator.newmdicon('alert', theme_text_color='Error'))
        self.add_widget(WidgetCreator.newlabel('Sensor Ocular:', valign='middle', size_hint=(1.0, None)))
        self.add_widget(WidgetCreator.newmdicon('eye-outline'))
        self.add_widget(WidgetCreator.newmdicon('alert', theme_text_color='Error'))
        with self.canvas.before:
            Color(subdivisionColor[0], subdivisionColor[1], subdivisionColor[2])
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])

        # listen to size and position changes
        self.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)