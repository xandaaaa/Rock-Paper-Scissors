import cv2
import random
import time
from handdetection import handDetector

WCAM, HCAM = 1320, 720

# Set camera settings
cap = cv2.VideoCapture(0)
cap.set(3, WCAM)
cap.set(4, HCAM)

# Init handDetector class
detector = handDetector()

# Detect current move (Paper, Scissor or Rock)
def move(frame):

    frame = detector.findhands(frame)
    coords, _ = detector.findPos(frame)

    if len(coords) > 0:
        if (coords[8][2] < coords[6][2] and coords[12][2] < coords[10][2] and 
            coords[16][2] < coords[14][2] and coords[20][2] < coords[18][2]):
            return "Paper"
        elif (coords[8][2] < coords[6][2] and coords[12][2] < coords[10][2]):
            return "Scissors"
        else:
            return "Rock"
    return

# Start signal and countdown
def start_signal():

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        cv2.putText(frame, "Press SPACE to start!", (470, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.putText(frame, "Make your choice during the countdown", (320, 500), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
        cv2.imshow("Rock Paper Scissors", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            return False
        if key == 32:
            return True

# Implement countdown counting from 3 to 1
def countdown():
    curr_time = time.time()
    countdown = 3

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        # Calculate remaining time and display it as long as it has not hit 0 yet
        elapsed_time = time.time() - curr_time
        remaining_time = countdown - int(elapsed_time)

        if remaining_time > 0:
            cv2.putText(frame, str(remaining_time), (600, 360), cv2.FONT_HERSHEY_DUPLEX, 5, (216, 50, 150), 5)
        else:
            break

        cv2.imshow("Rock Paper Scissors", frame)
        cv2.waitKey(20)

# Decides who won
def decide_winner(user_choice, comp_choice):
    if user_choice == comp_choice:
        return "It's a tie!"
    elif (user_choice == 'Rock' and comp_choice == 'Scissors') or \
         (user_choice == 'Scissors' and comp_choice == 'Paper') or \
         (user_choice == 'Paper' and comp_choice == 'Rock'):
        return "You win!"
    else:
        return "Computer wins!"

# Main loop
while cap.isOpened():
    
    # Wait until user presses "SPACEBAR"
    if start_signal() != True:
        break

    # Start countdown
    countdown() 
    
    # Capture choices after countdown is over
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    # Get user's choice
    user_choice = move(frame)

    # Generate computer's choice
    comp_choice = random.choice(['Rock', 'Paper', 'Scissors'])

    # Decide the winner
    winner = decide_winner(user_choice, comp_choice)

    # Display result, stay in result screen until new action
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        # Display user's choice, computer's choice and winner and further instructions
        cv2.putText(frame, f'User: {user_choice}', (50, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Computer: {comp_choice}', (950, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, winner, (560, 360), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, "Press SPACE to play again or ESC to quit", (300, 680), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Rock Paper Scissors", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27: # ESC key to exit
            cap.release()
            cv2.destroyAllWindows()
            exit()
        if key == 32: # Space to play again (break out of the results "screen")
            break

cap.release()
cv2.destroyAllWindows()