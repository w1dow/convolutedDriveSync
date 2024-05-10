import PIL.Image

# Add the missing CUBIC attribute to PIL's Image module
if not hasattr(PIL.Image, 'CUBIC'):
    PIL.Image.CUBIC = 3  # Use the value 3 as defined by BICUBIC in PIL's source code

import cv2
import mss
import numpy as np
import pyvjoy
from PIL import Image
from PIL import ImageGrab
import random
from pynput import keyboard
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.widgets import Meter
from PIL import Image, ImageTk
import threading
import time

# Initialize the vJoy device
# joy = pyvjoy.VJoyDevice(1)

# Function to simulate steering input
def simulate_steering(angle):
    # Convert the angle to a value between -1 and 1
    normalized_angle = max(-1, min(1, angle / 90.0))
    # Convert the value to the range of vJoy axis values (0 to 32767)
    axis_value = int((normalized_angle + 1) * 16383.5)
    # Set the steering axis value
    # joy.set_axis(pyvjoy.HID_USAGE_X, axis_value)

# Load the pre-trained model

# Function to preprocess the screen
def preprocess_screen(screen):
    with mss.mss() as sct:
        monitor_number = 1
        mon = sct.monitors[monitor_number]
        monitor = {"top": mon["top"], "left": mon["left"], "width": mon["width"], "height": mon["height"], "mon": monitor_number}

        sct_img = sct.grab(monitor)
        screenshot = np.array(sct_img)
    screenshot = cv2.resize(screenshot, (1960, 1080))
    m = 400
    left = (1960 - m) // 2 - 450
    top = (1080 - m - 100) // 1
    right = left + m + 900
    bottom = top + m - 310
    screenshot = np.array(screenshot)
    screenshot = screenshot.squeeze()  # Remove singleton dimensions
    image = Image.fromarray(screenshot)

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    # Convert RGB to grayscale
    gray_screen = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2GRAY)

    # Expand dimensions to simulate 3 channels (grayscale to RGB)
    expanded_screen = np.expand_dims(gray_screen, axis=-1)

    # Resize the image to match the input size of the model (66x200)
    resized_screen = cv2.resize(expanded_screen, (100, 33))

    # Normalize pixel values to [0, 1]
    normalized_screen = resized_screen / 255.0

    # Add batch dimension
    processed_screen = np.expand_dims(normalized_screen, axis=0)

    return processed_screen

# Function to predict steering angle
def predict_steering_angle(screen):
    processed_screen = preprocess_screen(screen)
    processed_screen = np.expand_dims(processed_screen, axis=-1)

    steering_angle = random.randint(-40, 40)

    return steering_angle

# Initialize mouse_movement_enabled
mouse_movement_enabled = True

# Callback function for key press event
def on_key_press(key):
    global mouse_movement_enabled
    try:
        if key.char == 'l':
            mouse_movement_enabled = not mouse_movement_enabled
    except AttributeError:
        pass

# Create a listener for key press events
listener = keyboard.Listener(on_press=on_key_press)
listener.start()

# UI
def UI():
    # Window
    window = ttk.Window(themename='darkly')
    window.geometry('1900x370')
    window.title('Convulated-drive_sync')
    window.overrideredirect(True)
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = screen_width
    window_height = screen_height // 2

    window_x = 0
    window_y = screen_height - window_height

    # Set window geometry
    window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

    # Make the window non-resizable
    window.resizable(False, False)


    # Button framing
    btn_frm = ttk.Frame(window)
    btn_frm.place(relx=0, rely=0, relheight=1, relwidth=0.25)

    def change_button_styles(event):
        global mouse_movement_enabled
        if event.char.lower() == 'l':
            # Change style of btn1
            if btn1['style'] == "success-outline.TButton":
                btn1.configure(style="success.TButton")
            else:
                btn1.configure(style="success-outline.TButton")

            # Change style of btn2
            if btn2['style'] == "danger.TButton":
                btn2.configure(style="danger-outline.TButton")
            else:
                btn2.configure(style="danger.TButton")

            # Toggle mouse_movement_enabled
            mouse_movement_enabled = not mouse_movement_enabled

    # Buttons
    style = ttk.Style()
    style.configure('success.TButton', foreground='white')
    style.configure('success-outline.TButton', foreground='white')
    style.configure('danger.TButton', foreground='white')
    style.configure('danger-outline.TButton', foreground='white')

    btn1 = ttk.Button(btn_frm, text='AUTO-PILOT Enabled', style='success-outline.TButton')
    btn2 = ttk.Button(btn_frm, text='AUTO-PILOT Disabled', style='danger.TButton')
    btn1.pack(expand=True, fill='both', side='top')
    btn2.pack(expand=True, fill='both', side='bottom')

    # Bind the '<Key>' event to the root window
    window.bind('<KeyPress-l>', change_button_styles)

    # Steering angle framing
    steer_frm = ttk.Frame(window)
    steer_frm.place(relx=0.25, rely=0, relheight=1, relwidth=0.5)




    # Speedometer framing
    speed_frm = ttk.Frame(window)
    speed_frm.place(relx=0.75, rely=0, relheight=1, relwidth=0.25)

    speed = ttk.Meter(speed_frm,
                      amounttotal=150,
                      amountused=0,
                      metertype='semi',
                      subtext='Mi/Hr',
                      bootstyle='vapour',
                      subtextstyle='danger')

    speed_frm.columnconfigure((0,1), weight=1, uniform='a')
    speed_frm.rowconfigure((0,1), weight=1, uniform='b')

    speed.grid(row=0, rowspan=2, column=0, columnspan=2, sticky='ew')


    # Run
    window.mainloop()

# Function to run UI
def run_UI():
    UI()

# Function to run the main loop for prediction and display
def run_main_loop():
    while True:
        # Capture the screen using PIL
        screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))  # Adjust the bounding box as needed

        # Predict the steering angle and confidence
        predicted_angle = predict_steering_angle(screen)

        # Print the predicted angle and confidence
        print(f"Predicted Angle: {predicted_angle}")

        processed_screen = preprocess_screen(screen)

        if mouse_movement_enabled:
            # Control the mouse based on the predicted angle
            simulate_steering(predicted_angle)

        cv2.imshow("Autonomous Driving Demo", cv2.resize(processed_screen[0], (200, 66)))

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the OpenCV window
    cv2.destroyAllWindows()

# Start threads for UI and main loop
ui_thread = threading.Thread(target=run_UI)
main_loop_thread = threading.Thread(target=run_main_loop)

ui_thread.start()
main_loop_thread.start()
