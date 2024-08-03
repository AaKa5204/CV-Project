import cv2 
import numpy as np
import HandTrackingModule as htm
import math 
import VolumeControls as vc

minvol = -6
maxvol = 11

cap = cv2.VideoCapture(0)
detector = htm.HandTracker(detection_confidence=0.95)
while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)
    if len(lmList)!= 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1 + x2)//2, (y1+y2)//2
        length = math.hypot(x2-x1, y2-y1)
        vol = np.interp(length, [40, 160], [minvol, maxvol])
        vc.set_volume(vol)
