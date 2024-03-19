from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import time
import math

#--------------------------------- Eye class --------------------------------------------------------------------------

class Eye(Widget):
    def __init__(self, pupil_color=(0, 0, 0, 1), pupil_position=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.radius = 100
        self.pupil_position = list(pupil_position)  # Convert tuple to list for easier modification
        with self.canvas:
            # Draw the outer circle (border)
            Color(0, 1, 0)  # Black color for the border
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

    def on_size(self, *args): # entire img 
        self.border.size = (2 * self.radius, 2 * self.radius)
        self.border.pos = (self.center_x - self.radius, self.center_y - self.radius)

        self.iris.size = (2 * (self.radius - 10), 2 * (self.radius - 10))
        self.iris.pos = (self.center_x - self.radius + 10, self.center_y - self.radius + 10)

        self.pupil.size = (3 * self.pupil_radius, 6 * self.pupil_radius)
        self.pupil.pos = (self.center_x + self.pupil_position[0] - 1.5 * self.pupil_radius,
                          self.center_y + self.pupil_position[1] - 3 * self.pupil_radius)
        
#-----------------------------------------------------------------------------------------------------------------------

#-------------------------------------------- Main function ------------------------------------------------------------


class MyFloatLayout(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movement_in_progress = False  # Variable to track movement state
        
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

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_touch_move(self, touch):
        # Get the position of the touch
        touch_x, touch_y = touch.pos

        # Update the position of the pupils
        self.update_pupils(touch_x, touch_y)

    def update_pupils(self, touch_x, touch_y):
        # Calculate the distance and angle of the touch relative to the center of each eye
        left_eye_distance = math.sqrt((touch_x - self.left_eye.center_x) ** 2 + (touch_y - self.left_eye.center_y) ** 2)
        left_eye_angle = math.atan2(touch_y - self.left_eye.center_y, touch_x - self.left_eye.center_x)
    
        right_eye_distance = math.sqrt((touch_x - self.right_eye.center_x) ** 2 + (touch_y - self.right_eye.center_y) ** 2)
        right_eye_angle = math.atan2(touch_y - self.right_eye.center_y, touch_x - self.right_eye.center_x)

        # Ensure the pupils stay within the eye boundaries
        max_distance = self.left_eye.radius - self.left_eye.pupil_radius
        if left_eye_distance > max_distance:
            left_eye_distance = max_distance
        max_distance = self.right_eye.radius - self.right_eye.pupil_radius
        if right_eye_distance > max_distance:
            right_eye_distance = max_distance

        # Calculate the new positions of the pupils
        left_eye_pupil_x = left_eye_distance * math.cos(left_eye_angle)
        left_eye_pupil_y = left_eye_distance * math.sin(left_eye_angle)

        right_eye_pupil_x = right_eye_distance * math.cos(right_eye_angle)
        right_eye_pupil_y = right_eye_distance * math.sin(right_eye_angle)

        # Update the positions of the pupils
        self.left_eye.pupil.pos = (self.left_eye.center_x + left_eye_pupil_x - self.left_eye.pupil_radius,
                                   self.left_eye.center_y + left_eye_pupil_y - self.left_eye.pupil_radius)

        self.right_eye.pupil.pos = (self.right_eye.center_x + right_eye_pupil_x - self.right_eye.pupil_radius,
                                    self.right_eye.center_y + right_eye_pupil_y - self.right_eye.pupil_radius)

        
class MyApp(App):
    def build(self):
        return MyFloatLayout()

if __name__ == '__main__':
    MyApp().run()
