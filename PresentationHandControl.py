import cv2
import time
import HandTrackingModule as htm
import KeyboardFunctions as kbf
import HandGestureDetection as hgt
import mediapipe

# Test the ports and returns a tuple with the available ports and the ones that are working.
dev_port = 0
working_ports = []
while True:
    camera = cv2.VideoCapture(dev_port)
    if not camera.isOpened():
        print("Port %s is not working." % dev_port)
        break
    else:
        is_reading, img = camera.read()
        w, h = camera.get(3), camera.get(4)
        if is_reading:
            print("Port %s is working and reads images (%s x %s)" % (dev_port, h, w))
            working_ports.append(dev_port)
        else:
            print("Port %s for camera (%s x %s) is present but does not read." % (dev_port, h, w))
    dev_port += 1


##########
wCam, hCam = 640, 480
##########

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
pointingGesture = []
prevAction = "None"
nRepeats = 0
detector = htm.HandDetector(detectionCon=0.8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    pointingGesture = []

    if len(lmList) != 0:
        for hand in lmList:
            pointingGesture.append(hgt.inPointingGesture(hand))

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                .7, (255, 0, 0), 2)
    cv2.putText(img, 'Press \'q\' to quit', (10, 460), cv2.FONT_HERSHEY_SIMPLEX,
                .7, (255, 0, 0), 2)
    if len(pointingGesture) != 0:

        cv2.putText(img, f'Orientation: {pointingGesture[0][0]}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    .7, (255, 0, 0), 2)
        cv2.putText(img, f'Pointer Extended: {pointingGesture[0][1]}', (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                    .7, (255, 0, 0), 2)
        cv2.putText(img, f'Thumb and Pointer Right Angle: {pointingGesture[0][2]}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX,
                    .7, (255, 0, 0), 2)
        cv2.putText(img, f'Middle, Ring, Pinky Closed: {pointingGesture[0][3]}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX,
                    .7, (255, 0, 0), 2)



    action = "None"
    vote = 0
    for idx, hand in enumerate(pointingGesture):
        if hand == "Left":
            vote -= 1
        elif hand == "Right":
            vote += 1

    if vote > 0:
        action = "Right"
    elif vote < 0:
        action = "Left"
    else:
        action = "None"

    if action == prevAction and prevAction != "None":
        nRepeats += 1
    else:
        prevAction = action
        nRepeats = 0

    if nRepeats == 2:
        kbf.arrowKeyPress(action)
    elif nRepeats % 6 == 0 and nRepeats != 0:
        kbf.arrowKeyPress(action)

    detector.drawHands(img, pointingGesture)

    if cv2.waitKey(1) == ord('q'):
        break

    cv2.imshow("Img", img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
