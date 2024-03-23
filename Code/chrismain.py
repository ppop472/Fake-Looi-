from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
import time
from kivy.vector import Vector
import math

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
    
            #random vierkant op de left eye
            Color(1, 0, 0, 0)
            Rectangle(pos=(self.maxwidth * 0.20 , self.maxheight * 0.30), 
                      size=(self.maxwidth * 0.2, self.maxheight * 0.4))

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
    
            #random vierkant op de left eye
            Color(1, 0, 0, 0)
            Rectangle(pos=(self.maxwidth * 0.60 , self.maxheight * 0.30), 
                      size=(self.maxwidth * 0.2, self.maxheight * 0.4))

class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

        #Background
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.maxSize, pos=self.pos)

        #Add to widgets
        self.left_eye = LeftEye()
        self.add_widget(self.left_eye)
        self.right_eye = RightEye()
        self.add_widget(self.right_eye)

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
        self.left_eye.left_pupil.pos = (left_eye_pupil_x, left_eye_pupil_y)
        self.right_eye.right_pupil.pos = (right_eye_pupil_x, right_eye_pupil_y)
    
    #On touch/drag ding
    def on_touch_down(self, touch):
        self.start_timer(instance=None)
        self.reset_timer()
        self.update_pupils(touch.x, touch.y)
        self.boos_reactie(touch)
        

    def on_touch_move(self, touch):
        self.start_timer(instance=None)
        self.reset_timer()
        self.update_pupils(touch.x, touch.y)


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
        self.right_eye.right_pupil.pos = (self.desiredwidth * 6.90, self.desiredheight * 4.6)
        self.left_eye.left_pupil.pos = (self.desiredwidth * 2.90,self.desiredheight * 4.6)
        self.right_eye.canvas.ask_update()

    #Emotions/Reaction Yeaaaa
        
    def boos_reactie(self,touch):
        touch_x, touch_y = touch.pos
        #left eye boos reactie position
        print("Clicked at:","X:", touch_x, "Y:", touch_y)

        self.left_minwidth_boos = self.maxwidth * 0.2
        self.left_maxwidth_boos = self.maxwidth * 0.4

        self.left_minheight_boos = self.maxheight * 0.3 
        self.left_maxheight_boos = self.maxheight * 0.7

        if touch_x > self.left_minwidth_boos and touch_x < self.left_maxwidth_boos and touch_y > self.left_minheight_boos and touch_y < self.left_maxheight_boos:
            print("Left eye BOOS!")
            self.boos_worden()

        #right eye boos reactie position
        self.right_minwidth_boos = self.maxwidth * 0.6
        self.right_maxwidth_boos = self.maxwidth * 0.8

        self.right_minheight_boos = self.maxheight * 0.3 
        self.right_maxheight_boos = self.maxheight * 0.7

        if touch_x > self.right_minwidth_boos and touch_x < self.right_maxwidth_boos and touch_y > self.right_minheight_boos and touch_y < self.right_maxheight_boos:
            print("Right eye BOOS!")
            self.boos_worden()

    def noreactie(self):
        self.right_eye.right_pupil_color.rgba = [0, 0, 0, 1]
        self.left_eye.left_pupil_color.rgba = [0, 0, 0, 1]

        self.left_eye.left_iris_color.rgba = [0.69, 0.86, 0.95, 1]
        self.right_eye.right_iris_color.rgba = [0.69, 0.86, 0.95, 1]

    def boos_worden(self):
        #self.right_eye.right_pupil_color.rgba = [1, 0, 0, 0.9]
        #self.left_eye.left_pupil_color.rgba = [1, 0, 0, 0.9]

        self.left_eye.left_iris_color.rgba = [1,0,0,0.8]
        self.right_eye.right_iris_color.rgba = [1,0,0,0.8]
        self.start_timer_reactie(instance=None)
        self.reset_timer_reactie()

    #Timer voor de Reacties
    def start_timer_reactie(self, instance): 
        self.time_limit_reactie = 2
        self.start_time_reactie = time.time()     
        self.elapsed_time_reactie = 0
        self.start_time = time.time()
        Clock.unschedule(self.update_timer_reactie)
        Clock.schedule_interval(self.update_timer_reactie, 0.1)

    def reset_timer_reactie(self):
        self.start_time_reactie = time.time()

    def update_timer_reactie(self, dt):
        current_time_reactie = time.time()
        elapsed_time_reactie = current_time_reactie - self.start_time_reactie

        if elapsed_time_reactie > self.time_limit_reactie:
            Clock.unschedule(self.update_timer_reactie)
            self.noreactie()

    def restart_timer_reactie(self, instance):
        self.reset_timer()
        self.start_timer(instance)

class MyApp(App):
    def build(self):
        return MyFloatLayout()

if __name__ == '__main__':
    MyApp().run()
