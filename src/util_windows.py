
from util import *
from window import *
import NotoSans_15 as font_15
import NotoSans_20 as font_20
import NotoSans_25 as font_25
import NotoSans_32 as font_32


class NumericEntryWindow:

    def __init__(self, window_manager, display, value_callback, initial_value=0, value_prefix = ''):
        self.window_manager = window_manager
        self.display = display
        self.value = str(initial_value)
        self.value_callback = value_callback
        self.value_prefix = value_prefix
        self.build_root_window()

    def build_root_window(self):
        self.root_window = Window(self.display, "NumericInput")

        box = Rectangle(Point(0, 0), Point(240, 240))
        main_view = View("Top", box.origin, box.extent)
        self.root_window.add_view(main_view)

        top_view = View("Top", Point(0, 0), Point(240, 58))
        middle_view = View("Middle", Point(40,58), Point(160, 124))
        bottom_view = View("Bottom", Point(0, 182), Point(240, 58))

        self.root_window.add_view(top_view)
        self.root_window.add_view(middle_view)
        self.root_window.add_view(bottom_view)

        value_box = Rectangle(Point(0, 15), Point(240, 40))
        self.value_label = VisualLabel(value_box, '{}{}'.format(self.value_prefix, self.value), font_25, True, Color.LABEL, Color.BACKGROUND)
        top_view.add_component(self.value_label)

        button_list = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '.', '0', '<=']
        button_index = 0
        for y in range(4):
            for x in range(3):
                x_pos = x * 53
                y_pos = y * 31
                label = button_list[button_index]
                button = VisualButton(Rectangle(Point(x_pos, y_pos), Point(52, 30)), label, font_20, Color.BUTTON)
                middle_view.add_component(button)
                button.register_click_handler(self.clicked_button, label)
                button_index += 1

        plus_minus_button = VisualButton(value_box, '', font_20, Color.BUTTON, False)
        plus_minus_button.register_click_handler(self.clicked_plus_minus)
        top_view.add_component(plus_minus_button)

        ok_button = VisualButton(Rectangle(Point(60, 10), Point(55, 30)), 'OK', font_20, Color.BUTTON)
        ok_button.register_click_handler(self.clicked_ok)
        cancel_button = VisualButton(Rectangle(Point(120, 10), Point(55, 30)), 'X', font_20, Color.BUTTON)
        cancel_button.register_click_handler(self.clicked_cancel)
        bottom_view.add_component(ok_button)
        bottom_view.add_component(cancel_button)

        self.window_manager.push_window(self.root_window)

    def clicked_button(self, label):
        digits = '0123456789'
        backspace = '<='
        if label in digits:
            if self.value == '0':
               self.value = label
            else:
               self.value = '{}{}'.format(self.value, label)
        if label == '.':
            if '.' not in self.value:
                self.value = '{}.'.format(self.value)
        if label == backspace:
            if len(self.value) > 0:
                self.value = self.value[0:-1]
            if self.value == '':
                self.value = '0'
        self.value_label.set_text('{}{}'.format(self.value_prefix, self.value))

    def clicked_plus_minus(self):
        if self.value.startswith('-'):
            self.value = self.value[1:]
        else:
            self.value = '-{}'.format(self.value)
        self.value_label.set_text('{}{}'.format(self.value_prefix, self.value))

    def clicked_ok(self):
        if '.' in self.value:
            self.value = float(self.value)
        else:
            if self.value == '':
                self.value = 0
            else:
                self.value = int(self.value)
        self.window_manager.pop_window()
        self.value_callback(self.value)

    def clicked_cancel(self):
        self.value = None
        self.window_manager.pop_window()
        self.value_callback(self.value)

    def get_value(self):
        return self.value
