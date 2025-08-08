import cv2 as cv
import numpy as np

class ColorTracker:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.track_state = 'init'
        self.selecting = False
        self.hsv_range = None
        self.mouse_start = (0, 0)
        self.mouse_end = (0, 0)
        self.roi = None
        cv.namedWindow('frame')
        cv.setMouseCallback('frame', self.on_mouse)

    def on_mouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.mouse_start = (x, y)
            self.selecting = True
            self.track_state = 'init'
        elif event == cv.EVENT_MOUSEMOVE and self.selecting:
            self.mouse_end = (x, y)
        elif event == cv.EVENT_LBUTTONUP:
            self.mouse_end = (x, y)
            self.selecting = False
            self.roi = (min(self.mouse_start[0], self.mouse_end[0]),
                        min(self.mouse_start[1], self.mouse_end[1]),
                        abs(self.mouse_end[0] - self.mouse_start[0]),
                        abs(self.mouse_end[1] - self.mouse_start[1]))
            self.track_state = 'identify'

    def get_hsv_from_roi(self, frame):
        x, y, w, h = self.roi
        roi = frame[y:y+h, x:x+w]
        hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        hmin, smin, vmin = hsv_roi.min(axis=(0, 1))
        hmax, smax, vmax = hsv_roi.max(axis=(0, 1))
        self.hsv_range = ((hmin, smin, vmin), (hmax, smax, vmax))
        print(f"HSV Range selected: {self.hsv_range}")

    def track_color(self, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower, upper = self.hsv_range
        mask = cv.inRange(hsv, np.array(lower), np.array(upper))
        result = cv.bitwise_and(frame, frame, mask=mask)

        # Find contours and draw a circle
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv.contourArea)
            (x, y), radius = cv.minEnclosingCircle(largest)
            center = (int(x), int(y))
            radius = int(radius)
            if radius > 5:
                cv.circle(frame, center, radius, (0, 255, 0), 2)
                cv.circle(result, center, radius, (0, 255, 0), 2)
        return result, mask

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv.resize(frame, (640, 480))
            display_frame = frame.copy()
            binary = np.zeros_like(frame)

            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.hsv_range = None
                self.track_state = 'init'
            elif key == ord('i') and self.roi is not None:
                self.get_hsv_from_roi(frame)

            if self.selecting:
                cv.rectangle(display_frame, self.mouse_start, self.mouse_end, (0, 255, 0), 2)

            if self.hsv_range:
                binary, mask = self.track_color(display_frame)

            combined = np.hstack((display_frame, binary))
            cv.imshow('frame', combined)

        self.cap.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    tracker = ColorTracker()
    tracker.run()
