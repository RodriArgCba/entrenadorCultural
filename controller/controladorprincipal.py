import kivy
from kivy.uix.screenmanager import ScreenManager
from model.conversacion import Conversacion
from model.culturaobjetivo import CulturaObjetivo
from view.menuprincipal import MenuPrincipal
from kivy.app import App

kivy.require('1.11.1')

culturaseleccionada = CulturaObjetivo(nombre="Japonesa")
conversacionseleccionada = Conversacion(
    nombre="Saludo y Presentaciones",
    duracion=120.0,
    culturaobjetivo=culturaseleccionada
)


class EntrenadorCulturalApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(name="menu"))
        return sm

