import hand_tracking_module as hand
import face_mesh as face
import pose_estimation as pose
import cv2 as cv
import pandas as pd
import numpy as np
import time




#only cpu slow


def main():
    cap = cv.VideoCapture(0)
    handT = hand.HandDetector()
    faceM = face.FaceMeshes()
    poseE = pose.PoseEstimation()

    pTime=0

    while True:
        success, img = cap.read()

        img = handT.find_hands(img)
        img = faceM.find_mesh(img)
        img = poseE.find_body(img)


        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), thickness=2)

        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF==ord("q"):
            break


if __name__=="__main__":
    main()