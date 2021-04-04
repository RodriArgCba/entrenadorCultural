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
        self.orientation = 'vertical'
        self.padding = padding
        table = MDDataTable(column_data=[
            ("Food", dp(30))
        ])
        self.add_widget(table)
