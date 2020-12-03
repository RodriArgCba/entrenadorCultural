import kivy.app
kivy.require('1.11.1')
from view.menuprincipal import MenuPrincipal



from kivy.app import App


class EntrenadorCulturalApp(App):
    def build(self):
        return MenuPrincipal()

if __name__ == '__main__':
    EntrenadorCulturalApp().run()