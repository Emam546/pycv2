import pytesseract,cv2,numpy as np
from pytesseract import Output 
file="H:\progrem file\Tesseract-Ocr\\tesseract.exe"

def read_text(mask):
    d=get_img_infromations(mask)
    dic=[]
    for i in range(len(d['text'])):
        small_dic={}
        for x in d:
            small_dic[x]=d[x][i]
        dic.append(small_dic)
    text=""
    lasline=1
    for val in dic:
        if val["conf"]>60:
            if int(val["lin_num"])>lasline:
                lasline=int(val["lin_num"])
                text+="\n"
            text+=val["text"]+" "          
    return text
def get_img_infromations(img):
    pytesseract.pytesseract.tesseract_cmd=file
    return  pytesseract.image_to_data(img,output_type=Output.DICT)
def get_img_boxes(img):
    pytesseract.pytesseract.tesseract_cmd=file
    h_img=img.shape[0]
    d=pytesseract.image_to_boxes(img,output_type=Output.DICT)
    boxes=[]
    n_boxes = len(d['char'])
    for i in range(n_boxes):
        (text,x1,y2,x2,y1) = (d['char'][i],d['left'][i],d['top'][i],d['right'][i],d['bottom'][i])
        text=text
        x,y=int(x1),int(h_img-int(y2))
        w,h=int(int(x2)-x),int(h_img-int(y1)-y)
        boxes.append((text,(x,y,w,h)))
    return boxes
def get_img_string(img):
    pytesseract.pytesseract.tesseract_cmd=file
    return pytesseract.image_to_string(img,lang="auto")
def get_text_mask(img):
        mask=np.zeros(img.shape[:2], dtype=np.uint8)
        dic=[]
        d=get_img_boxes(img)
        for _,box in d:
            small_dic={"conf":100}
            small_dic["box"]=box
            dic.append(small_dic)
        wide=3
        for val in dic:
            if int(val["conf"])>60:
                x,y,w,h=val["box"]
                x,y,w,h=max(0,x-wide),max(0,y-wide),min(mask.shape[1],w+wide),min(mask.shape[0],h+wide)
                gray = cv2.cvtColor(img[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 0, 255)
                mask[y:y+h,x:x+w]=edges
        mask = cv2.dilate(mask, None,iterations=2)
        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        for contour in contours:
            cv2.fillConvexPoly(mask, contour, (255))
        mask=cv2.erode(mask, None,iterations=2)
        return mask



# from langdetect import detect_langs
# #detect_langs(txt)
# #[en:0.714282468983554, es:0.2857145605644145]




if __name__=="__main__":
    img=cv2.imread("D:\Projects\small projects\images\Backegroundpng.png")
    mask=get_text_mask(img)
    cv2.imshow("image",mask)
    cv2.waitKey(0)







