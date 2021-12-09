import cv2,mediapipe as mp,time,math

from numpy.lib.function_base import angle

mppose=mp.solutions.pose
mpDraw=mp.solutions.drawing_utils
class poseDetctor():
    def __init__(self,mode=False,upperbody=False,smoothlandmarks=False,min_detect_confid=0.5,min_track_confid=0.5,drawSpec=mpDraw.DrawingSpec()):
        self.upper=upperbody
        self.drawSpec=drawSpec
        self.pose=mppose.Pose(mode,upperbody,smoothlandmarks,min_detect_confid,min_track_confid)
    def findPose(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.pose.process(imgRGB)
        if draw and results.pose_landmarks:
            if self.upper:
                mpDraw.draw_landmarks(img,results.pose_landmarks,mppose.UPPER_BODY_POSE_CONNECTIONS,self.drawSpec,self.drawSpec)
            else:
                mpDraw.draw_landmarks(img,results.pose_landmarks,mppose.POSE_CONNECTIONS,self.drawSpec,self.drawSpec)
            
        return img
    def findpositions(self,img,draw=True,color=(255,0,0),radius=5):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.pose.process(imgRGB)
        lmlist=[]
        if  results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmlist.append([cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),radius,color,cv2.FILLED)
        return lmlist
    def get_results(self,img):
        return self.pose.process(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

    def findAngel(self,img,p1,p2,p3,draw=True,color=(255,0,0),radius=5,lcolor=(255,255,255),thickness=1,drawtext=True,fontscale=5,font=cv2.FONT_HERSHEY_SIMPLEX,tcolor=(0,255,0),textthickness=1):
        lmlist=self.findpositions(img,False)
        x1,y1=lmlist[p1];x2,y2=lmlist[p2];x3,y3=lmlist[p3]
        angel=math.degrees(math.atan2(y3-y2,x3-x2)-
                math.atan2(y1-y2,x1-x2))
        if angel>180:angel=360-angel
        elif angel<0:angel+=360
        if draw:
            cv2.line(img,lmlist[p2],lmlist[p1],lcolor,thickness)
            cv2.line(img,lmlist[p2],lmlist[p3],lcolor,thickness)
            for center in [lmlist[p1],lmlist[p2],lmlist[p3]]:
               cv2.circle(img,center,int(radius/2),color,cv2.FILLED)
               cv2.circle(img,center,int(radius),color)
            if drawtext:
                cv2.putText(img,str(int(angel)),(x2-10,y2),font,fontscale,tcolor,textthickness)
        return angel
    
    def findLenght(self,img,p1,p2,draw=True,color=(255,0,0),radius=5,lcolor=(255,255,2555),thickness=3):
        lmlist=self.findpositions(img,False)
        x1,y1=lmlist[p1][0],lmlist[p1][1]
        x2,y2=lmlist[p2][0],lmlist[p2][1]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        lenght=math.hypot(x2-x1,y2-y1)  
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),lcolor,thickness)   
            cv2.circle(img,(x1,y1),radius,color,thickness,cv2.FILLED)
            cv2.circle(img,(x2,y2),radius,color,thickness,cv2.FILLED)
            cv2.circle(img,(cx,cy),radius,color,thickness,cv2.FILLED)
        return lenght
        

    

if __name__=="__main__":
    cap=cv2.VideoCapture("video3.mp4")
    ptime=0
    detector=poseDetctor(upperbody=True)
    while True:
        success,img=cap.read()
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        print(detector.get_results(img).pose_landmarks)

        cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_COMPLEX,3,(0,255,0))
        cv2.imshow("show",img)
        cv2.waitKey(1)
