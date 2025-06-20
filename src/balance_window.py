
import NotoSans_15 as font_15
import NotoSans_20 as font_20
import NotoSans_25 as font_25
import NotoSans_32 as font_32

from machine import Pin, Timer, ADC

from util import *
from util_windows import *
from telemetry import *
from window import *
import json
from secret import *


class BalanceDroidWindow:
    def __init__(self, window_manager, display):
        self.window_manager = window_manager
        self.display = display
        self.build_root_window()

    def build_root_window(self):
        self.root_window = Window(self.display, "Balance Droid")

        box = Rectangle(Point(0, 0), Point(240, 240))
        main_view = View("Top", box.origin, box.extent)
        self.root_window.add_view(main_view)

        button = VisualButton(Rectangle(Point(0, 78), Point(160, 80)), '', font_15, Color.LABEL, False)
        main_view.add_component(button)
        button.register_click_handler(self.open_balance_window)

        image = VisualJpgImage(box, 'Pendu-240.jpg')
        main_view.add_component(image)

    def open_balance_window(self):
        BalanceChooseWindow(self.window_manager, self.display)


class BalanceChooseWindow:
    def __init__(self, window_manager, display):
        self.window_manager = window_manager
        self.display = display
        self.build_balance_choose_window()
        self.window_manager.push_window(self.choose_window)

    def build_balance_choose_window(self):
        self.choose_window = Window(self.display, 'Balance Choose')

        top_view = View("Top", Point(0, 0), Point(240, 58))
        middle_view = View("Middle", Point(40,58), Point(160, 124))
        bottom_view = View("Bottom", Point(0, 182), Point(240, 58))

        self.choose_window.add_view(top_view)
        self.choose_window.add_view(middle_view)
        self.choose_window.add_view(bottom_view)

        label = VisualLabel(Point(0, 20), 'PENDU', font_32, True, Color.TITLE)
        top_view.add_component(label)

        button_y = 20
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "MISSION", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_mission)

        button_y += 40
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "SENSORS", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_sensors)

        button_y += 40
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "PID", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_pid)

    def clicked_mission(self):
        print('BALANCER Missions')
        BalanceMissionWindow(self.window_manager, self.display)

    def clicked_sensors(self):
        print('BALANCER Sensors')
        # BalanceSensorWindow(self.window_manager, self.display)

    def clicked_pid(self):
        print('BALANCER PID')
        BalanceTunePidWindow(self.window_manager, self.display)


