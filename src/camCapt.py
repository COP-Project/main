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
        strimg = "Image's text is: " + pytesseract.image_to_string(im)
        print(strimg)
        textPicL.config(text=strimg)
    except FileNotFoundError:
        print("Could not find that picture, try another name")
        
homeWindow = Tk()
homeWindow.geometry("300x200")
homeWindow.winfo_toplevel().title("License Plate Recognition Program")

takePicBtn = ttk.Button(homeWindow, text="Take Picure")
takePicBtn.pack()
takePicBtn.config(command=takePic)
takePic = Label(homeWindow, text="Type picture name here")
takePic.pack()
takePicBox = Entry(homeWindow)
takePicBox.pack()

readPicBtn = ttk.Button(homeWindow, text="Read Picure")
readPicBtn.pack()
readPicBtn.config(command=readPic)
readPic = Label(homeWindow, text="Type picture name here")
readPic.pack()
readPicBox = Entry(homeWindow)
readPicBox.pack()
textPicL = Label(homeWindow, text="-text-")
textPicL.pack()

homeWindow.mainloop()

def main():
    print ("Goodbye")
    
  

if __name__ == '__main__':
    main()
