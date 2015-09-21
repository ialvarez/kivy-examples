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

from sqlite_ex import TimeClock, Base

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
        time_stamp = self.app.time_clock.ids.clock.text
        new_time_clock = TimeClock(time_stamp=time_stamp, action=instance.text)
        self.app.session.add(new_time_clock)
        self.app.session.commit()
        self.app.time_clock.ids.entries.refresh()


class TimeClockListItem(BoxLayout, ListItemLabel):
    content = StringProperty()


class TimeClockList(BoxLayout):
    list_view = ObjectProperty()

    def __init__(self, **kwargs):
        super(TimeClockList, self).__init__(**kwargs)
        self.app = TimeClockApp.get_running_app()
        self.refresh()

    def roster_converter(self, index, value):
        if value.action == 'in':
            color = (0, 1, 0, 1)
        else:
            color = (1, 0, 0, 1)
        return {
            'content': value.time_stamp,
            'color': color,
        }

    def create_list_adapter(self, data=[]):
        return ListAdapter(data=data,
                           args_converter=self.roster_converter,
                           cls=TimeClockListItem)

    def refresh(self):
        if self.list_view:
            self.remove_widget(self.list_view)

        data = []
        for d in self.app.session.query(TimeClock).all():
            data.append(d)
        data = reversed(data)

        self.list_view = ListView(adapter=self.create_list_adapter(data))
        self.add_widget(self.list_view)


class TimeClockRoot(BoxLayout):
    pass


class TimeClockApp(App):
    time_clock = ObjectProperty()
    session = ObjectProperty()

    def build(self):
        self.init_db()
        self.time_clock = TimeClockRoot()
        Clock.schedule_interval(self.time_clock.ids.clock.update, 1)
        return self.time_clock

    def init_db(self):
        engine = create_engine('sqlite:///time_clock.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()



TimeClockApp().run()