class BalanceTunePidWindow:
    def __init__(self, window_manager, display):
        self.window_manager = window_manager
        self.display = display
        self.p_value = 0.0
        self.i_value = 0.0
        self.d_value = 0.0
        self.build_balance_choose_window()
        self.window_manager.push_window(self.choose_window)
        self.get_pid_values()

    def build_balance_choose_window(self):
        self.choose_window = Window(self.display, 'Balance Tune PID')

        top_view = View("Top", Point(0, 0), Point(240, 58))
        middle_view = View("Middle", Point(40,58), Point(160, 124))
        bottom_view = View("Bottom", Point(0, 182), Point(240, 58))

        self.choose_window.add_view(top_view)
        self.choose_window.add_view(middle_view)
        self.choose_window.add_view(bottom_view)

        label = VisualLabel(Point(0, 28), 'PID Tuning', font_32, True, Color.TITLE)
        top_view.add_component(label)

        button_y = 20
        button = VisualButton(Rectangle(Point(0, button_y), Point(40, 35)), "P", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_p)
        self.p_label = VisualLabel(Point(50, button_y + 3), str(self.p_value), font_25, False, Color.TITLE)
        middle_view.add_component(self.p_label)

        button_y += 40
        button = VisualButton(Rectangle(Point(0, button_y), Point(40, 35)), "I", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_i)
        self.i_label = VisualLabel(Point(50, button_y + 3), str(self.i_value), font_25, False, Color.TITLE)
        middle_view.add_component(self.i_label)

        button_y += 40
        button = VisualButton(Rectangle(Point(0, button_y), Point(40, 35)), "D", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_d)
        self.d_label = VisualLabel(Point(50, button_y + 3), str(self.d_value), font_25, False, Color.TITLE)
        middle_view.add_component(self.d_label)
        self.choose_window.register_about_to_close(self.about_to_close)

    def about_to_close(self, window):
        print('Shutting down')

    def clicked_p(self):
        print('PID - P')
        NumericEntryWindow(self.window_manager, self.display, self.p_callback, self.p_value, 'P: ')

    def p_callback(self, new_value):
        if new_value is None:
            return
        self.p_value = new_value
        self.p_label.set_text(str(self.p_value))
        self.send_pid_packet()

    def clicked_i(self):
        print('PID - I')
        NumericEntryWindow(self.window_manager, self.display, self.i_callback, self.i_value, 'I: ')

    def i_callback(self, new_value):
        if new_value is None:
            return
        self.i_value = new_value
        self.i_label.set_text(str(self.i_value))
        self.send_pid_packet()

    def clicked_d(self):
        print('PID - D')
        NumericEntryWindow(self.window_manager, self.display, self.d_callback, self.d_value, 'D: ')

    def d_callback(self, new_value):
        if new_value is None:
            return
        self.d_value = new_value
        self.d_label.set_text(str(self.d_value))
        self.send_pid_packet()

    def send_pid_packet(self):
        print('sending PID packet')
        self.telemetry = Telemetry(PENDU_MAC_ADDRESS)
        packet_string = json.dumps(
            {'type': 'SET_PID', 'p_value': self.p_value, 'i_value': self.i_value, 'd_value': self.d_value})
        result = self.telemetry.send_packet(packet_string)
        print('Send result: {}'.format(result))
        self.telemetry.shutdown()

    def get_pid_values(self):
        print('sending GET_PID packet')
        self.telemetry = Telemetry(PENDU_MAC_ADDRESS)
        self.telemetry.register_telemetry_callback(self.receive_pid_values)
        packet_string = json.dumps({'type': 'GET_PID'})
        result = self.telemetry.send_packet(packet_string)
        print('Send result: {}'.format(result))

    def receive_pid_values(self, packet):
        self.p_value = packet['pid_p']
        self.p_label.set_text(str(self.p_value))
        self.i_value = packet['pid_i']
        self.i_label.set_text(str(self.i_value))
        self.d_value = packet['pid_d']
        self.d_label.set_text(str(self.d_value))
        print('Got PID values from robot - P: {} I: {} D: {}'.format(self.p_value, self.i_value, self.d_value))
        Timer(1, mode=Timer.ONE_SHOT, period=100, callback=self.shutdown_callback)

    # We need to do this here to make sure ESPNow has finished
    def shutdown_callback(self, timer):
        self.telemetry.shutdown()


class BalanceMissionWindow:
    def __init__(self, window_manager, display):
        self.window_manager = window_manager
        self.display = display
        self.build_main_window()

    def build_main_window(self):
        mission_names = ['Balance', 'Quick Trip', 'Line Follow', 'Wander']
        windows = []
        for name in mission_names:
            windows.append(self.build_window_for_mission(name))
        chain = WindowChain('Mission Chooser', windows)
        self.window_manager.push_window_chain(chain)

    def build_window_for_mission(self, mission_name):
        window = Window(self.display, 'Mission: {}'.format(mission_name))

        top_view = View("Top", Point(0, 0), Point(240, 58))
        middle_view = View("Middle", Point(40,58), Point(160, 120))
        bottom_view = View("Bottom", Point(0, 182), Point(240, 58))

        window.add_view(top_view)
        window.add_view(middle_view)
        window.add_view(bottom_view)

        label = VisualLabel(Point(0, 20), 'PENDU', font_32, True, Color.TITLE)
        top_view.add_component(label)

        label = VisualLabel(Point(0, 20), 'Mission: {}'.format(mission_name), font_20, True, Color.LABEL)
        middle_view.add_component(label)

        button_y = 60
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "RUN", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_run_mission, mission_name)

        button_y += 40
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "CONFIGURE", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_edit_mission, mission_name)

        return window

    def clicked_run_mission(self, mission_name):
        print('Run Mission: {}'.format(mission_name))
        BalanceRunMissionWindow(self.window_manager, self.display, mission_name)

    def clicked_edit_mission(self, mission_name):
        print('Edit Mission: {}'.format(mission_name))
        # BalanceEditMissionWindow(self.window_manager, self.display)


