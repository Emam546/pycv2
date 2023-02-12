import cv2 ,numpy as np
from PIL import Image
def pil2cv(src):
    img=np.array(src)
    return cv2.cvtColor(img,cv2.COLOR_RGBA2BGR)
def cv2pil(src):
    img=cv2.cvtColor(src,cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)
