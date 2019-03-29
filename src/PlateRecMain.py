import pymysql.cursors
from tkinter import *
from tkinter import ttk
import tkinter as tk
from dbInterface import *
from dbCommands import *
from PIL import ImageTk, Image

# mySql connection, currently set to my local pc
# add login --OFF THIS IS IN AN IMPORT
# conn=pymysql.connect(host='127.0.0.1',port=3312,user='root',passwd='0485',db='poopproject')
# cursor = conn.cursor()

root = tk.Tk()
root.withdraw()  # won't need this

# this sets our current log info
# calls from out dbCommands which has access to our dbUsers information
# consists of a list of 4 fields 0 fname, 1 lname, 2 login name, 3 ADMIN or NON ADMIN
userInfoList = getUserInfo()

###set main window
mainWindow = Toplevel()
mainWindow.configure(background="white")

# SET GUI FRAMES
top = Frame(mainWindow)
bottom = Frame(mainWindow)
bottom.configure(background="black")
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

# Welcome label
welcomLabel = Label(mainWindow, bg="white",
                    text="Welcome " + userInfoList[0] + " you are logged in under " + userInfoList[2] + " as " +
                         userInfoList[3])
welcomLabel.pack()

####ADD bANNER PICTURE
path = "carpic.png"
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(mainWindow, image=img)
panel.pack(in_=top, expand="no")

# set user type
userType = DISABLED
if userInfoList[3] == "ADMIN":
    userType = NORMAL

# set main window properties
mainWindow.geometry("830x350")
mainWindow.winfo_toplevel().title("License Recognition Program")
# displayLogin()
# create all buttons

addDriverBtn = Button(mainWindow, bg="black", fg="white", text="Add New Driver", command=lambda: callAddDrivers())
searchDriverBtn = Button(mainWindow, bg="white", text="Search By Full Name", command=lambda: searchLastNameIntScreen())
searchZipBtn = Button(mainWindow, bg="white", text="Search By Zip", command=lambda: searchZipPlateInpScreen("zip"))
searchPlateBtn = Button(mainWindow, bg="white", text="Search By Plate Number",
                        command=lambda: searchZipPlateInpScreen("plate"))
deleteBtn = Button(mainWindow, bg="white", state=userType, text="Delete Driver", command=lambda: [delDriverScreen()])
editBtn = Button(mainWindow, bg="white", text="Edit Driver", command=lambda: [editDriverScreen()])  # implement
scanPlateBtn = Button(mainWindow, bg="white", text="Scan Plate", command=lambda: [print("implement")])  # implement
logOutBtn = Button(mainWindow, bg="white", text="Log Out", command=lambda: [logOut(), mainWindow.destroy()])

# set padding x
padx = 15

# Set driver
addDriverBtn.pack()

# Adds line seperator
seperator = Frame(height=2, bd=1, relief=SUNKEN)
seperator.pack(fill=X, padx=50, pady=50)

# set bottom part buttons
searchDriverBtn.pack(in_=bottom, side=LEFT, padx=padx)
searchZipBtn.pack(in_=bottom, side=LEFT, padx=padx)
searchPlateBtn.pack(in_=bottom, side=LEFT, padx=padx)
deleteBtn.pack(in_=bottom, side=LEFT, padx=padx)
editBtn.pack(in_=bottom, side=LEFT, padx=padx)
scanPlateBtn.pack(in_=bottom, side=LEFT, padx=padx)
logOutBtn.pack(in_=bottom, side=LEFT, padx=padx)


def main():
    print("Hello")


if __name__ == '__main__':
    main()