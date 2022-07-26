import cv2,time
import pykeyboard as keyboard_state 
from pycv2.img.drawing import fancydraw

class objectdetctor():
    def __init__(self,img,bbox):
        self.tracker=cv2.TrackerCSRT_create()
        self.tracker.init(img, bbox)
    def update(self,img):
        success,bbox=self.tracker.update(img)
        if success:
            bbox=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
        return bbox
    def fancydraw(self,img,bbox,l=30,color=(0,255,0),thickness=10):
        return fancydraw(img,bbox,l,color,thickness)
def __example(): 
    cap=cv2.VideoCapture("video.mp4")
    #tracker=cv2.TrackerMIL_create()
    success,img=cap.read()
    bbox=cv2.selectROI("result",img,False)
    
    ptime=0
    ctime=0

    while True:
        timer=cv2.getTickCount()
        success,img=cap.read()
        
        if success:
            cv2.putText(img,"tracking",(10,120),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)
        else:
            print("lost")
            cv2.putText(img,"lost",(10,120),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),2)
        fps=cv2.getTickFrequency()/(cv2.getTickCount()-timer)
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),2)
        cv2.imshow("result",img)
        if cv2.waitKey(1) and keyboard_state.check_key_pressed(0x51):
            break;    
if __name__=="__main__":
    __example()
