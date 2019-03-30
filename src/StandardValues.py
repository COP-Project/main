from tkinter import *


class StandardValues:
    def __init__(self):
        # Database Field restrictions
        self.firstNameChars = 20
        self.lastNameChars = 20
        self.addressChars = 20
        self.carmakeChars = 20
        self.plateNumChars = 7
        self.colorChars = 20
        self.modelChars = 20


class Error:
    # error window and prints it in a pop up window
    def error_window(string_in):
        error_window = Toplevel()
        error_window.geometry("500x200")
        error_window.winfo_toplevel().title("Error!!")
        error_label = Label(error_window, text="Error " + string_in)
        error_label.pack()
        ok_btn = Button(error_window, text="OK", command=error_window.destroy)
        ok_btn.pack()
