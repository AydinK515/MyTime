
'''
Author:  Aydin
Date written: 07/23/24
Assignment:   Final Project
Desc:  This code is a GUI aplication called MyTime it is a clock app with an alarm system, timer, and stopwatch.

'''
#all imports nessassary for gui and image processing and especially time since it is a clock app
from PIL import Image, ImageTk
import tkinter
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# sets the initial window
tk = tkinter
window = tk.Tk()
window.title("MyTime")

# initiates all variables
time_now = None  # current time in string format
am_alarm = False  # variable for AM alarm status
pm_alarm = False  # variable for PM alarm status
alarm_window = None  # reference to the alarm setting window
stopwatch_running = False  # flag to indicate if stopwatch is running
stopwatch_start_time = None  # start time of the stopwatch
timer_end_time = None  # endd time for the timer

# keeps the timing updating, it will update every 1 second
def time_update():
    """
    Updates the current time every second and displays it in the main window
    """
    global time_now  # makes it so other functions can access the time
    time_now = datetime.now().strftime("%I:%M:%S")  # uses datetime to make this
    am_pm = datetime.now().strftime("%p")  # adds a variable for the am or pm
    # displays the information
    time_display.config(text=time_now)
    am_or_pm.config(text=am_pm)
    window.after(1000, time_update)  # runs the function every 1 second

# function to open the alarm window
def set_alarm_window():
    """
    Opens a new window where the user can set the alarm time with all the buttons there
    """
    global alarm_window
    alarm_window = tk.Toplevel(window)
    alarm_window.title("Alarm")
    # tells instructions on how to tell the time
    alarm_label = ttk.Label(alarm_window, text="Enter alarm time like this: (HH:MM):")
    alarm_label.grid(row=0, column=0, padx=10, pady=10)
    # lets you type in the time
    global alarm_entry
    alarm_entry = ttk.Entry(alarm_window)
    alarm_entry.grid(row=0, column=1, padx=10, pady=10)
    # sets the alarm and activates the next step of the alarm process which is the function set_alarm()
    set_button = ttk.Button(alarm_window, text="Set Alarm", command=set_alarm)
    set_button.grid(row=1, column=0, columnspan=2, pady=10)
    # Add an exit button to close the alarm window
    exit_button = ttk.Button(alarm_window, text="Close", command=alarm_window.destroy)
    exit_button.grid(row=2, column=0, columnspan=2, pady=10)

# function to set the alarm
def set_alarm():
    """
    Sets the alarm time based on user input and starts checking for the alarm
    """
    global time_now
    # makes the entry that the user entered and turns it into an actual usable number instead of a str
    alarm_time = alarm_entry.get().strip()
    try:
        alarm_time = datetime.strptime(alarm_time, "%I:%M").strftime("%I:%M")
        datetime.strptime(alarm_time, "%I:%M")  # Validates the time format
        alarm_window.destroy()  # Closes the alarm setting window
        # tells the user that the alarm is set
        messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
        # activates the last part of the checking time process
        check_alarm(alarm_time)
    except ValueError:
        messagebox.showerror("Error", "Please re-enter your time in the (HH:MM) format.")

# function to check if the alarm time has passed
def check_alarm(alarm_time):
    """
    Continuously checks if the current time matches the set alarm time
    """
    global time_now
    # if the current time is greater than the alarm time then the alarm HAS to be over
    if time_now >= alarm_time:
        # says the alarm is ended
        messagebox.showinfo("Alarm Ended!", f"Alarm set for {alarm_time} has ended!")
    else:  # if the time is not greater then it will check again in another second
        window.after(1000, lambda: check_alarm(alarm_time))

# function to toggle the stopwatch
def toggle_stopwatch():
    """
    Starts or stops the stopwatch depending on its current state. so if its started it will say stop stopwatch and if its stopped it will say start
    """
    global stopwatch_running
    global stopwatch_start_time
    if stopwatch_running:
        stopwatch_running = False
        stopwatch_button.config(text="Start Stopwatch")  # updates button text to reflect current state
    else:
        stopwatch_running = True
        stopwatch_start_time = datetime.now()  # records the start time
        stopwatch_button.config(text="Stop Stopwatch")  # updates button text to reflect current state
        update_stopwatch()

