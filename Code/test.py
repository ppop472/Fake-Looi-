from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.clock import mainthread


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


class MyFloatLayout(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movement_in_progress = False  # Variable to track movement state
        self.reset_clock_time = 1  # Default reset clock time

        self.button = Button(text='Center Button', size_hint=(None, None), size=(100, 50),
                             pos_hint={'x': 0, 'y': 0.90})
        self.button.bind(on_press=self.on_button_click)

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

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    @mainthread
    def on_button_click(self, instance):
        if self.movement_in_progress:
            print("not gonna move hahahahaaha")
            return

        if not self.movement_in_progress:  # Check if no movement is in progress
            self.movement_in_progress = True
            print("movement aan")
            # Move the pupil of the right eye smoothly to (50, 50)
            Clock.schedule_interval(self.move_pupil_smoothly, 0.02)
            Clock.schedule_once(self.start_reset_clock, self.reset_clock_time)

    def start_reset_clock(self, dt):
        # Start the reset clock only if no movement is in progress
        if not self.movement_in_progress:
            Clock.schedule_once(self.reset_pupil_position, self.reset_clock_time)

    def move_pupil_smoothly(self, dt):
        # Calculate the distance to move in each step
        step_x_right = (-80 - self.right_eye.pupil_position[0]) / 5
        step_y_right = (0 - self.right_eye.pupil_position[1]) / 10

        step_x_left = (60 - self.left_eye.pupil_position[0]) / 5
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
        self.right_eye.canvas.ask_update()
        # If reached the target position, stop the clock and reset movement state
        if abs(step_x_right) < 0.1 and abs(step_y_right) < 0.1:
            Clock.unschedule(self.move_pupil_smoothly) 
            self.movement_in_progress = False
            print("movement uit")

        if abs(step_x_left) < 0.1 and abs(step_y_left) < 0.1:
            Clock.unschedule(self.move_pupil_smoothly)
            self.movement_in_progress = False
            print("movement uit")

    def reset_pupil_position(self, dt):
        # Move the pupil of the right eye smoothly back to its original position
        if not self.movement_in_progress:
            self.movement_in_progress = True
            print("reset begin")
            Clock.schedule_interval(self.move_pupil_back_smoothly, 0.0001)

    def move_pupil_back_smoothly(self, dt):
        # Calculate the distance to move in each step
        step_x_right = (-10 - self.right_eye.pupil_position[0]) / 10
        step_y_right = (0 - self.right_eye.pupil_position[1]) / 10

        step_x_left = (-10 - self.left_eye.pupil_position[0]) / 10
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


class MyApp(App):
    def build(self):
        return MyFloatLayout()


if __name__ == '__main__':
    MyApp().run()
