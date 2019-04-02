from tkinter import *


class StandardValues:
    # Database access
    username = 'admin'
    password = 'Hollander#6'
    aes_key = 'eIEtvO@OK^lW1rFokTZ%tF#fGErKJTr$'

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
    width = 500
    height = 500
    btn_text_clr = "black"
    btn_bk_clr = "white"
    padx = 15
    pady = 15

    options = [
        "Please Select",
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY"
    ]


class Error:
    # error window and prints it in a pop up window
    @staticmethod
    def error_window(string_in):
        error_window = Toplevel()
        error_window.configure(background=StandardValues.background)
        error_window.winfo_toplevel().title("Error!!")
        error_label = Label(error_window, text="Error : " + str(string_in))
        error_label.pack(side=TOP)

        ok_btn = Button(error_window, text="OK", command=lambda: [error_window.destroy()])
        ok_btn.pack(side=BOTTOM)
