import cv2 ,numpy as np
from PIL import Image,ImageFont,ImageDraw
from PIL.ImageDraw import ImageDraw
#text size=draw.textsize(text)
from typing import Any, Sequence, Union, overload

class Drawer(ImageDraw):
    def text2lines(self,
        text:str,
        width=9999999,
        font=None,
        spacing=4,
        direction=None,
        features=None,
        language=None,
        stroke_width=0,break_=False):
        new_text=""
        for line in text.splitlines():
            total_width=0
            if break_:
                for letter in line:
                    width_charcter=self.textsize(letter,font, spacing, direction, features, language, stroke_width)
                    if total_width+width_charcter>width:
                        total_width=width_charcter
                        new_text+="\n"
                    else:
                        total_width+=width_charcter
                    new_text+=letter
                new_text+="\n"
            else:
                space_width=self.textsize("A",font, spacing, direction, features, language, stroke_width)
                for word in line.split(" "):
                    width_charcter=self.textsize(word,font, spacing, direction, features, language, stroke_width)
                    if total_width+width_charcter>width:
                        total_width=width_charcter
                        new_text+="\n"
                    else:
                        total_width+=width_charcter+space_width
                    #space for next word
                    new_text+=word+" "
            new_text+="\n"
        return new_text
def __example():
    from utils import cv2pil,pil2cv
    img=cv2.imread("G:\python\opencv\images\messi5.jpg")
    imgPi=cv2pil(img)
    #font=ImageFont.truetype("sans-serif.ttf",16)
    #r,g,b
    drawer=ImageDraw.Draw(imgPi)
    #font=ImageFont.truetype(size=20)
    text="Simple text"
    drawer.text((0,0),text,(255,255,255),language="ar")
    cv2.imshow("image",pil2cv(imgPi))
    cv2.waitKey(0)
 
if __name__=="__main__":
    import os,sys
    
    sys.path.append(os.path.dirname(__file__))
    __example()