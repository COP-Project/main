from tkinter import *


class Login:
    def __init__(self):
        self.username = ""
        self.password = ""

    def login(self, username_tb, password_tb):
        self.username = username_tb.get()
        self.password = password_tb.get()

    def create_window(self):
        # set login screen
        root = Tk()
        root.withdraw()  # won't need this
        login_scrn = Toplevel()
        login_scrn.configure(background="white")
        login_scrn.geometry("550x100")
        login_scrn.winfo_toplevel().title("User Login")

        # set username and pw text boxes and labels
        username_label = Label(login_scrn, bg="white", text="User Name")
        username_label.grid(row=1, column=0)

        username_textbox = Entry(login_scrn)
        username_textbox.grid(row=1, column=1, padx=20)

        pw_label = Label(login_scrn, bg="white", text="Password")
        pw_label.grid(row=2, column=0)
        pw_textbox = Entry(login_scrn)
        pw_textbox.grid(row=2, column=1, padx=20)

        var = IntVar()  # variable use to pause until the submit button is pressed
        submit_btn = Button(login_scrn, bg="black", fg="white", text="Submit",
                            command=lambda: [var.set(1), self.login(username_textbox, pw_textbox),
                                             login_scrn.destroy()])

        submit_btn.grid(row=1, column=3, padx=15)
        submit_btn.wait_variable(var)  # wait
