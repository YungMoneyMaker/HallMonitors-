#Import Kivy Packages
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
import kivy.utils

#References the ImageButton in main.py
#Gives the images the properties of a button
class ImageButton(ButtonBehavior, Image):
    pass


class ImageButtonSelectable(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButtonSelectable, self).__init__(**kwargs)
        #Changing properties of the button
        with self.canvas.before:
            #Setting background color of the button
            self.canvas_color = Color(rgb=(kivy.utils.get_color_from_hex("#35477d")))
            #Settings size of the button
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[5,])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(state=self.update_color)

    #Updating color of button on press
    def update_color(self, *args):
        #Updating the state of the button
        print("self.canvas_Color: ", self.canvas_color.rgb)
        print("STATE IS ", self.state)
        print("self.canvas_Color: ", self.canvas_color.rgb)
        if self.state == 'normal':
            self.canvas_color = Color(rgb=(kivy.utils.get_color_from_hex("#35477d")))
        else:
            self.canvas_color = Color(rgb=(kivy.utils.get_color_from_hex("#6C5B7B")))
        with self.canvas.before:
            Color(rgb=self.canvas_color.rgba)#self.canvas_color = Color(rgb=(kivy.utils.get_color_from_hex("#FFFFFF")))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[5,])

    #On release change button back to normal
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


#Assign LabelButton class the behaviour of a button
class LabelButton(ButtonBehavior, Label):
    pass
