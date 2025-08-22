import cv2
import numpy as np
import time
import pyvjoy
import mss
import os
from PIL import Image, ImageFilter

joy = pyvjoy.VJoyDevice(1)
def create_folder(folder)
    full_path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(full_path):
        os.makedirs(full_path)



def calculate_orange_percentage(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_orange = np.array([10, 100, 20])
    upper_orange = np.array([25, 255, 255])
    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    orange_pixels = cv2.countNonZero(orange_mask)
    total_pixels = image.shape[0] * image.shape[1]
    orange_percentage = (orange_pixels / total_pixels) * 100
    return orange_percentage

def take_screenshot(folder, countt, name,count):
    with mss.mss() as sct:
        monitor_number = 1
        mon = sct.monitors[monitor_number]
        monitor = {"top": mon["top"], "left": mon["left"], "width": mon["width"], "height": mon["height"], "mon": monitor_number}

        sct_img = sct.grab(monitor)
        screenshot = np.array(sct_img)

    m = 400

    image = Image.fromarray(screenshot)
    screenshot = cv2.resize(screenshot, (1960, 1080))
    left = (sct_img.width - m) // 2 - 450
    top = (sct_img.height - m-500) // 1
    right = left + m + 900
    bottom = top + m -100
    cropped_image = image.crop((left, top, right, bottom))
    image_gray = cropped_image.convert('L')
    image_gray_blurred = image_gray.filter(ImageFilter.BLUR)
    resized_image = image_gray_blurred.resize((100, 33))

    height, width, _ = screenshot.shape
    cropped_screenshot = screenshot[int(height / 1.1):int(3 * height / 1.19), int(width / 2.26):int(3 * width / 5.365)]

    qheight, qwidth, _ = cropped_screenshot.shape
    cropped_screenshot = cropped_screenshot[:int(qheight / 2.81), :]
    left_half = cropped_screenshot[:, :int(qwidth / 2)]
    right_half = cropped_screenshot[:, int(qwidth / 2):]

    orange_percentage_left = calculate_orange_percentage(left_half)
    orange_percentage_right = calculate_orange_percentage(right_half)

    larger_half = max(orange_percentage_left, orange_percentage_right)
    if orange_percentage_left > orange_percentage_right:
        larger_half = -int(larger_half)

    larger_half = larger_half+count
    print(f"Orange Percentage: {larger_half:.2f}")


    steering_file_path = 'dataset/steering.txt'
    with open(steering_file_path, 'a') as file:
        file.write(f"{name}_{countt}.png {larger_half:.2f}\n")

    resized_image.save(f'dataset/img/{name}_{countt}.png')

def main(size):
    create_folder('dataset')
    create_folder('dataset/img')
    countt = 50000

    try:
        while countt < size:
            print(countt)
            count = 0
            while count <= 100 and countt < size:


                joy.set_button(5, 1)

                time.sleep(0.01)  # Sleep for 1 second
                take_screenshot('img', countt, "img_left",count/4)
                joy.set_button(5, 0)
                count += 1
                countt += 1
            count = 0
            while count <= 100and countt < size:

                joy.set_button(6, 1)

                time.sleep(0.01)  # Sleep for 0.5 seconds
                take_screenshot('img', countt, "img_front",0)
                joy.set_button(6, 0)
                count += 1
                countt += 1
            count = 0
            while count <= 100and countt < size:


                joy.set_button(7, 1)

                time.sleep(0.01)  # Sleep for 1 second
                take_screenshot('img', countt, "img_right",-count/4)
                joy.set_button(7, 0)
                count += 1
                countt += 1

            count = 0
            while count <= 100and countt < size:
                joy.set_button(6, 1)

                time.sleep(0.01)  # Sleep for 0.5 seconds
                take_screenshot('img', countt, "img_front",0)
                joy.set_button(6, 0)
                count += 1
                countt += 1



    except KeyboardInterrupt:
        pass

    cv2.destroyAllWindows()

if __name__ == "__main__":
    mainn=(int(input('Enter the desired size: ')))
    time.sleep(10)
    main(mainn)

