
from util import *
from touch_manager import TouchEvent


class VisualCircularList:
    def __init__(self, box, items, font, text_color=M_WHITE.as565(), frame_color=M_CYAN.as565()):
        self.box = box
        self.items = items
        self.font = font
        self.text_color = text_color
        self.frame_color = frame_color
        self.selected_index = 0
        self.click_callback = None
        self.start_point = None
        self.end_point = None
        self.drag_events = False
        self.last_selected_index = None
        self.top_index = 0
        self.inner_box = self.box.inset_by(70)
        self.display_count = (self.inner_box.height() - 4) // font.HEIGHT
        self.angle_tick = 30
        self.last_draw_point = None
        self.drag_ball_radius = 15


    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__, self.box)

    def set_view(self, view):
        self.view = view

    def register_click_handler(self, click_callback):
        self.click_callback = click_callback

    def set_drag_events(self, flag):
        self.drag_events = flag

    def visible_items(self):
        start = self.top_index
        stop = min(self.top_index + self.display_count, len(self.items))
        return self.items[start:stop]

    def draw_on(self, display, view_origin, view_extent):
        inner_radius = int(math.sqrt(self.inner_box.width()**2 * 2)) // 2 + 5
        display.draw_circle(self.inner_box.center().x, self.inner_box.center().y, inner_radius, self.frame_color)
        text_height = self.font.HEIGHT
        x = self.inner_box.origin.x + 2
        y = self.inner_box.origin.y + 2
        display_range = range(self.top_index, self.top_index + self.display_count)
        item_count = len(self.items)
        for index, item in enumerate(self.visible_items()):
            if self.selected_index is not None and index == (self.selected_index - self.top_index):
                display.screen.fill_rect(x, y, self.inner_box.extent.x - 4, self.font.HEIGHT, self.text_color)
                display.draw_text(item, self.font, x, y, M_BLACK.as565(), self.text_color)
            else:
                display.screen.fill_rect(x, y, self.inner_box.extent.x - 4, self.font.HEIGHT, M_BLACK.as565())
                display.draw_text(item, self.font, x, y, self.text_color, M_BLACK.as565())
            y += self.font.HEIGHT
        angle = math.radians(90 - (self.selected_index * self.angle_tick))
        ball_radius = (120 - inner_radius) // 2 + inner_radius
        ball_x = int(math.cos(angle) * ball_radius) + 120
        ball_y = 240 - (int(math.sin(angle) * ball_radius) + 120)
        if self.last_draw_point is not None:
            display.fill_circle(self.last_draw_point.x, self.last_draw_point.y, self.drag_ball_radius, M_BLACK.as565())
        self.last_draw_point = Point(ball_x, ball_y)
        display.fill_circle(ball_x, ball_y, self.drag_ball_radius, self.frame_color)

    def register_for_touch_events(self, touch_manager):
        touch_manager.register_interest_in(TouchEvent.TOUCH_RELEASE, self.inner_box, self.handle_touch_click)
        touch_manager.register_interest_in(TouchEvent.TOUCH_DRAG_START, self.box, self.handle_touch_drag_start)
        touch_manager.register_interest_in(TouchEvent.TOUCH_DRAG_CONTINUE, self.box, self.handle_touch_drag)
        # if not self.drag_events:
            # touch_manager.register_interest_in(TouchEvent.TOUCH_DRAG_STOP, self.box, self.handle_touch_drag_stop)

    def handle_touch_click(self, touch_event):
        item = self.items[self.selected_index]
        if item[0] == '*':
            self.items[self.selected_index] = item[1:]
        else:
            self.items[self.selected_index] = '*{}'.format(item)
        self.view.redraw()

    def handle_touch_drag_start(self, touch_event):
        self.last_delta_index = self.selected_index

    def handle_touch_drag(self, touch_event):
        current_point = touch_event.touch_point()
        rotation_point = Point(current_point.x - 120, (240 - current_point.y) - 120)
        if rotation_point.x == 0:
            if rotation_point.y > 0:
                angle = 0.0
            else:
                angle = 180.0
        else:
            fraction = float(rotation_point.y) / float(rotation_point.x)
            angle_radians = math.atan(fraction)
            angle = math.degrees(angle_radians)
            angle = (90 - angle) % 360
            if rotation_point.x < 0:
                angle = angle + 180
        delta_index = int(angle // self.angle_tick)
        if not (delta_index == self.last_delta_index):
            self.last_delta_index = delta_index
            max_top_index = len(self.items) - self.display_count
            self.top_index = min(max(0, delta_index), max_top_index)
            self.selected_index = min(max(0, delta_index), len(self.items) - 1)
            self.view.redraw()
