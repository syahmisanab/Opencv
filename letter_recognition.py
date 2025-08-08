import cv2
import pytesseract

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Define Region of Interest (ROI) for letter detection
    x1, y1, x2, y2 = 100, 100, 400, 300
    roi = frame[y1:y2, x1:x2]

    # Draw rectangle around ROI
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Convert ROI to grayscale and apply threshold
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(thresh, config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Filter only the first character (if any)
    if text.strip():
        letter = text.strip()[0].upper()
        cv2.putText(frame, f'Detected: {letter}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
    else:
        cv2.putText(frame, 'Detected: -', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

    # Show results
    cv2.imshow("Letter Detection", frame)
    cv2.imshow("ROI - Threshold", thresh)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
