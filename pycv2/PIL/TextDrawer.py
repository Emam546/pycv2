from PIL.ImageDraw import ImageDraw


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