from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.button import Button
from kivy.clock import Clock
import time

class Eye(Widget):
    def __init__(self, pupil_color=(0, 0, 0, 1), pupil_position=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.radius = 100
        self.pupil_position = pupil_position
        with self.canvas:
            # Draw the outer circle (border)
            Color(0, 1, 0 )  # Black color for the border
            self.border = Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius),
                                  size=(2 * self.radius, 2 * self.radius))
            # Draw the inner circle (eye)
            Color(0.1, 1, 0.2)  # White color for the eye
            self.iris = Ellipse(pos=(self.center_x - self.radius + 10, self.center_y - self.radius + 10),
                                size=(2 * (self.radius - 10), 2 * (self.radius - 10)))
            
            # Pupil
            Color(*pupil_color)  # Set pupil color
            self.pupil_radius = 20
            self.pupil = Ellipse(pos=(self.center_x + pupil_position[0] - self.pupil_radius,
                                       self.center_y + pupil_position[1] - self.pupil_radius),
                                 size=(3 * self.pupil_radius, 6 * self.pupil_radius))

    def on_size(self, *args):
        self.border.size = (2 * self.radius, 2 * self.radius)
        self.border.pos = (self.center_x - self.radius, self.center_y - self.radius)

        self.iris.size = (2 * (self.radius - 10), 2 * (self.radius - 10))
        self.iris.pos = (self.center_x - self.radius + 10, self.center_y - self.radius + 10)

        self.pupil.size = (3 * self.pupil_radius, 6 * self.pupil_radius)
        self.pupil.pos = (self.center_x + self.pupil_position[0] - 1.5 * self.pupil_radius,
                          self.center_y + self.pupil_position[1] - 3 * self.pupil_radius)


class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.button = Button(text='Middel Button', size_hint=(None, None), size=(100, 50),
                        pos_hint={'x': 0, 'y': 0.90})
        self.button.bind(on_press=self.on_button_click)

        self.button2 = Button(text='Boven Middel Button', size_hint=(None, None), size=(100, 50),
                        pos_hint={'x': 0.5, 'y': 0.90})
        self.button2.bind(on_press=self.on_button2_click)
        
        # Set background color
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Left eye
        self.left_eye = Eye(pupil_color=(0, 0, 0, 1), pupil_position=(0, 0))
        self.left_eye.center_x = self.width * -1.5
        self.add_widget(self.left_eye)

        # Right eye
        self.right_eye = Eye(pupil_color=(0, 0, 0, 1), pupil_position=(0, 0))
        self.right_eye.center_x = self.width * 2.5
        self.add_widget(self.right_eye)

        self.add_widget(self.button)

        self.add_widget(self.button2)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_button_click(self, instance):
        # Move the pupil of the right eye to (50, 50)
        self.right_eye.pupil.pos = (self.right_eye.center_x + -76 - self.right_eye.pupil_radius,
                                     self.right_eye.center_y - 3 * self.right_eye.pupil_radius)
        
        self.left_eye.pupil.pos = (self.left_eye.center_x + 56 - self.left_eye.pupil_radius,
                                     self.left_eye.center_y - 3 * self.left_eye.pupil_radius)
        
        # update oog
        self.right_eye.canvas.ask_update()
        self.left_eye.canvas.ask_update()
        # reset ahahhaha
        Clock.schedule_once(self.reset_pupil_position, 0.3)

    def on_button2_click(self, instance):
        # Move the pupil of the right eye to (50, 50)
        self.right_eye.pupil.pos = (self.right_eye.center_x + -76 - self.right_eye.pupil_radius,
                                     self.right_eye.center_y - 2 * self.right_eye.pupil_radius)
        
        self.left_eye.pupil.pos = (self.left_eye.center_x + 56 - self.left_eye.pupil_radius,
                                     self.left_eye.center_y - 2 * self.left_eye.pupil_radius)
        
        # update oog
        self.right_eye.canvas.ask_update()
        self.left_eye.canvas.ask_update()
        # reset ahahhaha
        Clock.schedule_once(self.reset_pupil_position, 0.3)

    def reset_pupil_position(self, dt):
        # Move the pupil of the right eye back to (0, 0)
        self.right_eye.pupil.pos = (self.right_eye.center_x - 1.5 * self.right_eye.pupil_radius,
                                     self.right_eye.center_y - 3 * self.right_eye.pupil_radius)
        
        self.left_eye.pupil.pos = (self.left_eye.center_x - 1.5 * self.left_eye.pupil_radius,
                                     self.left_eye.center_y - 3 * self.left_eye.pupil_radius)
        # Redraw the right eye widget
        self.right_eye.canvas.ask_update()
        self.left_eye.canvas.ask_update()


class MyApp(App):
    def build(self):
        return MyFloatLayout()


if __name__ == '__main__':
    MyApp().run()