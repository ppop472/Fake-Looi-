from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
import time
from kivy.vector import Vector
import math
import pygame

# ULTRA MEGA PRO CODE made by NIET HARDSTUCK GOLD

#--------------------------------- Eye class --------------------------------------------------------------------------

class Eye(Widget):
    def __init__(self, pupil_color=(0, 0, 0, 1), pupil_position=(0, 0), **kwargs):
        super().__init__(**kwargs)

        Window.maximize()
        maxSize = Window.system_size

        desiredSize = (maxSize[0]*1, maxSize[1]*1)
        desiredRadius = maxSize[0] * 0.08
        Window.size = desiredSize

        self.radius = desiredRadius
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
            self.pupil_radius = 15
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
        self.spam_input = False
        
        # Set background color
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Left eye
        self.left_eye = Eye(pupil_color=(0, 0, 0, 1), pupil_position=(0, 0))
        self.left_eye.center_x = self.width * -2
        self.add_widget(self.left_eye)

        # Right eye
        self.right_eye = Eye(pupil_color=(0, 0, 0, 1), pupil_position=(0, 0))
        self.right_eye.center_x = self.width * 3
        self.add_widget(self.right_eye)

        print("left eye x:", self.left_eye.pupil_position[0])
        print("left eze y:", self.left_eye.pupil_position[1])

        

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
            
            #Clock.schedule_once(self.reset_pupil_position, 1)

    # def move_pupil_smoothly(self, dt):
    #     # Calculate the distance to move in each step
        
    #     step_x_right = (-80 - self.right_eye.pupil_position[0]) / 5
    #     step_y_right = (0 - self.right_eye.pupil_position[1]) / 10

    #     step_x_left = (60 - self.left_eye.pupil_position[0]) / 5
    #     step_y_left = (0 - self.left_eye.pupil_position[1]) / 10

    #     # Update pupil position
    #     self.right_eye.pupil_position[0] += step_x_right
    #     self.right_eye.pupil_position[1] += step_y_right

    #     self.left_eye.pupil_position[0] += step_x_left
    #     self.left_eye.pupil_position[1] += step_y_left
    #     # Move the pupil
    #     self.right_eye.pupil.pos = (self.right_eye.center_x + self.right_eye.pupil_position[0] - self.right_eye.pupil_radius,
    #                                  self.right_eye.center_y + self.right_eye.pupil_position[1] - 3 * self.right_eye.pupil_radius)

    #     self.left_eye.pupil.pos = (self.left_eye.center_x + self.left_eye.pupil_position[0] - self.left_eye.pupil_radius,
    #                                  self.left_eye.center_y + self.left_eye.pupil_position[1] - 3 * self.left_eye.pupil_radius)
    #     # Redraw the right eye widget
    #     self.right_eye.canvas.ask_update()
    #     self.right_eye.canvas.ask_update()
    #     # If reached the target position, stop the clock and reset movement state
    #     if abs(step_x_right) < 0.1 and abs(step_y_right) < 0.1:
    #         Clock.unschedule(self.move_pupil_smoothly) 
    #         self.movement_in_progress = False
    #         print("movement uit")


    def reset_pupil_position(self, dt):
        # Move the pupil of the right eye smoothly back to its original position
        if not self.movement_in_progress:
            self.movement_in_progress = True
            print("reset begin")
            Clock.schedule_interval(self.move_pupil_back_smoothly, 0.0001)
            print("pos",self.left_eye.pupil.pos)

    def move_pupil_back_smoothly(self, dt):
        # Calculate the distance to move in each step
        step_x_right = (-5 - self.right_eye.pupil_position[0]) / 10
        step_y_right = (0 - self.right_eye.pupil_position[1]) / 10

        step_x_left = (-5 - self.left_eye.pupil_position[0]) / 10
        step_y_left = (0 - self.left_eye.pupil_position[1]) / 10

        # Update pupil position
        self.right_eye.pupil_position[0] += step_x_right
        self.right_eye.pupil_position[1] += step_y_right

        self.left_eye.pupil_position[0] += step_x_left
        self.left_eye.pupil_position[1] += step_y_left

        # Move the pupil
        self.right_eye.pupil.pos = (self.right_eye.center_x + self.right_eye.pupil_position[0] - self.right_eye.pupil_radius,
                                     self.right_eye.center_y + self.right_eye.pupil_position[1] - 3 * self.right_eye.pupil_radius)

        self.left_eye.pupil.pos = (self.left_eye.center_x + self.left_eye.pupil_position[0] - self.left_eye.pupil_radius,
                                     self.left_eye.center_y + self.left_eye.pupil_position[1] - 3 * self.left_eye.pupil_radius)
        
        # Redraw the right eye widget
        self.right_eye.canvas.ask_update()
        self.left_eye.canvas.ask_update()

        # If reached the target position, stop the clock and reset movement state
        if abs(step_x_right) < 0.1 and abs(step_y_right) < 0.1:
            Clock.unschedule(self.move_pupil_back_smoothly)
            self.movement_in_progress = False
            print("reset einde")