class BalanceRunMissionWindow:
    def __init__(self, window_manager, display, mission_name):
        self.window_manager = window_manager
        self.display = display
        self.mission_name = mission_name
        self.mission = BalanceMission(self.mission_name)
        self.build_main_window()
        self.window_manager.push_window(self.main_window)
        self.window_manager.disable_screensaver()
        self.update_timer = Timer(1, mode=Timer.PERIODIC, freq=2, callback=self.update)
        self.telemetry = Telemetry(PENDU_MAC_ADDRESS)
        self.telemetry.register_telemetry_callback(self.get_telemetry_packet)
        self.telemetry.send_packet(self.mission.mission_started_packet())

    def build_main_window(self):
        self.main_window = Window(self.display, "{} Run".format(self.mission_name))

        top_view = View("Top", Point(0, 0), Point(240, 58))
        middle_view = View("Middle", Point(40,58), Point(160, 124))
        bottom_view = View("Bottom", Point(0, 182), Point(240, 58))

        self.main_window.add_view(top_view)
        self.main_window.add_view(middle_view)
        self.main_window.add_view(bottom_view)

        self.running_label = VisualLabel(Rectangle(Point(55, 20), Point(75, 20)), 'PAUSED', font_15, False, Color.ALERT_LABEL, Color.BACKGROUND)
        top_view.add_component(self.running_label)

        self.timer_label = VisualLabel(Rectangle(Point(135, 20), Point(50, 20)), '00:00', font_15, False, Color.LABEL, Color.BACKGROUND)
        top_view.add_component(self.timer_label)

        self.obstacle_label = VisualLabel(Rectangle(Point(0, 40), Point(160, 20)), 'Obstacles: ---', font_15, True, Color.LABEL, Color.BACKGROUND)
        top_view.add_component(self.obstacle_label)

        self.nav_label = VisualLabel(Rectangle(Point(0, 10), Point(160, 20)), 'NAV: Waypoint', font_15, True, Color.LABEL, Color.BACKGROUND)
        middle_view.add_component(self.nav_label)

        self.target_name_label = VisualLabel(Rectangle(Point(0, 35), Point(160, 20)), 'No Target', font_15, True, Color.LABEL, Color.BACKGROUND)
        middle_view.add_component(self.target_name_label)

        self.target_pos_label = VisualLabel(Rectangle(Point(0, 55), Point(160, 20)), 'Target: 0 @ 0', font_15, True, Color.LABEL, Color.BACKGROUND)
        middle_view.add_component(self.target_pos_label)

        self.position_label = VisualLabel(Rectangle(Point(0, 80), Point(160, 20)), 'Position: 0 @ 0', font_15, True, Color.LABEL, Color.BACKGROUND)
        middle_view.add_component(self.position_label)

        self.heading_label = VisualLabel(Rectangle(Point(0, 100), Point(160, 20)), 'Heading: 325', font_15, True, Color.LABEL, Color.BACKGROUND)
        middle_view.add_component(self.heading_label)

        self.robot_voltage_label = VisualLabel(Rectangle(Point(37, 10), Point(90, 20)), 'Robot 8.3v', font_15, False, Color.GOOD_LABEL, Color.BACKGROUND)
        bottom_view.add_component(self.robot_voltage_label)

        self.urc_voltage_label = VisualLabel(Rectangle(Point(127, 10), Point(90, 20)), 'URC 4.15v', font_15, False, Color.GOOD_LABEL, Color.BACKGROUND)
        bottom_view.add_component(self.urc_voltage_label)

        # No Draw (invisible) button
        button = VisualButton(Rectangle(Point(0, 0), Point(160, 124)), '', font_15, Color.LABEL, False)
        middle_view.add_component(button)
        button.register_click_handler(self.pause_toggle)

        self.main_window.register_about_to_close(self.about_to_close)

    def pause_toggle(self):
        self.mission.toggle_paused()
        self.telemetry.send_packet(self.mission.mission_status_packet())

    def update_window(self):
        if not self.mission.paused:
            self.mission.increment_run_time_ticks()
        pair = self.mission.running_string_and_color()
        self.running_label.set_text(pair[0])
        self.running_label.set_color(pair[1])
        self.timer_label.set_text(self.mission.run_time_string())
        self.obstacle_label.set_text(self.mission.obstacle_string())
        self.nav_label.set_text(self.mission.navigator_string())
        self.target_name_label.set_text(self.mission.target_name_string())
        self.target_pos_label.set_text(self.mission.target_location_string())
        self.position_label.set_text(self.mission.position_string())
        self.heading_label.set_text(self.mission.heading_string())
        self.robot_voltage_label.set_text(self.mission.robot_voltage_string())
        self.robot_voltage_label.set_color(self.voltage_color(self.mission.robot_voltage, 3))
        self.urc_voltage_label.set_text(self.mission.urc_voltage_string())
        self.urc_voltage_label.set_color(self.voltage_color(self.mission.urc_voltage, 1))

    def update(self, timer):
        self.mission.update()
        self.update_window()

    def voltage_color(self, voltage, cell_count):
        cell_voltage = voltage / cell_count
        if cell_voltage < 3.4:
            return Color.ALERT_LABEL
        if cell_voltage < 3.7:
            return Color.WARNING_LABEL
        return Color.GOOD_LABEL

    def get_telemetry_packet(self, packet):
        self.mission.process_telemetry_packet(packet)

    def about_to_close(self, window):
        self.telemetry.send_packet(self.mission.mission_ended_packet())
        print('Finished Mission: {}'.format(window.name))
        self.window_manager.enable_screensaver()
        self.update_timer.deinit()
        self.telemetry.shutdown()


