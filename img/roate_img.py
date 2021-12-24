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
def rotate_keep_prestective(img,angle,center=None,scale=1):
    
    
    rot_mat = cv2.getRotationMatrix2D( center, angle, scale )
    warp_rotate_dst = cv2.warpAffine(warp_dst, rot_mat, (warp_dst.shape[1], warp_dst.shape[0]))
def rotate_object(pos,cropedimg,completeimg,angle,thresh=None):
        if thresh is None:
            thresh=np.ones(cropedimg.shape[:2],"uint8")
            thresh=cv2.bitwise_not(thresh)
        resultimg=completeimg.copy()
        rotated_img=rotate_all_image(cropedimg.copy(),angle)
        rotated_mask=rotate_all_image(thresh.copy(),angle)
        h,w=rotated_img.shape[:2]
        b=clamp_box([pos[0],pos[1],w,h],completeimg)
        thresh=rotated_mask.astype(np.bool)[0:b[3],0:b[2]]
        resultimg[b[1]:b[1]+b[3],b[0]:b[0]+b[2]][thresh]=rotated_img[0:b[3],0:b[2]][thresh]
        return resultimg
