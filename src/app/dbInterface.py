import tkinter as tk
from tkinter import *
from tkinter import messagebox

import dbCommands as dbC
from StandardValues import *
from dbCommands import *


class DbInterface:
    def __init__(self, username, password, debug):
        self.data_access = self.conn(username, password)
        self.debug = debug

        self.add_driver_window = None
        self.add_window_widgets = None

        self.edit_driver_window = None
        self.edit_window_widgets = None
        
        self.del_driver_window = None
        self.del_driver_widgets = None

    def invoke_add_btn(self, data_driver):
        self.add_window_widgets[0].insert(END, data_driver[0])
        self.add_window_widgets[1].insert(END, data_driver[1])
        self.add_window_widgets[2].insert(END, data_driver[2])
        self.add_window_widgets[3].insert(END, data_driver[3])
        self.add_window_widgets[4].set(data_driver[4])
        self.add_window_widgets[5].insert(END, data_driver[5])
        self.add_window_widgets[6].insert(END, data_driver[6])
        self.add_window_widgets[7].insert(END, data_driver[7])
        self.add_window_widgets[8].insert(END, data_driver[8])
        self.add_window_widgets[9].set(data_driver[9])

        self.add_window_widgets[10].invoke()

    def invoke_edit_button(self, data_driver):
        self.edit_window_widgets[0].delete(0, END)
        self.edit_window_widgets[1].delete(0, END)
        self.edit_window_widgets[2].delete(0, END)
        self.edit_window_widgets[3].delete(0, END)
        self.edit_window_widgets[5].delete(0, END)
        self.edit_window_widgets[6].delete(0, END)
        self.edit_window_widgets[7].delete(0, END)
        self.edit_window_widgets[8].delete(0, END)

        self.edit_window_widgets[0].insert(END, data_driver[0])
        self.edit_window_widgets[1].insert(END, data_driver[1])
        self.edit_window_widgets[2].insert(END, data_driver[2])
        self.edit_window_widgets[3].insert(END, data_driver[3])
        self.edit_window_widgets[4].set(data_driver[4])
        self.edit_window_widgets[5].insert(END, data_driver[5])
        self.edit_window_widgets[6].insert(END, data_driver[6])
        self.edit_window_widgets[7].insert(END, data_driver[7])
        self.edit_window_widgets[8].insert(END, data_driver[8])
        self.edit_window_widgets[9].set(data_driver[9])

        self.edit_window_widgets[10].invoke()

    def invoke_delete_button(self, data_driver):
        self.del_driver_widgets[0].insert(END, data_driver[5])
        self.del_driver_widgets[1].invoke()

    # sets up window for driver inputs calls addDrivers()
    def add_drivers_screen(self):
        # creates window
        self.add_driver_window = Toplevel()
        self.add_driver_window.configure(background=StandardValues.background)
        # self.add_driver_window.geometry(StandardValues.win_size)
        self.add_driver_window.winfo_toplevel().title("New Driver Entry")

        # text boxes and buttons
        # FIRST NAME LABEL AND BOX
        self.add_label("First Name", 0, 0, self.add_driver_window)
        first_name_tb = Entry(self.add_driver_window)  # textvariable=v
        first_name_tb.grid(row=0, column=1, padx=StandardValues.padx)

        # LAST NAME LABEL AND BOX
        self.add_label("Last Name", 1, 0, self.add_driver_window)
        last_name_tb = Entry(self.add_driver_window)
        last_name_tb.grid(row=1, column=1, padx=StandardValues.padx)

        # Streetname/ address
        self.add_label("Address", 2, 0, self.add_driver_window)
        address_tb = Entry(self.add_driver_window)
        address_tb.grid(row=2, column=1, padx=StandardValues.padx)

        # Zip Code
        self.add_label("Zip Code", 3, 0, self.add_driver_window)
        zipcode_tb = Entry(self.add_driver_window)
        zipcode_tb.grid(row=3, column=1, padx=StandardValues.padx)

        # State
        self.add_label("State", 4, 0, self.add_driver_window)
        state_om = StringVar()
        state_om.set(StandardValues.options[0])

        state_om_field = OptionMenu(self.add_driver_window, state_om, *StandardValues.options)
        state_om_field.grid(row=4, column=1, padx=StandardValues.padx)

        # platenumber
        self.add_label("Plate #", 5, 0, self.add_driver_window)
        platenum_tb = Entry(self.add_driver_window, state=NORMAL)
        platenum_tb.grid(row=5, column=1, padx=StandardValues.padx)

        # car make
        self.add_label("Car Make", 6, 0, self.add_driver_window)
        car_make_tb = Entry(self.add_driver_window)
        car_make_tb.grid(row=6, column=1, padx=StandardValues.padx)

        # model
        self.add_label("Model", 7, 0, self.add_driver_window)
        model_tb = Entry(self.add_driver_window)
        model_tb.grid(row=7, column=1, padx=StandardValues.padx)

        # Color
        self.add_label("Color", 8, 0, self.add_driver_window)
        color_tb = Entry(self.add_driver_window)
        color_tb.grid(row=8, column=1, padx=StandardValues.padx)

        # priority
        self.add_label("High Priority", 9, 0, self.add_driver_window)
        priority_om = StringVar()
        options = ("YES", "NO")

        priority_om.set(options[1])

        priority_om_field = OptionMenu(self.add_driver_window, priority_om, *options)
        priority_om_field.grid(row=9, column=1, padx=StandardValues.padx)

        # save button
        save_user_btn = Button(self.add_driver_window,
                               bg=StandardValues.btn_bk_clr,
                               fg=StandardValues.btn_text_clr,
                               text="Save")

        self.add_window_widgets = (first_name_tb,
                                   last_name_tb,
                                   address_tb,
                                   zipcode_tb,
                                   state_om,
                                   platenum_tb,
                                   car_make_tb,
                                   model_tb,
                                   color_tb,
                                   priority_om,
                                   save_user_btn)

        save_user_btn.grid(row=11, column=0, pady=30, padx=30)
        # save button action, runs addUser and then calls closeHomeWindow to close the top lvl window
        # NOTE: Removed closeWindowHome() from button.
        # This was causing the window to close even if a blank text box was passed.
        # Passing the self.add_driver_window in addUser() instead for a fix.<<<<REFACTOR

        save_user_btn.config(command=lambda: [self.data_access.add_driver(first_name_tb.get().upper(),
                                                                          last_name_tb.get().upper(),
                                                                          address_tb.get().upper(),
                                                                          zipcode_tb.get(),
                                                                          state_om.get(),
                                                                          platenum_tb.get().upper(),
                                                                          car_make_tb.get().upper(),
                                                                          model_tb.get().upper(),
                                                                          color_tb.get().upper(),
                                                                          priority_om.get()),
                                              self.add_driver_window.destroy()])

    def edit_driver_search(self):
        # creates window
        edit_driver_sch = Toplevel()
        edit_driver_sch.configure(background=StandardValues.background)
        # edit_driver_sch.geometry(StandardValues.win_size)
        edit_driver_sch.winfo_toplevel().title("Edit Driver")

        # label and text box
        submit_label = Label(edit_driver_sch, bg="white",
                             text="Please Enter the Driver's plate number you wish to edit.")
        submit_label.grid(row=1, column=0)
        submit_tb = Entry(edit_driver_sch)
        submit_tb.grid(row=1, column=1, padx=20)

        # edit button
        edit_submit_btn = Button(edit_driver_sch,
                                 bg=StandardValues.btn_bk_clr,
                                 fg=StandardValues.btn_text_clr,
                                 text="Submit")

        edit_submit_btn.grid(row=1, column=3, padx=15)

        # edit button functionality
        edit_submit_btn.config(
            command=lambda: [
                self.edit_driver_screen(submit_tb.get(), self.data_access.search_zip_plate("plate", submit_tb.get())),
                edit_driver_sch.destroy()
            ])

    def edit_driver_screen(self, platenum_old, row):
        if row is None:
            Error.error_window("There were no records with that license plate")
            return

        # creates window
        self.edit_driver_window = Toplevel()
        self.edit_driver_window.configure(background="white")
        # edit_driver_window.geometry(StandardValues.win_size)
        self.edit_driver_window.winfo_toplevel().title("Edit Driver")

        # text boxes and buttons
        # FIRST NAME LABEL AND BOX
        self.add_label("First Name", 0, 0, self.edit_driver_window)
        first_name_tb = Entry(self.edit_driver_window)  # textvariable=v
        first_name_tb.insert(END, row[0][0])
        first_name_tb.grid(row=0, column=1, padx=StandardValues.padx)

        # LAST NAME LABEL AND BOX
        self.add_label("Last Name", 1, 0, self.edit_driver_window)
        last_name_tb = Entry(self.edit_driver_window)
        last_name_tb.insert(END, row[0][1])
        last_name_tb.grid(row=1, column=1, padx=StandardValues.padx)

        # Streetname/ address
        self.add_label("Address", 2, 0, self.edit_driver_window)
        address_tb = Entry(self.edit_driver_window)
        address_tb.insert(END, row[0][2])
        address_tb.grid(row=2, column=1, padx=StandardValues.padx)

        # Zip Code
        self.add_label("Zip Code", 3, 0, self.edit_driver_window)
        zipcode_tb = Entry(self.edit_driver_window)
        zipcode_tb.insert(END, row[0][3])
        zipcode_tb.grid(row=3, column=1, padx=StandardValues.padx)

        # State
        self.add_label("State", 4, 0, self.edit_driver_window)
        state_om = StringVar()
        state_om.set(row[0][4])

        state_om_field = OptionMenu(self.edit_driver_window, state_om, *StandardValues.options)
        state_om_field.grid(row=4, column=1, padx=StandardValues.padx)

        # platenumber
        self.add_label("Plate #", 5, 0, self.edit_driver_window)
        platenum_tb = Entry(self.edit_driver_window, state=NORMAL)
        platenum_tb.insert(END, row[0][5])
        platenum_tb.grid(row=5, column=1, padx=StandardValues.padx)

        # car make
        self.add_label("Car Make", 6, 0, self.edit_driver_window)
        car_make_tb = Entry(self.edit_driver_window)
        car_make_tb.insert(END, row[0][6])
        car_make_tb.grid(row=6, column=1, padx=StandardValues.padx)

        # model
        self.add_label("Model", 7, 0, self.edit_driver_window)
        model_tb = Entry(self.edit_driver_window)
        model_tb.insert(END, row[0][7])
        model_tb.grid(row=7, column=1, padx=StandardValues.padx)

        # Color
        self.add_label("Color", 8, 0, self.edit_driver_window)
        color_tb = Entry(self.edit_driver_window)
        color_tb.insert(END, row[0][8])
        color_tb.grid(row=8, column=1, padx=StandardValues.padx)

        # priority
        self.add_label("High Priority", 9, 0, self.edit_driver_window)
        priority_om = StringVar()
        options = ("YES", "NO")

        priority_om.set(options[1])

        priority_om_field = OptionMenu(self.edit_driver_window, priority_om, *options)
        priority_om_field.grid(row=9, column=1, padx=StandardValues.padx)

        # save button
        save_user_btn = Button(self.edit_driver_window,
                               bg=StandardValues.btn_bk_clr,
                               fg=StandardValues.btn_text_clr,
                               text="Save")

        self.edit_window_widgets = (first_name_tb,
                                    last_name_tb,
                                    address_tb,
                                    zipcode_tb,
                                    state_om,
                                    platenum_tb,
                                    car_make_tb,
                                    model_tb,
                                    color_tb,
                                    priority_om,
                                    save_user_btn)

        save_user_btn.grid(row=11, column=0, pady=30, padx=30)

        save_user_btn.config(command=lambda: [print(self.data_access.edit_driver_request(platenum_old,
                                                                                   first_name_tb.get().upper(),
                                                                                   last_name_tb.get().upper(),
                                                                                   address_tb.get().upper(),
                                                                                   zipcode_tb.get(),
                                                                                   state_om.get(),
                                                                                   platenum_tb.get().upper(),
                                                                                   car_make_tb.get().upper(),
                                                                                   model_tb.get().upper(),
                                                                                   color_tb.get().upper(),
                                                                                   priority_om.get())),
                                              self.edit_driver_window.destroy()])

    # search by zip or plate or display all high priority
    def search_zip_plate_inp_screen(self, string):
        # are we searching by zip or plate?
        if string == "zip":
            label = "Zip Code"
        elif string == "plate":
            label = "Plate Number"
        else:
            Error.errorWindow("Cannot search by that value")
            return

        # set plate zip window
        search_zip_plate_screen = Toplevel()
        search_zip_plate_screen.configure(background=StandardValues.background)
        search_zip_plate_screen.winfo_toplevel().title("Search Driver By" + label)
        # search_zip_plate_screen.geometry(StandardValues.win_size)

        # variable text box AND LABEL
        self.add_label(label, 0, 0, search_zip_plate_screen)
        zip_plate_lbl_tb = Entry(search_zip_plate_screen)
        zip_plate_lbl_tb.grid(row=0, column=1, padx=20)

        # button displaysSearch() from string returned by searchZipPlate()
        search_zip_plate_btn = Button(search_zip_plate_screen,
                                      bg=StandardValues.btn_bk_clr,
                                      fg=StandardValues.btn_text_clr,
                                      text="Search",
                                      command=lambda: [
                                          self.display_search(
                                              self.data_access.search_zip_plate(string, zip_plate_lbl_tb.get())
                                          )
                                      ])

        search_zip_plate_btn.grid(row=0, column=3, padx=20)

    # searches by first and last name
    def search_lname_inp_screen(self):
        search_lname_screen = Toplevel()
        search_lname_screen.configure(background=StandardValues.background)
        search_lname_screen.winfo_toplevel().title("Search Driver By Name")
        # search_lname_screen.geometry(StandardValues.win_size)

        # text boxes and buttons
        # FIRST NAME LABEL AND BOX
        self.add_label("First Name", 0, 0, search_lname_screen)
        search_fname_tb = Entry(search_lname_screen)
        search_fname_tb.grid(row=0, column=1, padx=20)
        # LAST NAME LABEL AND BOX
        self.add_label("Last Name", 1, 0, search_lname_screen)
        search_lname_tb = Entry(search_lname_screen)
        search_lname_tb.grid(row=1, column=1, padx=20)

        search_name_driver_btn = Button(search_lname_screen,
                                        bg=StandardValues.btn_bk_clr,
                                        fg=StandardValues.btn_text_clr,
                                        text="Search",
                                        command=lambda: [
                                            self.display_search(
                                                self.data_access.search_driver_fname_lname(search_fname_tb.get(),
                                                                                           search_lname_tb.get())
                                            )
                                        ])

        search_name_driver_btn.grid(row=2, column=0, padx=20)

    # pop up screen to delete a driver
    def del_driver_screen(self):
        # creates window
        self.del_driver_window = Toplevel()
        self.del_driver_window.configure(background=StandardValues.background)
        # self.del_driver_window.geometry(StandardValues.win_size)
        self.del_driver_window.winfo_toplevel().title("Delete Driver")

        # label and text box
        submit_label = Label(self.del_driver_window, bg="white",
                             text="Please Enter the Driver's plate number you wish to delete.")
        submit_label.grid(row=1, column=0)
        submit_tb = Entry(self.del_driver_window)
        submit_tb.grid(row=1, column=1, padx=20)

        # delete button
        del_submit_btn = Button(self.del_driver_window,
                                bg=StandardValues.btn_bk_clr,
                                fg=StandardValues.btn_text_clr,
                                text="Submit")
        del_submit_btn.grid(row=1, column=3, padx=15)

        self.del_driver_widgets = (submit_tb,
                                   del_submit_btn)

        # delete button functionality
        del_submit_btn.config(command=lambda: [self.data_access.delete_driver(submit_tb.get()),
                                               self.del_driver_window.destroy()])

    # function to add a label to a window
    @staticmethod
    def add_label(string_in, row_in, col_in, window):
        platenum_label = Label(window, bg="white", text=string_in)
        platenum_label.grid(row=row_in, column=col_in)

    # displays the search results in a new window
    def display_search(self, rows):
        if rows == "":
            return

        # set up window
        display_zip_plate_screen = tk.Tk()
        display_zip_plate_screen.configure(background=StandardValues.background)
        display_zip_plate_screen.winfo_toplevel().title("Search Results")
        display_zip_plate_screen.minsize(StandardValues.width, StandardValues.height)

        results = Frame(display_zip_plate_screen)
        results.grid(row=0, column=0)

        buttons = Frame(display_zip_plate_screen)
        buttons.grid(row=1, column=0)

        # loop to print the header to the window
        header = (
            "First Name", "Last Name", "Street", "Zip Code", "State", "Plate", "Make", "Color", "Model", "Priority")
        for top_id, top in enumerate(header):
            header_row = Label(results, text=header[top_id], bg="white")
            header_row.grid(row=0, column=top_id, padx=3)

        # loop to print the data pulled from the database
        for row_id, row in enumerate(rows):
            for col_id, col in enumerate(row):
                search_row = Label(results, text=col, bg="white")
                search_row.grid(row=row_id + 1, column=col_id, padx=3)

        # adds the delete button to the bottom of the search window
        delete_btn = Button(buttons,
                            bg=StandardValues.btn_bk_clr,
                            fg=StandardValues.btn_text_clr,
                            text="Delete Driver",
                            command=lambda: [self.del_driver_screen()])

        edit_btn = Button(buttons,
                          bg=StandardValues.btn_bk_clr,
                          fg=StandardValues.btn_text_clr,
                          text="Edit Driver",
                          command=lambda: [self.edit_driver_search()])  # implement

        delete_btn.grid(row=0, column=0, padx=StandardValues.padx, pady=StandardValues.pady)
        edit_btn.grid(row=0, column=1, padx=StandardValues.padx, pady=StandardValues.pady)

    def log_out_screen(self):
        will_logout = messagebox.askyesno("Log Out", "Are you sure you want to log out?")

        if will_logout:
            self.data_access.log_out()
        else:
            return

    def scan_license_plate_screen(self):
        scan_screen = Toplevel()
        scan_screen.configure(background=StandardValues.background)
        scan_screen.winfo_toplevel().title("Scan License Plate")

        img_name_label = Label(scan_screen, text="Please enter an image location: ", bg="white")
        img_name_label.grid(row=0, column=0, padx=StandardValues.padx)

        img_name_tb = Entry(scan_screen)
        img_name_tb.grid(row=1, column=0, padx=StandardValues.padx)

        img_country_label = Label(scan_screen, text="Please enter the plate's country: ", bg="white")
        img_country_label.grid(row=2, column=0, padx=StandardValues.padx)

        img_country_tb = Entry(scan_screen)
        img_country_tb.grid(row=3, column=0, padx=StandardValues.padx)

        img_region_label = Label(scan_screen, text="Please enter the plate's region: ", bg="white")
        img_region_label.grid(row=4, column=0, padx=StandardValues.padx)

        img_region_tb = Entry(scan_screen)
        img_region_tb.grid(row=5, column=0, padx=StandardValues.padx)

        # delete button
        img_submit_btn = Button(scan_screen,
                                bg=StandardValues.btn_bk_clr,
                                fg=StandardValues.btn_text_clr,
                                text="Submit",
                                command=lambda: self.scan_license_plate(img_name_tb.get(), img_country_tb.get(),
                                                                        img_region_tb.get()))

        img_submit_btn.grid(row=6, column=0)

    def scan_license_plate(self, img, country, region):
        self.data_access.scan_license_plate(img, country, region)

    def get_user(self):
        return self.data_access.get_user()

    @staticmethod
    def conn(username, password):
        return dbC.DataAccess(username, password)
