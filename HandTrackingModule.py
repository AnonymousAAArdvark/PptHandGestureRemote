import cv2 as cv
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, maxHands=10, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        return img

    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                hand = []
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    hand.append([id, cx, cy, lm.x, lm.y, lm.z])
                    if draw:
                        cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)
                lmList.append(hand)

        return lmList

    def drawHands(self, img, pointingGesture):
        if self.results.multi_hand_landmarks:
            for idx, handLms in enumerate(self.results.multi_hand_landmarks):
                if len(pointingGesture) > idx:
                    if pointingGesture[idx] == "Left":
                        handColor = (0, 255, 255)
                    elif pointingGesture[idx] == "Right":
                        handColor = (0, 255, 0)
                    else:
                        handColor = (255, 0, 0)
                else:
                    handColor = (255, 0, 0)
                self.mpDraw.draw_landmarks(img, handLms, self.mphands.HAND_CONNECTIONS,
                                           self.mpDraw.DrawingSpec(handColor))