# Rock Paper Scissors Game with Hand Gesture Recognition

This is an implementation of the classic game **Rock, Paper, Scissors**, where the user can play against the computer using hand gestures detected by the webcam. The game uses a machine learning model to recognize the gestures and determine the outcome.  

*How to play:*

1.  Press **SPACE** to start the game  
2.  After that a countdown will appear in which you have to make your choice using your hands  
3.  The winner is then decided and displayed on the screen (Computer choice is completely random using the python random library)  
4.  Press **SPACE** to play again or **ESC** to quit  

**Features:**  

•	Real-time hand gesture recognition using the webcam  
•	Simple machine learning model using RandomForestClassifier to classify gestures  
•	Data collection script included to gather your own hand gesture data  
•	Countdown and user-friendly UI with OpenCV  

**Data Collection**  

A separate script, collect_data.py, is provided to collect the hand gesture data and label it correctly but unfortunately manually. The script extracts hand landmarks and labels them based on gestures such as Rock, Paper, and Scissors. The data is saved as a CSV file.  

**Installation:**  
To install the required libraries, run the following commands:
```
pip install opencv mediapipe
```

```
brew install gstreamer
```

if you wish to modify the machine learning model, additionally install:
```
pip install sk-learn pandas
```