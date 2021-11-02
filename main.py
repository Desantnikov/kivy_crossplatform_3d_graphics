from itertools import chain

from kivy.app import App, Widget
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

from calculations.cube import Cube, SIDE
from calculations.pos import Pos
from shadow_texture import make_texture


ROW_LENGTH = 4 # should be dividable by 2
HEIGHT = 1
DEPTH = 4

# multipliers
SPACES_X =9 # two-axis coords

CUBE_SIZE = 13

BRIGHTNESS_MULTIPLIER = 0.1 #

#direct values
X_OFFSET = 3
Y_OFFSET = 0

SPACES_Y = 7

INITIAL_BRIGHTNESS = .7

cubes_array = []
for height_level in range(HEIGHT): #Y_OFFSET, ROW_LENGTH + Y_OFFSET):
    cubes_plot = []
    for row_number in range(DEPTH):#Y_OFFSET, ROW_LENGTH + Y_OFFSET):

        cubes_row = []
        for real_cube_nuber, cube_number in enumerate(range(ROW_LENGTH * 2, 0, -2)):
            pos = Pos(
                x=(cube_number * SPACES_X + row_number * SPACES_X + X_OFFSET),
                y=(row_number * SPACES_X + (5 + height_level * SPACES_Y)),
            )
            cubes_row.append(Cube(front_bottom_left=pos, size=CUBE_SIZE, resize_back_size=0))


        cubes_plot.append(cubes_row)


    cubes_array.append(cubes_plot)




class MyWidget(Widget):
    def __init__(self, **kwargs):
        self.rect = None
        super(MyWidget, self).__init__(**kwargs)

        self.sides_color_values = [
            (1, 1, 0.999),  # right
            (1, 0.999, 1),  # front
            (0.999, 1, 1),  # top
        ]

        from calculations.cube import SIDE
        #

        # self.sides_color_values = {
        #     side: (
        #         INITIAL_BRIGHTNESS,
        #         INITIAL_BRIGHTNESS,
        #         INITIAL_BRIGHTNESS,
        #     )
        #     for side
        #     in Cube.SIDES_DRAWING_ORDER
        # }


        self.sides = []
        with self.canvas:
            for plot_idx, plot in enumerate(cubes_array, start=2):  # height (z)

                for row_idx, row in enumerate(reversed(plot), start=2):  # rows from back to front

                    for cube_idx, cube in enumerate(reversed(row), start=2):  # cubes from left to right  #

                        for side_idx, side in enumerate(cube.SIDES_DRAWING_ORDER):

                            def _colors_update(color_tuple, side_shadow_multiplier):
                                color = []
                                for color_part in color_tuple:
                                    color.append(color_part * side_shadow_multiplier * BRIGHTNESS_MULTIPLIER)

                                return color

                            side_shadow_multiplier_map = {
                                SIDE.TOP:  (plot_idx + plot_idx+ plot_idx + cube_idx + row_idx + SPACES_Y + SPACES_X) / 7,
                                SIDE.FRONT: (plot_idx + row_idx + cube_idx + row_idx + row_idx + SPACES_Y + SPACES_X) / 7,
                                SIDE.RIGHT: (cube_idx + plot_idx + cube_idx + row_idx + cube_idx + SPACES_Y + SPACES_X) / 7,
                            }

                            side_shadow_multiplier = side_shadow_multiplier_map[side]




                            color = self.sides_color_values[side]
                            color_updated = _colors_update(color_tuple=color,
                                                           side_shadow_multiplier=side_shadow_multiplier)


                            Color(rgb=color_updated)
                            self.sides.append(cube.sides[side].draw())



        from kivy.animation import Animation
        from calculations.cube import SIDE


    def on_touch_up(self, touch):
        print(touch)
        for z in cubes_array:
            for x in z:
                for cube in x:
                    for side in cube.sides.values():
                        touch_x = touch.pos[0]
                        touch_y = touch.pos[1]

                        if touch_x > side.corners[0].x * CUBE_SIZE and touch_y > side.corners[0].y * CUBE_SIZE:
                            print('1')
                            if touch_x < side.corners[2].x * CUBE_SIZE and touch_y < side.corners[2].y * CUBE_SIZE:
                                print('2')

                                print('Found cube!')

                                initial_coord_values = cube.sides[SIDE.TOP].get_coords()

                                modified_coord_values = [
                                    idx + coord * 20
                                    if idx % 2
                                    else
                                    coord * idx
                                    for idx, coord
                                    in enumerate(initial_coord_values)
                                ]
                                from kivy.animation import Animation
                                anim = Animation(points=modified_coord_values, duration=3)
                                anim.start(self.sides[-1])





class RootWidgetBoxLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidgetBoxLayout, self).__init__(**kwargs)

        self.bind(on_resize=self._update_rect)
        self.draw_background()

        my_widget = MyWidget(size=(500,500))
        self.add_widget(my_widget)

    def draw_background(self):
        with self.canvas.before:
            Color(rgb=(228, 228, 228))

            self.rect = Rectangle(pos=self.pos, size=self.size, texture=make_texture())

            points = [Pos(10, 10), Pos(450, 450), Pos(1600, 450), Pos(1600, 10)]



            pos_coords = chain(*[pos.coords() for pos in points])

            Color(rgb=(0.9, 0.4, 0.4))
            self.rect_two = Quad(points=pos_coords)  # , texture=make_texture(1000))  # , texture=texture)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MyApp(App):
    def build(self):
        self.bind(on_resize=self._update_rect)

        Window.size = (1400, 1000)
        Window.top = 20
        Window.left = 100
        # Window.clearcolor = (0.9, 0.9, 0.9, 0.5)

        self.root = root = RootWidgetBoxLayout()

        return root

    def _update_rect(self, instance, value):
        self.top = instance.top
        self.left = instance.left
        self.size = instance.size


if __name__ == '__main__':
    MyApp().run()
