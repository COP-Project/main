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

        self.parent_window = None

        self.add_driver_window = None
        self.add_window_widgets = None

        self.edit_driver_search_window = None
        self.edit_driver_search_widgets = None

        self.edit_driver_window = None
        self.edit_window_widgets = None

        self.del_driver_window = None
        self.del_driver_widgets = None

        self.search_zip_plate_window = None
        self.search_zip_plate_widgets = None

        self.search_fname_lname_window = None
        self.search_fname_lname_widgets = None

    @staticmethod
    def get_driver_data(driver):
        return (driver[0].get().upper(),
                driver[1].get().upper(),
                driver[2].get().upper(),
                driver[3].get().upper(),
                driver[4].get().upper(),
                driver[5].get().upper(),
                driver[6].get().upper(),
                driver[7].get().upper(),
                driver[8].get().upper(),
                driver[9].get().upper())

    # sets up window for driver inputs calls addDrivers()
    def add_drivers_screen(self):
        # creates window
        self.add_driver_window = Toplevel()
        self.add_driver_window.configure(background=StandardValues.background)
        self.add_driver_window.winfo_toplevel().title("New Driver Entry")

        size = self.parent_window.geometry()

        width = int(size.split("x")[0]) / 2
        x_offset = size.split("+")[1]

        height = int(size.split("x")[1].split("+")[0]) / 2
        y_offset = size.split("+")[2]

        self.add_driver_window.geometry("+{}+{}".format(str(int(width / 2)), str(int(height / 2))))

        first_name_lbl = Label(self.add_driver_window, text="First Name:")
        last_name_lbl = Label(self.add_driver_window, text="Last Name:")
        address_tb_lbl = Label(self.add_driver_window, text="Address:")
        zipcode_tb_lbl = Label(self.add_driver_window, text="Zip Code:")
        state_om_lbl = Label(self.add_driver_window, text="State:")
        platenum_tb_lbl = Label(self.add_driver_window, text="License Plate:")
        car_make_tb_lbl = Label(self.add_driver_window, text="Car Make:")
        model_tb_lbl = Label(self.add_driver_window, text="Car Model:")
        color_tb_lbl = Label(self.add_driver_window, text="Car Color:")
        priority_om_lbl = Label(self.add_driver_window, text="High Priority:")

        first_name_tb = Entry(self.add_driver_window)
        last_name_tb = Entry(self.add_driver_window)
        address_tb = Entry(self.add_driver_window)
        zipcode_tb = Entry(self.add_driver_window)
        platenum_tb = Entry(self.add_driver_window)
        car_make_tb = Entry(self.add_driver_window)
        model_tb = Entry(self.add_driver_window)
        color_tb = Entry(self.add_driver_window)

        # Adding labels to grid layout
        first_name_lbl.grid(sticky="w", row=0, column=0)
        last_name_lbl.grid(sticky="w", row=1, column=0)
        address_tb_lbl.grid(sticky="w", row=2, column=0)
        zipcode_tb_lbl.grid(sticky="w", row=3, column=0)
        state_om_lbl.grid(sticky="w", row=4, column=0)
        platenum_tb_lbl.grid(sticky="w", row=5, column=0)
        car_make_tb_lbl.grid(sticky="w", row=6, column=0)
        model_tb_lbl.grid(sticky="w", row=7, column=0)
        color_tb_lbl.grid(sticky="w", row=8, column=0)
        priority_om_lbl.grid(sticky="w", row=9, column=0)

        # Adding text boxes to grid
        first_name_tb.grid(sticky="w", row=0, column=1, padx=StandardValues.padx)
        last_name_tb.grid(sticky="w", row=1, column=1, padx=StandardValues.padx)
        address_tb.grid(sticky="w", row=2, column=1, padx=StandardValues.padx)
        zipcode_tb.grid(sticky="w", row=3, column=1, padx=StandardValues.padx)
        platenum_tb.grid(sticky="w", row=5, column=1, padx=StandardValues.padx)
        car_make_tb.grid(sticky="w", row=6, column=1, padx=StandardValues.padx)
        model_tb.grid(sticky="w", row=7, column=1, padx=StandardValues.padx)
        color_tb.grid(sticky="w", row=8, column=1, padx=StandardValues.padx)

        # Creating option menus
        state_om = StringVar()
        priority_om = StringVar()
        options = ("YES", "NO")

        state_om.set(StandardValues.options[0])
        priority_om.set(options[1])

        state_om_field = OptionMenu(self.add_driver_window, state_om, *StandardValues.options)
        priority_om_field = OptionMenu(self.add_driver_window, priority_om, *options)

        state_om_field.grid(sticky="ew", row=4, column=1, padx=StandardValues.padx)
        priority_om_field.grid(sticky="ew", row=9, column=1, padx=StandardValues.padx)

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

        save_user_btn.grid(sticky="w", row=11, column=1, pady=StandardValues.pady, padx=StandardValues.padx)
        # save button action, runs addUser and then calls closeHomeWindow to close the top lvl window
        # NOTE: Removed closeWindowHome() from button.
        # This was causing the window to close even if a blank text box was passed.
        # Passing the self.add_driver_window in addUser() instead for a fix.<<<<REFACTOR

        save_user_btn.config(command=lambda: [self.data_access.add_driver(self.get_driver_data(self.add_driver_window)),
                                              self.add_driver_window.destroy()])

    def edit_driver_search(self):
        # creates window
        self.edit_driver_search_window = Toplevel()
        self.edit_driver_search_window.configure(background=StandardValues.background)
        self.edit_driver_search_window.winfo_toplevel().title("Edit Driver")

        # label and text box
        submit_label = Label(self.edit_driver_search_window, bg="white",
                             text="Please Enter the Driver's plate number you wish to edit.")
        submit_label.grid(row=1, column=0)
        submit_tb = Entry(self.edit_driver_search_window)
        submit_tb.grid(row=1, column=1, padx=20)

        # edit button
        edit_submit_btn = Button(self.edit_driver_search_window,
                                 bg=StandardValues.btn_bk_clr,
                                 fg=StandardValues.btn_text_clr,
                                 text="Submit")

        self.edit_driver_search_widgets = (submit_tb,
                                           edit_submit_btn)

        edit_submit_btn.grid(row=1, column=3, padx=15)

        # edit button functionality
        edit_submit_btn.config(
            command=lambda: [
                self.edit_driver_screen(submit_tb.get(), self.data_access.search_zip_plate("plate", submit_tb.get())),
                self.edit_driver_search_window.destroy()
            ])

    def edit_driver_screen(self, platenum_old, row):
        if row == ():
            Error.error_window("There were no records with that license plate")
            return

            # creates window
        self.edit_driver_window = Toplevel()
        self.edit_driver_window.configure(background="white")
        self.edit_driver_window.winfo_toplevel().title("Edit Driver")

        first_name_lbl = Label(self.edit_driver_window, text="First Name:")
        last_name_lbl = Label(self.edit_driver_window, text="Last Name:")
        address_tb_lbl = Label(self.edit_driver_window, text="Address:")
        zipcode_tb_lbl = Label(self.edit_driver_window, text="Zip Code:")
        state_om_lbl = Label(self.edit_driver_window, text="State:")
        platenum_tb_lbl = Label(self.edit_driver_window, text="License Plate:")
        car_make_tb_lbl = Label(self.edit_driver_window, text="Car Make:")
        model_tb_lbl = Label(self.edit_driver_window, text="Car Model:")
        color_tb_lbl = Label(self.edit_driver_window, text="Car Color:")
        priority_om_lbl = Label(self.edit_driver_window, text="High Priority:")

        first_name_tb = Entry(self.edit_driver_window)
        last_name_tb = Entry(self.edit_driver_window)
        address_tb = Entry(self.edit_driver_window)
        zipcode_tb = Entry(self.edit_driver_window)
        platenum_tb = Entry(self.edit_driver_window)
        car_make_tb = Entry(self.edit_driver_window)
        model_tb = Entry(self.edit_driver_window)
        color_tb = Entry(self.edit_driver_window)

        # Adding labels to grid layout
        first_name_lbl.grid(sticky="w", row=0, column=0)
        last_name_lbl.grid(sticky="w", row=1, column=0)
        address_tb_lbl.grid(sticky="w", row=2, column=0)
        zipcode_tb_lbl.grid(sticky="w", row=3, column=0)
        state_om_lbl.grid(sticky="w", row=4, column=0)
        platenum_tb_lbl.grid(sticky="w", row=5, column=0)
        car_make_tb_lbl.grid(sticky="w", row=6, column=0)
        model_tb_lbl.grid(sticky="w", row=7, column=0)
        color_tb_lbl.grid(sticky="w", row=8, column=0)
        priority_om_lbl.grid(sticky="w", row=9, column=0)

        # Adding text boxes to grid
        first_name_tb.grid(sticky="w", row=0, column=1, padx=StandardValues.padx)
        last_name_tb.grid(sticky="w", row=1, column=1, padx=StandardValues.padx)
        address_tb.grid(sticky="w", row=2, column=1, padx=StandardValues.padx)
        zipcode_tb.grid(sticky="w", row=3, column=1, padx=StandardValues.padx)
        platenum_tb.grid(sticky="w", row=5, column=1, padx=StandardValues.padx)
        car_make_tb.grid(sticky="w", row=6, column=1, padx=StandardValues.padx)
        model_tb.grid(sticky="w", row=7, column=1, padx=StandardValues.padx)
        color_tb.grid(sticky="w", row=8, column=1, padx=StandardValues.padx)

        # Creating option menus
        state_om = StringVar()
        priority_om = StringVar()
        options = ("YES", "NO")

        state_om.set(StandardValues.options[0])
        priority_om.set(options[1])

        state_om_field = OptionMenu(self.edit_driver_window, state_om, *StandardValues.options)
        priority_om_field = OptionMenu(self.edit_driver_window, priority_om, *options)

        state_om_field.grid(sticky="ew", row=4, column=1, padx=StandardValues.padx)
        priority_om_field.grid(sticky="ew", row=9, column=1, padx=StandardValues.padx)

        # insert current values into text boxes
        first_name_tb.insert(END, row[0][0])
        last_name_tb.insert(END, row[0][1])
        address_tb.insert(END, row[0][2])
        zipcode_tb.insert(END, row[0][3])
        state_om.set(row[0][4])
        platenum_tb.insert(END, row[0][5])
        car_make_tb.insert(END, row[0][6])
        model_tb.insert(END, row[0][7])
        color_tb.insert(END, row[0][8])
        priority_om.set(row[0][9])

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

        save_user_btn.config(command=lambda: [self.data_access.edit_driver_request(
            self.get_driver_data(self.edit_window_widgets),
            platenum_old),
            self.edit_driver_window.destroy()])

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

        self.search_zip_plate_widgets = (zip_plate_lbl_tb,
                                         search_zip_plate_btn)

        search_zip_plate_btn.grid(row=0, column=3, padx=20)

    # searches by first and last name
    def search_lname_inp_screen(self):
        self.search_fname_lname_window = Toplevel()
        self.search_fname_lname_window.configure(background=StandardValues.background)
        self.search_fname_lname_window.winfo_toplevel().title("Search Driver By Name")
        # search_lname_screen.geometry(StandardValues.win_size)

        # text boxes and buttons
        # FIRST NAME LABEL AND BOX
        self.add_label("First Name", 0, 0, self.search_fname_lname_window)
        search_fname_tb = Entry(self.search_fname_lname_window)
        search_fname_tb.grid(row=0, column=1, padx=20)
        # LAST NAME LABEL AND BOX
        self.add_label("Last Name", 1, 0, self.search_fname_lname_window)
        search_lname_tb = Entry(self.search_fname_lname_window)
        search_lname_tb.grid(row=1, column=1, padx=20)

        search_name_driver_btn = Button(self.search_fname_lname_window,
                                        bg=StandardValues.btn_bk_clr,
                                        fg=StandardValues.btn_text_clr,
                                        text="Search",
                                        command=lambda: [
                                            self.display_search(
                                                self.data_access.search_driver_fname_lname(search_fname_tb.get(),
                                                                                           search_lname_tb.get())
                                            )
                                        ])

        self.search_fname_lname_widgets = (search_fname_tb,
                                           search_lname_tb,
                                           search_name_driver_btn)

        search_name_driver_btn.grid(row=2, column=0, padx=20)

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

    def log_out_screen(self, app):
        will_logout = messagebox.askyesno("Log Out", "Are you sure you want to log out?")

        if will_logout:
            self.data_access.log_out()
            app.main_window.destroy()
            app.login_user(0)
            app.create_main()
        else:
            return

    def scan_license_plate_screen(self):
        scan_screen = Toplevel()
        scan_screen.configure(background=StandardValues.background)
        scan_screen.winfo_toplevel().title("Scan License Plate")

        img_name_label = Label(scan_screen, text="Please enter an image location: ", bg="white")
        img_name_label.grid(row=0, column=0, padx=StandardValues.padx)

        img_name_tb = Entry(scan_screen)
        img_name_tb.grid(row=0, column=1, padx=StandardValues.padx)

        img_region_label = Label(scan_screen, text="Please enter the plate's origin state: ", bg="white")
        img_region_label.grid(row=2, column=0, padx=StandardValues.padx)

        state_om = StringVar()
        state_om.set(StandardValues.options[0])
        state_om_field = OptionMenu(scan_screen, state_om, *StandardValues.options)
        state_om_field.grid(row=2, column=1, padx=StandardValues.padx)

        img_submit_btn = Button(scan_screen,
                                bg=StandardValues.btn_bk_clr,
                                fg=StandardValues.btn_text_clr,
                                text="Submit",
                                command=lambda: self.scan_license_plate(img_name_tb.get(),
                                                                        state_om.get()))

        img_submit_btn.grid(row=6, column=0)

    def scan_license_plate(self, img, state):
        self.data_access.scan_license_plate(img, state)

    def get_user(self):
        return self.data_access.get_user()

    @staticmethod
    def conn(username, password):
        return dbC.DataAccess(username, password)

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

    def invoke_edit_search_button(self, data_driver):
        self.edit_driver_search_widgets[0].insert(END, data_driver[5])
        self.edit_driver_search_widgets[1].invoke()

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

    def invoke_search_zip_plate_button(self, data_driver):
        self.search_zip_plate_widgets[0].insert(END, data_driver[5])
        self.search_zip_plate_widgets[1].invoke()

    def invoke_search_fname_lname(self, data_driver):
        self.search_fname_lname_widgets[0].insert(END, data_driver[0])
        self.search_fname_lname_widgets[1].insert(END, data_driver[1])
        self.search_fname_lname_widgets[2].invoke()
