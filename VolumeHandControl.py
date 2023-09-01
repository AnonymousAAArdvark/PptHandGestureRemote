import math
import cv2
import time
import numpy as np
import osascript
import pyautogui
import HandTrackingModule as htm
import KeyboardFunctions as kbf
import HandGestureDetection as hgt

##########
wCam, hCam = 640, 480
##########

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
vol = 0
volBar = 400
closed_fingers = []
color = (255, 0, 0)
pointingGesture = "None"
detect_repeat = 0
detector = htm.HandDetector(detectionCon=0.8)

while True:
    success, img = cap.read()
    img = detector.findHands(img, True, color)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


        # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 300], [0, 100])
        volBar = np.interp(length, [50, 300], [400, 150])

        # print(hgt.findOrientation(lmList[0], lmList[9]))
        pointingGesture = hgt.inPointingGesture(lmList)
        # if length < 50:
        #     cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        #     kbf.rightArrowPress()
        # if length > 250:
        #     cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        #     kbf.leftArrowPress()

    # cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    # cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    # cv2.putText(img, f' {int(vol)} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX,
    #             1, (255, 0, 0), 3)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 3)

    if pointingGesture != "None":
        # print("detected" + str(detect_repeat))
        detect_repeat += 1
        color = (0, 255, 0)
        cv2.putText(img, f'Orientation: {pointingGesture}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 3)
    else:
        detect_repeat = 0
        color = (255, 0, 0)

    cv2.imshow("Img", img)
    cv2.waitKey(1)