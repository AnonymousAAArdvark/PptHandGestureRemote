import cv2
import time
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
pointingGesture = []
detect_repeat = 0
detector = htm.HandDetector(detectionCon=0.8)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    pointingGesture = []

    if len(lmList) != 0:
        for hand in lmList:
            pointingGesture.append(hgt.inPointingGesture(hand))

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 3)
    cv2.putText(img, f'Orientation: {pointingGesture}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                .7, (255, 0, 0), 2)

    for idx, hand in enumerate(pointingGesture):
        if hand != "None":
            detect_repeat += 1
        else:
            detect_repeat = 0
    detector.drawHands(img, pointingGesture)

    cv2.imshow("Img", img)
    cv2.waitKey(1)