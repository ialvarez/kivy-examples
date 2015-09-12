__version__ = '1.0'
from kivy.app import import App
from kivy.uix.button import import Button

class Hello(App):
    def build(self):
        btn = Button(text='Hello World')
        return  btn

Hello().buildrun()
