import cv2 as cv
import mediapipe as mep
import time

#https://solutions.mediapipe.dev/face_detection#model_selection
#https://solutions.mediapipe.dev/face_detection#min_detection_confidence
#https://developers.google.com/mediapipe/solutions/vision/face_detector/
class FaceDetection():
    def __init__(self, min_confidence=0.5, model_selection=0):
        self.mepFaceDetection = mep.solutions.face_detection
        self.faceDetection = self.mepFaceDetection.FaceDetection(min_confidence, model_selection)
        self.mepDraw = mep.solutions.drawing_utils

    def find_face(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.faceDetection.process(imgRGB)

        #form of result: self.result.detections is a list of objects containing data to score, 
        #accessing score of first face: detector.result.detections[0].score
        if self.result.detections:
            for id, detection in enumerate(self.result.detections):
                #bounding box class
                bboxC = detection.location_data.relative_bounding_box
                #height, width, channel
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                        int(bboxC.width * iw), int(bboxC.height * ih)
                


    
                #self.mepDraw.draw_detection(img, detection)
        return bbox
    
    def draw_detection_rectangle(self, bbox, img):
        score = self.result.detections[0].score[0]
        
        cv.rectangle(img, bbox, (255,0,255), thickness=2)
        #confidence value
        cv.putText(img, f"Score: {int(score*100)}%", (bbox[0], bbox[1]-20), cv.FONT_HERSHEY_PLAIN,
                    1,(255,0,255), 2)
        return img

            




def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = FaceDetection()


    while True:
        success, img = cap.read()

        box = detector.find_face(img)
        img = detector.draw_detection_rectangle(box, img)
       



        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (0,255, 0), thickness=2)

        cv.imshow("Face Detection", img)
        if cv.waitKey(1) & 0xFF==ord("q"):
            break



if __name__=="__main__":
    main()