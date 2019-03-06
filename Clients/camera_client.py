import cv2 as cv

video = cv.VideoCapture("http://192.168.0.128:8000/stream.mjpg")


while(True):
    ret, frame = video.read()

    key = cv.waitKey(1)

    cv.imshow('frame',frame)

video.release()
cv.destroyAllWindows()
