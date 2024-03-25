from kivy.app import App
from kivy.graphics import Ellipse, Color, Rectangle, Rotate, transformation
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import math
from kivy.animation import Animation


# Stupid eye thing

class Eye(Widget):
    def __init__(self, pupil_pos=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.eye_rad = 180  # Eye Size
        self.pupil_rad = 60  # Pupil Size
        self.pupil_pos = list(pupil_pos)
        self.eye_spacing = 120
        with self.canvas:
            # Iris
            Color(1, 1, 1)
            self.iris = Ellipse(size=(2 * (self.eye_rad - 10), 2 * (self.eye_rad - 10)),
                                pos=(self.center_x - self.eye_rad + 10,
                                     self.center_y - self.eye_rad + 10))

            # Pupil
            self.pupil_color = Color(0, 0.5, 1)
            self.pupil = Ellipse(size=(self.pupil_rad * 3, self.pupil_rad * 3),
                                 pos=(self.center_x + pupil_pos[0] - self.pupil_rad,
                                      self.center_y + pupil_pos[1] - self.pupil_rad))

            # Eyebrows
            self.eyebrow_color = Color(0.5, 0.3, 0)
            self.eyebrow = Rectangle(size=(self.eye_rad * 2, 20),
                                     pos=(self.center_x - self.eye_rad, self.center_y + self.eye_rad))

    # On Resize
    def on_size(self, *args):
        self.iris.size = (2 * (self.eye_rad - 10), 2 * (self.eye_rad - 10))
        self.iris.pos = (self.center_x - self.eye_rad + 10, self.center_y - self.eye_rad + 10)

        self.pupil.size = (self.pupil_rad * 3, self.pupil_rad * 3)
        self.pupil.pos = (self.center_x + self.pupil_pos[0] - 1.5 * self.pupil_rad,
                          self.center_y + self.pupil_pos[1] - 3 * self.pupil_rad + self.pupil_rad * 1.5)

        self.eyebrow.size = (self.eye_rad * 2, 10)
        self.eyebrow.pos = (self.center_x - self.eye_rad, self.center_y + self.eye_rad)


# Main Eye and Pupil Layout
class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Refer from Eye() class for pupil size changing
        eye = Eye()
        self.pupil_rad = eye.pupil_rad
        self.reset_pupil_timer = None  # Timer to reset pupils
        with self.canvas.before:
            Color(1, 0, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_bg, pos=self.update_bg)

        # Add in Eyes to Layout

        self.left_eye = Eye(pupil_pos=(0, 0))
        self.left_eye.center_x = self.width * -1.5 - eye.eye_spacing
        self.add_widget(self.left_eye)

        self.right_eye = Eye(pupil_pos=(0, 0))
        self.right_eye.center_x = self.width * 2.5 + eye.eye_spacing
        self.add_widget(self.right_eye)

    def update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    # Touch detection

    def on_touch_down(self, touch):
        touch_x, touch_y = touch.pos
        eye = Eye()
        # Check if touch is on the left or right eye
        if self.left_eye.collide_point(*touch.pos) and self.is_within_eye_bounds(self.left_eye, touch_x, touch_y):
            self.angry_mode()
        elif self.right_eye.collide_point(*touch.pos) and self.is_within_eye_bounds(self.right_eye, touch_x, touch_y):
            self.testing_mode()

        if self.collide_point(*touch.pos):
            self.update_pupils(touch_x, touch_y)
            self.touch_down_update(touch)
    def is_within_eye_bounds(self, eye, touch_x, touch_y):
        return (eye.center_x - eye.eye_rad <= touch_x <= eye.center_x + eye.eye_rad and
                eye.center_y - eye.eye_rad <= touch_y <= eye.center_y + eye.eye_rad)

    def happy_mode(self):  # Happy
        eye = Eye()
        self.left_eye.pupil_color.rgb = (0, 1, 0.2)
        self.right_eye.pupil_color.rgb = (0, 1, 0.2)
        self.right_eye.eyebrow.pos = (self.center_x + eye.eye_rad - 80 / 2, self.center_y + eye.eye_rad + 20)
        self.left_eye.eyebrow.pos = (self.center_x - eye.eye_rad - 80 * 4, self.center_y + eye.eye_rad + 20)

    def angry_mode(self):
        eye = Eye() # Angry
        self.left_eye.pupil_color.rgb = (1, 0, 0)
        self.right_eye.pupil_color.rgb = (1, 0, 0)
        self.right_eye.eyebrow.pos = (self.center_x + eye.eye_rad - 80 / 2, self.center_y + eye.eye_rad - 20)
        self.left_eye.eyebrow.pos = (self.center_x - eye.eye_rad - 80 * 4, self.center_y + eye.eye_rad - 20)
    def testing_mode(self): # Self-explanatory... come on.
        self.left_eye.pupil_color.rgb = (0, 1, 1)
        self.right_eye.pupil_color.rgb = (0, 1, 1)

    def on_touch_up(self, touch):
        eye = Eye()
        self.touch_up_update(touch)
        self.happy_mode()

    # When moving cursor

    def on_touch_move(self, touch):
        touch_x, touch_y = touch.pos
        if self.collide_point(*touch.pos):
            self.update_pupils(touch_x, touch_y)

    # Respond to touchDown

    def touch_down_update(self, touch):
        touch_x, touch_y = touch.pos
        self.pupil_rad = self.pupil_rad + 5
        if self.collide_point(*touch.pos):
            self.update_pupils(touch_x, touch_y)
            self.reset_pupil_timer_cancel()
            self.reset_pupil_timer = Clock.schedule_once(self.reset_pupil_positions, 2.0)

    # Respond to touchUP

    def touch_up_update(self, touch):
        touch_x, touch_y = touch.pos
        self.pupil_rad = self.pupil_rad - 5
        if self.collide_point(*touch.pos):
            self.update_pupils(touch_x, touch_y)
            self.reset_pupil_timer_cancel()
            self.reset_pupil_timer = Clock.schedule_once(self.reset_pupil_positions, 2.0)

    # Adjust pupil position based off of cursor pos

    def update_pupils(self, touch_x, touch_y):
        self.left_eye.pupil.size = (self.pupil_rad * 3, self.pupil_rad * 3)
        self.right_eye.pupil.size = (self.pupil_rad * 3, self.pupil_rad * 3)
        # Calculate the distance and angle of the touch relative to the center of each eye
        left_eye_distance = math.sqrt((touch_x - self.left_eye.center_x) ** 2 + (touch_y - self.left_eye.center_y) ** 2)
        left_eye_angle = math.atan2(touch_y - self.left_eye.center_y, touch_x - self.left_eye.center_x)

        right_eye_distance = math.sqrt(
            (touch_x - self.right_eye.center_x) ** 2 + (touch_y - self.right_eye.center_y) ** 2)
        right_eye_angle = math.atan2(touch_y - self.right_eye.center_y, touch_x - self.right_eye.center_x)

        # Ensure the pupils stay within the eye boundaries
        max_distance = self.left_eye.eye_rad - self.left_eye.pupil_rad - self.pupil_rad
        if left_eye_distance > max_distance:
            left_eye_distance = max_distance
        max_distance = self.right_eye.eye_rad - self.right_eye.pupil_rad - self.pupil_rad
        if right_eye_distance > max_distance:
            right_eye_distance = max_distance

        # Calculate the new positions of the pupils
        left_eye_pupil_x = left_eye_distance * math.cos(left_eye_angle) - self.left_eye.pupil.size[0] / 2
        left_eye_pupil_y = left_eye_distance * math.sin(left_eye_angle) - self.left_eye.pupil.size[1] / 2

        right_eye_pupil_x = right_eye_distance * math.cos(right_eye_angle) - self.right_eye.pupil.size[0] / 2
        right_eye_pupil_y = right_eye_distance * math.sin(right_eye_angle) - self.right_eye.pupil.size[1] / 2

        self.right_eye.pupil.pos = (self.right_eye.center_x + right_eye_pupil_x,
                                    self.right_eye.center_y + right_eye_pupil_y)
        self.left_eye.pupil.pos = (self.left_eye.center_x + left_eye_pupil_x,
                                   self.left_eye.center_y + left_eye_pupil_y)

    # Reset pupils to center after idle

    def reset_pupil_positions(self, dt):
        left_eye_pupil_anim = Animation(pos=(self.left_eye.center_x - self.left_eye.pupil.size[0] / 2,
                                             self.left_eye.center_y - self.left_eye.pupil.size[1] / 2),
                                        duration=0.5, t='out_quad')
        left_eye_pupil_anim.start(self.left_eye.pupil)

        right_eye_pupil_anim = Animation(pos=(self.right_eye.center_x - self.right_eye.pupil.size[0] / 2,
                                              self.right_eye.center_y - self.right_eye.pupil.size[1] / 2),
                                         duration=0.5, t='out_quad')
        right_eye_pupil_anim.start(self.right_eye.pupil)

    def reset_pupil_timer_cancel(self):
        # Cancel the reset timer if it's running
        if self.reset_pupil_timer is not None:
            self.reset_pupil_timer.cancel()
            self.reset_pupil_timer = None


class LooiApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    LooiApp().run()
