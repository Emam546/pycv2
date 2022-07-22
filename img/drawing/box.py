import cv2
from pycv2.img.utils import center_pts
COLORS_OF_WRAPPING = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
def fancydraw(img,bbox,l=30,color=(0,255,0),thickness=10):
    x,y,w,h=bbox
    x1,y1=x+w,y+h
    cv2.line(img,(x,y),(x+l,y),color,thickness)
    cv2.line(img,(x,y),(x,y+l),color,thickness)
    cv2.line(img,(x1,y),(x1-l,y),color,thickness)
    cv2.line(img,(x1,y),(x1,y+l),color,thickness)
    cv2.line(img,(x,y1),(x+l,y1),color,thickness)
    cv2.line(img,(x,y1),(x,y1-l),color,thickness)
    cv2.line(img,(x1,y1),(x1-l,y1),color,thickness)
    cv2.line(img,(x1,y1),(x1,y1-l),color,thickness)
    return img
def drawbox(img,bbox,color=(0,255,0),thickness=3,linetype=1):
    x,y,w,h=bbox
    cv2.rectangle(img,(x,y),((x+w),(y+h)),color,thickness,linetype)
    return img

""" def draw_rotated_box_img(imgcv,points=None):
    if points is None:return imgcv
    resultimg = imgcv.copy()
    if len(resultimg.shape)==2:
        resultimg=cv2.cvtColor(resultimg,cv2.COLOR_GRAY2BGR)
    for x in range(len(points)):
        if x < 3:
            cv2.line(resultimg, points[x],
                    points[x+1], (255, 255, 0), 2)
        if x == 0:
            cv2.line(resultimg, points[x],
                    points[3], (255, 255, 0), 2)
        cv2.circle(resultimg, points[x],
                6, (0, 0, 255), cv2.FILLED)
    return resultimg """

def draw_box_moving(img,points:list,
        color_line=(255,255,0),thickness=2,radius=2,
        colors:tuple=COLORS_OF_WRAPPING,center_state=False,colorcenter=(0,0,255),radius_center=2):
    img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR) if len(img.shape)==2 else img
    for id,pt in enumerate(points):
        if id<3 and len(points)>=id+2:
            cv2.line(img,pt,points[id+1],color_line,thickness)
        if id==0 and len(points)>=4:
            cv2.line(img,pt,points[3],color_line,thickness)
    for id,pt in enumerate(points):
        n=min(id,len(colors)-1)
        cv2.circle(img,pt,radius,colors[n],cv2.FILLED)
    if center_state:
        cv2.circle(img,center_pts(points),radius_center,colorcenter,cv2.FILLED)
    return img