from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivymd.uix import Screen
from kivymd.uix.boxlayout import MDBoxLayout as BoxLayout
from kivymd.uix.gridlayout import MDGridLayout as GridLayout
from kivymd.uix.label import MDLabel as Label

from model.fase import Fase
from model.linearesultado import LineaResultado
from model.simulacion import Simulacion
from view.selectordeiconos import SelectorDeIconos
from view.widgetsmethods import WidgetCreator

backgroundColor = '6A3192'
subdivisionColor = [0.58, 0.337, 0.639]
firstrowcolor = [183.09 / 255, 210.885 / 255, 236.895 / 255]
secondrowcolor = [207.06 / 255, 224.91 / 255, 250.92 / 255]
padding = [45, 0, 45, 10]
textcolor = (1, 1, 1, 1)
gridpadding = [5, 5, 5, 5]


class ResultadoScreen(Screen):
    def __init__(self, simulacion: Simulacion, **kwargs):
        super(ResultadoScreen, self).__init__(**kwargs)
        self.resultadosscreenlayout = ResultadoScreenLayout(simulacion)
        self.add_widget(self.resultadosscreenlayout)

    def updatedata(self, simulacion: Simulacion):
        pass


class ResultadoScreenLayout(BoxLayout):

    def __init__(self, simulacion, **kwargs):
        super(ResultadoScreenLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        boxtitular = BoxLayout(size_hint=(1.0, None), height=40)
        boxtitular.orientation = 'horizontal'
        boxtitular.add_widget(Label(text="Resultado General:", size_hint=(1.0, None), height=20, color=textcolor))
        boxtitular.barraderesultado = BoxLayout()
        boxtitular.barraderesultado.orientation = 'vertical'
        boxtitular.barraderesultado.add_widget(Label(text="Barra", size_hint=(1.0, None), height=20))
        boxtitular.barraderesultado.add_widget(Label(text="Porcentaje", size_hint=(1.0, None), height=20))
        boxtitular.add_widget(boxtitular.barraderesultado)
        boxtitular.add_widget(Label(text="Usuario", size_hint=(1.0, 1.0), height=20))
        self.add_widget(boxtitular)
        self.add_widget(TabbedPanelResultados(simulacion))
        btn = WidgetCreator.newbutton("Volver")
        btn.bind(on_press=self.callback_volver)
        self.add_widget(btn)
        self.guardarsimulacionalsalir = True
        # Llenar pantalla hacia abajo

    def callback_volver(self, obj):
        print("Boton volver")
        from controller.controladorprincipal import ControladorPrincipal
        if self.guardarsimulacionalsalir:
            ControladorPrincipal().guardarsimulacion()
        ControladorPrincipal().volveramenu()


class TabbedPanelResultados(TabbedPanel):

    def __init__(self, simulacion: Simulacion, **kwargs):
        super(TabbedPanelResultados, self).__init__(**kwargs)
        self.do_default_tab = False
        self.tab_pos = 'left_top'
        self.background_color = subdivisionColor
        fases = simulacion.conversacion.fases
        i = 0
        for resultado in simulacion.resultados:
            self.add_widget(TabbedPanelItemResultados(resultado, fases[i], i + 1))
            i = i + 1


class TabbedPanelItemResultados(TabbedPanelItem):

    def __init__(self, resultado: LineaResultado, fase, nrodefase: Fase, **kwargs):
        super(TabbedPanelItemResultados, self).__init__(**kwargs)
        self.text = f"Fase {nrodefase}"
        content = BoxLayout(padding=gridpadding)
        # content = BoxLayout(halign='left', valign="middle")
        content.orientation = 'vertical'
        content.add_widget(Label(text=f"{fase.nombre}", size_hint=(1.0, None), height=20))
        content.add_widget(Label(text="Captura de usuario:", size_hint=(1.0, None), height=20))

        grid = GridLayout(
            cols=2,
            row_force_default=True,
            row_default_height=40,
            size_hint=(1.0, None),
            height=240,
            spacing=5,
            padding=gridpadding,
        )
        label = Label(text="Rostro", size_hint=(None, 1), width=100)
        with label.canvas.before:
            Color(firstrowcolor[0], firstrowcolor[1], firstrowcolor[2])
            label.rect = Rectangle(size=self.size, pos=self.pos)
        label.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(label)

        rostro = BoxLayout(orientation='horizontal')
        rostro.add_widget(Label(text=resultado.captura.rostro.name))
        rostro.add_widget(
            Image(
                size_hint=(None, 0.9),
                width=40,
                source=SelectorDeIconos.iconoderostro(resultado.captura.rostro)
            )
        )
        with rostro.canvas.before:
            Color(firstrowcolor[0], firstrowcolor[1], firstrowcolor[2])
            rostro.rect = Rectangle(size=self.size, pos=self.pos)
        rostro.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(rostro)

        label = Label(text="Mirada", size_hint=(None, 1), width=100)
        with label.canvas.before:
            Color(secondrowcolor[0], secondrowcolor[1], secondrowcolor[2])
            label.rect = Rectangle(size=self.size, pos=self.pos)
        label.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(label)

        mirada = BoxLayout(orientation='horizontal')
        mirada.add_widget(Label(text=resultado.captura.mirada.name))
        mirada.add_widget(
            Image(
                size_hint=(None, 0.9),
                width=40,
                source=SelectorDeIconos.iconodemirada(resultado.captura.mirada)
            )
        )
        with mirada.canvas.before:
            Color(secondrowcolor[0], secondrowcolor[1], secondrowcolor[2])
            mirada.rect = Rectangle(size=self.size, pos=self.pos)
        mirada.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(mirada)

        label = Label(text="Cabeza", size_hint=(None, 1), width=100)
        with label.canvas.before:
            Color(firstrowcolor[0], firstrowcolor[1], firstrowcolor[2])
            label.rect = Rectangle(size=self.size, pos=self.pos)
        label.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(label)

        cabeza = BoxLayout(orientation='horizontal')
        cabeza.add_widget(Label(text=resultado.captura.cabeza.name))
        cabeza.add_widget(
            Image(
                size_hint=(None, 0.9),
                width=40,
                source=SelectorDeIconos.iconodecabeza(resultado.captura.cabeza)
            )
        )
        with cabeza.canvas.before:
            Color(firstrowcolor[0], firstrowcolor[1], firstrowcolor[2])
            cabeza.rect = Rectangle(size=self.size, pos=self.pos)
        cabeza.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(cabeza)

        label = Label(text="Brazos", size_hint=(None, 1), width=100)
        with label.canvas.before:
            Color(secondrowcolor[0], secondrowcolor[1], secondrowcolor[2])
            label.rect = Rectangle(size=self.size, pos=self.pos)
        label.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(label)

        brazos = BoxLayout(orientation='horizontal')
        brazos.add_widget(Label(text=resultado.captura.posicionbrazos.name))
        brazos.add_widget(
            Image(
                size_hint=(None, 0.9),
                width=40,
                source=SelectorDeIconos.iconodebrazos(resultado.captura.posicionbrazos)
            )
        )
        with brazos.canvas.before:
            Color(secondrowcolor[0], secondrowcolor[1], secondrowcolor[2])
            brazos.rect = Rectangle(size=self.size, pos=self.pos)
        brazos.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(brazos)

        label = Label(text="Volumen de Voz", size_hint=(None, 1), width=100)
        with label.canvas.before:
            Color(firstrowcolor[0], firstrowcolor[1], firstrowcolor[2])
            label.rect = Rectangle(size=self.size, pos=self.pos)
        label.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(label)

        volumen = BoxLayout(orientation='horizontal')
        volumen.add_widget(Label(text=str(resultado.captura.volumendevoz)))
        volumen.add_widget(
            Image(
                size_hint=(None, 0.9),
                width=40,
                source=SelectorDeIconos.iconodevolumen(resultado.captura.volumendevoz)
            )
        )
        with volumen.canvas.before:
            Color(firstrowcolor[0], firstrowcolor[1], firstrowcolor[2])
            volumen.rect = Rectangle(size=self.size, pos=self.pos)
        volumen.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(volumen)

        label = Label(text="Palabras por minuto", size_hint=(None, 1), width=100)
        with label.canvas.before:
            Color(secondrowcolor[0], secondrowcolor[1], secondrowcolor[2])
            label.rect = Rectangle(size=self.size, pos=self.pos)
        label.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(label)

        velocidad = BoxLayout(orientation='horizontal')
        velocidad.add_widget(Label(text=str(resultado.captura.palabrasporsegundo)))
        velocidad.add_widget(
            Image(
                size_hint=(None, 0.9),
                width=40,
                source=SelectorDeIconos.iconodevelocidad(resultado.captura.palabrasporsegundo)
            )
        )
        with velocidad.canvas.before:
            Color(secondrowcolor[0], secondrowcolor[1], secondrowcolor[2])
            velocidad.rect = Rectangle(size=self.size, pos=self.pos)
        velocidad.bind(pos=WidgetCreator.update_rect, size=WidgetCreator.update_rect)
        grid.add_widget(velocidad)

        content.add_widget(grid)

        box = BoxLayout()
        box.add_widget(
            Label(text=f"Interpretación: {resultado.interpretacion.lectura}", size_hint=(1.0, None), height=20))
        content.add_widget(box)


        scrollableInfo = ScrollView(size_hint=(1.0, 1.0))
        scrollableInfo.add_widget(Label(text=f"{resultado.interpretacion.masinfo}"))
        content.add_widget(scrollableInfo)
        self.add_widget(content)
