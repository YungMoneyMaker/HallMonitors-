import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import turtle
import math
import random
import time

class MyGrid(Widget):
    start = ObjectProperty(None)
    end = ObjectProperty(None)
    
    def btn(self):
        print(self.start.text)


class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()
