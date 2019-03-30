import tkinter as tk
from tkinter import *

import PIL.Image
import PIL.ImageTk
from StandardValues import *
from dbInterface import *

# mySql connection, currently set to my local pc
# add login --OFF THIS IS IN AN IMPORT
# conn=pymysql.connect(host='127.0.0.1',port=3312,user='root',passwd='0485',db='poopproject')
# cursor = conn.cursor()

root = tk.Tk()
root.withdraw()  # won't need this

# Prompt user to login
login_scrn = Login()
login_scrn.create_window()

# Create interface to interact with database, handles connection
db_interface = DbInterface(login_scrn.username, login_scrn.password)

# this sets our current log info
# calls from out dbCommands which has access to our dbUsers information
# consists of a list of 4 fields 0 fname, 1 lname, 2 login name, 3 ADMIN or NON ADMIN
user = db_interface.getUser()
passport = user.passport

# set main window
mainWindow = Toplevel()
mainWindow.configure(background=StandardValues.background)

# SET GUI FRAMES
top = Frame(mainWindow)
bottom = Frame(mainWindow)
bottom.configure(background="black")
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

# Welcome label
welcomLabel = Label(mainWindow, bg="white",
                    text="Welcome " + passport.firstName + " you are logged in under " + passport.loginName + " as " +
                         passport.access)
welcomLabel.pack()

# ADD bANNER PICTURE
path = "img/carpic.png"
img = PIL.ImageTk.PhotoImage(PIL.Image.open(path))
panel = tk.Label(mainWindow, image=img)
panel.pack(in_=top, expand="no")

# set user type
userType = DISABLED
if passport.access == "ADMIN":
    userType = NORMAL

# set main window properties
mainWindow.geometry("830x350")
mainWindow.winfo_toplevel().title("License Recognition Program")
# displayLogin()
# create all buttons

addDriverBtn = Button(mainWindow,
                      bg=StandardValues.btn_bk_clr,
                      fg=StandardValues.btn_text_clr,
                      text="Add New Driver",
                      command=lambda: db_interface.callAddDrivers())

searchDriverBtn = Button(mainWindow,
                         bg=StandardValues.btn_bk_clr,
                         fg=StandardValues.btn_text_clr,
                         text="Search By Full Name",
                         command=lambda: db_interface.searchLastNameIntScreen())

searchZipBtn = Button(mainWindow,
                      bg=StandardValues.btn_bk_clr,
                      fg=StandardValues.btn_text_clr,
                      text="Search By Zip",
                      command=lambda: db_interface.searchZipPlateInpScreen("zip"))

searchPlateBtn = Button(mainWindow,
                        bg=StandardValues.btn_bk_clr,
                        fg=StandardValues.btn_text_clr,
                        text="Search By Plate Number",
                        command=lambda: db_interface.searchZipPlateInpScreen("plate"))

deleteBtn = Button(mainWindow,
                   bg=StandardValues.btn_bk_clr,
                   fg=StandardValues.btn_text_clr,
                   state=userType,
                   text="Delete Driver",
                   command=lambda: [db_interface.delDriverScreen()])

editBtn = Button(mainWindow,
                 bg=StandardValues.btn_bk_clr,
                 fg=StandardValues.btn_text_clr,
                 text="Edit Driver",
                 command=lambda: [db_interface.editDriverSearch()])  # implement

scanPlateBtn = Button(mainWindow,
                      bg=StandardValues.btn_bk_clr,
                      fg=StandardValues.btn_text_clr,
                      text="Scan Plate",
                      command=lambda: [print("implement")])  # implement

logOutBtn = Button(mainWindow,
                   bg=StandardValues.btn_bk_clr,
                   fg=StandardValues.btn_text_clr,
                   text="Log Out",
                   command=lambda: [db_interface.logOutScreen()])

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
