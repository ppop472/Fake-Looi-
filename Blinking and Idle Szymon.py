import math
import random
import time
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle, Rotate
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.vector import Vector


class LeftEye(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        maxSize = Window.system_size
        desiredSize = (maxSize[0] * 1, maxSize[1] * 1)
        desiredRadius = maxSize[0] * 0.1
        Window.size = desiredSize
        self.maxwidth = maxSize[0]
        self.desiredwidth = maxSize[0] * 0.1
        self.maxheight = maxSize[1]
        self.desiredheight = maxSize[1] * 0.1
        self.radius = desiredRadius
        with self.canvas:
            # left eye lol
            self.left_iris_color = Color(0.69, 0.86, 0.95, 1)
            self.left_iris = Ellipse(pos=(self.desiredwidth * 2, self.desiredheight * 3),
                                     size=(self.maxwidth * 0.2, self.maxheight * 0.4))
            # left pupil hehe
            self.left_pupil_color = Color(0, 0, 0, 1)
            self.left_pupil_radius = desiredRadius / 10
            self.left_pupil = Ellipse(pos=(self.desiredwidth * 2.90, self.desiredheight * 4.6),
                                      size=(self.maxwidth * 0.02, self.maxheight * 0.08))


class RightEye(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        maxSize = Window.system_size
        desiredSize = (maxSize[0] * 1, maxSize[1] * 1)
        desiredRadius = maxSize[0] * 0.1
        Window.size = desiredSize
        self.maxwidth = maxSize[0]
        self.desiredwidth = maxSize[0] * 0.1
        self.maxheight = maxSize[1]
        self.desiredheight = maxSize[1] * 0.1
        self.radius = desiredRadius
        with self.canvas:
            # right eye lol
            self.right_iris_color = Color(0.69, 0.86, 0.95, 1)
            self.right_iris = Ellipse(pos=(self.desiredwidth * 6, self.desiredheight * 3),
                                      size=(self.maxwidth * 0.2, self.maxheight * 0.4))
            # right eye lmao
            self.right_pupil_color = Color(0, 0, 0, 1)
            self.right_pupil_radius = desiredRadius / 10
            self.right_pupil = Ellipse(pos=(self.desiredwidth * 6.90, self.desiredheight * 4.6),
                                       size=(self.maxwidth * 0.02, self.maxheight * 0.08))


class LeftEyeBrows(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        maxSize = Window.system_size
        desiredSize = (maxSize[0] * 1, maxSize[1] * 1)
        Window.size = desiredSize
        self.maxwidth = maxSize[0]
        self.maxheight = maxSize[1]
        border_radius = (10, 1000, 10, 1000)
        self.left_eyebrows_angle = 0
        with self.canvas:
            self.rotate_left = Rotate(origin=(self.maxwidth * 0.2, self.maxheight * 0.72),
                                      angle=self.left_eyebrows_angle)
            self.left_eyebrows_color = Color(rgb=(255, 255, 255))
            self.left_eyebrows = Rectangle(pos=(self.maxwidth * 0.2, self.maxheight * 0.72),
                                           size=(self.maxwidth * 0.2, self.maxheight * 0.015),
                                           radius=border_radius)


class RightEyeBrows(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        maxSize = Window.system_size
        desiredSize = (maxSize[0] * 1, maxSize[1] * 1)
        Window.size = desiredSize
        self.maxwidth = maxSize[0]
        self.maxheight = maxSize[1]
        border_radius = (1000, 10, 1000, 10)
        self.right_eyebrows_angle = 0
        with self.canvas:
            self.rotate_right = Rotate(origin=(self.maxwidth * 0.6, self.maxheight * 0.72),
                                       angle=self.right_eyebrows_angle)
            self.right_eyebrows_color = Color(rgb=(255, 255, 255))
            self.right_eyebrows = Rectangle(pos=(self.maxwidth * 0.6, self.maxheight * 0.72),
                                            size=(self.maxwidth * 0.2, self.maxheight * 0.015),
                                            radius=border_radius)


class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # User Input/Current Emotion
        self.is_idle = False  # Is user Idle?
        self.is_boos = False  # Is Looi Mad?
        # Variable of the screens
        Window.maximize()
        self.maxSize = Window.system_size
        self.desiredSize = (self.maxSize[0] * 1, self.maxSize[1] * 1)
        self.desiredRadius = self.maxSize[0] * 0.1
        Window.size = self.desiredSize
        self.maxwidth = self.maxSize[0]
        self.desiredwidth = self.maxSize[0] * 0.1
        self.maxheight = self.maxSize[1]
        self.desiredheight = self.maxSize[1] * 0.1
        self.radius = self.desiredRadius
        # Counter variabel voor de boos onclick ding
        self.counter_boos = 0
        # Background
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.maxSize, pos=self.pos)
        # Add to widgets
        self.left_eye = LeftEye()
        self.add_widget(self.left_eye)
        self.right_eye = RightEye()
        self.add_widget(self.right_eye)
        self.left_eyebrows = LeftEyeBrows()
        self.add_widget(self.left_eyebrows)
        self.right_eyebrows = RightEyeBrows()
        self.add_widget(self.right_eyebrows)
        # Animaties en Blinking
        self.start_idle_timer(instance=None)
        rand_blonk = random.randint(7, 21)
        Clock.schedule_interval(self.blink_animation, rand_blonk)  # Random Blinking

    # Movement DYING INSIDE
    def update_pupils(self, touch_x, touch_y):
        left_eye_center = (self.maxwidth * 0.3, (self.maxheight * 0.5) - (self.maxwidth / 64))
        right_eye_center = (self.maxwidth * 0.7, (self.maxheight * 0.5) - (self.maxwidth / 64))
        left_eye_distance = math.sqrt((touch_x - left_eye_center[0]) ** 2 + (touch_y - left_eye_center[1]) ** 2)
        left_eye_angle = math.atan2(touch_y - left_eye_center[1], touch_x - left_eye_center[0])
        right_eye_distance = math.sqrt((touch_x - right_eye_center[0]) ** 2 + (touch_y - right_eye_center[1]) ** 2)
        right_eye_angle = math.atan2(touch_y - right_eye_center[1], touch_x - right_eye_center[0])
        max_distance_left = self.maxwidth / 24
        max_distance_right = self.maxwidth / 24
        if left_eye_distance > max_distance_left:
            left_eye_distance = max_distance_left
        if right_eye_distance > max_distance_right:
            right_eye_distance = max_distance_right
        # new positie bullshit
        left_eye_pupil_x = left_eye_distance * math.cos(left_eye_angle) + left_eye_center[0] - 10
        left_eye_pupil_y = left_eye_distance * math.sin(left_eye_angle) + left_eye_center[1] - 10
        right_eye_pupil_x = right_eye_distance * math.cos(right_eye_angle) + right_eye_center[0] - 10
        right_eye_pupil_y = right_eye_distance * math.sin(right_eye_angle) + right_eye_center[1] - 10
        # lil position update
        self.left_eye.left_pupil.pos = (left_eye_pupil_x, left_eye_pupil_y)
        self.right_eye.right_pupil.pos = (right_eye_pupil_x, right_eye_pupil_y)

    # On touch/drag ding
    def on_touch_down(self, touch):
        self.start_timer(instance=None)
        self.reset_timer()
        self.update_pupils(touch.x, touch.y)
        self.boos_reactie(touch)
        self.restart_idle_timer(instance=None)  # Restart Idle timer on touch - Szymon

    def on_touch_move(self, touch):
        self.start_timer(instance=None)
        self.update_pupils(touch.x, touch.y)
        self.restart_idle_timer(instance=None)  # Restart Idle timer on move - Szymon

    # Idle timeywimey FUCK MY LIFE - Love, Szymon
    def start_idle_timer(self, instance):
        self.time_limit = random.randint(3, 12)
        self.idle_time = time.time()
        self.elapsed_time = 0
        self.idle_time = time.time()
        Clock.unschedule(self.update_idle_timer)
        Clock.schedule_interval(self.update_idle_timer, 0.1)

    def update_idle_timer(self, dt):
        current_time = time.time()
        elapsed_time = current_time - self.idle_time
        if elapsed_time > self.time_limit:
            self.is_idle = True
            Clock.unschedule(self.update_idle_timer)
            Clock.schedule_interval(self.idle_animation, 3)

    def reset_idle_timer(self):
        self.idle_time = time.time()

    def restart_idle_timer(self, instance):
        self.is_idle = False
        self.reset_idle_timer()
        self.start_idle_timer(instance)
        Clock.unschedule(self.idle_animation)

    # Timer voor de pupilen
    def start_timer(self, instance):
        self.time_limit = 2
        self.start_time = time.time()
        self.elapsed_time = 0
        self.start_time = time.time()
        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 0.1)

    def reset_timer(self):
        self.start_time = time.time()

    def update_timer(self, dt):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time > self.time_limit:
            Clock.unschedule(self.update_timer)
            self.move_pupil_back_smoothly()

    def restart_timer(self, instance):
        self.reset_timer()
        self.start_timer(instance)

    # Reset pupil naar de middle hehe
    def reset_pupil_position(self, dt):
        self.movement_in_progress = True
        Clock.schedule_interval(self.move_pupil_back_smoothly, 0.0001)

    # Mooie smooth animatie toegevoegd en idle timer toegevoegd - Sailmun
    def move_pupil_back_smoothly(self):
        right_eye_anim = Animation(pos=(self.desiredwidth * 6.90, self.desiredheight * 4.6),
                                   duration=0.6, t='out_cubic')
        right_eye_anim.start(self.right_eye.right_pupil)
        left_eye_anim = Animation(pos=(self.desiredwidth * 2.90, self.desiredheight * 4.6),
                                  duration=0.6, t='out_cubic')
        left_eye_anim.start(self.left_eye.left_pupil)
        self.right_eye.canvas.ask_update()
        self.start_idle_timer(instance=None)

    # Emotions/Reaction Yeaaaa
    def boos_reactie(self, touch):
        touch_x, touch_y = touch.pos
        # Screen locatie van de boos right oog bepalen
        self.left_minwidth_boos = self.maxwidth * 0.2
        self.left_maxwidth_boos = self.maxwidth * 0.4
        self.left_minheight_boos = self.maxheight * 0.3
        self.left_maxheight_boos = self.maxheight * 0.7
        self.right_minwidth_boos = self.maxwidth * 0.6
        self.right_maxwidth_boos = self.maxwidth * 0.8
        self.right_minheight_boos = self.maxheight * 0.3
        self.right_maxheight_boos = self.maxheight * 0.7
        if (self.right_minwidth_boos < touch_x < self.right_maxwidth_boos and
                self.right_minheight_boos < touch_y < self.right_maxheight_boos or
                self.left_minwidth_boos < touch_x < self.left_maxwidth_boos and
                self.left_minheight_boos < touch_y < self.left_maxheight_boos):
            self.counter_boos += 1
            self.start_timer_reactie_boos(instance=None)
            self.reset_timer_reactie_boos()
        if self.counter_boos == 10:
            self.is_boos = True
            self.boos_worden()

    def noreactie(self):
        self.counter_boos = 0
        self.is_boos = False
        # Ogen
        self.right_eye.right_pupil_color.rgba = [0, 0, 0, 1]
        self.left_eye.left_pupil_color.rgba = [0, 0, 0, 1]
        self.left_eye.left_iris_color.rgba = [0.69, 0.86, 0.95, 1]
        self.right_eye.right_iris_color.rgba = [0.69, 0.86, 0.95, 1]

        # wenkbrauw
        self.left_eyebrows.left_eyebrows_color.rgba = [1, 1, 1, 1]
        self.left_eyebrows.rotate_left.angle = 0
        self.right_eyebrows.right_eyebrows_color.rgba = [1, 1, 1, 1]
        self.right_eyebrows.rotate_right.angle = 0
        self.right_eyebrows.right_eyebrows.pos = (self.maxwidth * 0.6, self.maxheight * 0.72)

    def boos_worden(self):
        self.left_eye.left_iris_color.rgba = [0.9, 0, 0, 1]
        self.right_eye.right_iris_color.rgba = [0.9, 0, 0, 1]
        self.left_eyebrows.left_eyebrows_color.rgba = [0, 0, 0, 1]
        self.left_eyebrows.rotate_left.angle = -5
        self.left_eyebrows.left_eyebrows.pos = (self.maxwidth * 0.2, self.maxheight * 0.72)
        self.right_eyebrows.right_eyebrows_color.rgba = [0, 0, 0, 1]
        self.right_eyebrows.rotate_right.angle = 10
        self.right_eyebrows.right_eyebrows.pos = (self.maxwidth * 0.6, self.maxheight * 0.751)
        if hasattr(self.right_eye, 'haha'):
            print("ïets")
        self.start_timer_reactie_boos(instance=None)
        self.reset_timer_reactie_boos()

    # Timer voor de Boos reacties
    def start_timer_reactie_boos(self, instance):
        self.time_limit_reactie_boos = 4
        self.start_time_reactie_boos = time.time()
        self.elapsed_time_reactie_boos = 0
        Clock.unschedule(self.update_timer_reactie_boos)
        Clock.schedule_interval(self.update_timer_reactie_boos, 0.1)

    def reset_timer_reactie_boos(self):
        self.start_time_reactie = time.time()

    def update_timer_reactie_boos(self, dt):
        current_time_reactie_boos = time.time()
        elapsed_time_reactie_boos = current_time_reactie_boos - self.start_time_reactie_boos
        if elapsed_time_reactie_boos > self.time_limit_reactie_boos:
            self.counter_boos = 0
            Clock.unschedule(self.update_timer_reactie_boos)
            self.noreactie()

    # Idle animation + Szymon
    # Make this shit smooth yay fuck my like cancer aids cunt
    def idle_animation(self, dt):
        # random direction vector
        direction = Vector(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        # eye center calculation
        left_eye_center = (self.maxwidth * 0.3, (self.maxheight * 0.5) - (self.maxwidth / 64))
        right_eye_center = (self.maxwidth * 0.7, (self.maxheight * 0.5) - (self.maxwidth / 64))
        # Give pupils position for goofy random
        left_pupil_anim = Animation(pos=(left_eye_center[0] + direction[0] * self.maxwidth / 24,
                                         left_eye_center[1] + direction[1] * self.maxwidth / 24), duration=0.6,
                                    t='out_cubic')
        right_pupil_anim = Animation(pos=(right_eye_center[0] + direction[0] * self.maxwidth / 24,
                                          right_eye_center[1] + direction[1] * self.maxwidth / 24), duration=0.6,
                                     t='out_cubic')
        # quirky anim starts
        left_pupil_anim.start(self.left_eye.left_pupil)
        right_pupil_anim.start(self.right_eye.right_pupil)

    # Blinking anim
    def blink_blonk(self, dt):
        self.left_eye.left_pupil_color.a = 0
        self.right_eye.right_pupil_color.a = 0
        if self.is_boos:
            self.left_eye.left_iris_color.rgba = (0.7, 0, 0, 1)
            self.right_eye.right_iris_color.rgba = (0.7, 0, 0, 1)
        else:
            self.right_eye.right_iris_color.rgba = (0.59, 0.76, 0.85, 1)
            self.left_eye.left_iris_color.rgba = (0.59, 0.76, 0.85, 1)

    def un_blink_blonk(self, dt):
        self.left_eye.left_pupil_color.a = 1
        self.right_eye.right_pupil_color.a = 1
        if self.is_boos:
            self.left_eye.left_iris_color.rgba = (0.9, 0, 0, 1)
            self.right_eye.right_iris_color.rgba = (0.9, 0, 0, 1)
        else:
            self.left_eye.left_iris_color.rgba = (0.69, 0.86, 0.95, 1)
            self.right_eye.right_iris_color.rgba = (0.69, 0.86, 0.95, 1)

    def blink_animation(self, dt):
        Clock.schedule_once(self.blink_blonk)
        Clock.schedule_once(self.un_blink_blonk, 0.2)


class MyApp(App):
    def build(self):
        return MyFloatLayout()


if __name__ == '__main__':
    MyApp().run()
