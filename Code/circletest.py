from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.button import Button

class Eye(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = 100
        with self.canvas:
            # Draw the outer circle (border)
            Color(0, 0, 0)  # Black color for the border
            self.border = Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius),
                                  size=(2 * self.radius, 2 * self.radius))
            # Draw the inner circle (eye)
            Color(0.1, 1, 0.2)  # White color for the eye
            self.iris = Ellipse(pos=(self.center_x - self.radius + 10, self.center_y - self.radius + 10),
                                size=(2 * (self.radius - 10), 2 * (self.radius - 10)))
            
            #pupil
            Color(0, 0, 0, 1)  # Black color for the pupil
            self.pupil_radius = 20
            self.pupil = Ellipse(pos=(self.center_x - self.pupil_radius, self.center_y - self.pupil_radius),
                                  size=(2 * self.pupil_radius, 2 * self.pupil_radius))

    def on_size(self, *args):
        self.border.size = (2 * self.radius, 2 * self.radius)
        self.border.pos = (self.center_x - self.radius, self.center_y - self.radius)

        self.iris.size = (2 * (self.radius - 10), 2 * (self.radius - 10))
        self.iris.pos = (self.center_x - self.radius + 10, self.center_y - self.radius + 10)

        self.pupil.size = (3 * self.pupil_radius, 6 * self.pupil_radius)
        self.pupil.pos = (self.center_x - self.pupil_radius * 1.5, self.center_y - self.pupil_radius * 3)


class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set background color
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        #ogen (* ￣3)(ε￣ *)
        left_eye = Eye() 
        right_eye = Eye()
        left_eye.center_x = self.width * -1.5
        right_eye.center_x = self.width * 2.50

        
        
        self.add_widget(left_eye)
        self.add_widget(right_eye)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MyApp(App):
    def build(self):
        return MyFloatLayout()


if __name__ == '__main__':
    MyApp().run()
