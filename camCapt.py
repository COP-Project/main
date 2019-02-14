import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

try:
    from PIL import Image
except ImportError:
    import Image


def main():
    #takes picture and saves it
    #cam = cv2.VideoCapture(0)
    #frame = cam.read()[1]
    #cv2.imwrite(filename='img0.jpg', img=frame)
  
    #takes text from specified image
    im = Image.open('text.png')
    strimg = pytesseract.image_to_string(im)
    print(strimg)
  

if __name__ == '__main__':
    main()