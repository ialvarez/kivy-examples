from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App

import random


class DecisionLabel(Label):
    pass


class YesLabel(Label):
    pass


class NoLabel(Label):
    pass


class ProgressList(BoxLayout):
    total = NumericProperty(25)
    colored = NumericProperty(0)

    def generate(self, label_type):
        self.clear_widgets()

        if label_type == 'yes':
            yes_no_label = YesLabel
        if label_type == 'no':
            yes_no_label = NoLabel

        for _ in range(0, self.total - self.colored):
            self.add_widget(Label())
        for _ in range(self.total - self.colored, self.total):
            self.add_widget(yes_no_label())


class DecisionRoot(BoxLayout):
    done = BooleanProperty(True)

    def set_up(self):
        self.ids.result.text = ' '

        self.ids.yes.colored = 0
        self.ids.yes.generate('yes')

        self.ids.no.colored = 0
        self.ids.no.generate('no')

    def start(self):
        self.ids.start.text = 'wait...'

        try:
            self.remove_widget(self.ids.welcome)
        except ReferenceError:
            pass

        if self.done:
            self.done = False
            self.set_up()
            Clock.schedule_interval(self.increment, 1.0/10)

    def increment(self, dt):
        r = random.randint(0, 1)
        if r == 0:
            option = 'yes'
        if r == 1:
            option = 'no'

        self.ids[option].colored += 1
        self.ids[option].generate(option)

        if self.ids[option].colored == self.ids[option].total:
            self.done = True
            self.ids.result.text = option.upper()
            self.ids.start.text = 'START'
            return False


class UniversalDecisionMakerApp(App):
    root = ObjectProperty()

    def build(self):
        return DecisionRoot()

if __name__ == "__main__":
    UniversalDecisionMakerApp().run()
