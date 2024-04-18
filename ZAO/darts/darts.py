import cv2
from PIL import ImageGrab
from pynput.mouse import Button, Controller
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import time
import os

# https://cdn-factory.marketjs.com/en/dart-master/index.html

def make_screenshot():
    image_grab = ImageGrab.grab(xdisplay=os.getenv('DISPLAY'))
    image = np.array(image_grab)
    source = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('source.png', source)

def find_target():
    src = cv2.cvtColor(cv2.imread('source.png'), cv2.COLOR_BGR2GRAY)
    temp = cv2.cvtColor(cv2.imread('temp_a.png'), cv2.COLOR_BGR2GRAY)

    src_h = src.shape[0]
    src_w = src.shape[1]
    temp_h = temp.shape[0]
    temp_w = temp.shape[1]

    result = cv2.matchTemplate(src, temp, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

    x = int((top_left[0] + bottom_right[0])/2)
    y = int((top_left[1] + bottom_right[1])/2)

    return max_val, x, y

mouse = Controller()
while(True):
    make_screenshot()
    acc, x, y = find_target()

    if acc > 0.8:
        mouse.position = (x, y)
        mouse.press(Button.left)
        mouse.release(Button.left)
        time.sleep(0.5)