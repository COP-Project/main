import cv2
import pytesseract
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageEnhance, ImageFilter

try:
    from PIL import Image
except ImportError:
    import Image


def take_pic():
    # takes picture and saves it
    cam = cv2.VideoCapture(0)
    frame = cam.read()[1]
    name = takePicBox.get()
    if name == "":
        name = 'default'
    name = name + '.jpg'
    cv2.imwrite(filename=name, img=frame)


def read_pic():
    name = readPicBox.get()
    if name == "":
        textPicL.config(text="Invalid Picture")
        return
    try:
        im = Image.open(name)
        strimg = "Image's text is: " + pytesseract.image_to_string(im)
        textPicL.config(text=strimg)
    except FileNotFoundError:
        print("Could not find that picture, try another name")


homeWindow = Tk()
homeWindow.geometry("400x200")
homeWindow.winfo_toplevel().title("License Plate Recognition Program")

takePicBtn = ttk.Button(homeWindow, text="Take Picure")
takePicBtn.pack()
takePicBtn.config(command=take_pic)
takePic = Label(homeWindow, text="Type the new picture's name here, no extension please")
takePic.config(font=("TkDefaultFont", 12))
takePic.pack()
takePicBox = Entry(homeWindow)
takePicBox.pack()

readPicBtn = ttk.Button(homeWindow, text="Read Picure")
readPicBtn.pack()
readPicBtn.config(command=read_pic)
readPic = Label(homeWindow, text="Type a picture name here to be read")
readPic.config(font=("TkDefaultFont", 12))
readPic.pack()
readPicBox = Entry(homeWindow)
readPicBox.pack()
textPicL = Label(homeWindow, text="-text-", font=("TkDefaultFont", 12))
textPicL.pack()

homeWindow.mainloop()


def main():
    print("Goodbye")
  

if __name__ == '__main__':
    main()
