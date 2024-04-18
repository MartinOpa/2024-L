import sys
import cv2
import numpy as np
import math
import struct
import matplotlib as plt
from datetime import datetime
import glob

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect

def four_point_transform(image, one_c):
    #https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    
    pts = [((float(one_c[0])), float(one_c[1])),
            ((float(one_c[2])), float(one_c[3])),
            ((float(one_c[4])), float(one_c[5])),
            ((float(one_c[6])), float(one_c[7]))]
    
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(np.array(pts))
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
	    [0, 0],
	    [maxWidth - 1, 0],
	    [maxWidth - 1, maxHeight - 1],
	    [0, maxHeight - 1]], dtype = "float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped

#############################################################################
#############################################################################
#############################################################################

pkm_file = open('parking_map_python.txt', 'r')
pkm_lines = pkm_file.readlines()
pkm_coordinates = []

accuracies = []
f_scores = []

for line in pkm_lines:
    st_line = line.strip()
    sp_line = list(st_line.split(" "))
    pkm_coordinates.append(sp_line)
    
test_images = [img for img in glob.glob("test_images_zao/*.jpg")]
test_images.sort()

cv2.namedWindow('image', 0) 

size_edges = (360, 360)
size = (60, 60)
template_blank = cv2.cvtColor(cv2.resize(cv2.imread('template.png'), size_edges), cv2.COLOR_BGR2GRAY)
# cv2.cvtColor( , cv2.COLOR_BGR2GRAY)
template_empty_dark = cv2.cvtColor(cv2.resize(cv2.imread('template_empty_dark.png'), size), cv2.COLOR_BGR2GRAY)
template_empty_snow = cv2.cvtColor(cv2.resize(cv2.imread('template_empty_snow.png'), size), cv2.COLOR_BGR2GRAY)
for img_name in test_images:
    image = cv2.imread(img_name, 1)
    results = []

    for coord in pkm_coordinates:
        color = (0, 255, 0)
        occupied = False
        parking_spot = image
        
        parking_spot = cv2.resize(four_point_transform(image, coord), size)
        parking_spot = cv2.convertScaleAbs(parking_spot, alpha=0.97, beta=2)
        parking_spot = cv2.cvtColor(parking_spot, cv2.COLOR_BGR2GRAY)

        parking_spot_canny = cv2.Canny(parking_spot, 95, 400)

        contours, _ = cv2.findContours(parking_spot_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        edge_count = cv2.countNonZero(parking_spot_canny)

        # result_car_front = cv2.matchTemplate(parking_spot, template_empty_dark, cv2.TM_CCORR_NORMED)
        # min_val_car_front, max_val_car_front, min_loc_car_front, max_loc_car_front = cv2.minMaxLoc(result_car_front)

        # result_car_rear = cv2.matchTemplate(parking_spot, template_empty_snow, cv2.TM_CCORR_NORMED)
        # min_val_car_rear, max_val_car_rear, min_loc_car_rear, max_loc_car_rear = cv2.minMaxLoc(result_car_rear)

        if (edge_count > 170 or len(contours) > 5):
            color = (0, 0, 255)
            occupied = True

        cv2.line(image, (int(coord[0]), int(coord[1])), (int(coord[2]), int(coord[3])), color, 2)
        cv2.line(image, (int(coord[2]), int(coord[3])), (int(coord[4]), int(coord[5])), color, 2)
        cv2.line(image, (int(coord[4]), int(coord[5])), (int(coord[6]), int(coord[7])), color, 2)
        cv2.line(image, (int(coord[6]), int(coord[7])), (int(coord[0]), int(coord[1])), color, 2)
    
        if occupied:
            results.append('1')
        else:
            results.append('0')

    with open(img_name[:-3] + 'txt', 'r') as file:
        values = [line.strip() for line in file.readlines()]

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for i in range(len(values)):
        if values[i] == results[i]:
            if values[i] == '1':
                true_positive += 1
            else:
                true_negative += 1
        else:
            if values[i] == '1':
                false_positive += 1
            else:
                false_negative += 1

    accuracy = (true_positive + true_negative) / (len(values))
    accuracies.append(accuracy)

    if (true_positive + false_positive) > 0:
        try:
            precision = true_positive / (true_positive + false_positive)
            recall = true_positive / (true_positive + false_negative)
            if (precision + recall) == 0:
                f_score = 0
                f_scores.append(f_score)
            else:
                f_score = (2 * precision * recall) / (precision + recall)
                f_scores.append(f_score)
        except:
            f_score = 0
            f_scores.append(f_score)
    else:
        f_score = 1.0
        f_scores.append(f_score)
        
    print(f'Accuracy: {accuracy}, F-Score: {f_score}')

    # cv2.imshow('image', image)
    # cv2.waitKey(0)

print(f'Accuracy total: {sum(accuracies)/len(accuracies)} F-Score total: {sum(f_scores)/len(f_scores)}')
