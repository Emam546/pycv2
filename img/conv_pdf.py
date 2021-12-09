from pdf2image import convert_from_path
import os,cv2,numpy as np
#file_path = os.path.realpath(__file__)
file_path=os.path.dirname(__file__)
popplerpath=file_path+"\\poppler-0.68.0\\bin"
def savePdf2Img(path,when=0,to=100000000):
    # print(file_path)
    # print (os.path.abspath(__file__))
    images = convert_from_path(path,poppler_path=popplerpath)
    for id,img in enumerate(images):
        if id>=when and id<=to:
            cv2.imshow("",img)
            cv2.waitKey(0)
            img.save(str(id) +'.jpg', 'JPEG')
def convert_pdf_to_image(path,frist,last,dpi=200):
    images = []
    images.extend(
                    list(
                        map(
                            lambda image: cv2.cvtColor(
                                np.asarray(image), code=cv2.COLOR_RGB2BGR
                            ),
                            convert_from_path(path, dpi=dpi,poppler_path=popplerpath,first_page=frist,last_page=last),
                        )
                    )
                )
    return images

