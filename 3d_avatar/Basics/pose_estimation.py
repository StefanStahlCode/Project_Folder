import cv2 as cv
import mediapipe as mep
import time
#https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
class PoseEstimation():
    def __init__(self, mode=False,complexity=1, smooth_landmarks=True, enable_segmentation=False, smooth_segmentation=True, 
                min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mepPose = mep.solutions.pose
        self.pose = self.mepPose.Pose(mode, complexity, smooth_landmarks, enable_segmentation,smooth_segmentation, 
                                    min_detection_confidence, min_tracking_confidence)
        self.mepDraw = mep.solutions.drawing_utils

    #getting list of landmarks and drawing them on the image
    def find_body(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks and draw:
            self.mepDraw.draw_landmarks(img, self.results.pose_landmarks, self.mepPose.POSE_CONNECTIONS)

        return img

    def get_position(self, img):
        lm_list = []

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #landmark values relativ to image size (from 0 to 1) for each coordinate
                cx, cy = int(lm.x*w), int(lm.y*h)
                lm_list.append([id, cx, cy])
        

        return lm_list
        
        



def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = PoseEstimation()

    while True:
        success, img = cap.read()
        img = detector.find_body(img)
        lm_list = detector.get_position(img)

        if lm_list:
            #cv.circle(img, (lm_list[0][1], lm_list[0][2]), 10, (255,0,0), cv.FILLED)
            print(lm_list[0])
        #fps 
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), thickness=2)


        cv.imshow("Body Tracking", img)
        if cv.waitKey(1) & 0xFF==ord("q"):
            break


if __name__ == "__main__":
    main()