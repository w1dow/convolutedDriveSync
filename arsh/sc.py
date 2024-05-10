import mss
import cv2
import numpy as np
from PIL import Image,ImageFilter,ImageGrab

def preprocess_screen(screen):
    m = 400
    screenshot = cv2.resize(screen, (1960, 1080))

    left = (1960 - m) // 2 - 450
    top = (1080- m - 200) // 1
    right = left + m + 900
    bottom = top + m - 180

    # Crop the screen
    cropped_screen = screenshot[top:bottom, left:right]

    return cropped_screen

with mss.mss() as sct:
    # Define the monitor to capture
    monitor = sct.monitors[1]
    mon = sct.monitors[1]
    monitor = {"top": mon["top"], "left": mon["left"], "width": mon["width"], "height": mon["height"],
               "mon": 1}

    while True:
        # Capture the screen
        screen = np.array(ImageGrab.grab((0,0,2560,1600)))

        # Preprocess the screen
        processed_screen = preprocess_screen(screen)

        # Convert processed_screen to BGR format (if it's not already)
        processed_screen = cv2.cvtColor(processed_screen, cv2.COLOR_RGB2BGR)

        # Display the processed screen
        cv2.imshow("out", processed_screen)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
