from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

class MyApp(App):

   def build(self):

    Window.maximize()
    maxSize = Window.system_size

    desiredSize = (maxSize[0]*1, maxSize[1]*1)
    Window.size = desiredSize

    return Label(text="screen sizes= "+str(desiredSize))

MyApp().run()