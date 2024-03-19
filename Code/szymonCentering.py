from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.animation import Animation
import random
import time


class EyesWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eye_radius = 50
        self.pupil_radius = 20
        self.eye_spacing = 350  # Adjust this value for the desired spacing
        self.eye1_pos = (Window.width / 2 - self.eye_spacing / 2, self.center_y)
        self.eye2_pos = (Window.width / 2 + self.eye_spacing / 2, self.center_y)
        self.pupil1_pos = list(self.eye1_pos)
        self.pupil2_pos = list(self.eye2_pos)
        self.follow_cursor = False
        self.tap_count = 0  # Tap count for mode testing
        self.return_delay = 0.5  # Delay in seconds before pupils return to the middle
        self.idle_interval = random.randint(1, 6)
        self.eyeTrack = False

        with self.canvas.before:
            with self.canvas.before:
                Color(0, 1, 0, 1)
                self.rect = Rectangle(size=self.size, pos=self.pos)

            self.bind(size=self._update_rect, pos=self._update_rect)

            self.eye_color = Color(1, 1, 1)
            self.eye1 = Ellipse(pos=(self.eye1_pos[0] - self.eye_radius, self.eye1_pos[1] - self.eye_radius),
                                size=(self.eye_radius * 2, self.eye_radius * 2))
            self.eye2 = Ellipse(pos=(self.eye2_pos[0] - self.eye_radius, self.eye2_pos[1] - self.eye_radius),
                                size=(self.eye_radius * 2, self.eye_radius * 2))
            self.pupil_color = Color(0, 0, 0)
            self.pupil1 = Ellipse(pos=(self.pupil1_pos[0] - self.pupil_radius, self.pupil1_pos[1] - self.pupil_radius),
                                  size=(self.pupil_radius * 1, self.pupil_radius * 2))
            self.pupil2 = Ellipse(pos=(self.pupil2_pos[0] - self.pupil_radius, self.pupil2_pos[1] - self.pupil_radius),
                                  size=(self.pupil_radius * 1, self.pupil_radius * 2))

        self.update_pupils()
        Window.bind(mouse_pos=self.on_mouse_move)  # Get mouse position

        # Schedule idle animation
        Clock.schedule_interval(self.idle_animation, self.idle_interval)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_mouse_move(self, window, pos):
        if self.follow_cursor:
            x, y = pos
            print(pos)
            self.move_pupil(self.pupil1_pos, x, y, self.eye1_pos)
            self.move_pupil(self.pupil2_pos, x, y, self.eye2_pos)

    def angry_mode(self):  # Make Eyes Red
        self.pupil_color.rgb = (1, 0, 0)
        print('done!')

    def happy_mode(self):  # Make eyes Green
        self.pupil_color.rgb = (0, 1, 0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.follow_cursor = True
            Clock.unschedule(self.return_to_middle)
            Animation.stop_all(self.pupil1)
            Animation.stop_all(self.pupil2)
            print(self.tap_count)
            self.tap_count += 1
            if self.tap_count == 10:
                self.angry_mode()
            if self.tap_count == 15:
                self.happy_mode()
                self.tap_count = 0

    def on_touch_up(self, touch):
        self.follow_cursor = False
        Clock.unschedule(self.return_to_middle)
        Clock.schedule_once(self.return_to_middle, self.return_delay)

    def move_pupil(self, pupil_pos, target_x, target_y, eye_pos):
        direction = Vector(target_x - eye_pos[0], target_y - eye_pos[1]).normalize()
        distance = min(Vector(target_x - eye_pos[0], target_y - eye_pos[1]).length(),
                       self.eye_radius - self.pupil_radius)
        pupil_pos[0] = eye_pos[0] + direction.x * distance
        pupil_pos[1] = eye_pos[1] + direction.y * distance
        self.update_pupils()

    def return_to_middle(self, dt):
        animation1 = Animation(pos=(self.eye1_pos[0] - self.pupil_radius, self.eye1_pos[1] - self.pupil_radius),
                               t='out_cubic', duration=0.5)
        animation2 = Animation(pos=(self.eye2_pos[0] - self.pupil_radius, self.eye2_pos[1] - self.pupil_radius),
                               t='out_cubic', duration=0.5)
        animation1.start(self.pupil1)
        animation2.start(self.pupil2)

    def idle_animation(self, dt):
        rand_eyes = random.uniform(10, -10)
        rand_eyes2 = random.uniform(10, -10)
        idle_anim1 = Animation(pos=(self.eye1_pos[0] - self.pupil_radius + rand_eyes,
                                    self.eye1_pos[1] - self.pupil_radius + rand_eyes2),
                               t='out_cubic', duration=0.45)
        idle_anim2 = Animation(pos=(self.eye2_pos[0] - self.pupil_radius + rand_eyes,
                                    self.eye2_pos[1] - self.pupil_radius + rand_eyes2),
                               t='out_cubic', duration=0.45)
        if not self.follow_cursor:
            time.sleep(0.5)
            idle_anim1.start(self.pupil1)
            idle_anim2.start(self.pupil2)

    def update_pupils(self):
        self.pupil1.pos = (self.pupil1_pos[0] - self.pupil_radius, self.pupil1_pos[1] - self.pupil_radius)
        self.pupil2.pos = (self.pupil2_pos[0] - self.pupil_radius, self.pupil2_pos[1] - self.pupil_radius)

        # Check if the pupils are getting close to each other
        distance_between_pupils = Vector(self.pupil1_pos).distance(self.pupil2_pos)
        if distance_between_pupils < self.pupil_radius * 2:
            Clock.unschedule(self.return_to_middle)
            self.return_to_middle(0)  # Call immediately to prevent overlapping delays


class EyesApp(App):
    def build(self):
        return EyesWidget()


if __name__ == '__main__':
    EyesApp().run()
