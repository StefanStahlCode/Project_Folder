import cv2 as cv
import mediapipe as mep
import time

#minimum code for hand tracking to work
#0 means the standard webcam
cap = cv.VideoCapture(0)

#creating hands object
mepHands = mep.solutions.hands
#Default values for Hands: static_image_mode=False(True means every frame will be checked for Hands, is slow), 
#max_num_hands=2,
#model_complexity = 1
#min_detection_confidence=0.5
#min_tracking_confidence=0.5 (if the tracking confidence is below this threshold it will detect again)
hands = mepHands.Hands()

#method to draw hand landmarks
mepDraw = mep.solutions.drawing_utils

#frame counter
#previous time, current time
pTime = 0
cTime = 0



while True:
    success, img = cap.read()
    #converting opencv bgr to rgb for hands object
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        #for every hand landmark 
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #each handlms has 21 entries with id and coordinates relative to image size
                # print(id, lm)
                h, w, c = img.shape
                #calculating pixel position for each landmark
                cx,cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)
                #if id == 0:
                #    cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

            #drawing landmarks
            #here: drawing on the displayed image not the rgb image
            #mepHands.HAND_CONECTIONS shows connections between points
            mepDraw.draw_landmarks(img, handLms, mepHands.HAND_CONNECTIONS)

    #calculating fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    #displaying fps
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), thickness=2)

    cv.imshow("Image", img)
    if cv.waitKey(1) & 0xFF==ord("q"):
        break

cap.release()
cv.destroyAllWindows()