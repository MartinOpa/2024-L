import sys
import cv2
import numpy as np
import math
import struct
import matplotlib as plt
from datetime import datetime
import glob

def face_detect():
    cv2.namedWindow('frame', 0)
    video = cv2.VideoCapture('fusek_face_car_01.avi')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
    eye_cascade = cv2.CascadeClassifier('eye_cascade_fusek.xml')

    while True:
        ret, frame = video.read()
        paint_frame = frame.copy()
        if ret:
            faces, _, levelWeights = face_cascade.detectMultiScale3(
                frame,
                scaleFactor=1.2,
                minNeighbors=3,
                minSize=(150, 150),
                maxSize=(600, 600),
                outputRejectLevels=True
            )

            profiles, _, levelWeights = profile_cascade.detectMultiScale3(
                frame,
                scaleFactor=1.2,
                minNeighbors=3,
                minSize=(200, 200),
                maxSize=(600, 600),
                outputRejectLevels=True
            )

            eyes, _, levelWeights = eye_cascade.detectMultiScale3(
                frame,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(20, 20),
                maxSize=(400, 400),
                outputRejectLevels=True
            )

            for face in faces:
                cv2.rectangle(paint_frame, face, (0, 255, 0), 10)

            for profile in profiles:
                cv2.rectangle(paint_frame, profile, (255, 0, 0), 10)

            i = 0
            for eye in eyes:
                #if levelWeights[i] > 7.5:
                cv2.rectangle(paint_frame, eye, (0, 0, 255), 10)
                i += 1

            cv2.imshow('frame', paint_frame)
            if cv2.waitKey(2) == ord('q'):
                break

face_detect()