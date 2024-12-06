import cv2
import csv
import os
from handdetection import handDetector

# Camera settings
WCAM, HCAM = 1320, 720

cap = cv2.VideoCapture(1)
cap.set(3, WCAM)
cap.set(4, HCAM)

# Initialise handDetector class
detector = handDetector()

# Path to save collected data
data_file = "hand_gesture_data.csv"

# Create the CSV file with headers if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["label", "handType"] + [f"x{i}" for i in range(21)] + [f"y{i}" for i in range(21)])

# Start capturing data
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = detector.findhands(frame)  # Detect hands and draw landmarks
    lmList, handType = detector.findPos(frame)  # Get landmark positions and hand type

    # Instructions
    cv2.putText(frame, "Press R, P, S to label gestures", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "ESC to quit", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Data Collection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key to quit
        break

    label = None
    if key == ord('r'):  # Rock
        label = "Rock"
    elif key == ord('p'):  # Paper
        label = "Paper"
    elif key == ord('s'):  # Scissors
        label = "Scissors"

    # Save when label has been selected
    if label and lmList: 
        data_row = [label, handType] + [coord[1] for coord in lmList] + [coord[2] for coord in lmList]
        with open(data_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_row)
        print(f"Saved {label} data.")

cap.release()
cv2.destroyAllWindows()