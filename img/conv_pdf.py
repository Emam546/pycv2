from pathlib import PurePath
from pdf2image import convert_from_path
import os,cv2,numpy as np

file_path=os.path.dirname(__file__)
popplerpath=os.path.join(file_path,"\\poppler-0.68.0\\bin")
def savePdf2Img(path,when=0,to=float("inf")):
    images = convert_from_path(path,poppler_path=popplerpath)
    for i,img in enumerate(images):
        if i>=when and i<=to:
            img.save(str(i) +'.jpg', 'JPEG')
def convert_pdf_to_image(path:str | PurePath,first:int,last:int,dpi=200):
    images = []
    images.extend(
                    list(
                        map(
                            lambda image: cv2.cvtColor(
                                np.asarray(image), code=cv2.COLOR_RGB2BGR
                            ),
                            convert_from_path(path, dpi=dpi,poppler_path=popplerpath,first_page=first,last_page=last),
                        )
                    )
                )
    return images

