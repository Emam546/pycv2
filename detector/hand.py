import mediapipe as mp,cv2,math
from google.protobuf.json_format import MessageToDict
mpDraw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands
HAND_LANDMARKS_LENGTH=21
HAND_CONNECTIONS=mp_hand.HAND_CONNECTIONS
LEFT_HAND="left"
RIGHT_HAND="right"
tipIds = [4, 8, 12, 16, 20]
class Hand_detector(mp_hand.Hands):
    def __init__(self,mode=False,maxhands=2,detectioncon=0.5,trackcon=0.5,drawSpec=mpDraw.DrawingSpec()):
        super().__init__(mode,maxhands,detectioncon,trackcon)
        self.drawSpec=drawSpec
        self.results=None
    
    def find_hands(self,img):
        img.flags.writeable = False
        imgRgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.process(imgRgb)
        img.flags.writeable = True
        return self.result

    def draw_land_marks(self,img,results=None):
        if results is None:
            results=self.result
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img,handLms,HAND_CONNECTIONS,mpDraw.DrawingSpec(),mpDraw.DrawingSpec())
        return img
    def hands_type(self,results=None):
        if results is None:
            results=self.result
        hand_type={}
        def convert(hand):
            return MessageToDict(hand)["classification"][0]
        if results.multi_handedness:
            hand_classification=list(map(convert,results.multi_handedness))
            for num,hand in enumerate(hand_classification):
                label=hand["label"] 
                if label not in hand_type:
                    hand_type[label]=num
                else:
                    other_hand=hand_classification[hand_type[label]]["score"]
                    if other_hand>hand["score"]:
                        hand_type[label]=num
        return hand_type
    def findpositions(self,img,handnum=0,draw=True):
        lmlist=[]
        if self.result.multi_hand_landmarks:
            handLms = self.result.multi_hand_landmarks[handnum]
            for lm in handLms.landmark:
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
