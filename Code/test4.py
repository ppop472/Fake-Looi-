from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle

# Eye
class CenterCircle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 200
        border_width = 2  # Adjust the border 

# Pupil
class Midddlecircle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 200
        border_width = 2  # Adjust the border 

        # Border
        with self.canvas:
            # Border Color
            Color(0, 0, 0) 
            self.border = Ellipse(pos=(self.center_x - self.radius - border_width,
                                       self.center_y - self.radius - border_width),
                                  size=(2 * (self.radius + border_width), 2 * (self.radius + border_width)))

            # Draw the circle in the center
            Color(1, 1, 1)  # White color for the circle (R, G, B)
            self.circle = Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius),
                                  size=(2 * self.radius, 2 * self.radius))

    def on_size(self, *args):
        # Update the positions and sizes when the widget size changes
        border_width = 5  # Adjust the border width as needed
        self.border.pos = (self.center_x - self.radius - border_width, self.center_y - self.radius - border_width)
        self.border.size = (2 * (self.radius + border_width), 2 * (self.radius + border_width))

        self.circle.size = (2 * self.radius, 2 * self.radius)
        self.circle.pos = (self.center_x - self.radius, self.center_y - self.radius)


class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Green background
        with self.canvas.before:
            Color(0, 0.70, 0)  # Green color for the background (R, G, B)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        center_circle = CenterCircle()
        self.add_widget(center_circle)

    def on_size(self, *args):
        self.rect.size = self.size


class MyApp(App):
    def build(self):
        return MyFloatLayout()


if __name__ == '__main__':
    MyApp().run()
