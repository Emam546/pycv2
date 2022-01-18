import cv2 ,numpy as np
from PIL import Image
def pil2cv(src):
    img=np.array(src)
    return cv2.cvtColor(img,cv2.COLOR_RGBA2BGR)
def cv2pil(src):
    img=cv2.cvtColor(src,cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)
def __example():
    
    img=cv2.imread("G:\python\opencv\images\messi5.jpg")
    print(cv2pil(img))
if __name__=="__main__":
    __example()