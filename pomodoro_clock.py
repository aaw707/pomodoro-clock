import PySimpleGUI as sg
from win10toast import ToastNotifier
from psgtray import SystemTray
import csv
import pandas as pd
import datetime as dt

# parameters
default_mins = 25
font = "Courier"
font_size = 12
background_color = "#FFEEED"
button_color = "#FFC2C0"
text_color = "#4A154B"

# daily pomodoro count
my_pomodoros = pd.read_csv('my_pomodoros.csv')
my_pomodoros['date'] = my_pomodoros['timestamp'].apply(lambda x: pd.to_datetime(x).strftime("%d/%m/%Y"))
today = dt.date.today().strftime("%d/%m/%Y")
daily_pomodoro_counts = my_pomodoros[my_pomodoros['date'] == today].shape[0]

# window layout
layout = [   
            [sg.Text(f"You've had {daily_pomodoro_counts} pomodoros today!", font = (font, font_size - 2), text_color = text_color, background_color = background_color)],
            [sg.Text('Task', size=(8, 1), font=(font, font_size), key="_TASK_", text_color = text_color, background_color = background_color),
                sg.Input('Coding', do_not_clear=True, key='_TASK_CONTENT_', size = (18, 1), font = (font, font_size - 2), text_color = text_color)],
            [sg.Text('Length', size=(8, 1), font=(font, font_size), key="_LENGTH_", text_color = text_color, background_color = background_color),
                sg.Input(default_mins, key='_LENGTH_MIN_',  size=(3, 1), font = (font, font_size - 2), text_color = text_color),
                sg.Text('minutes', size=(8, 1), font=(font, font_size), key="_TIME_UNIT_", text_color = text_color, background_color = background_color)],
            [sg.Text('00:00:00', size=(10, 1), font=(font, 28), text_color = text_color, background_color = background_color,
                        justification='center', key='_COUNT_DOWN_')],
            [sg.Button('Start', font=(font, font_size), focus=True, button_color = (text_color, button_color)),
                sg.Button('Reset', focus=False, font=(font, font_size), button_color = (text_color, button_color)),
                sg.Button('Hide', focus=False, font=(font, font_size), button_color = (text_color, button_color)),
                sg.Button('Exit', font=(font, font_size), button_color = (text_color, button_color))]]

# initiate the window
window = sg.Window('Pomodoro', enable_close_attempted_event=True, background_color = background_color).Layout(layout)

# minimized system tray
menu = ['', ['Show Window', 'Exit']]
tray = SystemTray(menu, single_click_events=False, window=window, tooltip='Pomodoro', icon='icon.png')

# initiate the toaster
toaster = ToastNotifier()

is_clock_running = False
is_window_showing = True
current_left_seconds = 0

# Event Loop
while True:
    event, values = window.Read(timeout = 1000)
    current_left_seconds -= 1 * (is_clock_running is True)

    # use the System Tray's event as if was from the window
    if event == tray.key:
        event = values[event]       # use the System Tray's event as if was from the window

    if event in ('Exit', sg.WIN_CLOSED):
        break

    if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
        window.un_hide()
        window.bring_to_front()

    elif event in ('Hide', sg.WIN_CLOSE_ATTEMPTED_EVENT):
        window.hide()
        tray.show_icon()    

    if current_left_seconds == 0 and is_clock_running: # Pomodoro over
        #task = str(values["_TASK_CONTENT_"])
        is_clock_running = False
        toaster.show_toast('Pomodoro', "Completed!", icon_path='icon.ico', duration=10, threaded=True)
        # write this pomodoro into the record

        fields=[dt.datetime.now(), values['_TASK_CONTENT_'], values['_LENGTH_MIN_']]
        with open('my_pomodoros.csv', 'a', newline = '') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            f.close()

    if event == "Start":
        is_clock_running = True
        clock_mins = int(values["_LENGTH_MIN_"])
        current_left_seconds = clock_mins * 60

    if event == "Reset":
        window['_LENGTH_MIN_'].Update(default_mins)
        current_left_seconds = default_mins * 60
        is_clock_running = False

    window['_COUNT_DOWN_'].Update(
        '{:02d}:{:02d}:{:02d}'.format(current_left_seconds // 3600, current_left_seconds // 60,
                                    current_left_seconds % 60))

tray.close()            # optional but without a close, the icon may "linger" until moused over
window.close()
             


