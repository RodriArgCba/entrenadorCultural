from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.utils import get_color_from_hex as getcolor
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

textColor = 'ffffff'
spinnerBackColor = 'af7ead'


class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super(CustomSpinnerOption, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = getcolor(spinnerBackColor)
        self.color = getcolor(textColor)
        self.padding_x = 5
        self.bind(size=self.setter('text_size'))
        self.halign = 'left'
        self.valign = 'middle'
        self.height = 35


class WidgetCreator:

    @staticmethod
    def newlabel(innertext, valign='bottom'):
        label = Label(
            text='[color=' + textColor + ']' + innertext + '[/color]',
            size_hint=(1.0, None),
            halign='left',
            valign=valign,
            markup=True
        )
        label.height = 44
        label.bind(size=label.setter('text_size'))
        return label

    @staticmethod
    def newspinner(innertext, values):
        spinner = Spinner(
            text='[color=' + textColor + ']' + innertext + '[/color]',
            values=values,
            height=44,
            size_hint=(0.7, None),
            halign='left',
            valign='middle',
            padding_x=5,
            option_cls=Factory.get('CustomSpinnerOption')
        )
        spinner.height = 35
        spinner.bind(size=spinner.setter('text_size'))
        spinner.background_normal = ''
        spinner.background_color = getcolor(spinnerBackColor)
        spinner.markup = True
        return spinner

    @staticmethod
    def newicon(source) -> Image:
        image = BoxLayout(
            padding=5,
            size_hint=(0.1, 0.1)
        )
        image.add_widget(Image(source=source))
        return image

    def newbutton(text):
        button = Button(
            height=44,
            size_hint=(0.7, None),
            text=text,
            halign='center',
            valign='middle',
        )
        button.bind(size=button.setter('text_size'))
        return button