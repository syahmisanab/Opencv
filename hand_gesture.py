import cv2
import mediapipe as mp

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configure the model
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Finger tips IDs as per your diagram
finger_tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip horizontally
    h, w, c = frame.shape

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process with MediaPipe
    result = hands.process(rgb)

    finger_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks on hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Convert landmarks to a list of (x, y)
            landmarks = hand_landmarks.landmark

            # Count fingers
            # Thumb (left vs right hand detection would improve this)
            if landmarks[finger_tips_ids[0]].x < landmarks[finger_tips_ids[0] - 1].x:
                finger_count += 1

            # Other 4 fingers
            for tip_id in finger_tips_ids[1:]:
                if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                    finger_count += 1

            # Display finger count
            cv2.putText(frame, f'Fingers: {finger_count}', (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
