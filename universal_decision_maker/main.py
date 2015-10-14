from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App

import random


class YesLabel(Label):
    pass


class NeutralLabel(Label):
    pass


class NoLabel(Label):
    pass


class ProgressList(BoxLayout):
    total = NumericProperty(25)
    colored = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ProgressList, self).__init__(**kwargs)

    def generate(self, label_type):
        self.clear_widgets()
        for _ in range(0, self.total - self.colored):
            self.add_widget(NeutralLabel())
        for _ in range(self.total - self.colored, self.total):
            self.add_widget(label_type())


class DecisionRoot(BoxLayout):
    done = BooleanProperty(True)

    def set_up(self):
        self.ids.result.text = ''
        self.ids.yes.colored = 0
        self.ids.no.colored = 0
        self.ids.yes.generate(YesLabel)
        self.ids.no.generate(NoLabel)

    def start(self):
        self.ids.start.text = 'wait...'
        if self.done:
            self.done = False
            self.set_up()
            Clock.schedule_interval(self.increment, 0.15)

    def increment(self, dt):
        r = random.randint(0, 1)
        options = ['yes', 'no']
        labels = [YesLabel, NoLabel]

        option = self.ids[options[r]]

        option.colored += 1
        option.generate(labels[r])
        if option.colored == option.total:
            self.ids.result.text = options[r].upper()
            self.done = True
            self.ids.start.text = 'START'
            return False


class UniversalDecisionMakerApp(App):
    root = ObjectProperty()

    def build(self):
        root = DecisionRoot()
        root.set_up()
        return root

if __name__ == "__main__":
    UniversalDecisionMakerApp().run()
