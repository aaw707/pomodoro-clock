###
# The PySimpleGUI version
# with countdown and "minimized to taskbar" function
# need to fix countdown
# doesn't count the daily pomodoros
# need to add quality check

import PySimpleGUI as sg
from psgtray import SystemTray
from PIL import Image
import datetime as dt
import time

menu = ['', ['Show Window', 'Exit']]

layout = [[sg.Text('Time for a fresh pomodoro!')],
            [sg.T('Aim to focus for...'), sg.Input(25, key='pomodoro_time', s = (3, 1)), sg.T('minutes'), sg.Button('Start')],
            [sg.T('Break time set for...'), sg.Input(5, key='break_time', s = (3, 1)), sg.T('minutes')],
            [sg.T('Time remains:'), sg.T(key = 'remaining_time')],
            #[sg.Multiline(size=(60,10), reroute_stdout=False, reroute_cprint=True, write_only=True, key='-OUT-')],
            [sg.B('Hide Window'), sg.B('Export Report'), sg.Button('Exit')]]

window = sg.Window('Pomodoro Clock', layout, finalize=True, enable_close_attempted_event=True)


tray = SystemTray(menu, single_click_events=False, window=window, tooltip='Pomodoro Clock', icon='icon.png')


t_start = dt.datetime.now()
t_complete = dt.datetime.now()

while True:
    event, values = window.read(timeout=10)

    if event == 'Start':
        pomodoro_time = int(values['pomodoro_time'])
        t_start = dt.datetime.now()
        t_delta = dt.timedelta(0, pomodoro_time * 60)    
        t_complete = t_start + t_delta

    t_now = dt.datetime.now()
    t_remain = (t_complete - t_now).total_seconds()
    
    if t_remain > 0:
        window['remaining_time'].update(f'{int(t_remain // 60)}:{int(t_remain % 60)}')
    elif t_remain == 0:


        

    # IMPORTANT step. It's not required, but convenient. Set event to value from tray
    # if it's a tray event, change the event variable to be whatever the tray sent
    if event == tray.key:
        event = values[event]       # use the System Tray's event as if was from the window

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
        window.un_hide()
        window.bring_to_front()

    elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
        window.hide()
        tray.show_icon()        



tray.close()            # optional but without a close, the icon may "linger" until moused over
window.close()
