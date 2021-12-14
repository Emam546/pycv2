import cv2,mediapipe as mp,time
mpdraw=mp.solutions.drawing_utils
mpfacedetction=mp.solutions.face_detection
#,drawSpec=mpdraw.DrawingSpec()
class facedetection():
    def __init__(self,minconfidence=0.5):
        self.faceDetection=mpfacedetction.FaceDetection(minconfidence)
    
    def findfaces(self,img):
        h,w=img.shape[:2]
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.faceDetection.process(imgRGB)
        bboxs=[]
        if results.detections:
            for detection in results.detections:
                pos=detection.location_data.relative_bounding_box
                bbox=int(pos.xmin*w),int(pos.ymin*h),\
                    int(pos.width*w),int(pos.height*h)
                bboxs.append([bbox,detection.score[0]])
        return bboxs

def main():
    cap=cv2.VideoCapture("video.mp4")
    ptime=0
    detector=facedetection()
    while True:
        success,img=cap.read()
        try:
            ctime=time.time()
            fps=1/(ctime-ptime)
            ptime=ctime
            cv2.putText(img,str(int(fps)),(50,100),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0))
        except:pass
        img,bbox=detector.findfaces(img,False)
        if len(bbox)!=0:
            pos=bbox[0][0]
            
            detector.fancydraw(img,pos)
        cv2.imshow("show",img)
        cv2.waitKey(1)
    
if __name__=="__main__":
    main()