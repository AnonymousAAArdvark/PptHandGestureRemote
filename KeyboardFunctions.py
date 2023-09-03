import cv2
import mediapipe as mp
import time
import pyautogui

def arrowKeyPress(direction):
    pyautogui.press(direction.lower())
