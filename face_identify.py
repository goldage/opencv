#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#usage : ./vending_cv.py 0

import cv2
import sys
from PIL import Image

def CatchUsbVideo(window_name,camera_idx):
	cv2.namedWindow(window_name)

	cap = cv2.VideoCapture(camera_idx)

	classfier = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml")

	color = (0,255,0)

	num = 0

	while cap.isOpened():
		ok,frame = cap.read()
		if not ok:
			break

		grey = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

		faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.2, minNeighbors = 3, minSize = (32, 32))
		if len(faceRects) > 0:
			for faceRect in faceRects:
				x,y,w,h = faceRect
				cv2.rectangle(frame,(x - 10,y - 10),(x + w + 10,y + h + 10),color,2)

		cv2.imshow(window_name,frame)
		c = cv2.waitKey(10)
		if c & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__  == '__main__':
	if len(sys.argv) != 2 :
		print("Usage:%s camera_id face_num_max path_name\r\n" % (sys.argv[0]))
	else:
		 CatchUsbVideo("face filed:", int(sys.argv[1]))
