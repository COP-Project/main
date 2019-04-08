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
        self.exit_btn = None

        self.create_window()

    def login(self):
        self.username = self.username_tb.get()
        self.password = self.pw_tb.get()

    def create_window(self):
        # set login screen
        self.login_scrn = Toplevel()
        self.login_scrn.configure(background=StandardValues.background)
        self.login_scrn.winfo_toplevel().title("User Login")

        StandardValues.get_screen_position(self.root)

        # Positions the window in the center of the page.
        self.login_scrn.geometry("+{}+{}".format(StandardValues.scr_width, StandardValues.scr_height))
        self.create_buttons()

    def create_buttons(self):
        # set username and pw text boxes and labels
        self.username_label = Label(self.login_scrn, bg="white", text="User Name")
        self.username_label.grid(row=0, column=0)

        self.username_tb = Entry(self.login_scrn)
        self.username_tb.insert(END, "")
        self.username_tb.bind('<Return>', self.submit)
        self.username_tb.grid(row=0, column=1, padx=20)

        self.pw_label = Label(self.login_scrn, bg="white", text="Password")
        self.pw_label.grid(row=1, column=0)

        self.pw_tb = Entry(self.login_scrn)
        self.pw_tb.insert(END, "")
        self.pw_tb.bind('<Return>', self.submit)
        self.pw_tb.grid(row=1, column=1, padx=20)

        self.create_submit(self.username_tb, self.pw_tb)
        # self.create_exit()


    def create_submit(self, username_textbox, pw_textbox):
        var = IntVar()
        self.submit_btn = Button(self.login_scrn,
                                 text="Submit")
        self.submit_btn.config(command=lambda: {var.set(1),
                                                self.login(),
                                                self.login_scrn.destroy()})

        self.submit_btn.grid(row=0, column=2, padx=15)
        self.submit_btn.bind('<Return>', self.submit)

        if self.debug:
            username_textbox.insert(END, "TESTUSER")
            pw_textbox.insert(END, "TESTUSER")
            self.click_submit()
        else:
            self.submit_btn.wait_variable(var)

    # def create_exit(self):
    #     var = IntVar()
    #     self.exit_btn = ttk.Button(self.login_scrn,
    #                                text="Exit",
    #                                command=lambda: {var.set(1), self.login_scrn.destroy()})
    #     self.exit_btn.grid(row=1, column=2, padx=15)
    #     self.exit_btn.bind('<Return>', self.exit)
    #     self.exit_btn.wait_variable(var)

    def exit(self, event):
        self.exit_btn.invoke()

    def submit(self, event):
        self.submit_btn.invoke()

    def click_submit(self):
        self.submit_btn.invoke()
