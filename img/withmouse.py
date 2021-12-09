import cv2,numpy as np,pycv2.img.utils as utils
import pycv2.img.imgprocess as imgprocess
import pykeyboard as key
from pycv2.img.utils import resizeimage_keeprespective,all_closetest_nodes,closest_node,distance,four_point_transform, resizeimg

colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
grabing,drawing,ease,holding=False,False,False,False
counter=0
def crop_img_with_mouse(img,showcrosshair=False):
    roi=(0,0,0,0)
    while roi==(0,0,0,0):
        roi=cv2.selectROI("crop img with mouse",img,showCrosshair=showcrosshair,)
        cv2.destroyWindow("crop img with mouse")
        roi =int(roi[0]),int(roi[1]),int(roi[2]),int(roi[3])
    return img[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])],roi

def box_with_mouse(img):
    global counter
    circles=np.zeros((4,2),np.int)
    counter=0
    print("click to start a point")
    def mousepoints(event,x,y,flags,arguments,maxdistance=20):
        global counter
        if event ==cv2.EVENT_LBUTTONDOWN:
            for n in range(4):
                if np.array_equal(circles[n],[0,0]):
                        circles[n]=int(x),int(y);break
            counter+=1
        elif event==cv2.EVENT_RBUTTONDOWN:
            close=closest_node([x,y],circles,maxdistance=maxdistance)
            for x in range(4):
                if np.array_equal(circles[x],[0,0]):continue
                if np.array_equal(circles[x],close):
                    circles[x]=[0,0];print("Delet")
                    counter-=1    
    while True:
        if counter>=4:
            if key.pressedkey(0x0D):break
        else:key.check_key_pressed(0x0D)
        scondimg=img.copy()
        for x in range(4):
            if np.array_equal(circles[x],[0,0]):continue
            color=max(counter,len(colors))
            if np.array_equal(circles[x-1],[0,0])==False:
                cv2.line(scondimg,circles[x],circles[x-1],(0,255,0),1)
            cv2.circle(scondimg,circles[x],2,colors[x],3,cv2.FILLED)
            
        cv2.imshow("crop image mouse",scondimg)
        cv2.setMouseCallback("crop image mouse",mousepoints)
        cv2.waitKey(1)
    cv2.destroyWindow("crop image mouse")
    circles=utils.order_points(circles)
    return circles
def edit_box_With_mouse(org_img,circles):
    circles=utils.order_points(circles)
    def mousepoints(event,x,y,flags,arguments,maxdistance=20):
        global grabing
        if event == cv2.EVENT_LBUTTONDOWN:grabing=True
        elif event == cv2.EVENT_LBUTTONUP:grabing=False
        elif grabing and event ==cv2.EVENT_MOUSEMOVE:
            closestnode=closest_node([x,y],circles,30)
            for z in range(4):
                if np.array_equal(circles[z],closestnode):
                    circles[z]=[int(x),int(y)] 
    while True:
        scondimg=org_img.copy()
        #circles=utils.order_points(circles)
        if key.pressedkey(0x0D):break
        for x in range(4):
            cx,cy=int(circles[x][0]),int(circles[x][1])
            if x-1 in range(4):
                cx1,cy1=int(circles[x-1][0]),int(circles[x-1][1])
                cv2.line(scondimg,(cx,cy),(cx1,cy1),(0,255,0),1)
            cv2.circle(scondimg,(cx,cy),2,colors[x],3,cv2.FILLED)
        cv2.imshow("result",resizeimg(four_point_transform(org_img.copy(),circles),1.5))
        cv2.imshow("crop image mouse",scondimg)
        cv2.setMouseCallback("crop image mouse",mousepoints)
        cv2.waitKey(1)
    for id,x in enumerate(circles):
            circles[id]=int(x[0]),int(x[1])
    cv2.destroyAllWindows()
    return circles   
        
