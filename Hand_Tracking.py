# u will need mediapipe and opencv module
# run command --> pip install mediapipe 
# run command --> pip install opencv-python
# for documentation on mediapipe    https://google.github.io/mediapipe/solutions/hands
import cv2
import mediapipe as mp
import math

def len(x1,y1, x2, y2):
    return int(pow( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) ,0.5))

# initialise the camera
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
line = mp.solutions.drawing_utils

# Hand Tracking  for reference https://www.youtube.com/watch?v=NZde8Xt78Iw
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    fingers = 0    # Number of fingers shown
    ok = 100
    if result.multi_hand_landmarks:
        for hand_mark in result.multi_hand_landmarks:
            line.draw_landmarks(frame, hand_mark, mpHands.HAND_CONNECTIONS)
            h,w,c = frame.shape
            org_x, org_y = int(hand_mark.landmark[0].x*w), int((hand_mark.landmark[0].y*h))
            lmlist = []               # Create a list With info of all Landmarks
            for id, lm in enumerate(hand_mark.landmark):
                x, y = int(lm.x*w), int((lm.y*h))
                lmlist.append([id,x,y,len(org_x, org_y, x, y)])     
                if id%4 == 0 and id > 4:          # Highlighting the finger tips
                    cv2.circle(frame , (x,y), 10 , (255,0,255) , cv2.FILLED)
            ok = abs(lmlist[8][3]-lmlist[4][3])
            for i in range(8, 21, 4):
                if lmlist[i][3] > lmlist[i-2][3]:     # Counting Fingers Shown
                    fingers+=1

    cv2.putText(frame, "Press Q to Quit", (325,30), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,255), 2)
    cv2.putText(frame, "or", (430,60), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,255), 2)
    cv2.putText(frame, "Join Index Finger and Thumb", (250,90), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0,0,255), 2)
    cv2.putText(frame, str(fingers), (20,50), cv2.FONT_HERSHEY_COMPLEX, 1.5 , (255,0,0), 2)
    cv2.imshow("Frame",frame)
    
    if(cv2.waitKey(1) & 0xFF == ord('q')):   # Quit By pressing Q
        break
    if ok < 20 and fingers >= 3:             # Quit by Joining Index Finegr and Thumb 
        break
