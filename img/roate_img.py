import cv2,math,pykeyboard as key,numpy as np
from pycv2.img.utils import *

def rotate(image,angel):
    center=(int(image.shape[1]/2),int(image.shape[0]/2))
    shape = ( image.shape[1], image.shape[0] ) # cv2.warpAffine expects shape in (length, height)
    matrix = cv2.getRotationMatrix2D( center=center, angle=(angel/np.pi), scale=1 )
    return cv2.warpAffine(image,matrix,shape)
def rotate_all_image(image, angle,):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def rotate_object(pos,cropedimg,src,angle,thresh=None,box=None):
    thresh=thresh if not thresh is None else np.ones(cropedimg.shape[:2],"uint8")*255
    oh,ow=cropedimg.shape[:2]
    img_box=np.zeros((oh,ow),"uint8")
    box=box if not box is None else [0,0,ow,oh]
    cv2.rectangle(img_box,[box[0]-pos[0],box[1]-pos[1]],box[2:],255,cv2.FILLED)

    pos=pos.copy()
    resultimg=src.copy()
    rotated_img=rotate_all_image(cropedimg,angle)
    rotated_mask=rotate_all_image(thresh,angle)
    img_box=rotate_all_image(img_box,angle)
    rotated_mask=cv2.bitwise_and(img_box,rotated_mask)

    h,w=rotated_img.shape[:2]
    #clamping the box
    pos[0]+=(ow-w)//2
    pos[1]+=(oh-h)//2
    _x=0 if pos[0]>0 else abs(pos[0])
    _y=0 if pos[1]>0 else abs(pos[1])
    #to decrease the width and height either
    b=pts_2_xywh(clamp_points(xywh_2_pts([pos[0],pos[1],w,h]),resultimg))
    thresh=rotated_mask.astype(np.bool)[_y:b[3]+_y,_x:b[2]+_x]
    
    resultimg[b[1]:b[1]+b[3],b[0]:b[0]+b[2]][thresh]=rotated_img[_y:b[3]+_y,_x:b[2]+_x][thresh]
    
    return resultimg
