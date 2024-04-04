import cv2
from PIL import ImageGrab
from pynput.mouse import Button, Controller
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import time
import os
import threading

# https://duckhuntjs.com/
# 8200

threads = []
results = []

def make_screenshot():
    image_grab = ImageGrab.grab(xdisplay=os.getenv('DISPLAY'))
    image = np.array(image_grab)
    source = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('source.png', source)

def find_target(i, src): 
    max_val, x, y = 0, 0, 0     
    temp = cv2.cvtColor(cv2.imread(f'temp{i}.png'), cv2.COLOR_BGR2GRAY)

    src_h = src.shape[0]
    src_w = src.shape[1]
    temp_h = temp.shape[0]
    temp_w = temp.shape[1]

    result = cv2.matchTemplate(src, temp, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.97:
        top_left = max_loc
        bottom_right = (top_left[0] + temp_w, top_left[1] + temp_h)

        if i & 1 == 0:
            x = bottom_right[0] + int(temp_w/4)
            y = int((top_left[1] + bottom_right[1])/2)
        else:
            x = top_left[0] - int(temp_w/4)
            y = int((top_left[1] + bottom_right[1])/2)

        results.append((max_val, x, y))

try:
    mouse = Controller()
    while(True):
        make_screenshot()

        threads = []
        results = []
        src = cv2.cvtColor(cv2.imread('source.png'), cv2.COLOR_BGR2GRAY)
        for i in range(10):
            thread = threading.Thread(target=find_target, args=(i,src))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if len(results) > 0:
            results = sorted(results, key=lambda tup: tup[0], reverse=True)
            
            mouse.position = (results[0][1], results[0][2])
            mouse.press(Button.left)
            mouse.release(Button.left)
            time.sleep(0.75)
            
except KeyboardInterrupt:
    for thread in threads:
        thread.join()   