def __removeimage(cloneMask,drawingimg,circles,radius):
    white = (255, 255, 255)
    for x in circles:
        cv2.circle(cloneMask,x,radius,white,cv2.FILLED)
    cloneMask=imgprocess.get_grayscale(cloneMask)
    cloneMask=imgprocess.thresholding(cloneMask)
    return cv2.inpaint(drawingimg, cloneMask, 2, cv2.INPAINT_TELEA)
def inpainting_with_mouse(img,radius=20):
    circles=[];global drawing,ease;ease=False;drawing=False
    radius=20
    window_name="remove image mouse"
    cv2.namedWindow(window_name)
    cv2.createTrackbar("trackbar_value", window_name , radius, 100,pass_function)
    def mousepoints(event,x,y,_,__):
        global drawing,ease
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing=True;ease=False
            if  (x,y) not in circles:
                circles.append((x,y))
        elif event==cv2.EVENT_RBUTTONDOWN:
            ease=True;drawing=False
            close=all_closetest_nodes([x,y],circles,maxdistance=20)
            for x in close:
                circles.pop(circles.index(x))
        elif event == cv2.EVENT_LBUTTONUP:
            drawing=False;ease=False
        elif event==cv2.EVENT_RBUTTONUP:
            drawing=False;ease=False
        elif drawing and event ==cv2.EVENT_MOUSEMOVE:
            if  (x,y) not in circles:
                circles.append((x,y))
        if ease and event ==cv2.EVENT_MOUSEMOVE:
                close=all_closetest_nodes([x,y],circles,maxdistance=20)
                for x in close:
                    circles.pop(circles.index(x))

        
    mask = np.zeros(img.shape, dtype=np.uint8)
    timer=0
    while True:
        if timer>=10 and key.pressedkey(key.findmostsimilarkey("Enter")):break
        if timer<=10:timer+=1
        radius = cv2.getTrackbarPos("trackbar_value", window_name)
        resultimg=__removeimage(mask.copy(),img.copy(),circles,radius)
        cv2.imshow("remove image mouse",resultimg)
        cv2.setMouseCallback("remove image mouse",mousepoints)
        cv2.waitKey(1)
    cv2.destroyWindow("remove image mouse")
    
    resultimg=__removeimage(mask.copy(),img.copy(),circles,radius)
    for x in circles:
        cv2.circle(mask,x,radius,(255, 255, 255),cv2.FILLED)
    return resultimg,mask

def pass_function(val):pass
def makecircles(img,radius=20,color=(255,255,0)):
    circles=[]
    def mousepoints(event,x,y,_,__):
        global drawing,ease
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing=True;ease=False
            if  (x,y) not in circles:
                circles.append((x,y))
        elif event==cv2.EVENT_RBUTTONDOWN:
            ease=True;drawing=False
            close=all_closetest_nodes([x,y],circles,maxdistance=20)
            for x in close:
                circles.pop(circles.index(x))
        elif event == cv2.EVENT_LBUTTONUP:
            drawing=False;ease=False
        elif event==cv2.EVENT_RBUTTONUP:
            drawing=False;ease=False
        elif drawing and event ==cv2.EVENT_MOUSEMOVE:
            if  (x,y) not in circles:
                circles.append((x,y))
        if ease and event ==cv2.EVENT_MOUSEMOVE:
                close=all_closetest_nodes([x,y],circles,maxdistance=20)
                for x in close:
                    circles.pop(circles.index(x))
    imagecopy=img.copy()
    while True:
        if len(circles)>=1 and key.pressedkey(key.findmostsimilarkey("Enter")):break
        for x in circles:
            cv2.circle(imagecopy,x,radius,color,cv2.FILLED)
        cv2.imshow("circles image mouse",imagecopy)
        cv2.setMouseCallback("circles image mouse",mousepoints)
    return circles

