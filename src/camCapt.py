import cv2
import pytesseract
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageEnhance, ImageFilter

try:
    from PIL import Image
except ImportError:
    import Image

def takePic():
    #takes picture and saves it
    cam = cv2.VideoCapture(0)
    frame = cam.read()[1]
    name = takePicBox.get()
    if(name == ""):
        name = 'default'
    name = name + '.jpg'
    cv2.imwrite(filename=name, img=frame)

def readPic():
    name = readPicBox.get()
    if(name == ""):
        print("Invalid Picture")
    try:
        im = Image.open(name)
        strimg = pytesseract.image_to_string(im)
        print("Image's text is: " + strimg)
    except FileNotFoundError:
        print("Could not find that picture, try another name")
        
homeWindow = Tk()
homeWindow.geometry("300x200")

takePicBtn = ttk.Button(homeWindow, text="Take Picure")
takePicBtn.pack()
takePicBtn.config(command=takePic)
takePicBox = Entry(homeWindow)
takePicBox.pack()

readPicBtn = ttk.Button(homeWindow, text="Read Picure")
readPicBtn.pack()
readPicBtn.config(command=readPic)
readPicBox = Entry(homeWindow)
readPicBox.pack()

homeWindow.mainloop()

def main():
    #takes text from specified image
    im = Image.open('book.JPG')
    strimg = pytesseract.image_to_string(im)
    print(strimg)
    
  

if __name__ == '__main__':
    main()
