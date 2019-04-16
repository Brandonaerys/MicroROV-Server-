import cv2
import numpy as np

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.03 * peri, True)
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		box = np.int0(box)
		(x, y), (w, h), rot = rect
		if w < h :
			ar = w / h
		else:
			ar = h / w
		area = w*h
        # if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3 and ar > 0.5:
			shape = "triangle"

		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if 0.6 < ar < 1.5 else "line"
        # otherwise, we assume the shape is a circle
		else:
			shape = "circle" if area > 12 else "null"
		return shape
'''
    		rect = cv2.minAreaRect(c)
    		box = cv2.boxPoints(rect)
    		box = np.int0(box)
			if len(box) == 4:
				(x, y, w, h) = cv2.boundingRect(box)
				ar = w / float(h)
				shape = "circle" if ar >= 0.95 and ar <= 1.05 else "line"
			#shape = "circle"
'''
        # return the name of the shape
