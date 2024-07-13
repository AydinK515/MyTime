'''
Author:  Aydin
Date written: 07/12/24
Assignment:   Final Project
Desc:  This code is a clock app with a timer alarm and other features

'''
#all imporst nessassary
import tkinter
from tkinter import ttk, messagebox
from datetime import datetime

#sets the inital window
tk = tkinter
window = tk.Tk()
window.title("MyTime")
#initates all variables
time_now = None
am_alarm = False
pm_alarm = False
alarm_window = None

#keeps the timing updating, it will update every 1 seccond 
def time_update():
    global time_now     #makes it so other functions can access the time
    time_now = datetime.now().strftime("%I:%M:%S") #uses datetime to make this
    am_pm = datetime.now().strftime("%p") #adds a variable for the am or pm
    #displays the information
    time_display.config(text=time_now) 
    am_or_pm.config(text=am_pm) 
    window.after(1000, time_update) #runs the function every 1 second

def set_alarm_window():
    #this makes the window for the alarm that allows the user to type in a time and am/pm
    global alarm_window
    global am_alarm
    global pm_alarm
    am_alarm = False
    pm_alarm = False
    #makes the window
    alarm_window = tk.Toplevel(window)
    alarm_window.title("Alarm")
    #tells instructions on how to tell the time
    alarm_label = ttk.Label(alarm_window, text="Enter alarm time like this: (HH:MM):")
    alarm_label.grid(row=0, column=0, padx=10, pady=10)
    #AM button
    am_alarm_button = tk.Button(alarm_window, text="AM", command=am_alarm)
    am_alarm_button.grid(row=0, column=3, padx=10, pady=10)
    #PM button
    pm_alarm_button = tk.Button(alarm_window, text="PM", command=pm_alarm)
    pm_alarm_button.grid(row=0, column=2, padx=10, pady=10)
    #lets you type in the time
    global alarm_entry
    alarm_entry = ttk.Entry(alarm_window)
    alarm_entry.grid(row=0, column=1, padx=10, pady=10)
    #sets the alarm and activates the next step of the alarm process which is the function set_alarm()
    set_button = ttk.Button(alarm_window, text="Set Alarm", command=set_alarm)
    set_button.grid(row=1, column=0, columnspan=2, pady=10)

def set_alarm():

    global time_now
    #makes the entry that the user entered and turns it into an actual usable number instead of a str
    alarm_time = alarm_entry.get().strip()
    alarm_time = datetime.strptime(alarm_time, "%I:%M").strftime("%I:%M")
    print(alarm_time)
    print(time_now)
    #will attempt to make the alarm making sure that the user entered an actual valid response with the value error check
    try:
        datetime.strptime(alarm_time, "%I:%M")
        alarm_window.destroy()
    except ValueError:
        messagebox.showerror("Error", "Please re-enter your time in the (HH:MM) format.")
        return
    #tells the user that the alarm is set
    messagebox.showinfo("Alarm Set", "Alarm set for " +str(alarm_time) + "")
    #activates the last part of the checking time process
    check_alarm(alarm_time)

#takes in the alarm time given by set_alarm
def check_alarm(alarm_time):
    global time_now
    #if the current time is greater than the alarm time then the alarm HAS to be over
    if time_now >= alarm_time:
        #says the alarm is ended
        messagebox.showinfo("Alarm Ended!", "Alarm set for " + str(alarm_time) + " has ended!")

        print("time up!")

        # alarm_end_window = tk.Toplevel(window) makes it a window instead of message box
        # alarm_end_window.title("Alarm up!")
        
        # alarm_end_label = tk.Label(alarm_end_window, font=("Helvetica", 24), text="The alarm for " + str(alarm_time) + " is up!")
        # alarm_end_label.grid(row=1, column=0, columnspan=2, pady=10)
    else: #if the time is not greater then it will check again in another second
        window.after(1000, lambda: check_alarm(alarm_time))

#just changes the variable to true if the button is pressed
def am_alarm():
    global am_alarm
    am_alarm = True
#changes variable to true when button is pressed
def pm_alarm():
    global pm_alarm
    pm_alarm = True

#the button to get the alarm menu activated
alarm_button = tk.Button(window, text="Alarm", command=set_alarm_window)
alarm_button.grid(row=10, column=1, padx=10, pady=10)
#just displays the time
time_display = tk.Label(window, text="", font=("Helvetica", 48))
time_display.grid(row=0, column=0, columnspan=3, pady=10)
#displays if the time is in AM or PM
am_or_pm = tk.Label(window, text="", font=("Helvetica", 16))
am_or_pm.grid(row=1, column=0, columnspan=3, pady=10)

#initates the time updating
time_update()
#runs the window
window.mainloop()
