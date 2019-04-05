import pymysql.cursors
import sys
import dbUsers
from StandardValues import StandardValues, Error
from readPlate import readaPlate, create_alpr, destroy_alpr
from openalpr import Alpr

alpr = create_alpr()

class DataAccess:
    # data bas info, it needs to match either your local mysql server
    # ---command to CREATE TABLE poopproject.drivers(fname VARCHAR(20),
    # lname VARCHAR(20), address VARCHAR(20),zipcod VARCHAR(5),state VARCHAR(2),
    # platenum VARCHAR(12), carmake VARCHAR(20), color VARCHAR(20), model VARCHAR(20), priority VARCHAR(3));
    # or the AWS server

    def __init__(self, username, password):
        self.cursor = None
        self.conn = self.connect()
        self.user = dbUsers.Users(username, self)

        if not self.is_right_password(password):
            Error.error_window("Invalid password")

    # database self.connection and login screen########################
    def connect(self):
        # uses the inputs from the user to log in
        try:
            # self.connection to AWS database
            new_conn = pymysql.connect(host='copproject.cveza4dgo3d2.us-east-2.rds.amazonaws.com',
                                       port=3306,
                                       user=StandardValues.username,
                                       passwd=StandardValues.password,
                                       db='poopproject')

            self.cursor = new_conn.cursor()
            return new_conn
        except pymysql.OperationalError:
            Error.error_window("Could not connect to database")
            return pymysql.OperationalError

    # Searches by Zip or Plate Depeding on paramater from search_zip_plateInpScreen()
    def search_zip_plate(self, string, value):
        try:
            assert string == "zip" or string == "plate", "Please enter either zip or plate"

            if value == "":
                return None

            # check if we are searching by zip
            if string == "zip":
                self.cursor.execute("SELECT * FROM drivers WHERE (zipcod = %s)", value)
                rows = self.cursor.fetchall()
            # checks if we are searching by plate number
            elif string == "plate":
                self.cursor.execute("SELECT * FROM drivers WHERE (platenum = %s)", value)
                rows = self.cursor.fetchall()
            else:
                return None

            # return rows which is passed to displaySearch
            return rows
        except AssertionError as ae:
            Error.error_window(ae.__str__())
            return AssertionError

    # functionality to search and display all drivers in the data base by first and last name
    def search_driver_fname_lname(self, fname, lname):
        try:
            assert (fname != "" and lname != "")

            self.cursor.execute("SELECT * FROM drivers WHERE (fname = %s and lname = %s)", (fname, lname))
            rows = self.cursor.fetchall()

            # displaySearch(rows)
            return rows
        except AssertionError:
            Error.error_window("First name and Last name required")
            return AssertionError
        except Error as e:
            print(e)

    # the logic to to read in all the text boxes from calladd_drivers() probably way to many paramaters
    # REFACTOR in the future to group boxes into a object and pass object
    def add_driver(self, fname, lname, address, zipcode, state, platenum, make, color, model, priority):
        error = check_input(fname, lname, address, zipcode, state, platenum, make, color, model, priority)

        if error == -1:
            return -1

        # plate number duplication
        if self.plate_check(platenum) == 1:
            Error.error_window("Duplicate License Plate Number")
            return -1

        # runs query against database
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")
        # execute query
        data_driver = (fname, lname, address, zipcode, state, platenum, make, color, model, priority)
        self.cursor.execute(add_driver, data_driver)

        self.conn.commit()
        # self.cursorclose()

    # reads text entry boxes
    @staticmethod
    def read_textbox(tbox):
        return tbox.get()

    # deletes a driver
    def delete_driver(self, plate):
        rows = "DELETE FROM drivers WHERE platenum = %s"
        self.cursor.execute(rows, plate)
        self.conn.commit()

    # checks for duplicate plates upon  data entry into the DB
    def plate_check(self, string_in):
        self.cursor.execute("SELECT * FROM drivers WHERE platenum = %s ", string_in)

        return 1 if (self.cursor.rowcount == 1) else 0

    def edit_driver_request(self, platenum_old, fname, lname, address, zipcode, state, platenum_new,
                            make, color, model, priority):
        error = check_input(fname, lname, address, zipcode, state, platenum_new, make, color, model, priority)

        if error == -1:
            return -1

        edit_driver = ("UPDATE drivers "
                       "SET fname = %s, lname = %s, address = %s, zipcod = %s, state = %s, "
                       "platenum = %s, carmake = %s, color = %s, model = %s, priority = %s "
                       "WHERE platenum = %s ")

        data_driver = (fname, lname, address, zipcode, state, platenum_new, make, color, model, priority, platenum_old)
        self.cursor.execute(edit_driver, data_driver)

        self.conn.commit()

    def scan_license_plate(self, img, state):
        check = check_file_input(img)
        if check == -1:
            return -1

        plates = readaPlate(alpr, state.lower(), img)
        for eachplate in plates:
            print(eachplate)

    def is_right_password(self, password):
        check_password = ("SELECT 1 "
                          "FROM users "
                          "WHERE passwords = AES_ENCRYPT(%s, %s) ")

        data_password = (password, StandardValues.aes_key)
        self.cursor.execute(check_password, data_password)

        rows = self.cursor.fetchall()

        if self.cursor.rowcount > 0 and rows[0][0] == 1:
            return 1

        return 0

    # returns the user info from dbUser.py object >>thisUser
    def get_user(self):
        return self.user

    def log_out(self):
        self.conn.close()


def check_file_input(img):
    try:
        check_opened_file = open(img, 'r')
    except IOError:
        Error.error_window("File not found")
        return -1


def check_input(fname, lname, address, zipcode, state, platenum, make, color, model, priority):
    try:
        assert len(fname) <= StandardValues.firstNameChars and fname != "", "First Name must be less than or equal to " + str(StandardValues.firstNameChars)
        assert len(lname) <= StandardValues.lastNameChars and lname != "", "Last Name must be less than or equal to " + str(StandardValues.lastNameChars)
        assert len(address) <= StandardValues.addressChars and address != "", "Address must be less than or equal to " + str(StandardValues.addressChars)
        assert len(zipcode) == 5 and zipcode != "" and str(zipcode).isdigit(), "Zip code should be 5 numbers"
        assert len(platenum) <= StandardValues.plateNumChars and platenum != "", "Plate number must be " + str(StandardValues.plateNumChars) + " characters."
        assert len(make) <= StandardValues.carmakeChars and make != "", "Car Make must be less than or equal to " + str(StandardValues.carmakeChars)
        assert len(color) <= StandardValues.colorChars and color != "", "Color must be less than or equal to " + str(StandardValues.colorChars)
        assert len(model) <= StandardValues.modelChars and model != "",  "Model must be less than or equal to " + str(StandardValues.modelChars)
    except AssertionError as ae:
        Error.error_window(ae.__str__())
        return -1
    except ValueError as ve:
        Error.error_window(ve.__str__())
        return -1

    return 0
