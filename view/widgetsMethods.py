from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.utils import get_color_from_hex as getColor
from kivy.factory import Factory

textColor = 'ffffff'

class customSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super(customSpinnerOption, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = getColor('9456A3')
        self.color = getColor(textColor)
        self.padding_x = 5
        self.bind(size=self.setter('text_size'))
        self.halign = 'left'
        self.valign = 'middle'
        self.height = 35

class WidgetCreator():
    def newLabel(self,innerText):
        label = Label(
            text='[color=' + textColor + ']' + innerText + '[/color]',
            size_hint=(1.0, None),
            halign='left',
            valign='middle',
            markup=True
        )
        label.height = 35
        label.bind(size=label.setter('text_size'))
        return label

    def newSpinner(self, innerText, values):
        spinner = Spinner(
            text='[color=' + textColor + ']' + innerText + '[/color]',
            values=values,
            height=44,
            size_hint=(1.0, None),
            halign='left',
            valign='middle',
            padding_x=5,
            option_cls=Factory.get('customSpinnerOption')
        )
        spinner.height = 35
        spinner.bind(size=spinner.setter('text_size'))
        spinner.background_normal = ''
        spinner.background_color = getColor('9456A3')
        spinner.markup = True
        return spinner

WidgetCreator = WidgetCreator()