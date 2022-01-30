
from PIL.ImageDraw import ImageDraw
#text size=draw.textsize(text)

class TextDrawer(ImageDraw):
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
        lines=text.splitlines()
        for i,line in enumerate(lines):
            total_width=0
            if break_:
                for letter in line:
                    width_charcter=self.textsize(letter,font, spacing, direction, features, language, stroke_width)[0]
                    if total_width+width_charcter>width:
                        total_width=width_charcter
                        new_text+="\n"
                    else:
                        total_width+=width_charcter
                    new_text+=letter
            else:
                space_width=self.textsize(" ",font, spacing, direction, features, language, stroke_width)[0]
                words=line.split(" ")
                
                for iw,word in enumerate(words):
                    width_charcter=self.textsize(word,font, spacing, direction, features, language, stroke_width)[0]
                    if total_width+width_charcter>width:
                        total_width=width_charcter
                        new_text+="\n"
                    else:
                        total_width+=width_charcter+space_width
                    new_text+=word
                    #space for next word
                    if iw!=len(words)-1:
                        new_text+=" "      
            #to ensure that he will not add a space at the end of the text
            if i!=len(lines)-1:
                new_text+="\n"
        return new_text
  
def Draw(im, mode=None):
    try:
        return im.getdraw(mode)
    except AttributeError:
        return TextDrawer(im, mode)
def __example():
    from utils import cv2pil,pil2cv
    import cv2 
    from PIL import ImageFont
    img=cv2.imread("G:\python\opencv\images\messi5.jpg")
    imgPi=cv2pil(img)
    #font=ImageFont.truetype("sans-serif.ttf",16)
    #r,g,b
    drawer=Draw(imgPi)
    ImageFont.load_default()
    #font=ImageFont.truetype(size=20)
    text="Accessing individual pixels is fairly slow. If you are looping over all of the pixels in an image, there is likely a faster way using other parts of the Pillow API."
    text=drawer.text2lines(text,200,break_=True)
    drawer.multiline_text((0,0),text,(255,255,255))

    cv2.imshow("image",pil2cv(imgPi))
    cv2.waitKey(0)
 
if __name__=="__main__":
    import os,sys
    
    sys.path.append(os.path.dirname(__file__))
    __example()