import cv2
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

