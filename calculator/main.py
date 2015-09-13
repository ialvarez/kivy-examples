from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class CalculatorNumbers(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(**kwargs)
        self.generate_numbers()

    def generate_numbers(self):
        numbers = [7, 8, 9, 4, 5, 6, 1, 2, 3, 0]
        number_row = BoxLayout()
        for number in numbers:
            button = Button(text=str(number))
            number_row.add_widget(button)
        self.add_widget(number_row)


class CalculatorDisplay(Label):
    pass


class CalculatorRoot(BoxLayout):
    pass


class CalculatorApp(App):
    def build(self):
        calculator = CalculatorRoot()
        return calculator

CalculatorApp().run()
