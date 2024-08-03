import cv2 
import numpy as np
import HandTrackingModule as htm
import math 
import VolumeControls as vc

minvol = -5
maxvol = 11
print(vc.get_volume())
vc.set_volume(100)
################################
wcam, hcam = 1920, 1080
################################

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
detector = htm.HandTracker(detection_confidence=0.95)
while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)
    if len(lmList)!= 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1 + x2)//2, (y1+y2)//2
        cv2.circle(img, (x1, y1), 5, (0,255,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (0,255,0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), color=(0,0,255), thickness=1)
        cv2.circle(img, (cx,cy), 5, (0,255,0), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        vol = np.interp(length, [30, 160], [minvol, maxvol])
        print(int(vol))
        vc.set_volume(vol)
    cv2.imshow("Controller", img)
    cv2.waitKey(1)
