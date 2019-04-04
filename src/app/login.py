from tkinter import ttk
from StandardValues import *


class Login:
    def __init__(self, debug):
        self.debug = debug

        self.username = ""
        self.password = ""

        self.root = Tk()
        self.root.withdraw()

        self.login_scrn = None

        self.username_label = None
        self.username_tb = None

        self.pw_label = None
        self.pw_tb = None

        self.submit_btn = None

        self.create_window()

    def login(self, username_tb, password_tb):
        self.username = username_tb.get()
        self.password = password_tb.get()

    def create_window(self):
        # set login screen
        self.login_scrn = Toplevel()
        self.login_scrn.configure(background=StandardValues.background)
        self.login_scrn.winfo_toplevel().title("User Login")

        self.create_buttons()

    def create_buttons(self):
        # set username and pw text boxes and labels
        self.username_label = Label(self.login_scrn, bg="white", text="User Name")
        self.username_label.grid(row=1, column=0)

        self.username_tb = Entry(self.login_scrn)
        self.username_tb.insert(END, "")
        self.username_tb.grid(row=1, column=1, padx=20)

        self.pw_label = Label(self.login_scrn, bg="white", text="Password")
        self.pw_label.grid(row=2, column=0)

        self.pw_tb = Entry(self.login_scrn)
        self.pw_tb.insert(END, "")
        self.pw_tb.grid(row=2, column=1, padx=20)

        self.create_submit(self.username_tb, self.pw_tb)

    def create_submit(self, username_textbox, pw_textbox):
        var = IntVar()  # variable use to pause until the submit button is pressed
        self.submit_btn = ttk.Button(self.login_scrn,
                                     text="Submit",
                                     command=lambda: {var.set(1), self.login(username_textbox, pw_textbox),
                                                      self.login_scrn.destroy()})

        self.submit_btn.grid(row=1, column=3, padx=15)

        if self.debug:
            username_textbox.insert(END, "TESTUSER")
            pw_textbox.insert(END, "TESTUSER")
            self.click_submit()
        else:
            self.submit_btn.wait_variable(var)  # wait

    def click_submit(self):
        self.submit_btn.invoke()
