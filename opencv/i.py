import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture('mario.gif')

_, img_rgb = cap.read()

state = 0

rectangle_points = [[None, None], [None, None]]

def draw_rectangle(event, x, y, *args):
    global state, img_rgb

    if event == cv2.EVENT_LBUTTONUP:
        if state == 0:
            rectangle_points[0][0] = x
            rectangle_points[0][1] = y
            state = 1
        elif state == 1:
            template = img_rgb[
                min(rectangle_points[0][1], rectangle_points[1][1]):
                max(rectangle_points[0][1], rectangle_points[1][1]),

                min(rectangle_points[0][0], rectangle_points[1][0]):
                max(rectangle_points[0][0], rectangle_points[1][0])
            ]

            w, h = template.shape[:-1]

            ret, img_rgb = cap.read()
            while cap.isOpened():
                if not ret:
                    break
                res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

                cv2.imshow('image', img_rgb)
                cv2.waitKey(20)
                ret, img_rgb = cap.read()

            state = 2
    if state == 1 and event == cv2.EVENT_MOUSEMOVE:
        rectangle_points[1][0] = x
        rectangle_points[1][1] = y
        cv2.imshow('image', cv2.rectangle(img_rgb.copy(),
            (rectangle_points[0][0], rectangle_points[0][1]),
            (rectangle_points[1][0], rectangle_points[1][1]),
            (0, 0, 255),
            1
        ))


cv2.imshow('image', img_rgb)
cv2.setMouseCallback('image', draw_rectangle)

while True:
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()
        break
