from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.properties import ObjectProperty


class CalculatorDisplay(Label):
    pass


class CalculatorNumbers(BoxLayout):
    def __init__(self, **kwargs):
        super(CalculatorNumbers, self).__init__(**kwargs)
        self.app = CalculatorApp.get_running_app()

    def add_numbers(self):
        numbers = [[7, 8, 9],
                   [4, 5, 6],
                   [1, 2, 3],
                   [0]]

        while(numbers):
            numbers_row = BoxLayout()
            for number in numbers.pop(0):
                n = Button(text=str(number))
                n.bind(on_press=self.add_to_display)
                numbers_row.add_widget(n)
            self.add_widget(numbers_row)

    def add_to_display(self, instance):
        self.app.calculator.ids.display.text += instance.text


class CalculatorRoot(BoxLayout):
    def generate(self):
        self.ids.numbers.add_numbers()


class CalculatorApp(App):
    calculator = ObjectProperty()

    def build(self):
        self.calculator = CalculatorRoot()
        self.calculator.generate()
        return self.calculator

CalculatorApp().run()
