from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemLabel
from kivy.uix.listview import ListView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.clock import Clock

import time


class TimeClockLabel(Label):
    def update(self, *args):
        self.text = time.asctime()


class TimeClockButton(Button):
    def __init__(self, **kwargs):
        super(TimeClockButton, self).__init__(**kwargs)
        self.app = TimeClockApp.get_running_app()
        self.bind(on_press=self.add_time)

    def add_time(self, instance):
        self.app.time_list.append(self.app.time_clock.ids.clock.text)
        self.app.time_clock.ids.entries.refresh()


class TimeClockListItem(BoxLayout, ListItemLabel):
    content = StringProperty()


class TimeClockList(BoxLayout):
    list_view = ObjectProperty()

    def __init__(self, **kwargs):
        super(TimeClockList, self).__init__(**kwargs)
        self.app = TimeClockApp.get_running_app()

        self.list_view = ListView(adapter=self.create_list_adapter())
        self.add_widget(self.list_view)

    def roster_converter(self, index, value):
        return {'content': value}

    def create_list_adapter(self, data=[]):
        return ListAdapter(data=data,
                           args_converter=self.roster_converter,
                           cls=TimeClockListItem)

    def refresh(self):
        self.remove_widget(self.list_view)
        data = reversed(self.app.time_list)
        self.list_view = ListView(adapter=self.create_list_adapter(data))
        self.add_widget(self.list_view)


class TimeClockRoot(BoxLayout):
    pass


class TimeClockApp(App):
    time_list = ObjectProperty([])
    time_clock = ObjectProperty()

    def build(self):
        self.time_clock = TimeClockRoot()
        Clock.schedule_interval(self.time_clock.ids.clock.update, 1)
        return self.time_clock


TimeClockApp().run()
