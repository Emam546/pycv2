import cv2

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

def draw_rotated_box_img(imgcv,circles=None):
    if circles is None:return imgcv
    resultimg = imgcv.copy()
    if len(resultimg.shape)==2:
        resultimg=cv2.cvtColor(resultimg,cv2.COLOR_GRAY2BGR)
    for x in range(len(circles)):
        if x < 3:
            cv2.line(resultimg, circles[x],
                    circles[x+1], (255, 255, 0), 2)
        if x == 0:
            cv2.line(resultimg, circles[x],
                    circles[3], (255, 255, 0), 2)
        cv2.circle(resultimg, circles[x],
                6, (0, 0, 255), cv2.FILLED)
    return resultimg
def centerbox(box):
    return box[0]+int(box[2]/2),box[1]+int(box[3]/2)
def pts_2_xywh(pts):
    if len(pts)<=3:
        raise "the points are not four points"
    x,y=99999999999999999,999999999999999999
    mx,my=0,0
    for pos in pts:
        if pos[0]<x:
            x=int(pos[0])
        if pos[0]>mx:
            mx=int(pos[0])
        if pos[1]<y:
            y=int(pos[1])
        if pos[1]>my:
            my=int(pos[1])
    w,h=(mx-x),(my-y)
    return [x,y,w,h]    
    
def center_pts(pts):
    return centerbox(pts_2_xywh(pts))
def draw_box_moving(img,circles:list,
        color_line=(255,255,0),thickness=2,radius=2,
        colors:tuple=COLORS_OF_WRAPPING,center_state=False,colorcenter=(0,0,255)):
    img=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR) if len(img.shape)==2 else img

    circles=circles.copy()

    for id,pt in enumerate(circles):
        if id<=2 and len(circles)>=id+2:
            cv2.line(img,pt,circles[id+1],color_line,thickness)
        if id==0 and len(circles)==4:
            cv2.line(img,pt,circles[3],color_line,thickness)
        for n,pt in enumerate(circles):
            n=min(n,len(colors))
            cv2.circle(img,pt,radius,colors[n],thickness,cv2.FILLED)
    if center_state:
        cv2.circle(img,center_pts(circles),radius,colorcenter,thickness)
    return img