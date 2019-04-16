import numpy as np
import cv2
from shapedetector import ShapeDetector
import datetime

img = cv2.VideoCapture("http://192.168.69.2:8000/stream.mjpg")

recording = False

def nothing(x):
    pass

image = np.zeros((0, 0, 0), np.uint8)
cv2.namedWindow('tracker')

cv2.createTrackbar('y','tracker', 435, 500, nothing)
cv2.createTrackbar('topy', 'tracker', 145, 400, nothing)
cv2.createTrackbar('topx', 'tracker', 112, 400, nothing)
cv2.createTrackbar('crop_height', 'tracker', 400, 800, nothing)
cv2.createTrackbar('crop_width', 'tracker', 400, 800, nothing)
cv2.createTrackbar('MaxS', 'tracker', 55, 255, nothing)
cv2.createTrackbar('MinV', 'tracker', 95, 255, nothing)

while(img.isOpened()):
    ret, frame = img.read()
    width = int(img.get(3))
    height = int(img.get(4))
    if recording:
      out.write(frame)
      cv2.circle(frame, (40, 40), 15, (0, 0, 255), -1)

    key = cv2.waitKey(1)
    cv2.imshow('frame', frame)

    topx = cv2.getTrackbarPos('topx', 'tracker')
    topy = cv2.getTrackbarPos('topy', 'tracker')
    crop_width = cv2.getTrackbarPos('crop_width', 'tracker')
    crop_height = cv2.getTrackbarPos('crop_height', 'tracker')
    maxs = cv2.getTrackbarPos('MaxS', 'tracker')
    minv = cv2.getTrackbarPos('MinV', 'tracker')

    y = cv2.getTrackbarPos('y', 'tracker')
    m = 2 * height / width
    xl  = int(y/m)
    xr = int(-(y-2*height)/m)

    pts1 = np.float32([[0,height], [width, height], [xr, y], [xl, y]])
    ptsmap = np.float32([[0,height], [width, height], [width, 0], [0, 0]])

    M = cv2.getPerspectiveTransform(pts1, ptsmap)
    frame_transformed = cv2.warpPerspective(frame, M, (width, height))
    cv2.rectangle(frame_transformed, (topx, topy), (topx+crop_width, topy+crop_height), (0, 0, 255), 2)

    cv2.imshow('Transformed', frame_transformed)
    bgr_cropped = frame_transformed[topy:topy+crop_height, topx:topx+crop_width]
    hsv_cropped = cv2.cvtColor(bgr_cropped, cv2.COLOR_BGR2HSV)

    upper = np.array([180, maxs, 255])
    lower = np.array([0, 0, minv])

    upper = np.array(upper, dtype = "uint8")
    lower = np.array(lower, dtype = "uint8")

    blur = cv2.GaussianBlur(hsv_cropped,(5,5),0)
    mask = cv2.inRange(blur, lower, upper)
    # cv2.imshow('mask', mask)
    kernel_crop = np.ones((5, 5), np.uint8)
    closing_crop = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_crop)

    closing_blur = cv2.GaussianBlur(closing_crop, (5,5), 0)
    cv2.imshow('c blur', closing_blur)

    cv2.imshow('closing', closing_crop)

    '''
    #output = cv2.bitwise_and(frame_transformed, frame_transformed, mask = mask)
    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    im2, contours,heirarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    ret_crop, thresh_crop = cv2.threshold(blurred_crop, 80, 255, cv2.THRESH_BINARY_INV)
    kernel_crop = np.ones((5, 5), np.uint8)
    closing_crop = cv2.morphologyEx(thresh_crop, cv2.MORPH_CLOSE, kernel_crop)
    '''

    if key == 32:
        img_crop, contours_crop, hierarchy_crop = cv2.findContours(closing_crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sd = ShapeDetector()
    # loop over the contours
        shapeDict = {
            "triangle" : 0,
            "circle" : 0,
            "line" : 0,
            "square" : 0
            }
        draw_frame = bgr_cropped.copy()
        for c in contours_crop:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
            M = cv2.moments(c)
            if M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(draw_frame, (cX, cY), 5, (255, 0, 255), thickness=4)
            shape = sd.detect(c)

            rect_crop = cv2.minAreaRect(c)
            box_crop = cv2.boxPoints(rect_crop)
            box_crop = np.int0(box_crop)
            if shape == "triangle":
                shapeDict["triangle"] = shapeDict["triangle"] + 1
            elif shape == "square":
                shapeDict["square"] = shapeDict["square"] + 1
            elif shape == "circle":
                shapeDict["circle"] = shapeDict["circle"] + 1
            else:
                shapeDict["line"] = shapeDict["line"] + 1

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
            cv2.drawContours(draw_frame, [c], -1, (0,255,0), 1)
        # print(shape)
            cv2.putText(draw_frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,\
                0.5, (255, 255, 0), 2)

            # cv2.drawContours(draw_frame, [box_crop], 0, (0,0,255), 2)

        print(shapeDict)
        blank = np.zeros((512, 512, 3), np.uint8)

        cv2.circle(blank, (80, 80), 30, (0, 0, 255), -1)
        cv2.rectangle(blank, (50, 140), (110, 200), (0, 0, 255), -1)
        cv2.line(blank, (80, 230), (80, 290), (0, 0, 255), 5)
        pts = np.array([[80, 320], [50, 380], [110, 380]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(blank, [pts], (0, 0, 255))

        circleQty = shapeDict["circle"]
        squareQty = shapeDict["square"]
        triQty = shapeDict["triangle"]
        lineQty = shapeDict["line"]
        cv2.putText(blank, str(circleQty), (160, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(blank, str(squareQty), (160, 185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(blank, str(triQty), (160, 365), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(blank, str(lineQty), (160, 275), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('blank',blank)
        cv2.imshow('Draw Frame', draw_frame)
    elif key & 0xFF == ord('r'):
    # Write the frame into the file 'output.avi'
      if not recording:
          recording = True
          current = datetime.datetime.now()
          name = "C:\\Users\\underground\\Desktop\\WaterTrial\\"  + str(current).replace(':', '_') + ".avi"
          out = cv2.VideoWriter(name,cv2.VideoWriter_fourcc('M','J','P','G'), 20, (width, height))
          print(name)

    elif key & 0xFF == ord('s'):
      if recording:
          recording = False
          out.release()

    elif key & 0xFF == ord('q'):
      if recording:
          recording = False
          out.release()
      break

cv2.destroyAllWindows()
