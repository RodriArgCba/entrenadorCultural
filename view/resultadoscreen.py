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
from view.widgetsmethods import WidgetCreator

backgroundColor = '6A3192'
subdivisionColor = [0.58, 0.337, 0.639]
padding = [45, 0, 45, 10]
textcolor = (1, 1, 1, 1)


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
        content = BoxLayout()
        # content = BoxLayout(halign='left', valign="middle")
        content.orientation = 'vertical'
        content.add_widget(Label(text=f"{fase.nombre}", size_hint=(1.0, None), height=20))
        content.add_widget(Label(text="Captura de usuario:", size_hint=(1.0, None), height=20))

        grid = GridLayout(cols=2, row_force_default=True, row_default_height=40, size_hint=(1.0, None), height=240)

        grid.add_widget(Label(text="Rostro", size_hint=(None, 1), width=100))
        rostro = BoxLayout(orientation='horizontal')
        rostro.add_widget(Label(text=resultado.captura.rostro.name))
        rostro.add_widget(Image(size_hint=(None, 0.9), width=40, source='assets/Sonriendo.png'))
        grid.add_widget(rostro)

        grid.add_widget(Label(text="Mirada", size_hint=(None, 1), width=100))
        mirada = BoxLayout(orientation='horizontal')
        mirada.add_widget(Label(text=resultado.captura.mirada.name))
        mirada.add_widget(Image(size_hint=(None, 0.9), width=40, source='assets/Sonriendo.png'))
        grid.add_widget(mirada)

        grid.add_widget(Label(text="Cabeza", size_hint=(None, 1), width=100))
        cabeza = BoxLayout(orientation='horizontal')
        cabeza.add_widget(Label(text=resultado.captura.cabeza.name))
        cabeza.add_widget(Image(size_hint=(None, 0.9), width=40, source='assets/Sonriendo.png'))
        grid.add_widget(cabeza)

        grid.add_widget(Label(text="Brazos", size_hint=(None, 1), width=100))
        brazos = BoxLayout(orientation='horizontal')
        brazos.add_widget(Label(text=resultado.captura.posicionbrazos.name))
        brazos.add_widget(Image(size_hint=(None, 0.9), width=40, source='assets/Sonriendo.png'))
        grid.add_widget(brazos)

        grid.add_widget(Label(text="Volumen de Voz", size_hint=(None, 1), width=100))
        volumen = BoxLayout(orientation='horizontal')
        volumen.add_widget(Label(text=str(resultado.captura.volumendevoz)))
        volumen.add_widget(Image(size_hint=(None, 0.9), width=40, source='assets/Sonriendo.png'))
        grid.add_widget(volumen)

        grid.add_widget(Label(text="Palabras por minuto", size_hint=(None, 1), width=100))
        velocidad = BoxLayout(orientation='horizontal')
        velocidad.add_widget(Label(text=str(resultado.captura.palabrasporsegundo)))
        velocidad.add_widget(Image(size_hint=(None, 0.9), width=40, source='assets/Sonriendo.png'))
        grid.add_widget(velocidad)

        content.add_widget(grid)

        content.add_widget(
            Label(text=f"Interpretación: {resultado.interpretacion.lectura}", size_hint=(1.0, None), height=20))

        scrollableInfo = ScrollView(size_hint=(1.0, 1.0))
        scrollableInfo.add_widget(Label(text=f"{resultado.interpretacion.masinfo}"))
        content.add_widget(scrollableInfo)
        self.add_widget(content)
