import cv2
def draw_text(img,text:str,org, fontFace, fontScale,color, thickness):
    x,y=org
    for line in text.splitlines():
        cv2.putText(img,line,(x,y),fontFace, fontScale,color, thickness)
        (_,h),base_line=cv2.getTextSize(line,fontFace, fontScale, thickness)
        y+=base_line+h
def text_size(text:str,fontFace, fontScale, thickness):
    current_width=0
    currentheight=0
    for line in text.splitlines():
        (w,h),base_line=cv2.getTextSize(line,fontFace=fontFace,fontScale=fontScale,thickness=thickness)
        current_width=w if w>current_width else current_width
        currentheight+=(h+base_line)
    return current_width,currentheight
def text2lines(text:str,width,
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,thickness=1,
    size_charcter=(None,None),
    break_=False,):
        new_text=""
        for line in text.splitlines():
            total_width=0
            if break_:
                for letter in line:
                    width_charcter=size_charcter[0] if size_charcter!=(None,None) else cv2.getTextSize(letter,fontFace=fontFace,fontScale=fontScale,thickness=thickness)[0][0]
                    if total_width+width_charcter>width:
                        total_width=width_charcter
                        new_text+="\n"
                    else:
                        total_width+=width_charcter
                    new_text+=letter
                new_text+="\n"
            else:
                space_width=size_charcter[0] if size_charcter!=(None,None) else cv2.getTextSize(" ",fontFace=fontFace,fontScale=fontScale,thickness=thickness)[0][0]
                for word in line.split(" "):

                    width_charcter=size_charcter[0] if size_charcter!=(None,None) else cv2.getTextSize(word,fontFace=fontFace,fontScale=fontScale,thickness=thickness)[0][0]

                    if total_width+width_charcter>width:
                        total_width=width_charcter
                        new_text+="\n"
                    else:
                        total_width+=width_charcter+space_width
                    #space for next word
                    new_text+=word+" "
            new_text+="\n"
        return new_text
