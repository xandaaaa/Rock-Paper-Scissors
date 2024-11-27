import cv2
import mediapipe as mp
import time

# Class for detecting hands
class handDetector():
    def __init__(self, mode=False, max_num_hands = 2, model_complexity = 1, detectionConf = 0.5, trackConf = 0.5):
        self.mode = mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        # Init hand
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.max_num_hands, self.model_complexity, self.detectionConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    # Put landmarks on hand
    def findhands(self, frame, draw=True):

        # Convert to RGB
        imgrgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgrgb)

        # Get landmarks
        if self.results.multi_hand_landmarks:
            for landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, landmarks, self.mphands.HAND_CONNECTIONS)
        
        return frame
    
    # Find the position of each index
    def findPos(self, frame, handNo=0):

        lmList = []
        handType = None
        
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

            if self.results.multi_handedness:
                handType = self.results.multi_handedness[handNo].classification[0].label

        return lmList, handType

# Testing
def main():

    cap = cv2.VideoCapture(1)
    prev_time = 0
    detector = handDetector()

    # Open frame
    while cap.isOpened():
        success, frame = cap.read()
        frame = detector.findhands(frame)
        coords = detector.findPos(frame)
        if len(coords) != 0:
            print(coords[0])

        if not success:
            break

        # Flip frame
        frame = cv2.flip(frame, 1)

        # Show FPS
        curr_time = time.time()
        fps = 1/(curr_time-prev_time)
        prev_time = curr_time
        cv2.putText(frame, f'FPS: {int(fps)}', (1100, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

        cv2.imshow("Hand Gesture Recognition", frame)

        # Close if ESC is pressed
        if cv2.waitKey(20) & 0xFF == 27:
            print("Terminating")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()