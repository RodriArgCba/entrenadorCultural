from kivymd.uix.label import MDLabel as Label, MDIcon
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.utils import get_color_from_hex as getcolor
from kivy.factory import Factory
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout as BoxLayout
from kivymd.uix.button import MDTextButton as Button, MDIconButton as IconButton

textColor = '000000'
spinnerBackColor = 'e0e0e0'


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
    def newlabel(innertext, **kwargs):
        label = Label(
            color=getcolor(textColor),
            text=innertext,
            markup=True,
            **kwargs
        )
        label.height = 44
        label.bind(size=label.setter('text_size'))
        return label

    @staticmethod
    def newspinner(innertext, values):
        spinner = Spinner(
            color=getcolor(textColor),
            text=innertext,
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
    def newmdicon(iconname, **kwargs):
        image = BoxLayout(
            padding=5,
            size_hint=(0.1, 0.1)
        )
        image.add_widget(MDIcon(
            icon=iconname,
            **kwargs
        ))
        return image

    @staticmethod
    def newicon(source) -> Image:
        image = BoxLayout(
            padding=5,
            size_hint=(0.1, 0.1)
        )
        image.add_widget(Image(source=source))
        return image

    @staticmethod
    def newimage(source, size=(0.4, 1)) -> Image:
        image = BoxLayout(
            size_hint=size
        )
        image.add_widget(Image(source=source))
        return image

    @staticmethod
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

    @staticmethod
    def newiconbutton(text, color="Primary"):
        button = IconButton(
            height=44,
            size_hint=(0.7, None),
            icon=text,
            theme_text_color=color
        )
        return button

    @staticmethod
    def update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
