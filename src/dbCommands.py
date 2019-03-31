import pymysql.cursors
import sys
import dbUsers
from login import Login
from StandardValues import StandardValues, Error


class DataAccess:
    # data bas info, it needs to match either your local mysql server
    # ---command to CREATE TABLE poopproject.drivers(fname VARCHAR(20),
    # lname VARCHAR(20), address VARCHAR(20),zipcod VARCHAR(5),state VARCHAR(2),
    # platenum VARCHAR(12), carmake VARCHAR(20), color VARCHAR(20), model VARCHAR(20), priority VARCHAR(3));
    # or the AWS server

    def __init__(self, username, password):
        self.conn = self.conn(username, password)
        self.cursor = self.conn.cursor()
        self.user = dbUsers.Users(self.findUser(username), self)

    # database self.connection and login screen########################
    def conn(self, username, password):
        # uses the inputs from the user to log in
        try:
            # self.connection to AWS database
            new_conn = pymysql.connect(host='copproject.cveza4dgo3d2.us-east-2.rds.amazonaws.com', port=3306,
                                       user=username,
                                       passwd=password, db='poopproject')

            # self.connection to local db database
            # OFF###conn=pymysql.connect(host='127.0.0.1',port=3312,user=username,passwd=password,db='poopproject')
            return new_conn
        except:
            Error.error_window("Could not connect to database")

    # Searches by Zip or Plate Depeding on paramater from searchZipPlateInpScreen()
    def searchZipPlate(self, string, value):
        # check for empty string.
        if value == "":
            Error.error_window("Please Enter a " + string)
            return ""
        # check if we are searching by zip
        if string == "zip":
            label = "Zip Code"
            self.cursor.execute("SELECT * FROM drivers WHERE (zipcod = %s)", value)
            rows = self.cursor.fetchall()
        # checks if we are searching by plate number
        if string == "plate":
            label = "Plate Number"
            self.cursor.execute("SELECT * FROM drivers WHERE (platenum = %s)", value)
            rows = self.cursor.fetchall()
        # return rows which is passed to displaySearch

        return rows
        # displaySearch(rows)

    # functionality to search and display all drivers in the data base by first and last name
    def searchDriverFirstLastName(self, fname, lname):

        if fname == "" or lname == "":
            Error.error_window("Please Enter a first and last name. ")
            return ""

        try:
            self.cursor.execute("SELECT * FROM drivers WHERE (fname = %s and lname = %s)", (fname, lname))
            rows = self.cursor.fetchall()

            # displaySearch(rows)
            return rows
        except Error as e:
            print(e)

    def check_input(self, fname, lname, address, zipcode, state, platenum, make, color, model, priority):
        # REads in each value from the text box and checks if the value is valid for the DB#################
        # and check if all fields fall within the valid Database character length TRY TO REFACTOR

        if len(fname) > StandardValues.firstNameChars:
            Error.error_window("First Name must be less than or equal to " + str(StandardValues.firstNameChars))
            return -1

        if len(lname) > StandardValues.lastNameChars:
            Error.error_window("Last Name must be less than or equal to " + str(StandardValues.lastNameChars))
            return -1

        if len(address) > StandardValues.addressChars:
            Error.error_window("Address must be less than or equal to " + str(StandardValues.addressChars))
            return -1

        # check length of zip
        if len(zipcode) != 5:
            Error.error_window("Zip code should be 5 numbers")
            return -1

        if len(platenum) != StandardValues.plateNumChars:
            Error.error_window("Plate number must be " + str(StandardValues.plateNumChars) + " characters.")
            return -1

        if len(make) > StandardValues.addressChars:
            Error.error_window("Car Make must be less than or equal to " + str(StandardValues.carmakeChars))
            return -1

        if len(color) > StandardValues.colorChars:
            Error.error_window("Color must be less than or equal to " + str(StandardValues.colorChars))
            return -1

        if len(model) > StandardValues.modelChars:
            Error.error_window("Model must be less than or equal to " + str(StandardValues.modelChars))
            return -1

        # checks if any fields are empty
        if fname == "" or lname == "" or address == "" or platenum == "" or make == "" or color == "" or model == "" or priority == "" or zipcode == "" or state == "":
            Error.error_window("All fields must be completed.")
            return -1

        return 0
        
    # the logic to to read in all the text boxes from callAddDrivers() probably way to many paramaters
    # REFACTOR in the future to group boxes into a object and pass object
    def addDriver(self, fname, lname, address, zipcode, state, platenum, make, color, model, priority):
        error = self.check_input(fname, lname, address, zipcode, state, platenum, make, color, model, priority)

        if error == -1:
            return

        # plate number duplication
        if self.plateCheck(platenum) == 1:
            Error.error_window("Duplicate License Plate Number")
            return -1

        # runs query against database
        addDriver = ("INSERT INTO drivers"
                     "(fname, lname,address,zipcod,state,platenum,carmake,color,model,priority)"
                     "VALUES (%s, %s,%s,%s,%s, %s,%s,%s,%s,%s)")
        # execute query
        dataDriver = (fname, lname, address, zipcode, state, platenum, make, color, model, priority)
        self.cursor.execute(addDriver, dataDriver)

        self.conn.commit()
        # self.cursorclose()

    # reads text entry boxes
    def read_textbox(self, tbox):
        return tbox.get()

    # deletes a driver
    def deleteDriver(self, plate):
        rows = ("DELETE FROM drivers WHERE platenum = %s")
        self.cursor.execute(rows, plate)
        self.conn.commit()

    # checks for duplicate plates upon  data entry into the DB
    def plateCheck(self, stringIn):
        self.cursor.execute("SELECT * FROM drivers")
        rows = self.cursor.fetchall()

        for row in rows:

            if stringIn == row[5]:
                return 1

    def editDriverRequest(self, platenum_old, fname, lname, address, zipcode, state, platenum_new, make, color, model, priority):
        error = self.check_input(fname, lname, address, zipcode, state, platenum_new, make, color, model, priority)

        if error == -1:
            return

        edit_driver = ("UPDATE drivers "
                       "SET fname = %s, lname = %s, address = %s, zipcod = %s, state = %s, "
                       "platenum = %s, carmake = %s, color = %s, model = %s, priority = %s "
                       "WHERE platenum = %s ")

        data_driver = (fname, lname, address, zipcode, state, platenum_new, make, color, model, priority, platenum_old)
        self.cursor.execute(edit_driver, data_driver)

        self.conn.commit()

    def scan_license_plate(self, img):
        print("Hello")

    # searches the user table in the database for the user login that has self.connected.
    # this fucntion is used to determine user permissions ADMIN or NON-ADMIN
    def findUser(self, login_name):
        try:
            self.cursor.execute("SELECT * FROM users WHERE (loginname = %s)", login_name)
            rows = self.cursor.fetchall()
            return rows
        except Error as e:
            print(e)
            Error.error_window("Not a valid user.")
            sys.exit()

    # returns the user info from dbUser.py object >>thisUser
    def getUser(self):
        return self.user

    def logOut(self):
        self.conn.close()