# function to update the stopwatch display
def update_stopwatch():
    """
    Updates the stopwatch display every second while the stopwatch is running
    """
    if stopwatch_running:
        elapsed_time = datetime.now() - stopwatch_start_time  # calculates elapsed time
        stopwatch_display.config(text=str(elapsed_time).split('.')[0])  # updates display with formatted elapsed time
        window.after(1000, update_stopwatch)  # Runs the function every 1 second

# function to set the timer
def set_timer():
    """
    Sets a countdown timer based on whatever the user providies
    """
    global timer_end_time
    timer_text = timer_entry.get().strip()
    if timer_text.isdigit():  # checks if the input is a valid number
        timer_minutes = int(timer_text)
        timer_end_time = datetime.now() + timedelta(minutes=timer_minutes)  # sets the end time for the timer
        messagebox.showinfo("Timer Set", f"Timer set for {timer_minutes} minutes.")
        check_timer()
    else:
        messagebox.showerror("Input Error", "Please enter a valid number of minutes.")

# function to check if the timer has ended
def check_timer():
    """
    Continuously checks if the timer has reached its end time
    """
    global timer_end_time
    if datetime.now() >= timer_end_time:
        messagebox.showinfo("Timer Ended!", "Your timer has ended!")  # alerts when timer ends
    else:
        window.after(1000, check_timer)  # checks again in another second

# function to exit the application
def exit_application():
    """
    Closes the application
    """
    window.quit()  # closes the main application window

# adding image and alternate text
def load_image(image_path, size=(100, 100)):
    """
    This is what i do to load the images so that they are all like the same like 100x100
    """
    try:
        image = Image.open(image_path)  # opens the image file
        image = image.resize(size)  # reesizes the image
        return ImageTk.PhotoImage(image)  # returns the image as a PhotoImage object
    except Exception as e:
        print(f"Error loading image: {e}")  # prints an error message if image loading fails
        return None

# main window layout
image1 = load_image("Pictures/clockpic.jpg")  # loads the clock image
image2 = load_image("Pictures/alarmpicutre.jpg")  # loads the alarm image

# display image1 above the clock
image_label1 = tk.Label(window, image=image1, text="Clock!", compound="top")
image_label1.grid(row=0, column=0, columnspan=3, pady=10)

# display the clock time
time_display = tk.Label(window, text="", font=("Helvetica", 48))
time_display.grid(row=1, column=0, columnspan=3, pady=10)

# displays if the time is in AM or PM
am_or_pm = tk.Label(window, text="", font=("Helvetica", 16))
am_or_pm.grid(row=2, column=0, columnspan=3, pady=10)

image_label2 = tk.Label(window, image=image2, text="Alarm!", compound="top")
image_label2.grid(row=3, column=0, columnspan=3, pady=10)

# stopwatch display
stopwatch_display = tk.Label(window, text="00:00:00", font=("Helvetica", 24))
stopwatch_display.grid(row=4, column=0, columnspan=3, pady=10)

# the button to get the alarm menu activated
alarm_button = tk.Button(window, text="Alarm", command=set_alarm_window)
alarm_button.grid(row=5, column=0, padx=10, pady=10)

# stopwatch button
stopwatch_button = tk.Button(window, text="Start Stopwatch", command=toggle_stopwatch)
stopwatch_button.grid(row=6, column=0, padx=10, pady=10)

# timer button
timer_button = tk.Button(window, text="Set Timer", command=set_timer)
timer_button.grid(row=7, column=0, padx=10, pady=10)

# exit button
exit_button = tk.Button(window, text="Exit", command=exit_application)
exit_button.grid(row=8, column=0, padx=10, pady=10)

# timer entry
timer_entry = ttk.Entry(window)
timer_entry.grid(row=7, column=1, padx=10, pady=10)
timer_entry.insert(0, "Minutes")  # Placeholder text for timer entry box

# initiates the time updating
time_update()

# runs the window
window.mainloop()
