import random as ran
import cv2
def rarecolor(img):
    height = img.shape[0]
    width = img.shape[1]
    colorlist=[]
    for x in range(0,width,1):
        for y in range(0,height,1):
            b,g,r = (img[y, x])
            colorlist.append((b,g,r))
    while True:
        rancolor=(ran.randrange(0,255),ran.randrange(0,255),ran.randrange(0,255))
        if rancolor not in colorlist:
            return rancolor
image=cv2.imread("image.jpg")

print(rarecolor(image))