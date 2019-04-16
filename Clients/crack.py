import numpy as np
import cv2

img = cv2.VideoCapture(0)

while(img.isOpened()):
    ret, frame = img.read()
    width = img.get(3)
    height = img.get(4)
    ratio = width/height
    dim = (int(500*ratio), 500)
    resized = cv2.resize(frame, dim)
    lower = np.array([60, 30, 25])
    upper = np.array([255, 80, 80])
    upper = np.array(upper, dtype = "uint8")
    lower = np.array(lower, dtype = "uint8")
    mask = cv2.inRange(resized, lower, upper)
#    output = cv2.bitwise_and(resized, resized, mask = mask)
    #gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(mask, (3, 3), 0)
    ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    #print(len(contours))
    #cv2.drawContours(resized, contours, -1, (0,255,0), 3)
    length = 0

    for c in contours:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour

        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(resized, (cX, cY), 5, (255, 0, 255), thickness=4)

        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            (x, y), (w, l), rot = rect
            if w < l :
                ar = 1.8 / w
                length = ar * l
            else:
                ar = 1.8 / l
                length = ar * w

        # then draw the contours and the name of the shape on the image
        cv2.drawContours(resized, [c], -1, (0,255,0), 2)
        # print(shape)
        cv2.putText(resized, str(length), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.drawContours(resized, [box], 0, (0,0,255), 2)

    cv2.imshow("resized", resized)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
