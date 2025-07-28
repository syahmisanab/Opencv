import cv2
import numpy as np

def empty(a): pass

def initTrackbars():
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
    cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
    cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
    cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
    cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

def getTrackbarValues():
    return [
        [cv2.getTrackbarPos("Hue Min", "TrackBars"),
         cv2.getTrackbarPos("Sat Min", "TrackBars"),
         cv2.getTrackbarPos("Val Min", "TrackBars")],
        [cv2.getTrackbarPos("Hue Max", "TrackBars"),
         cv2.getTrackbarPos("Sat Max", "TrackBars"),
         cv2.getTrackbarPos("Val Max", "TrackBars")]
    ]

def findColor(img, hsvVals):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array(hsvVals[0])
    upper = np.array(hsvVals[1])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgColor = cv2.bitwise_and(img, img, mask=mask)
    return mask, imgColor

initTrackbars()
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    hsvVals = getTrackbarValues()
    mask, imgColor = findColor(img, hsvVals)

    cv2.imshow("Camera", img)
    cv2.imshow("Detected Color", imgColor)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