#------------------------------------------------------------------------------------------------
            
#-------------------------------- Cordinaten ----------------------------------------------------
            
    def on_touch_down(self, touch):
        print("Clicked at:", touch.pos)
        
        print("pos",self.left_eye.pupil.pos)
        print("position",self.left_eye.pupil_position)
        if not self.movement_in_progress:
            touch_x, touch_y = touch.pos
            self.update_pupils(touch_x, touch_y)
            self.start_timer(instance=None)
            self.reset_timer()
            #self.play_music()

    def on_touch_up(self, touch):
        print("up")

    def on_touch_move(self, touch):
        if not self.movement_in_progress:
            self.movement_in_progress = True 
            touch_x, touch_y = touch.pos
            self.update_pupils(touch_x, touch_y)
            self.start_timer(instance=None)
            self.reset_timer()
            #self.play_music()

    def play_music(self):
        mp3_file_path = "zene/zene.mp3"  # Update the file path to match your MP3 file
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file_path)
        pygame.mixer.music.play()
        print(mp3_file_path, "is playing...")

    def stop_music(self):
        pygame.mixer.init()
        pygame.mixer.music.stop()
        
    


    def update_pupils(self, touch_x, touch_y):
            # Calculate the distance and angle of the touch relative to the center of each eye
        left_eye_distance = math.sqrt((touch_x - self.left_eye.center_x) ** 2 + (touch_y - self.left_eye.center_y) ** 2)
        left_eye_angle = math.atan2(touch_y - self.left_eye.center_y, touch_x - self.left_eye.center_x)

        right_eye_distance = math.sqrt((touch_x - self.right_eye.center_x) ** 2 + (touch_y - self.right_eye.center_y) ** 2)
        right_eye_angle = math.atan2(touch_y - self.right_eye.center_y, touch_x - self.right_eye.center_x)

        # Ensure the pupils stay within the eye boundaries
        max_distance_left = (self.left_eye.radius - self.left_eye.pupil_radius) * 0.5
        if left_eye_distance > max_distance_left:
            left_eye_distance = max_distance_left

        max_distance_right = (self.right_eye.radius - self.right_eye.pupil_radius) * 0.5
        if right_eye_distance > max_distance_right:
            right_eye_distance = max_distance_right

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
        self.movement_in_progress = False


#------------------------------------------------------------------------------------------------
            
#----------------------------------------- Timer ------------------------------------------------
       

    def start_timer(self, instance): 
        self.time_limit = 2
        self.start_time = time.time()     
        self.elapsed_time = 0
        self.start_time = time.time()
        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 0.1)

    def reset_timer(self):
        self.start_time = time.time()
        print("pos",self.left_eye.pupil.pos)
        self.stop_music()

    def update_timer(self, dt):
        current_time = time.time()
        self.elapsed_time = current_time - self.start_time

        if self.elapsed_time > self.time_limit:
            Clock.unschedule(self.update_timer)
        
            self.restart_timer(instance=None) 

            Clock.schedule_once(self.reset_pupil_position, 1)


    def restart_timer(self, instance):
        self.reset_timer()
        self.start_timer(instance)
    
#------------------------------------------------------------------------------------------------          
            
class MyApp(App):
    def build(self):
        return MyFloatLayout()

    

if __name__ == '__main__':
    MyApp().run()