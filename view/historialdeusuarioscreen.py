from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

backgroundColor = '6A3192'
subdivisionColor = [0.58, 0.337, 0.639]
padding = [45, 0, 45, 10]


class HistorialDeUsuario(Screen):
    def __init__(self, data, **kwargs):
        super(HistorialDeUsuario, self).__init__(**kwargs)
        self.add_widget(HistorialDeUsuarioLayout(data))

    def updatedata(self, data):
        pass


class HistorialDeUsuarioLayout(BoxLayout):
    def __init__(self, data, **kwargs):
        super(HistorialDeUsuarioLayout, self).__init__(**kwargs)
        self.data = data
        self.orientation = 'vertical'
        self.padding = padding
        row_data = []
        for simulacion in data:
            tupla = (simulacion.id,
                     str(simulacion.fecha),
                     simulacion.conversacion.culturaobjetivo.nombre,
                     simulacion.conversacion.nombre,
                     simulacion.calificaciondeusuario, "Detalles")
            row_data.append(tupla)
        table = MDDataTable(column_data=[
            ("", dp(10)),
            ("FECHA", dp(30)),
            ("CULTURA OBJETIVO", dp(30)),
            ("CONVERSACIÓN", dp(30)),
            ("RESULTADO", dp(20)),
            ("", dp(30))
        ], row_data=row_data)
        table.bind(on_row_press=self.detallesdesimulacion)
        self.add_widget(table)

    def detallesdesimulacion(self, table, row):
        for simulacion in self.data:
            if simulacion.id == int(row.Index):
                from controller.controladorprincipal import ControladorPrincipal
                ControladorPrincipal().detallesdesimulacion(simulacion)