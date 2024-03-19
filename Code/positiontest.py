from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window


class EyesWidget(Widget):
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)
        with self.canvas:
            # Draw a white ellipse (you can adjust the size as needed)
            self.ellipse = Ellipse(pos=(Window.width / 2 - 25, Window.height / 2 - 25), size=(50, 50))
            Color(1, 1, 1)  # White color

    def on_touch_down(self, touch):
        print("Clicked at:", touch.pos)
        x_pos, y_pos = touch.pos
        print("X:", x_pos)
        print("Y:", y_pos)

        # Move the ellipse to the position where clicked
        self.ellipse.pos = (x_pos - 25, y_pos - 25)

    def on_touch_move(self, touch):
        print("Touch moved to:", touch.pos)
        
        # Update the position of the ellipse while dragging
        self.ellipse.pos = (touch.pos[0] - 25, touch.pos[1] - 25)


class EyesApp(App):
    def build(self):
        return EyesWidget()


if __name__ == '__main__':
    EyesApp().run()
