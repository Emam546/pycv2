import cv2
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
    x,y,w,h=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),color,thickness,linetype)
    return img