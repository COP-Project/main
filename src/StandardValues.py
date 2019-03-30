from tkinter import *


class StandardValues:
    # Database Field Values
    firstNameChars = 20
    lastNameChars = 20
    addressChars = 20
    carmakeChars = 20
    plateNumChars = 7
    colorChars = 20
    modelChars = 20

    # Tkinter Values
    background = "white"
    win_size = "700x500"
    btn_text_clr = "black"
    btn_bk_clr = "white"
    padding = 20

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
