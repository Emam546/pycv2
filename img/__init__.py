
import cv2,numpy as np
from imutils import contours
from pycv2.img.utils import *
from pycv2.img.roate_img import *
from pycv2.img.roate_img import *
COLORS = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))
def get_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)
    return cnts 
counter=0

def get_contours_boxs(image,cnts,minarea=1000,draw=False):
        c=None;i=None;bigarea=0
        for (i_small, c_small) in enumerate(cnts):
            if cv2.contourArea(c_small) > minarea and bigarea<cv2.contourArea(c_small):
                bigarea=cv2.contourArea(c_small)
                c=c_small;i=i=i_small
                
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        rect = order_points(box)
        if draw:
            cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
            for ((x, y), color) in zip(rect, COLORS):
                cv2.circle(image, (int(x), int(y)), 5, color, -1)

            cv2.putText(image, "Object #{}".format(i + 1),
                (int(rect[0][0] - 15), int(rect[0][1] - 15)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
        return image,box
def get_all_contours_boxs(image,cnts,minarea=1000,draw=False):
        boxs=[]
        for (i, c) in enumerate(cnts):
            if cv2.contourArea(c) < minarea:
                continue
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            rect = order_points(box)
            boxs.append(box)
            if draw:
                cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
                for ((x, y), color) in zip(rect, COLORS):
                    cv2.circle(image, (int(x), int(y)), 5, color, -1)

                cv2.putText(image, "Object #{}".format(i + 1),
                    (int(rect[0][0] - 15), int(rect[0][1] - 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
        return image,boxs
def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src

    
