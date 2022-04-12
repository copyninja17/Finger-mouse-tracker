import cv2
import mediapipe as mp
import time
import os
import pyautogui

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.1)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
mouse_pos_x = 0
mouse_pos_y = 0

ind_relative_x = 0
ind_relative_y = 0
tmb_relative_x = 0
tmb_relative_y = 0
mid_relative_x = 0
mid_relative_y = 0

pyautogui.FAILSAFE = False

res_x = 1280
res_y = 960

while True:
    success, img = cap.read()
    img = cv2.resize(img, (res_x,res_y))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            count = 0
            for landmark in handLms.landmark:
                x = landmark.x
                y = landmark.y

                shape = img.shape
                relative_x = int(x * shape[1])
                relative_y = int(y * shape[0])
                if count == 4:
                    tmb_relative_x = relative_x
                    tmb_relative_y = relative_y
                if count == 8:
                    ind_relative_x = relative_x
                    ind_relative_y = relative_y
                if count == 12:
                    mid_relative_x = relative_x
                    mid_relative_y = relative_y
                    pyautogui.moveTo(1920 - ind_relative_x, ind_relative_y)
                if int(((mid_relative_x-tmb_relative_x)**2 + (mid_relative_y-tmb_relative_y)**2)**(1/2)) < 75:
                    # pyautogui.click()
                    print(int(((mid_relative_x-tmb_relative_x)**2 + (mid_relative_y-tmb_relative_y)**2)**(1/2)))
                count += 1
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    img = cv2.flip(img,1)

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.rectangle(img,(res_x//10,res_y//10),(res_x*9//10,res_y*9//10),(255,0,0),4)

    
    if os.name =='windows':
        os.system('cls')
    elif os.name =='posix':
        os.system('clear')
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break