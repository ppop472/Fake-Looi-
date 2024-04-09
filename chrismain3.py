from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line, Bezier
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader 
import time
from kivy.vector import Vector
import random
import math
from kivy.graphics import Color, RoundedRectangle

class LeftEye(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
                
        Window.maximize()
        maxSize = Window.system_size
        desiredSize = (maxSize[0]*1, maxSize[1]*1)
        desiredRadius = maxSize[0] * 0.1
        Window.size = desiredSize

        self.maxwidth = maxSize[0]
        self.desiredwidth = maxSize[0] * 0.1

        self.maxheight = maxSize[1]
        self.desiredheight = maxSize[1] * 0.1

        self.radius = desiredRadius

        with self.canvas:
            #left eye lol
            self.left_iris_color = Color(0.69, 0.86, 0.95, 1)
            self.left_iris = Ellipse(pos=(self.desiredwidth * 2,self.desiredheight * 3), 
                                size=(self.maxwidth * 0.2 , self.maxheight * 0.4))
            
            #left pupil hehe
            self.left_pupil_color = Color(0, 0, 0, 1)
            self.left_pupil_radius = desiredRadius / 10
            self.left_pupil = Ellipse(pos=(self.desiredwidth * 2.90,self.desiredheight * 4.6), 
                                size=(self.maxwidth * 0.02 , self.maxheight * 0.08))
            
class RightEye(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.maximize()
        maxSize = Window.system_size
        desiredSize = (maxSize[0]*1, maxSize[1]*1)
        desiredRadius = maxSize[0] * 0.1
        Window.size = desiredSize

        self.maxwidth = maxSize[0]
        self.desiredwidth = maxSize[0] * 0.1

        self.maxheight = maxSize[1]
        self.desiredheight = maxSize[1] * 0.1

        self.radius = desiredRadius

        with self.canvas:
            #right eye lol
            self.right_iris_color = Color(0.69, 0.86, 0.95, 1)
            self.right_iris = Ellipse(pos=(self.desiredwidth * 6,self.desiredheight * 3), 
                                size=(self.maxwidth * 0.2 , self.maxheight * 0.4))

            #right eye lmao
            self.right_pupil_color = Color(0, 0, 0, 1)
            self.right_pupil_radius = desiredRadius / 10
            self.right_pupil = Ellipse(pos=(self.desiredwidth * 6.90,self.desiredheight * 4.6), 
                                size=(self.maxwidth * 0.02 , self.maxheight * 0.08))
            
            
class BendLines(Widget):
    def __init__(self, **kwargs):
        super(BendLines, self).__init__(**kwargs)

        Window.maximize()
        maxSize = Window.system_size
        desiredSize = (maxSize[0]*1, maxSize[1]*1)
        Window.size = desiredSize

        self.maxwidth = maxSize[0]
        self.maxheight = maxSize[1]

        self.line_width = 5

        self.cp1_x_left = self.maxwidth * 0.2
        self.cp1_y_left = self.maxheight * 0.75
        self.cp2_x_left = self.maxwidth * 0.3
        self.cp2_y_left = self.maxheight * 0.75
        self.cp3_x_left = self.maxwidth * 0.4
        self.cp3_y_left = self.maxheight * 0.75

        self.cp1_x_right = self.maxwidth * 0.8
        self.cp1_y_right = self.maxheight * 0.75
        self.cp2_x_right = self.maxwidth * 0.7
        self.cp2_y_right = self.maxheight * 0.75
        self.cp3_x_right = self.maxwidth * 0.6
        self.cp3_y_right = self.maxheight * 0.75
        
        self.draw_bezier_left()
        self.draw_bezier_right()

    def draw_bezier_left(self):
        self.canvas.clear()
        with self.canvas:
            self.line_left_color = Color(0, 0, 0, 1)
            self.line_left = Line(bezier=[self.cp1_x_left, self.cp1_y_left,
                                           self.cp2_x_left, self.cp2_y_left,
                                           self.cp3_x_left, self.cp3_y_left], width=self.line_width)

    def draw_bezier_right(self):
        with self.canvas:
            self.line_right_color = Color(0, 0, 0, 1)
            self.line_right = Line(bezier=[self.cp1_x_right, self.cp1_y_right,
                                            self.cp2_x_right, self.cp2_y_right,
                                            self.cp3_x_right, self.cp3_y_right], width=self.line_width)
            
    def animate_control_points(self, cp1_left, cp2_left, cp3_left, cp1_right, cp2_right, cp3_right, duration):
        anim_left = Animation(cp1_x_left=cp1_left[0], cp1_y_left=cp1_left[1],
                              cp2_x_left=cp2_left[0], cp2_y_left=cp2_left[1],
                              cp3_x_left=cp3_left[0], cp3_y_left=cp3_left[1], duration=duration)
        anim_left.bind(on_progress=self.update_line)
        anim_left.start(self)

        anim_right = Animation(cp1_x_right=cp1_right[0], cp1_y_right=cp1_right[1],
                               cp2_x_right=cp2_right[0], cp2_y_right=cp2_right[1],
                               cp3_x_right=cp3_right[0], cp3_y_right=cp3_right[1], duration=duration)
        anim_right.bind(on_progress=self.update_line)
        anim_right.start(self)
            
    def update_line(self, instance, value, progression):
        self.draw_bezier_left()
        self.draw_bezier_right()

class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # AFK / VERDRIETIGE emotie/reactie
        self.restart_idle_timer(instance=None)
        self.boos_worden_bool = False
        self.start_timer_reactie_sad(instance=None)

        # Variable of the screens
        Window.maximize()
        self.maxSize = Window.system_size

        self.desiredSize = (self.maxSize[0]*1, self.maxSize[1]*1)
        self.desiredRadius = self.maxSize[0] * 0.1
        Window.size = self.desiredSize

        self.maxwidth = self.maxSize[0]
        self.desiredwidth = self.maxSize[0] * 0.1

        self.maxheight = self.maxSize[1]
        self.desiredheight =self. maxSize[1] * 0.1

        self.radius = self.desiredRadius

        #Geluiden
        self.boos_sound = SoundLoader.load('grrrr Clash Royale (Official Video).mp3')
        self.verdrietig_sound = SoundLoader.load('Clash Royale skeleton cry emote sound but loud.mp3')
        
        #Counter variabel voor de boos onclick ding
        self.counter_boos = 0

        #Bink variableren :P
        self.start_idle_timer(instance=None) # Idle animation start
        rand_blonk = random.randint(7, 21) # Random seconds for blinking
        Clock.schedule_interval(self.blink_animation, rand_blonk)  # Random Blinking
                
        #Background
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.maxSize, pos=self.pos)

        #Add to widgets
        self.left_eye = LeftEye()
        self.add_widget(self.left_eye)
        self.right_eye = RightEye()
        self.add_widget(self.right_eye)

        self.bendlines = BendLines()
        self.add_widget(self.bendlines)
        
    #Movement DYING INSIDE
    def update_pupils(self, touch_x, touch_y):
        left_eye_center = (self.maxwidth * 0.3, (self.maxheight * 0.5) - (self.maxwidth / 64))
        right_eye_center = (self.maxwidth * 0.7,  (self.maxheight * 0.5) - (self.maxwidth / 64))

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

        #new positie bullshit
        left_eye_pupil_x = left_eye_distance * math.cos(left_eye_angle) + left_eye_center[0] - 10
        left_eye_pupil_y = left_eye_distance * math.sin(left_eye_angle) + left_eye_center[1] - 10
        right_eye_pupil_x = right_eye_distance * math.cos(right_eye_angle) + right_eye_center[0] - 10
        right_eye_pupil_y = right_eye_distance * math.sin(right_eye_angle) + right_eye_center[1] - 10
        
        #lil position update
        # self.left_eye.left_pupil.pos = (left_eye_pupil_x, left_eye_pupil_y)
        # self.right_eye.right_pupil.pos = (right_eye_pupil_x, right_eye_pupil_y)

         # Smooth animation using Kivy's Animation class
        animation_left_eye = Animation(pos=(left_eye_pupil_x, left_eye_pupil_y), duration=0.2)
        animation_right_eye = Animation(pos=(right_eye_pupil_x, right_eye_pupil_y), duration=0.2)

        animation_left_eye.start(self.left_eye.left_pupil)
        animation_right_eye.start(self.right_eye.right_pupil)

    def update_pupils_drag(self, touch_x, touch_y):
        left_eye_center = (self.maxwidth * 0.3, (self.maxheight * 0.5) - (self.maxwidth / 64))
        right_eye_center = (self.maxwidth * 0.7,  (self.maxheight * 0.5) - (self.maxwidth / 64))

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

        
        #new positie bullshit
        left_eye_pupil_x = left_eye_distance * math.cos(left_eye_angle) + left_eye_center[0] - 10
        left_eye_pupil_y = left_eye_distance * math.sin(left_eye_angle) + left_eye_center[1] - 10
        right_eye_pupil_x = right_eye_distance * math.cos(right_eye_angle) + right_eye_center[0] - 10
        right_eye_pupil_y = right_eye_distance * math.sin(right_eye_angle) + right_eye_center[1] - 10
        
        #lil position update
        self.left_eye.left_pupil.pos = (left_eye_pupil_x, left_eye_pupil_y)
        self.right_eye.right_pupil.pos = (right_eye_pupil_x, right_eye_pupil_y)

    #On touch/drag ding
    def on_touch_down(self, touch):
        self.start_timer(instance=None)
        self.reset_timer()
        self.update_pupils(touch.x, touch.y)
        self.restart_idle_timer(instance=None)
        if not self.boos_worden_bool:
            self.noreactie()
            self.start_timer_reactie_sad(instance=None)

        #reacties
        self.boos_reactie(touch)

    def on_touch_up(self,touch):
        if not self.boos_worden_bool:
            self.noreactie()
            self.start_timer_reactie_sad(instance=None)

    def on_touch_move(self, touch):
        self.restart_idle_timer(instance=None)
        self.start_timer(instance=None)
        self.reset_timer()
        self.update_pupils_drag(touch.x, touch.y)
        if not self.boos_worden_bool:
            self.noreactie()
            self.start_timer_reactie_sad(instance=None)

    #Timer voor de pupilen
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

    #Reset pupil naar de middle hehe
    def reset_pupil_position(self, dt):
        self.movement_in_progress = True
        Clock.schedule_interval(self.move_pupil_back_smoothly, 0.0001)

    def move_pupil_back_smoothly(self):
        right_eye_anim = Animation(pos=(self.desiredwidth * 6.90, self.desiredheight * 4.6),
                                   duration=0.6, t='out_cubic')
        right_eye_anim.start(self.right_eye.right_pupil)
        left_eye_anim = Animation(pos=(self.desiredwidth * 2.90, self.desiredheight * 4.6),
                                  duration=0.6, t='out_cubic')
        left_eye_anim.start(self.left_eye.left_pupil)
        self.right_eye.canvas.ask_update()
        self.start_idle_timer(instance=None)

    #Emotions/Reaction Yeaaaa
        
    def boos_reactie(self, touch):
        touch_x, touch_y = touch.pos
        
        #Screen locatie van de boos right oog bepalen
        self.left_minwidth_boos = self.maxwidth * 0.2
        self.left_maxwidth_boos = self.maxwidth * 0.4
        self.left_minheight_boos = self.maxheight * 0.3 
        self.left_maxheight_boos = self.maxheight * 0.7
        
        self.right_minwidth_boos = self.maxwidth * 0.6
        self.right_maxwidth_boos = self.maxwidth * 0.8
        self.right_minheight_boos = self.maxheight * 0.3 
        self.right_maxheight_boos = self.maxheight * 0.7
        
        print("Clicked at:", "X:", touch_x, "Y:", touch_y)

        if (touch_x > self.right_minwidth_boos and
            touch_x < self.right_maxwidth_boos and
            touch_y > self.right_minheight_boos and
            touch_y < self.right_maxheight_boos or
            touch_x > self.left_minwidth_boos and 
            touch_x < self.left_maxwidth_boos and 
            touch_y > self.left_minheight_boos and 
            touch_y < self.left_maxheight_boos):
                self.counter_boos += 1
                print("Counter increased!")
                self.start_timer_reactie_boos(instance=None)
                self.reset_timer_reactie_boos()
        
        print("Counter value:", self.counter_boos)
        
        if self.counter_boos == 10:
            print("BOOS!", self.counter_boos)
            self.boos_worden()
            self.counter_boos = 0
            self.start_timer_reactie_sad(instance=None)
            

    def noreactie(self):
        # Ogen
        self.right_eye.right_pupil_color.rgba = [0, 0, 0, 1]
        self.left_eye.left_pupil_color.rgba = [0, 0, 0, 1]

        self.left_eye.left_iris_color.rgba = [0.69, 0.86, 0.95, 1]
        self.right_eye.right_iris_color.rgba = [0.69, 0.86, 0.95, 1]

        #Wenkbrouw
        cp1_left = [self.maxwidth * 0.2, self.maxheight * 0.75]
        cp2_left = [self.maxwidth * 0.3, self.maxheight * 0.75]
        cp3_left = [self.maxwidth * 0.4, self.maxheight * 0.75]
        cp1_right = [self.maxwidth * 0.8, self.maxheight * 0.75]
        cp2_right = [self.maxwidth * 0.7, self.maxheight * 0.75]
        cp3_right = [self.maxwidth * 0.6, self.maxheight * 0.75]
        self.bendlines.animate_control_points(cp1_left, cp2_left, cp3_left, cp1_right, cp2_right, cp3_right, 0.1)

        # Call function to start the timer for the reaction
        self.start_timer_reactie_sad(instance=None)
# BOOS HAHAHAHAH
    def boos_worden(self):
        self.left_eye.left_iris_color.rgba = [1,0,0,0.8]
        self.right_eye.right_iris_color.rgba = [1,0,0,0.8]

        self.boos_worden_bool = True

        #Wenkbrouwen
        cp1_left = [self.maxwidth * 0.2, self.maxheight * 0.75]
        cp2_left = [self.maxwidth * 0.40, self.maxheight * 0.75]
        cp3_left = [self.maxwidth * 0.45, self.maxheight * 0.65]
        cp1_right = [self.maxwidth * 0.8, self.maxheight * 0.75]
        cp2_right = [self.maxwidth * 0.6, self.maxheight * 0.75]
        cp3_right = [self.maxwidth * 0.55, self.maxheight * 0.65]

        self.bendlines.line_right_color.rgba=(0,0,0,0)

        self.bendlines.animate_control_points(cp1_left, cp2_left, cp3_left, cp1_right, cp2_right, cp3_right, 0.1)

        
        self.start_timer_reactie_boos(instance=None)
        self.reset_timer_reactie_boos()

    #Timer voor de Boos reacties
    def start_timer_reactie_boos(self, instance): 
        self.time_limit_reactie_boos = 4
        self.start_time_reactie_boos = time.time()     
        self.elapsed_time_reactie_boos = 0
        Clock.unschedule(self.update_timer_reactie_boos)
        Clock.schedule_interval(self.update_timer_reactie_boos, 0.1)

    def reset_timer_reactie_boos(self):
        self.start_time_reactie_boos = time.time()

    def update_timer_reactie_boos(self, dt):
        current_time_reactie_boos = time.time()
        elapsed_time_reactie_boos = current_time_reactie_boos - self.start_time_reactie_boos

        if elapsed_time_reactie_boos > self.time_limit_reactie_boos:
            self.counter_boos = 0
            Clock.unschedule(self.update_timer_reactie_boos)
            self.boos_worden_bool = False
            self.noreactie()
            
# SAD BRUHUUHUHU AFK REACTIE     
    def sad_worden_bepalen(self):
        if not self.boos_worden_bool:
            print("not boos sad")
            self.sad_worden()
        
            
    def sad_worden(self):
        #wenkbrouwen
        cp1_left = [self.maxwidth * 0.2, self.maxheight * 0.75]
        cp2_left = [self.maxwidth * 0.40, self.maxheight * 0.75]
        cp3_left = [self.maxwidth * 0.45, self.maxheight * 0.85]
        cp1_right = [self.maxwidth * 0.8, self.maxheight * 0.75]
        cp2_right = [self.maxwidth * 0.6, self.maxheight * 0.75]
        cp3_right = [self.maxwidth * 0.55, self.maxheight * 0.85]

        self.bendlines.animate_control_points(cp1_left, cp2_left, cp3_left, cp1_right, cp2_right, cp3_right, 0.1)

    def start_timer_reactie_sad(self, instance): 
        self.time_limit_reactie_sad = 30
        self.start_time_reactie_sad = time.time()     
        self.elapsed_time_reactie_sad = 0
        Clock.unschedule(self.update_timer_reactie_sad)
        Clock.schedule_interval(self.update_timer_reactie_sad, 0.1)

    def reset_timer_reactie_sad(self):
        self.start_time_reactie_sad = time.time()

    def update_timer_reactie_sad(self, dt):
        current_time_reactie_sad = time.time()
        elapsed_time_reactie_sad = current_time_reactie_sad - self.start_time_reactie_sad

        if elapsed_time_reactie_sad > self.time_limit_reactie_sad:
            self.counter_sad = 0
            Clock.unschedule(self.update_timer_reactie_sad)
            self.sad_worden_bepalen()
    
    #Idle animatie DISDISDISDISDIS    
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

    #Idle animation disdisdisdis
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

    #Knipperen KNIPKNIPKNIP HAHA
    def blink_blonk(self, dt):
        self.left_eye.left_pupil_color.a = 0
        self.right_eye.right_pupil_color.a = 0
        if self.boos_worden_bool:
            self.left_eye.left_iris_color.rgba = (0.7, 0, 0, 1)
            self.right_eye.right_iris_color.rgba = (0.7, 0, 0, 1)
        elif not self.boos_worden_bool:
            self.right_eye.right_iris_color.rgba = (0.59, 0.76, 0.85, 1)
            self.left_eye.left_iris_color.rgba = (0.59, 0.76, 0.85, 1)

    def un_blink_blonk(self, dt):
        self.left_eye.left_pupil_color.a = 1
        self.right_eye.right_pupil_color.a = 1
        if self.boos_worden_bool:
            self.left_eye.left_iris_color.rgba = (1, 0, 0, 0.8)
            self.right_eye.right_iris_color.rgba = (1, 0, 0, 0.8)
        elif not self.boos_worden_bool:
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