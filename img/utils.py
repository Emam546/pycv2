from collections.abc import Iterable
import cv2,numpy as np
from scipy.spatial import distance as dist
#from skimage.metrics import structural_similarity as compare_ssim
import math
import re

        
def remove_back_ground(mask,img):
    threshimg= cv2.threshold(mask, 0, 255, 0)[1]
    black_img=np.zeros(img.shape,np.uint8)
    result2 = cv2.bitwise_and(black_img,black_img,mask=threshimg)
    maskimg = cv2.bitwise_and(img.copy(),img.copy(),mask=255-threshimg)
    #the removed image
    finalimage=cv2.add(maskimg,result2)
    return finalimage

def duplicate_image(img,shape):
    "shape is height and width"
    h,w=shape
    newimage=np.zeros((h,w,3),"uint8")
    ih,iw=img.shape[:2]
    start=[0,0]
    while start!=[h,w]:
        start[1]=0
        y=min(h,start[0]+ih)
        cy=y-start[0]
        while start[1]!=w:
            x=min(w,start[1]+iw)
            cx=x-start[1]
            newimage[start[0]:y,start[1]:x]=img[0:cy,0:cx]
            start[1]=x
        start[0]=y
        
    return newimage
 
def clamp_box(box,imgcv):
    box=list(box)
    h,w=imgcv.shape[:2]
    box[0]=min(w,max(0,box[0]))
    box[1]=min(h,max(0,box[1]))
    box[2]=max(0,min(box[0]+box[2],w)-box[0])
    box[3]=max(0,min(box[1]+box[3],h)-box[1])
    return box
def clamp_points(points: list,imgcv):
    points=list(points.copy())
    if len(points)==4:
        for id,pt in enumerate(points):
            points[id]=clamp_point(pt,imgcv)
        return points
    else:
        raise"the number of points is not four"
def clamp_point(pt,imgcv):
    h,w=imgcv.shape[:2]
    pt=list(pt)
    pt[0]=max(0,min(int(pt[0]),w-1))
    pt[1]=max(0,min(int(pt[1]),h-1))
    return pt
def centerbox(box):
    return box[0]+int(box[2]/2),box[1]+int(box[3]/2)
def center_pts(pts):
    return centerbox(pts_2_xywh(pts))
def compare_maskes(mask1,mask2):
    if mask1.shape==mask2.shape:
        newmask=cv2.bitwise_xor(mask1,mask2)
        for color in cv2.split(newmask):
            return (cv2.countNonZero(color)/(mask1.shape[1]*mask1.shape[0]))*100        
    else:
        raise "the makses are not the same shape "
def ARE_EQUALE(img1,img2):
    if img1 is None or img2 is None:return False
    if img1.shape==img2.shape:
        diff=np.subtract(img1.astype(np.float),img2.astype(np.float))
        mask=diff!=0
        if np.unique(mask).shape[0]>1:
            return False
        else:
            return True
        
    else:
        return False
# def checksimilarty(img1,img2):
#     if img1 is None or img2 is None:return False
#     if img1.shape==img2.shape:
#         grayA=cv2.cvtColor(img1.copy(),cv2.COLOR_BGR2GRAY)
#         grayB=cv2.cvtColor(img2.copy(),cv2.COLOR_BGR2GRAY)
#         difference=compare_ssim(grayA, grayB, full=True)[1]
#         thresh=cv2.threshold(difference,0,255,cv2.THRESH_BINARY_INV)[1]
#         for color in cv2.split(thresh):
#             if cv2.countNonZero(color)!=0:
#                 #print(cv2.countNonZero(color))
#                 return False
#         return True
#     else:return False

def convert_tupel_to_list(object):
    if isinstance(object,Iterable):
        object=list(object)
        for id,x in enumerate(object):
            object[id]=convert_tupel_to_list(x)
    return object
def conv_pts_to_np(pts): 
    return np.array(pts)
def conv_np_to_pts(circles):
    if type(circles)==np.ndarray:
        pts=[0,0,0,0]
        for n in range(4):
            pts[n]=[int(circles[n][0]),int(circles[n][1])]
        return pts
    else:raise "the is not numpy array "
def order_points(pts):
	xSorted = pts[np.argsort(pts[:, 0]), :]
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]
	return np.array([tl, tr, br, bl], dtype="float32")
def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped
def padimage(img,pad):
    return img[pad:img.shape[0]-pad,pad:img.shape[1]-pad]

def resizeimg(img,precent=0.1):
    return cv2.resize(img,(0,0),None,precent,precent)
def rectContains(rect,pt):
    logic = rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]
    return logic
def resizeimage_keeprespective(img, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = img.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return img

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(img, dim, interpolation = inter)

    # return the resized image
    return resized


# def Zoom(img, zoomSize):
#     img = cv2.resize(img, width=(zoomSize * img.shape[1]))
#     center = (img.shape[0]/2,img.shape[1]/2)
#     cropScale = (center[0]/zoomSize, center[1]/zoomSize)
#     img = img[cropScale[0]:(center[0] + cropScale[0]), cropScale[1]:(center[1] + cropScale[1])]
#     return img


def closest_node(node, nodes,maxdistance=999999999):
    pt = None
    dist = 9999999
    for n in nodes:
        if  distance(node,n)<maxdistance and distance(node, n) <= dist:
            dist = distance(node, n)
            pt = n
    return pt
def all_closetest_nodes(node, nodes,maxdistance=999999999):
    pt = []
    dist = 9999999
    for n in nodes:
        if  distance(node,n)<maxdistance:
            pt.append(n)
    return pt
def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)
def xywh_2_pts(box):
    return [
    [box[0],box[1]],
    [box[0]+box[2],box[1]],
    [box[0]+box[2],box[1]+box[3]],
    [box[0],box[1]+box[3]],
    ]
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
    