def cut_edges_withmouse(img):
    global grabing;grabing=False
    h,w,_=img.shape
    pts=[[0,0],[w,0],[0,h],[w,h]]
    xsame=((0,2),(1,3))
    ysame=[(0,1),(2,3)]
    def mousepoints(event,x,y,_,__):
        global grabing
        if event == cv2.EVENT_LBUTTONDOWN:
            grabing=True;
        elif event == cv2.EVENT_LBUTTONUP:
            grabing=False
        elif grabing and event ==cv2.EVENT_MOUSEMOVE:
            closestnode=closest_node([x,y],pts,30)
            if closestnode!=None:
                for id,same in enumerate([xsame,ysame]):
                    for groub in same:
                        if  pts.index(closestnode) in groub:
                            for cor in groub:
                                pts[cor][id]=[x,y][id]
                                #print("value",pts[cor][id])
    timer=0;rect=[0,1,3,2]
    while True:
        if timer>=10 and key.pressedkey(key.findmostsimilarkey("Enter")):break
        if timer<=10:timer+=1
        resultimg=img.copy()
        for id,x in enumerate(rect):
            if id<3:
                cv2.line(resultimg,pts[rect[id]],pts[rect[id+1]],(255,255,0),7)
            if id==0:
                cv2.line(resultimg,pts[rect[id]],pts[rect[3]],(255,255,0),7)
            cv2.circle(resultimg,pts[id],10,(0,0,255),cv2.FILLED)
        cv2.imshow("remove image mouse",resultimg)
        cv2.setMouseCallback("remove image mouse",mousepoints)
        cv2.waitKey(1)
    cv2.destroyWindow("remove image mouse")
    return img[pts[0][1]:pts[2][1],pts[0][0]:pts[1][0]]

def add_image_another(org_img,s_img,x=0,y=0):
    global grabing,holding;grabing,holding=False,False
    bh,bw,_=org_img.shape
    sh,sw,_=s_img.shape
    test_img=s_img.copy()
    if sh>bh:test_img=resizeimage_keeprespective(test_img,height=bh)
    if sw>bw:test_img=resizeimage_keeprespective(test_img,width=bw)
    pts=[[x,y],[sw+x,y],[x,sh+y],[sw+x,sh+y]]
    def mousepoints(event,x,y,_,__):
        global grabing,holding;
        if event == cv2.EVENT_LBUTTONDOWN:
            grabing=True;
        elif event == cv2.EVENT_LBUTTONUP:
            grabing=False;holding=False
        elif grabing and event ==cv2.EVENT_MOUSEMOVE:
            cx,cy=int(pts[0][0]+(sw/2)),int(pts[0][1]+(sh/2))
            if holding or distance([x,y],[cx,cy])<=30:
                holding=True
                nx,ny=int(abs(x-sw/2)),int(abs(y-sh/2))
                pts[0],pts[1],pts[2],pts[3]=[nx,ny],[sw+nx,ny],[nx,sh+ny],[sw+nx,sh+ny]

    timer=0;rect=[0,1,3,2]
    finalimage=org_img.copy()
    while True:
        if timer>=10 and key.pressedkey(key.findmostsimilarkey("Enter")):break
        if timer<=10:timer+=1
        resultimg=org_img.copy()
        nx,ny=pts[0][0],pts[0][1]
        resultimg[ny:ny+test_img.shape[0], nx:nx+test_img.shape[1]] = test_img
        finalimage=resultimg.copy()
        viewingimg=resultimg.copy()
        for id,x in enumerate(rect):
            if id<3:cv2.line(viewingimg,pts[rect[id]],pts[rect[id+1]],(255,255,0),7)
            if id==0:cv2.line(viewingimg,pts[rect[id]],pts[rect[3]],(255,255,0),7)
            cv2.circle(viewingimg,pts[id],10,(0,0,255),cv2.FILLED)
        
        cx,cy=int(pts[0][0]+(sw/2)),int(pts[0][1]+(sh/2))
        cv2.circle(viewingimg,(cx,cy),15,(0,255,0),cv2.FILLED)
        
        cv2.imshow("add image mouse",viewingimg)
        cv2.setMouseCallback("add image mouse",mousepoints)
        cv2.waitKey(1)
    try:cv2.destroyWindow("add image mouse")
    except:pass
    return finalimage



    
