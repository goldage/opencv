#!/usr/bin/env python3
#-*- coding : utf-8 -*-

import cv2
import time
import datetime
import os

def mkdir(path):
	folder = os.path.exists(path)

	if not folder :
		os.makedirs(path) 
		print ("--- new folder ... ---")
		print ("--- ok ---")

	else :
		print ("--- there is this folder ---")

def nothing(x):
	pass

objectFile = "./motionObject"
mkdir(objectFile)
print ("save folder : ./motionObject")

# Select which camera.
camera = cv2.VideoCapture(0)
time.sleep(2)
background = None

cv2.namedWindow("fps")
cv2.createTrackbar('level', 'fps', 21, 255, nothing)
shot_idx = 0

while True:
	text = "No Target"
	flat = 0
	
	kerne = cv2.getTrackbarPos('level', 'fps')
	if kerne % 2 == 0:
		kerne = kerne + 1
	
	(grabbed, frame) = camera.read()
	
	# To grayscale.
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	# Use Gaussian filter.
	gray = cv2.GaussianBlur(gray, (kerne, kerne), 0)
	
	if background is None:
		background = gray
		continue

	frameDelta = cv2.absdiff(background, gray)
	thresh = cv2.threshold(frameDelta,25,255,cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh,None,iterations=2)
	# Contouring.
	cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

	for c in cnts:
		# Ignore the smaller rectangular region.
		if cv2.contourArea(c) < 100: 
			continue
		flat = 1
		# Calculate the bounding box outline.
		(x, y , w, h) = cv2.boundingRect(c)
		# Circle the box in the current frame.
		cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0),2)
		print ("Find Target")
	
	cv2.imshow("fps",frame)

	key = cv2.waitKey(1) & 0xFF
	ch = cv2.waitKey(1)
	if key == ord("q"):
		break
	
	if flat == 1:
		fn = './motionObject/shot%d.jpg' % (shot_idx)
		cv2.imwrite(fn,frame)
		shot_idx += 1
		continue

	
camera.release()
cv2.destroyAllWindows()
