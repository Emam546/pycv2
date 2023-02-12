import cv2,mediapipe as mp,math,time
mpdraw=mp.solutions.drawing_utils
mpfacemesh=mp.solutions.face_mesh
#cap=cv2.VideoCapture("http://192.168.0.104:8080/video")
class Face_landmarks():
    def __init__(self,mode=False,max_num_faces=1,detect_confid=0.5,track_confid=0.5,drawSpec=mpdraw.DrawingSpec()):
        self.drawSpec=drawSpec
        self.facemesh=mpfacemesh.FaceMesh(mode,max_num_faces,detect_confid,track_confid)
    def findface(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.facemesh.process(imgRGB)
        if draw and results.multi_face_landmarks:
            for facelms in results.multi_face_landmarks:
                mpdraw.draw_landmarks(img,facelms,mpfacemesh.FACE_CONNECTIONS,
                self.drawSpec,self.drawSpec)
        return img
    def findpositions(self,img,draw=True,color=(255,0,0),radius=5):
        h,w=img.shape[:2]
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.facemesh.process(imgRGB)
        lmlist=[]
        if results.multi_face_landmarks:
            for facelms in results.multi_face_landmarks:
                for id,lm in enumerate(facelms.landmark):
                    cx,cy=(int(lm.x*w)),(int(lm.y*h))
                    lmlist.append([id,cx,cy])
                    if draw:
                        cv2.circle(img,(cx,cy),radius,color,cv2.FILLED)
        return lmlist

