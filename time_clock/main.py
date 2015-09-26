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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlite_ex import TimeClockTable, Base
from time_aux import TimeAux

import time


class TimeClockHeader(Label):
    pass


class TimeClockLabel(Label):
    pass


class TimeClockStatus(BoxLayout):
    pass


class TimeClockButton(Button):
    def __init__(self, **kwargs):
        super(TimeClockButton, self).__init__(**kwargs)
        self.app = TimeClockApp.get_running_app()
        self.bind(on_press=self.add_time)

    def add_time(self, instance):
        time_stamp = self.app.time_aux.time_stamp()
        self.app.add_new(time_stamp=time_stamp, action=instance.text)
        self.app.time_clock.ids.entries.generate_list_view()


class TimeClockListItem(BoxLayout, ListItemLabel):
    content = StringProperty()


class TimeClockList(BoxLayout):
    list_view = ObjectProperty()

    def __init__(self, **kwargs):
        super(TimeClockList, self).__init__(**kwargs)

        self.app = TimeClockApp.get_running_app()
        self.generate_list_view()

    def roster_converter(self, index, value):
        color = (0, 1, 0, 1) if value.action == 'in' else (1, 0, 0, 1)
        return {
            'content': value.time_stamp,
            'color': color,
        }

    def generate_list_view(self):
        if self.list_view:
            self.remove_widget(self.list_view)

        data = reversed([d for d in self.app.get_all()])

        adapter = ListAdapter(data=data,
                              args_converter=self.roster_converter,
                              cls=TimeClockListItem)

        self.list_view = ListView(adapter=adapter)
        self.add_widget(self.list_view)


class TimeClockRoot(BoxLayout):
    pass


class TimeClockApp(App):
    session = ObjectProperty()
    time_clock = ObjectProperty()
    time_aux = ObjectProperty()

    def build(self):
        engine = create_engine('sqlite:///time_clock.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.time_aux = TimeAux()
        self.time_clock = TimeClockRoot()
        Clock.schedule_interval(self.update, 1)
        return self.time_clock

    def update(self, dt):
        self.time_aux.update()

    def get_all(self):
        return self.session.query(TimeClockTable).all()

    def add_new(self, time_stamp, action):
        self.session.add(TimeClockTable(time_stamp=time_stamp, action=action))
        self.session.commit()

    def current_date(self):
        return self.time_aux.current_date()


TimeClockApp().run()
