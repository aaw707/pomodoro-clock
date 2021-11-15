###
# The tkinter version
# with countdown and ending notification
# doesn't have "minimized to taskbar" function
# doesn't count the daily pomodoros
# quality check not completed

from tkinter import *
import time
import datetime as dt
import win10toast
from PIL import Image, ImageTk

root = Tk()
root.title("Pomodoro Clock")

# counter
daily_pomodoros = 0

# what's on the ui
greetings = Label(root, text = "Time for a fresh pomodoro!")

time_prompt = Label(root, text = "Aim to focus for...")
time_entry = Entry(root, width = 5)
time_entry.insert(0, 25)

break_prompt = Label(root, text = "Break time set for...")
break_entry = Entry(root, width = 5)
break_entry.insert(0, 5)

remaining_text = Label(root, text = "Time remains:")
remaining_text.grid(row = 4, column = 0)
remaining_min = Label(root)
remaining_min.grid(row = 4, column = 1)

toaster = win10toast.ToastNotifier()


def my_timer():
    time_length = int(time_entry.get()) * 60 # by sec
    t_start = dt.datetime.now()
    t_delta = dt.timedelta(0, time_length)    
    t_complete = t_start + t_delta

    t_break = int(break_entry.get()) * 60

    countdown(int(time_length / 60)) # by min

def countdown(minutes):
    remaining_min['text'] = minutes
    if minutes > 0:
        root.after(1000, countdown, minutes - 1) # countdown every minute
    elif minutes == 0:
        toaster.show_toast('Pomodoro Clock', 'Completed!', duration = 5, threaded=True)
        quality_check()

def quality_check():
    quality_message = Label(root, text = "How was this pomodoro?")
    quality_good = Button(root, text = "Great!")
    quality_hmm = Button(root, text = "Hmm..")

    quality_message.grid(row = 5, column = 0)
    quality_good.grid(row = 5, column = 1)
    quality_hmm.grid(row = 5, column = 2)

# button: start
start_button = Button(root, text = "Start", command = my_timer)

# text: has completed x pomodoros today
summary = Label(root, text = f"You have completed {daily_pomodoros} pomodoros today!")

# set ui positions
greetings.grid(row = 0, column = 0)
start_button.grid(row = 0, column = 1)
time_prompt.grid(row = 1, column = 0)
time_entry.grid(row = 1, column = 1)
break_prompt.grid(row = 2, column = 0)
break_entry.grid(row = 2, column = 1)
summary.grid(row = 7)

root.mainloop()

#label.place(x=35, y=15)