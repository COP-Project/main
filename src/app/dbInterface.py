import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

import dbCommands as dbC
from StandardValues import *
from dbCommands import *


class DbInterface:
    def __init__(self, username, password, debug):
        self.data_access = self.conn(username, password)
        self.debug = debug

        self.is_priority_changed = FALSE

        self.parent_window = None

        self.add_driver_window = None
        self.add_window_widgets = None

        self.edit_driver_search_window = None
        self.edit_driver_search_widgets = None

        self.edit_driver_window = None
        self.edit_window_widgets = None

        self.del_driver_window = None
        self.del_driver_widgets = None

        self.search_driver = None
        self.search_widgets = None

        self.search_zip_plate_window = None
        self.search_zip_plate_widgets = None

        self.search_fname_lname_window = None
        self.search_fname_lname_widgets = None

    def add_fields(self, window, row, col):
        # Variables for binding to fields
        state_om = StringVar()
        state_om.set(StandardValues.options[0])

        priority_om = BooleanVar()

        # labels
        first_name_lbl = Label(window, text="First Name:")
        last_name_lbl = Label(window, text="Last Name:")
        address_tb_lbl = Label(window, text="Address:")
        zipcode_tb_lbl = Label(window, text="Zip Code:")
        state_om_lbl = Label(window, text="State:")
        platenum_tb_lbl = Label(window, text="License Plate:")
        car_make_tb_lbl = Label(window, text="Car Make:")
        model_tb_lbl = Label(window, text="Car Model:")
        color_tb_lbl = Label(window, text="Car Color:")
        priority_om_lbl = Label(window, text="High Priority:")

        # Create widgets
        first_name_tb = Entry(window)
        last_name_tb = Entry(window)
        address_tb = Entry(window)
        zipcode_tb = Entry(window)

        state_om_field = OptionMenu(window, state_om, *StandardValues.options)

        def handle_up_key(event, var=state_om.__str__()):
            return self.up_key(event, var)

        def handle_down_key(event, var=state_om.__str__()):
            return self.down_key(event, var)

        state_om_field.bind('<Up>', handle_up_key)
        state_om_field.bind('<Down>', handle_down_key)
        state_om_field.configure(takefocus=1)

        platenum_tb = Entry(window)
        car_make_tb = Entry(window)
        model_tb = Entry(window)
        color_tb = Entry(window)

        priority_om_field = Checkbutton(window, variable=priority_om, command=lambda: [self.set_priority_changed(TRUE)])

        priority_om_field.bind('<Return>', self.toggle)

        # Adding labels to grid layout
        first_name_lbl.grid(sticky="w", row=row + 0, column=col + 0)
        last_name_lbl.grid(sticky="w", row=row + 1, column=col + 0)
        address_tb_lbl.grid(sticky="w", row=row + 2, column=col + 0)
        zipcode_tb_lbl.grid(sticky="w", row=row + 3, column=col + 0)
        state_om_lbl.grid(sticky="w", row=row + 4, column=col + 0)
        platenum_tb_lbl.grid(sticky="w", row=row + 5, column=col + 0)
        car_make_tb_lbl.grid(sticky="w", row=row + 6, column=col + 0)
        model_tb_lbl.grid(sticky="w", row=row + 7, column=col + 0)
        color_tb_lbl.grid(sticky="w", row=row + 8, column=col + 0)
        priority_om_lbl.grid(sticky="w", row=row + 9, column=col + 0)

        # Adding text boxes to grid
        first_name_tb.grid(sticky="w", row=row + 0, column=col + 1, padx=StandardValues.padx)
        last_name_tb.grid(sticky="w", row=row + 1, column=col + 1, padx=StandardValues.padx)
        address_tb.grid(sticky="w", row=row + 2, column=col + 1, padx=StandardValues.padx)
        zipcode_tb.grid(sticky="w", row=row + 3, column=col + 1, padx=StandardValues.padx)
        platenum_tb.grid(sticky="w", row=row + 5, column=col + 1, padx=StandardValues.padx)
        car_make_tb.grid(sticky="w", row=row + 6, column=col + 1, padx=StandardValues.padx)
        model_tb.grid(sticky="w", row=row + 7, column=col + 1, padx=StandardValues.padx)
        color_tb.grid(sticky="w", row=row + 8, column=col + 1, padx=StandardValues.padx)

        state_om_field.grid(sticky="ew", row=row + 4, column=col + 1, padx=StandardValues.padx)
        priority_om_field.grid(sticky="ew", row=row + 9, column=col + 1, padx=StandardValues.padx)

        return (first_name_tb,
                last_name_tb,
                address_tb,
                zipcode_tb,
                state_om,
                platenum_tb,
                car_make_tb,
                model_tb,
                color_tb,
                priority_om)

    def up_key(self, event, var):
        value = StandardValues.options.index(event.widget.getvar(var))

        new_variable = StandardValues.options[value - 1] if value != 0 else (
            StandardValues.options[int(StandardValues.options.__len__()) - 1])

        event.widget.setvar(var, new_variable)

    def down_key(self, event, var):
        value = StandardValues.options.index(event.widget.getvar(var))

        new_variable = StandardValues.options[value + 1] if value != 50 else (StandardValues.options[0])

        event.widget.setvar(var, new_variable)

    def toggle(self, event):
        event.widget.toggle()

    def invoke_btn(self, event):
        event.widget.invoke()

    def set_priority_changed(self, has_changed):
        self.is_priority_changed = has_changed

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

        temp_widgets = self.add_fields(self.add_driver_window, 0, 0)

        # save button
        save_user_btn = Button(self.add_driver_window,
                               bg=StandardValues.btn_bk_clr,
                               fg=StandardValues.btn_text_clr,
                               text="Save")

        self.add_window_widgets = temp_widgets + (save_user_btn,)

        save_user_btn.grid(sticky="w", row=11, column=1, pady=StandardValues.pady, padx=StandardValues.padx)
        # save button action, runs addUser and then calls closeHomeWindow to close the top lvl window
        # NOTE: Removed closeWindowHome() from button.
        # This was causing the window to close even if a blank text box was passed.
        # Passing the self.add_driver_window in addUser() instead for a fix.<<<<REFACTOR

        save_user_btn.bind('<Return>', self.invoke_btn)
        save_user_btn.config(
            command=lambda: [self.data_access.add_driver(self.get_driver_data(self.add_window_widgets)),
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
        edit_submit_btn.bind('<Return>', self.invoke_btn)
        edit_submit_btn.config(
            command=lambda: [
                self.edit_driver_screen(submit_tb.get(), self.data_access.search_driver(
                    ("", "", "", "", "", submit_tb.get().upper(), "", "", "", ""), True)),
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

        temp_widgets = self.add_fields(self.edit_driver_window, 0, 0)

        # insert current values into text boxes
        temp_widgets[0].insert(END, row[0][0])
        temp_widgets[1].insert(END, row[0][1])
        temp_widgets[2].insert(END, row[0][2])
        temp_widgets[3].insert(END, row[0][3])
        temp_widgets[4].set(row[0][4])
        temp_widgets[5].insert(END, row[0][5])
        temp_widgets[6].insert(END, row[0][6])
        temp_widgets[7].insert(END, row[0][7])
        temp_widgets[8].insert(END, row[0][8])
        temp_widgets[9].set(row[0][9])

        # save button
        save_user_btn = Button(self.edit_driver_window,
                               bg=StandardValues.btn_bk_clr,
                               fg=StandardValues.btn_text_clr,
                               text="Save")

        self.edit_window_widgets = temp_widgets + (save_user_btn,)

        save_user_btn.grid(row=11, column=0, pady=30, padx=30)

        save_user_btn.bind('<Return>', self.invoke_btn)
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
        del_submit_btn.bind('<Return>', self.invoke_btn)
        del_submit_btn.config(command=lambda: [self.data_access.delete_driver(submit_tb.get()),
                                               self.del_driver_window.destroy()])

    def search_drivers(self):
        # set plate zip window
        self.search_driver = Toplevel()
        self.search_driver.configure(background=StandardValues.background)
        self.search_driver.winfo_toplevel().title("Search Driver")

        # variable text box AND LABEL
        temp_widgets = self.add_fields(self.search_driver, 0, 0)

        # button displaysSearch() from string returned by searchZipPlate()
        search_btn = Button(self.search_driver,
                            bg=StandardValues.btn_bk_clr,
                            fg=StandardValues.btn_text_clr,
                            text="Search",
                            command=lambda: [
                                self.display_search(
                                    self.data_access.search_driver(self.get_driver_data(self.search_widgets),
                                                                   self.is_priority_changed)
                                )
                            ])

        self.search_widgets = temp_widgets + (search_btn,)

        search_btn.bind('<Return>', self.invoke_btn)
        search_btn.grid(row=10, column=1, pady=15)

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
        header = ("First Name",
                  "Last Name",
                  "Street",
                  "Zip Code",
                  "State",
                  "Plate",
                  "Make",
                  "Color",
                  "Model",
                  "High Priority")

        for top_id, top in enumerate(header):
            header_row = Label(results, text=header[top_id], bg="white")
            header_row.grid(row=0, column=top_id, padx=3)

        for row_id, row in enumerate(rows):
            row_fname = Label(results, text=str(row[0]), bg="white", borderwidth=2)
            row_lname = Label(results, text=str(row[1]), bg="white")
            row_address = Label(results, text=str(row[2]), bg="white")
            row_zipcod = Label(results, text=str(row[3]), bg="white")
            row_state = Label(results, text=str(row[4]), bg="white")
            row_platenum = Label(results, text=str(row[5]), bg="white")
            row_make = Label(results, text=str(row[6]), bg="white")
            row_color = Label(results, text=str(row[7]), bg="white")
            row_model = Label(results, text=str(row[8]), bg="white")
            row_priority = Checkbutton(results, state=DISABLED)
            if row[9]:
                row_priority.select()

            row_fname.grid(sticky="w", row=row_id + 1, column=0, padx=3)
            row_lname.grid(sticky="w", row=row_id + 1, column=1, padx=3)
            row_address.grid(sticky="w", row=row_id + 1, column=2, padx=3)
            row_zipcod.grid(sticky="w", row=row_id + 1, column=3, padx=3)
            row_state.grid(sticky="w", row=row_id + 1, column=4, padx=3)
            row_platenum.grid(sticky="w", row=row_id + 1, column=5, padx=3)
            row_make.grid(sticky="w", row=row_id + 1, column=6, padx=3)
            row_color.grid(sticky="w", row=row_id + 1, column=7, padx=3)
            row_model.grid(sticky="w", row=row_id + 1, column=8, padx=3)
            row_priority.grid(sticky="w", row=row_id + 1, column=9, padx=3)

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
            app.login_user()
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
                driver[9].get())

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
