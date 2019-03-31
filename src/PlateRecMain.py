import tkinter as tk
from tkinter import *

import PIL.Image
import PIL.ImageTk
from StandardValues import *
from dbInterface import *

from login import Login


class App:
    def __init__(self):
        self.main_window = None

        self.user = None
        self.passport = None

        self.db_interface = None
        self.login = None

        # Request login credentials from user
        self.login_user()

        # if login credentials accepted, create main application
        self.create_main()

    def login_user(self):
        self.login = Login()
        self.login.create_window()

        self.db_interface = DbInterface(self.login.username, self.login.password)

        self.user = self.db_interface.getUser()
        self.passport = self.user.passport

    def create_main(self):
        root = tk.Tk()
        root.withdraw()

        self.main_window = Toplevel()
        self.main_window.configure(background=StandardValues.background)

        # SET GUI FRAMES
        top_frame = Frame(self.main_window)
        bottom_frame = Frame(self.main_window)
        bottom_frame.configure(background="black")
        top_frame.pack(side=TOP)
        bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        bottom_frame_left = Frame(bottom_frame)
        bottom_frame_right = Frame(bottom_frame)

        bottom_frame_left.configure(background="black")
        bottom_frame_right.configure(background="black")

        bottom_frame_left.pack(side=LEFT, fill=BOTH, expand=True)
        bottom_frame_right.pack(side=RIGHT, fill=BOTH, expand=True)

        # Welcome label
        welcome_lbl = Label(top_frame, bg="white",
                            text="Welcome " + self.passport.firstName + "\nYou are logged in under " + self.passport.loginName + " as " +
                                 self.passport.access)
        welcome_lbl.pack(side=BOTTOM, padx=10, pady=10)

        # ADD bANNER PICTURE
        path = "img/carpic.png"
        img = PIL.ImageTk.PhotoImage(PIL.Image.open(path))
        panel = tk.Label(self.main_window, image=img)
        panel.pack(in_=top_frame, side=TOP, expand="no")

        # set user type
        userType = DISABLED
        if self.passport.access == "ADMIN":
            userType = NORMAL

        # set main window properties
        self.main_window.winfo_toplevel().title("License Recognition Program")
        # create all buttons

        add_driver_btn = Button(bottom_frame_left,
                                bg=StandardValues.btn_bk_clr,
                                fg=StandardValues.btn_text_clr,
                                text="Add New Driver",
                                command=lambda: self.db_interface.callAddDrivers())

        search_driver_btn = Button(bottom_frame_left,
                                   bg=StandardValues.btn_bk_clr,
                                   fg=StandardValues.btn_text_clr,
                                   text="Search By Full Name",
                                   command=lambda: self.db_interface.searchLastNameIntScreen())

        search_zip_btn = Button(bottom_frame_left,
                                bg=StandardValues.btn_bk_clr,
                                fg=StandardValues.btn_text_clr,
                                text="Search By Zip",
                                command=lambda: self.db_interface.searchZipPlateInpScreen("zip"))

        search_plate_btn = Button(bottom_frame_left,
                                  bg=StandardValues.btn_bk_clr,
                                  fg=StandardValues.btn_text_clr,
                                  text="Search By Plate Number",
                                  command=lambda: self.db_interface.searchZipPlateInpScreen("plate"))

        delete_btn = Button(bottom_frame_right,
                            bg=StandardValues.btn_bk_clr,
                            fg=StandardValues.btn_text_clr,
                            state=userType,
                            text="Delete Driver",
                            command=lambda: [self.db_interface.delDriverScreen()])

        edit_btn = Button(bottom_frame_right,
                          bg=StandardValues.btn_bk_clr,
                          fg=StandardValues.btn_text_clr,
                          text="Edit Driver",
                          command=lambda: [self.db_interface.editDriverSearch()])  # implement

        scan_plate_btn = Button(bottom_frame_right,
                                bg=StandardValues.btn_bk_clr,
                                fg=StandardValues.btn_text_clr,
                                text="Scan Plate",
                                command=lambda: [self.db_interface.scan_license_plate_screen()])  # implement

        logout_btn = Button(bottom_frame_right,
                            bg=StandardValues.btn_bk_clr,
                            fg=StandardValues.btn_text_clr,
                            text="Log Out",
                            command=lambda: [self.db_interface.logOutScreen()])

        # set padding x
        padx = 15
        pady = 15

        # Set driver
        add_driver_btn.pack()

        # Adds line seperator
        seperator = Frame(height=2, bd=1, relief=SUNKEN)
        seperator.pack(fill=X, padx=50, pady=50)

        # set bottom part buttons
        add_driver_btn.pack(side=TOP, padx=padx, pady=pady)
        search_driver_btn.pack(side=TOP, padx=padx, pady=pady)
        search_zip_btn.pack(side=TOP, padx=padx, pady=pady)
        search_plate_btn.pack(side=TOP, padx=padx, pady=pady)
        delete_btn.pack(side=TOP, padx=padx, pady=pady)
        edit_btn.pack(side=TOP, padx=padx, pady=pady)
        scan_plate_btn.pack(side=TOP, padx=padx, pady=pady)
        logout_btn.pack(side=TOP, padx=padx, pady=pady)

        self.main_window.mainloop()


def main():
    app = App()


if __name__ == '__main__':
    main()
