import cv2 as cv
import mediapipe as mep
import time


class HandDetector():
    #same parameter as Hands() function
    def __init__(self, mode=False, max_hands=2, complexity=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.mepHands = mep.solutions.hands
        self.hands = self.mepHands.Hands(mode, max_hands, complexity, detection_confidence, tracking_confidence)
        self.mepDraw = mep.solutions.drawing_utils

        
    def find_hands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks and draw:
            #for every hand landmark 
            for handLms in self.results.multi_hand_landmarks:
                self.mepDraw.draw_landmarks(img, handLms, self.mepHands.HAND_CONNECTIONS)

        return img
    
    #hand_no is position of hand, not count of hands
    #return list of lists containing id, cx and cy for every landmark
    def find_position(self, img, hand_no=0):
        #return landmark list
        lm_list = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lm_list.append([id, cx, cy])
        return lm_list




    

def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        #if statement to avoid error on image without detected hand
        if len(lm_list) !=0:
            print(lm_list[0])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), thickness=2)

        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF==ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()