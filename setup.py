from setuptools import setup, find_packages
VERSION = '0.0.1'
DESCRIPTION = 'Just a package i used in many projects to get which key pressed from keyboard'
LONG_DESCRIPTION = 'Just a package i used in many projects to get which key pressed from keyboard'

# Setting up
setup(
    name="pykeyboard-input",
    version=VERSION,
    author="Emam_ahsour",
    author_email="emam54637@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["opencv-python","numpy","mediapipe","Pillow","scipy","imutils","pdf2image","pytesseract"],
    keywords=['python', 'cv2-utils', 'tools', 'pycv2', 'cv2-functions',"cv2-most-used functions"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
