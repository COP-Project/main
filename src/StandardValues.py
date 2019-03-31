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
    def error_window(string_in):
        error_window = Tk()
        error_window.configure(background=StandardValues.background)
        error_window.winfo_toplevel().title("Error!!")
        error_label = Label(error_window, text="Error : " + str(string_in))
        error_label.pack(side=TOP)

        var = IntVar()

        ok_btn = Button(error_window, text="OK", command=lambda: error_window.destroy())
        ok_btn.pack(side=BOTTOM)

        error_window.wait_variable(var)
