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


def draw_box_moving(img,points:list,
        color_line=(255,255,0),thickness=2,radius=2,
        colors:tuple=COLORS_OF_WRAPPING,center_state=False,colorcenter=(0,0,255),radius_center=2):
    img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR) if len(img.shape)==2 else img
    for i,pt in enumerate(points):
        nexI=(i+1)%len(points)
        cv2.line(img,pt,points[nexI],color_line,thickness)
        
    for i,pt in enumerate(points):
        cv2.circle(img,pt,radius,colors[i%len(colors)],cv2.FILLED)
    if center_state:
        cv2.circle(img,center_pts(points),radius_center,colorcenter,cv2.FILLED)
    return img