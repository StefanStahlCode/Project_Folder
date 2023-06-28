import cv2 as cv
import mediapipe as mep
import time

#detecting landmarks on faces

class FaceMeshes():
    #static_image_mode whether detection is run on every frame, False a lot better for performance
    #refine_landmarks: Whether to further refine the landmark coordinates
    #around the eyes and lips, and output additional landmarks around the
    #irises. Default to False. See details in
    #https://solutions.mediapipe.dev/face_mesh#refine_landmarks.
    def __init__(self, static_image_mode=False,
               max_num_faces=1,
               refine_landmarks=False,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        self.mepDraw = mep.solutions.drawing_utils
        self.mepFaceMesh = mep.solutions.face_mesh
        self.mepFaceConnections = mep.solutions.face_mesh_connections
        self.faceMesh = self.mepFaceMesh.FaceMesh(static_image_mode, max_num_faces, refine_landmarks, 
                                                   min_detection_confidence, min_tracking_confidence)
        self.drawSpecs = self.mepDraw.DrawingSpec(thickness=1, circle_radius=1)

    def find_mesh(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)
        if self.results.multi_face_landmarks and draw:
            for faceLms in self.results.multi_face_landmarks:
                self.mepDraw.draw_landmarks(img, faceLms, self.mepFaceConnections.FACEMESH_CONTOURS, 
                                            self.drawSpecs, self.drawSpecs)
                
        return img
                
        
    #changes relative landmark cooridnates to absolute pixel values depending on image size
    #returns 
    def landmark_relativ_to_absolute(self, img):
        list_lm = []
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                for id,lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x,y = int(lm.x*iw), int(lm.y*ih)
                    list_lm.append([id, x, y])
        return list_lm
        




def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    meshes = FaceMeshes()


    while True:
        success, img = cap.read()
        img = meshes.find_mesh(img)
        meshes.landmark_relativ_to_absolute(img)
        list_lm = meshes.landmark_relativ_to_absolute(img)
        print(list_lm)






        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 2, (0,255, 0), thickness=2)

        cv.imshow("Face Meshes", img)
        if cv.waitKey(1) & 0xFF==ord("q"):
            break




if __name__ == "__main__":
    main()