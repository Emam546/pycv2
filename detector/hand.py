import mediapipe as mp,cv2,math,numpy as np,time
mpDraw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands
tipIds = [4, 8, 12, 16, 20]
class Hand_detector():
    def __init__(self,mode=False,maxhands=2,detectioncon=0.5,trackcon=0.5,drawSpec=mpDraw.DrawingSpec()):
        self.drawSpec=drawSpec
        self.hands=mp_hand.Hands(mode,maxhands,detectioncon,trackcon)
    def find_hands(self,img,draw=True):
        imgRgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgRgb)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:mpDraw.draw_landmarks(img,handLms,mp_hand.HAND_CONNECTIONS,self.drawSpec,self.drawSpec)
        return img
    def findpositions(self,img,handnum=0,draw=True):
        lmlist=[]
        if self.result.multi_hand_landmarks:
            handLms = self.result.multi_hand_landmarks[handnum]
            for id,lm in enumerate(handLms.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                lmlist.append([cx,cy])
                if draw:cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
        return lmlist 
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
    def get_results(self,img):
        imgRgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        return self.hands.process(imgRgb)
    def fingersUp(self,img):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        results=self.get_results()
        
        if results.multi_hand_landmarks:
            myHandType = self.handType()
            fingers = []
            # Thumb
            if myHandType == "Right":
                lmlist=self.findpositions(img,)
                if self.lmList[tipIds[0]][0] > self.lmList[tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if self.lmList[tipIds[0]][0] < self.lmList[tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if self.lmList[tipIds[id]][1] < self.lmList[tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers
    def handType(self,img):
        """
        Checks if the hand is left or right
        :return: "Right" or "Left"
        """
        results=self.get_results()
        if results.multi_hand_landmarks:
            lmList=self.findpositions(img,0,False)
            if lmList[17][0] < lmList[5][0]:
                return "Right"
            else:
                return "Left"