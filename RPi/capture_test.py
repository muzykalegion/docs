# Takes screenshot from camera on button push

import os
import time
import RPi.GPIO as GPIO
import cv2

cap = cv2.VideoCapture('/dev/video0', cv2.CAP_FFMPEG)
if not cap.isOpened():
    cap.open('/dev/video0')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN)

try:
    count = 0
    while True:
        if GPIO.input(6) == 1:
            count += 1
            ret, frame = cap.read()
            if not ret:
                print('failed to grab frame')
                break
            cv2.imwrite('img%s.jpg' % count, frame)
            print('Got image %s' % count)

finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
