from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
import math

class LeftEye(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.69, 0.86, 0.95, 1)  # Eye color
            self.left_iris = Ellipse(pos=(200, 200), size=(100, 100))  # Adjust size and position as needed

            Color(0, 0, 0, 1)  # Pupil color
            self.left_pupil_radius = 10  # Pupil radius
            self.left_pupil = Ellipse(pos=(220, 220), size=(20, 20))  # Adjust size and position as needed

            Color(1, 0, 0, 0)  # Rectangle color (example)
            Rectangle(pos=(200, 200), size=(100, 100))  # Example rectangle (adjust as needed)

class RightEye(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.69, 0.86, 0.95, 1)  # Eye color
            self.right_iris = Ellipse(pos=(600, 200), size=(100, 100))  # Adjust size and position as needed

            Color(0, 0, 0, 1)  # Pupil color
            self.right_pupil_radius = 10  # Pupil radius
            self.right_pupil = Ellipse(pos=(620, 220), size=(20, 20))  # Adjust size and position as needed

            Color(1, 0, 0, 0)  # Rectangle color (example)
            Rectangle(pos=(600, 200), size=(100, 100))  # Example rectangle (adjust as needed)

class MyFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add left eye to layout
        self.left_eye = LeftEye()
        self.add_widget(self.left_eye)

        # Add right eye to layout
        self.right_eye = RightEye()
        self.add_widget(self.right_eye)

    def update_pupils(self, touch_x, touch_y):
        # Calculate new positions of the pupils based on the mouse position
        left_eye_center = (250, 250)  # Adjust as needed
        right_eye_center = (650, 250)  # Adjust as needed

        # Calculate distance and angle of the touch relative to the center of each eye
        left_eye_distance = math.sqrt((touch_x - left_eye_center[0]) ** 2 + (touch_y - left_eye_center[1]) ** 2)
        left_eye_angle = math.atan2(touch_y - left_eye_center[1], touch_x - left_eye_center[0])

        right_eye_distance = math.sqrt((touch_x - right_eye_center[0]) ** 2 + (touch_y - right_eye_center[1]) ** 2)
        right_eye_angle = math.atan2(touch_y - right_eye_center[1], touch_x - right_eye_center[0])

        # Ensure the pupils stay within the eye boundaries (adjust as needed)
        max_distance_left = 30  # Maximum distance of pupil from left eye center
        max_distance_right = 30  # Maximum distance of pupil from right eye center

        if left_eye_distance > max_distance_left:
            left_eye_distance = max_distance_left

        if right_eye_distance > max_distance_right:
            right_eye_distance = max_distance_right

        # Calculate new positions of the pupils
        left_eye_pupil_x = left_eye_distance * math.cos(left_eye_angle) + left_eye_center[0] - 10  # Adjust for pupil size
        left_eye_pupil_y = left_eye_distance * math.sin(left_eye_angle) + left_eye_center[1] - 10  # Adjust for pupil size

        right_eye_pupil_x = right_eye_distance * math.cos(right_eye_angle) + right_eye_center[0] - 10  # Adjust for pupil size
        right_eye_pupil_y = right_eye_distance * math.sin(right_eye_angle) + right_eye_center[1] - 10  # Adjust for pupil size

        # Update positions of the pupils
        self.left_eye.left_pupil.pos = (left_eye_pupil_x, left_eye_pupil_y)
        self.right_eye.right_pupil.pos = (right_eye_pupil_x, right_eye_pupil_y)

    def on_touch_down(self, touch):
        # Call update_pupils method when screen is touched
        self.update_pupils(touch.x, touch.y)

    def on_touch_move(self, touch):
        # Call update_pupils method when mouse is moved on the screen
        self.update_pupils(touch.x, touch.y)

class MyApp(App):
    def build(self):
        return MyFloatLayout()

if __name__ == '__main__':
    MyApp().run()