def organise_pts(pts):
    if len(pts)==4:
        circles=np.array(pts,np.float)
        circles=order_points(circles)
        circles=circles.astype(int)
        circles=list(circles)
        return circles
    else:raise "This must be only 4 points"
def rgb_to_hex(r, g, b):
    def clamp(x): 
        return max(0, min(x, 255))
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))
def hex_to_rgb(hexcolor:str):
    match=re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(hexcolor))
    if match:
        h = hexcolor.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    else:raise "the hex color is not correct"
def get_trasperancy_image(img,thresh):
    b, g, r = cv2.split(img)
    rgba = [b,g,r, thresh]
    dst = cv2.merge(rgba,4)
    return dst
def get_containing_boxs(all_points):
    postions=[[],[]]
    for points in all_points:
        for pt in points:
            postions[0].append(pt[0])
            postions[1].append(pt[1])
    min_x,min_y=sorted(postions[0])[0],sorted(postions[1])[0]
    max_x=sorted(postions[0],reverse=True)[0]
    max_y=sorted(postions[1],reverse=True)[0]
    return min_x,min_y,(max_x-min_x),(max_y-min_y)

def newbox(threshimg,box=None):
    #the croped_threshimage
    box=box if not box is None else [0,0,threshimg.shape[1],threshimg.shape[0]] 
    contours = cv2.findContours(threshimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
    if len(contours)!=0:
        all_points=[]
        for cnt in contours: 
            all_points.append(xywh_2_pts(cv2.boundingRect(cnt)))
        the_new_box=list(get_containing_boxs(all_points))
        the_new_box[0]+=box[0];the_new_box[1]+=box[1]
        return the_new_box
    return box
        

def get_blured_thresh(thresh):
    edges=cv2.Laplacian(thresh,cv2.CV_64F,ksize=3)
    edges=np.uint8(np.absolute(edges))
    edges2 = cv2.Canny(thresh, 100, 255)
    edges2 = cv2.dilate(edges, None)
    edges2 = cv2.erode(edges, None)
    
    sobel_x=cv2.Sobel(thresh,cv2.CV_64F,1,0)
    sobel_y=cv2.Sobel(thresh,cv2.CV_64F,0,1)
    sobel_x=np.uint8(np.absolute(sobel_x))
    sobel_y=np.uint8(np.absolute(sobel_y))
    edges3=cv2.bitwise_or(sobel_x,sobel_y)
    final_result=cv2.bitwise_or(edges,edges2)
    final_result=cv2.bitwise_or(final_result,edges3)
    
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,3))
    close = cv2.morphologyEx(final_result, cv2.MORPH_CLOSE, close_kernel, iterations=1)

    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,3))
    return cv2.dilate(close, dilate_kernel, iterations=1)

def get_rotated_box(box,theta,center=None):
    c=center if not center is None else centerbox(box)
    new_pts=[]
    for pt in xywh_2_pts(box[:4]):
        new_pts.append(get_rotated_point(c,pt,theta))
    return pts_2_xywh(new_pts)
def get_rotated_pts(pts,theta,center=None):
    c=center if not center is None else center_pts(pts)
    new_pts=[]
    for pt in pts:
        new_pts.append(get_rotated_point(c,pt,theta))
    return new_pts
def get_rotated_point(center,pt,theta):
    rotated_x = math.cos(theta) * (pt[0] - center[0]) - math.sin(theta) * (pt[1] - center[1]) + center[0]
    rotated_y = math.sin(theta) * (pt[0] - center[0]) + math.cos(theta) * (pt[1]- center[1]) + center[1]
    return [int(rotated_x),int(rotated_y)]
def pyramids(img,num:int):
    gussing_pyramid=img.copy()
    if num>0:
        for x in range(0,num):
            gussing_pyramid=cv2.pyrUp(gussing_pyramid)
    elif num<0:
        for x in range(abs(num),0,-1):
            gussing_pyramid=cv2.pyrDown(gussing_pyramid)
    return gussing_pyramid

def color_back_ground(img,mask,color:tuple):
    coloredbackground=np.zeros(img.shape,dtype="uint8")
    coloredbackground[:] = color
    return add_back_ground(img,mask,coloredbackground)
def add_back_ground(img,mask,another_img):
    mask=mask.astype(np.bool)
    img[mask]=another_img[mask]
    return img
def bluring(img,mask,radius=7):
    bluredimg=cv2.blur(img.copy(),(radius,radius))
    return add_back_ground(img,mask,bluredimg)
def isgray(img):
    if len(img.shape) < 3: return True
    if img.shape[2]  == 1: return True
    b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
    if (b==g).all() and (b==r).all(): return True
    return False
