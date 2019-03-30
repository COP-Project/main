import tkinter as tk
from tkinter import *
from tkinter import messagebox
import dbCommands as dbC
from dbCommands import *
from StandardValues import Error


class DbInterface:
    def __init__(self, username, password):
        self.data_access = self.conn(username, password)

    # EDIT DRIVER IS IN PROGRESS
    def editDriverScreen(self):
        # creates window
        edit_driver_scrn = Toplevel()
        edit_driver_scrn.configure(background="white")
        edit_driver_scrn.geometry("550x750")
        edit_driver_scrn.winfo_toplevel().title("Edit Driver")

        # label and text box
        submit_label = Label(edit_driver_scrn, bg="white",
                             text="Please Enter the Driver's plate number you wish to edit.")
        submit_label.grid(row=1, column=0)
        submit_tb = Entry(edit_driver_scrn)
        submit_tb.grid(row=1, column=1, padx=20)

        # edit button
        edit_submit_btn = Button(edit_driver_scrn, bg="black", fg="white", text="Submit")
        edit_submit_btn.grid(row=1, column=3, padx=15)

        # edit button functionality
        edit_submit_btn.config(
            command=lambda: [self.data_access.editDriverRequest(submit_tb), edit_driver_scrn.destroy()])

    # search by zip or plate or display all high priority
    def searchZipPlateInpScreen(self, string):
        # are we searching by zip or plate?
        if string == "zip":
            label = "Zip Code"
        elif string == "plate":
            label = "Plate Number"
        else:
            Error.errorWindow("Cannot search by that value")
            return

        # set plate zip window
        search_zip_plate_screen = tk.Tk()
        search_zip_plate_screen.configure(background="white")
        search_zip_plate_screen.winfo_toplevel().title("Search Driver By" + label)
        search_zip_plate_screen.geometry("350x100")

        # variable text box AND LABEL
        self.addLabel(label, 0, 0, search_zip_plate_screen)
        zip_plate_lbl_tb = Entry(search_zip_plate_screen)
        zip_plate_lbl_tb.grid(row=0, column=1, padx=20)

        # button displaysSearch() from string returned by searchZipPlate()
        search_zip_plate_btn = Button(search_zip_plate_screen, bg="black", fg="white", text="Search",
                                      command=lambda: [
                                          self.displaySearch(
                                              self.data_access.searchZipPlate(string, zip_plate_lbl_tb.get())
                                          )
                                      ])

        search_zip_plate_btn.grid(row=0, column=3, padx=20)

    # searches by first and last name
    def searchLastNameIntScreen(self):
        search_lname_screen = tk.Tk()
        search_lname_screen.configure(background="white")
        search_lname_screen.winfo_toplevel().title("Search Driver By Name")
        search_lname_screen.geometry("250x200")

        # text boxes and buttons
        # FIRST NAME LABEL AND BOX
        self.addLabel("First Name", 0, 0, search_lname_screen)
        search_fname_tb = Entry(search_lname_screen)
        search_fname_tb.grid(row=0, column=1, padx=20)
        # LAST NAME LABEL AND BOX
        self.addLabel("Last Name", 1, 0, search_lname_screen)
        search_lname_tb = Entry(search_lname_screen)
        search_lname_tb.grid(row=1, column=1, padx=20)

        search_name_driver_btn = Button(search_lname_screen, text="Search", bg="black", fg="white",
                                        command=lambda: [
                                            self.displaySearch(
                                                self.data_access.searchDriverFirstLastName(search_fname_tb.get(),
                                                                                           search_lname_tb.get())
                                            )
                                        ])

        search_name_driver_btn.grid(row=2, column=0, padx=20)

    # sets up window for driver inputs calls addDrivers()
    def callAddDrivers(self):
        # creates window
        add_driver_window = Toplevel()
        add_driver_window.configure(background="white")
        add_driver_window.geometry("400x400")
        add_driver_window.winfo_toplevel().title("New Driver Entry")

        padding = 20

        # text boxes and buttons
        # FIRST NAME LABEL AND BOX
        self.addLabel("First Name", 0, 0, add_driver_window)
        first_name_tb = Entry(add_driver_window)  # textvariable=v
        first_name_tb.grid(row=0, column=1, padx=padding)

        # LAST NAME LABEL AND BOX
        self.addLabel("Last Name", 1, 0, add_driver_window)
        last_name_tb = Entry(add_driver_window)
        last_name_tb.grid(row=1, column=1, padx=padding)

        # Streetname/ address
        self.addLabel("Address", 2, 0, add_driver_window)
        address_tb = Entry(add_driver_window)
        address_tb.grid(row=2, column=1, padx=padding)

        # Zip Code
        self.addLabel("Zip Code", 3, 0, add_driver_window)
        zipcode_tb = Entry(add_driver_window)
        zipcode_tb.grid(row=3, column=1, padx=padding)

        # State
        self.addLabel("State", 4, 0, add_driver_window)
        state_tb = Entry(add_driver_window)
        state_tb.grid(row=4, column=1, padx=padding)

        # platenumber
        self.addLabel("Plate #", 5, 0, add_driver_window)
        platenum_tb = Entry(add_driver_window, state=NORMAL)
        platenum_tb.grid(row=5, column=1, padx=padding)

        # car make
        self.addLabel("Car Make", 6, 0, add_driver_window)
        car_make_tb = Entry(add_driver_window)
        car_make_tb.grid(row=6, column=1, padx=padding)

        # model
        self.addLabel("Model", 7, 0, add_driver_window)
        model_tb = Entry(add_driver_window)
        model_tb.grid(row=7, column=1, padx=padding)

        # Color
        self.addLabel("Color", 8, 0, add_driver_window)
        color_tb = Entry(add_driver_window)
        color_tb.grid(row=8, column=1, padx=padding)

        # priority
        self.addLabel("High Priority?", 9, 0, add_driver_window)
        priority_tb = Entry(add_driver_window)
        priority_tb.grid(row=9, column=1, padx=padding)

        # save button
        save_user_btn = Button(add_driver_window, bg="black", fg="white", text="Save")
        save_user_btn.grid(row=11, column=0, pady=30, padx=30)
        # save button action, runs addUser and then calls closeHomeWindow to close the top lvl window
        # NOTE: Removed closeWindowHome() from button.
        # This was causing the window to close even if a blank text box was passed.
        # Passing the add_driver_window in addUser() instead for a fix.<<<<REFACTOR

        save_user_btn.config(command=lambda: [self.data_access.addDriver(first_name_tb.get().upper(),
                                                                         last_name_tb.get().upper(),
                                                                         address_tb.get().upper(),
                                                                         zipcode_tb.get(),
                                                                         state_tb.get().upper(),
                                                                         platenum_tb.get().upper(),
                                                                         car_make_tb.get().upper(),
                                                                         model_tb.get().upper(),
                                                                         color_tb.get().upper(),
                                                                         priority_tb.get().upper(),
                                                                         add_driver_window),
                                              add_driver_window.destroy()])

    # pop up screen to delete a driver
    def delDriverScreen(self):
        # creates window
        del_driver_scrn = Toplevel()
        del_driver_scrn.configure(background="white")
        del_driver_scrn.geometry("550x100")
        del_driver_scrn.winfo_toplevel().title("Delete Driver")

        # label and text box
        submit_label = Label(del_driver_scrn, bg="white",
                             text="Please Enter the Driver's plate number you wish to delete.")
        submit_label.grid(row=1, column=0)
        submit_tb = Entry(del_driver_scrn)
        submit_tb.grid(row=1, column=1, padx=20)

        # delete button
        del_submit_btn = Button(del_driver_scrn, bg="black", fg="white", text="Submit")
        del_submit_btn.grid(row=1, column=3, padx=15)

        # delete button functionality
        del_submit_btn.config(command=lambda: [self.data_access.deleteDriver(submit_tb.get()),
                                               del_driver_scrn.destroy()])

    # function to add a label to a window
    def addLabel(self, string_in, row_in, col_in, window):
        platenum_label = Label(window, bg="white", text=string_in)
        platenum_label.grid(row=row_in, column=col_in)

    # displays the search results in a new window
    def displaySearch(self, rows):
        n = 2
        y = 0
        if rows == "":
            return
        # set up window
        display_zip_plate_screen = tk.Tk()
        display_zip_plate_screen.configure(background="white")
        display_zip_plate_screen.winfo_toplevel().title("Search Results")
        display_zip_plate_screen.geometry("700x400")

        # loop to print the header to the window
        header = (
            "First Name", "Last Name", "Street", "Zip Code", "State", "Plate", "Make", "Color", "Model", "Priority")
        for top in header:
            header_row = Label(display_zip_plate_screen, text=header[y], bg="white")
            header_row.grid(row=0, column=y, padx=3)
            y = y + 1

        # loop to print the data pulled from the database
        for row in rows:
            i = 0
            # newString= row[0] +'\t'+ row[1] +'\t'+ row[2]+'\t'+ row[3] + '\t' + row[4] + '\t' + row[5] + '\t' + row[6]
            # + '\t' + row[7]+ '\t' + row[8] + '\t' + row[9]
            for line in row:
                search_row = Label(display_zip_plate_screen, text=row[i], bg="white")
                search_row.grid(row=n, column=i, padx=3)
                i = i + 1
            search_row.grid(row=n, column=i)
            n = n + 1

        # adds the delete button to the bottom of the search window
        delete_btn = Button(display_zip_plate_screen, bg="black", fg="white", text="Delete Driver",
                            command=lambda: [self.data_access.delDriverScreen()])
        edit_btn = Button(display_zip_plate_screen, bg="black", fg="white", text="Edit Driver",
                          command=lambda: [self.data_access.editDriverScreen()])  # implement
        delete_btn.grid(row=n + 3, column=3)
        edit_btn.grid(row=n + 4, column=3)

    def logOutScreen(self):
        will_logout = messagebox.askyesno("Log Out", "Are you sure you want to log out?")

        if will_logout:
            self.data_access.logOut()
        else:
            return

    def getUser(self):
        return self.data_access.getUser()

    def conn(self, username, password):
        return dbC.DataAccess(username, password)
