from display import *
from util import *
import time
from visual_dialog import *

d = Display()
box = Rectangle(Point(0, 0), Point(240, 240))
items = ['Start -> BC#1', 'Start -> BC#2', 'Start -> Finish', 'BC#1 -> BC#2', 'BC#2 -> BC#1', 'BC#1 -> Finish', 'BC#2 -> Finish']
cl = VisualCircularList(box, items, font_15, M_WHITE.as565(), M_CYAN.as565())

cl.draw_on(d, box.origin, box.extent)

print("Hello world")
