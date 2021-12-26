import threading
from kivy.core.window import Window
from kivy.uix.widget import Widget
from controller.dbcontroller import simulacionporid

selectorderesultado = {'f': 1, 'g': 2, 'h': 3, 'j': 4}


class ForzarResultadoController(Widget):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with threading.Lock():
                if cls._instance is None:
                    cls._instance = super(ForzarResultadoController, cls).__new__(cls)
                    print('Creating the object')
                    cls._instance._keyboard = Window.request_keyboard(
                        cls._instance._keyboard_closed, cls._instance, 'text')
                    if cls._instance._keyboard.widget:
                        # If it exists, this widget is a VKeyboard object which you can use
                        # to change the keyboard layout.
                        pass
                    cls._instance._keyboard.bind(on_key_down=cls._instance._on_keyboard_down)
        return cls._instance

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()
        elif text in selectorderesultado:
            self.forzarresultado(selectorderesultado[text])
        return True

    def forzarresultado(self, idsimulacion):
        from controller.controladorprincipal import ControladorPrincipal
        simulacion = simulacionporid(idsimulacion)
        simulacion.calcularcalificacion()
        controladorprincipal = ControladorPrincipal()
        if hasattr(controladorprincipal, 'pantallasimulacion'):
            if not controladorprincipal.pantallasimulacion.layout.simulacionfinalizada:
                controladorprincipal.cancelarsimulacion()
        controladorprincipal.detallesdesimulacion(simulacion)