class BalanceMission:
    def __init__(self, mission_name):
        self.mission_name = mission_name
        self.paused = True
        self.run_time = 0
        self.run_time_ticks = 0
        self.urc_voltage = 3.9
        self.battery = ADC(Pin(1))
        self.battery.atten(ADC.ATTN_11DB)  # get the full range 0 - 3.3v
        self.update_count = 0
        # Telemetry updated values below
        self.obstacles = '---'
        self.navigator = 'None'
        self.current_state = 'None'
        self.target_position = Point(150.0, 125.0)
        self.target_name = ''
        self.position = Point(0.0, 0.0)
        self.heading = 0
        self.robot_voltage = 12.4

    def update(self):
        self.update_count += 1
        if self.update_count == 2:
            self.update_count = 0
            # Update the URC voltage once per second
            self.urc_voltage = get_battery_level(self.battery)

    def mission_started_packet(self):
        return json.dumps({'type': 'MISSION-STARTED', 'mission_name': self.mission_name})

    def mission_status_packet(self):
        return json.dumps({'type': 'MISSION-STATUS', 'paused': self.pause_status()})

    def mission_ended_packet(self):
        return json.dumps({'type': 'MISSION-ENDED'})

    def pause_status(self):
        if self.paused:
            return True
        else:
            return False

    # Call this at 2Hz
    def increment_run_time_ticks(self):
        self.run_time_ticks += 1
        if self.run_time_ticks == 2:
            self.run_time_ticks = 0
            self.run_time += 1

    def toggle_paused(self):
        self.paused = not self.paused

    def run_time_string(self):
        seconds = self.run_time % 60
        minutes = self.run_time // 60
        return '{:02d}:{:02d}'.format(minutes, seconds)

    def running_string_and_color(self):
        if self.paused:
            return ('PAUSED', Color.ALERT_LABEL)
        else:
            return ('RUNNING', Color.GOOD_LABEL)

    def target_heading(self):
        return self.position.compass_heading_to(self.target_position)

    def target_range(self):
        return self.position.distance_to(self.target_position)

    def target_name_string(self):
        if self.target_name == '':
            return 'No Target'
        else:
            return self.target_name

    def target_location_string(self):
        if self.target_name == '':
            return '0.0m @ 0.0 deg'
        else:
            return '{:.1f}m @ {:.1f} deg'.format(self.target_range(), int(self.target_heading()))

    def obstacle_string(self):
        return 'Obstacles: {}'.format(self.obstacles)

    def position_string(self):
        return 'Position: {:.1f} @ {:.1f}'.format(self.position.x, self.position.y)

    def current_state_string(self):
        return 'FSM: {}'.format(self.current_state)

    def navigator_string(self):
        return 'NAV: {}'.format(self.navigator)

    def heading_string(self):
        return 'Heading: {:.1f} deg'.format(self.heading)

    def robot_voltage_string(self):
        return 'Robot {:.1f}v'.format(self.robot_voltage)

    def urc_voltage_string(self):
        return 'URC {:.2f}v'.format(self.urc_voltage)

    def process_telemetry_packet(self, packet):
        if 'rv' in packet:
            self.robot_voltage = packet['rv']
        if 'heading' in packet:
            self.heading = packet['heading']
        if 'pos' in packet:
            elements = packet['pos']
            self.position = Point(elements[0], elements[1])
        if 't_pos' in packet:
            elements = packet['t_pos']
            self.target_position = Point(elements[0], elements[1])
        if 't_name' in packet:
            self.target_name = packet['t_name']
        if 'nav' in packet:
            self.navigator = packet['nav']
        if 'obstacle' in packet:
            self.obstacles = packet['obstacle']

