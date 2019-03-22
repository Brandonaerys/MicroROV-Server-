import cv2 as cv
import numpy as np
import datetime
import time

# video = cv.VideoCapture("http://192.168.68.2:8000/stream.mjpg")
video = cv.VideoCapture("C:/Users/underground/Desktop/Myles/cv/CV Line Following/Test_RLWBBC_2.mov")

while(True):
    ret, frame = video.read()

    key = cv.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('p'):
        name = str(datetime.datetime.now()).replace(":", "-")

        filename = "C:Users/underground/Desktop/SavedShots/" + name + ".jpeg"
        cv.imwrite(filename, frame)
        time.sleep(1)
    cv.imshow('frame',frame)

video.release()
cv.destroyAllWindows()
