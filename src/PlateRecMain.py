import pymysql.cursors
from tkinter import *
from tkinter import ttk
import tkinter as tk
#from dbCommands import *
from dbInterface import *
from PIL import ImageTk, Image

#mySql connection, currently set to my local pc
#add login --OFF THIS IS IN AN IMPORT
#conn=pymysql.connect(host='127.0.0.1',port=3312,user='root',passwd='0485',db='poopproject')
#cursor = conn.cursor()



###set main window
mainWindow = Tk()
mainWindow.configure(background="white")

#SET FRAMES
top=Frame(mainWindow)
bottom=Frame(mainWindow)
bottom.configure(background="black")
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

####ADD bANNER PICTURE
path = "carpic.png"
img=ImageTk.PhotoImage(Image.open(path))
panel=tk.Label(mainWindow,image = img)
panel.pack(in_=top, expand="no")

#set main window properties
mainWindow.geometry("830x400")
mainWindow.winfo_toplevel().title("License Recognition Program")

#create all buttons
addDriverBtn = Button(mainWindow,bg="black",fg="white", text="Add New Driver",command=lambda : callAddDrivers())
searchDriverBtn = Button(mainWindow,bg="white", text="Search By Full Name",command= lambda:  searchLastNameIntScreen())
searchZipBtn = Button(mainWindow,bg="white", text="Search By Zip",command= lambda:  searchZipPlateInpScreen("zip"))
searchPlateBtn = Button(mainWindow,bg="white", text="Search By Plate Number",command= lambda:  searchZipPlateInpScreen("plate"))
deleteBtn = Button(mainWindow,bg="white", text="Delete Driver",command= lambda:  [delDriverScreen()])
editBtn = Button(mainWindow,bg="white", text="Edit Driver",command= lambda:[print("implement")])#implement
scanPlateBtn = Button(mainWindow,bg="white", text="Scan Plate",command= lambda:[print("implement")])#implement
logOutBtn = Button(mainWindow,bg="white", text="Log Out",command= lambda:[print("implement")])#implement

#set padding x
padx=15

#Set driver
addDriverBtn.pack()

#Adds line seperator
seperator = Frame(height=2, bd=1, relief=SUNKEN)
seperator.pack(fill=X,padx=50,pady=50)

#set bottom part buttons
searchDriverBtn.pack(in_=bottom,side=LEFT,padx=padx)
searchZipBtn.pack(in_=bottom,side=LEFT,padx=padx)
searchPlateBtn.pack(in_=bottom,side=LEFT,padx=padx)
deleteBtn.pack(in_=bottom,side=LEFT,padx=padx)
editBtn.pack(in_=bottom,side=LEFT,padx=padx)
scanPlateBtn.pack(in_=bottom,side=LEFT,padx=padx)
logOutBtn.pack(in_=bottom,side=LEFT,padx=padx)


def main():
    print("Hello")
    
    
if __name__ == '__main__':
   main()
