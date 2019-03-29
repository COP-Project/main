import pymysql.cursors
from tkinter import *
from tkinter import ttk
import tkinter as tk
import dbUsers
from login import Login
from StandardValues import StandardValues, Error

# data bas info, it needs to match either your local mysql server
# ---command to CREATE TABLE poopproject.drivers(fname VARCHAR(20), lname VARCHAR(20), address VARCHAR(20),zipcod VARCHAR(5),state VARCHAR(2),
# platenum VARCHAR(12), carmake VARCHAR(20), color VARCHAR(20), model VARCHAR(20), priority VARCHAR(3));
# or the AWS server

# Searches by Zip or Plate Depeding on paramater from searchZipPlateInpScreen()
def searchZipPlate(string, textfield):
    zipOrPlate = read_textbox(textfield)

    # check for empty string. 
    if zipOrPlate == "":
        Error.error_window("Please Enter a " + string)
        return ""
    # check if we are searching by zip
    if string == "zip":
        label = "Zip Code"
        cursor.execute("SELECT * FROM drivers WHERE (zipcod = %s)", (zipOrPlate,))
        rows = cursor.fetchall()
    # checks if we are searching by plate number
    if string == "plate":
        label = "Plate Number"
        cursor.execute("SELECT * FROM drivers WHERE (platenum = %s)", (zipOrPlate,))
        rows = cursor.fetchall()
    # return rows which is passed to displaySearch

    return rows
    # displaySearch(rows)


# functionality to search and display all drivers in the data base by first and last name   
def searchDriverFirstLastName(fname, lname):
    firstName = read_textbox(fname)
    lastName = read_textbox(lname)

    if firstName == "" or lastName == "":
        Error.error_window("Please Enter a first and last name. ")
        return ""

    try:
        cursor.execute("SELECT * FROM drivers WHERE (fname = %s and lname = %s)", (firstName, lastName,))
        rows = cursor.fetchall()

        # displaySearch(rows)
        return rows
    except Error as e:
        print(e)


def close_window():
    mainWindow.destroy()


# the logic to to read in all the text boxes from callAddDrivers() probably way to many paramaters
# REFACTOR in the future to group boxes into a object and pass object
def addDriver(fname, lname, address, zipcode, state, platenum, make, color, model, priority, addDriverWindow):
    stdvalues = StandardValues()

    # REads in each value from the text box and checks if the value is valid for the DB#################
    # and check if all fields fall within the valid Database character length TRY TO REFACTOR

    if len(fname) > stdvalues.firstNameChars:
        Error.error_window("First Name must be less than or equal to " + str(stdvalues.firstNameChars))
        return

    if len(lname) > stdvalues.lastNameChars:
        Error.error_window("Last Name must be less than or equal to " + str(stdvalues.lastNameChars))
        return

    if len(address) > stdvalues.addressChars:
        Error.error_window("Address must be less than or equal to " + str(stdvalues.addressChars))
        return

    # check length of zip
    if len(zipcode) != 5:
        Error.error_window("Zip code should be 5 numbers")
        return

    # no error check, this will be implemented as a drop down

    if len(platenum) != stdvalues.plateNumChars:
        Error.error_window("Plate number must be " + str(stdvalues.plateNumChars) + " characters.")
        return

    if len(make) > stdvalues.addressChars:
        Error.error_window("Car Make must be less than or equal to " + str(stdvalues.carmakeChars))
        return

    if len(color) > stdvalues.colorChars:
        Error.error_window("Color must be less than or equal to " + str(stdvalues.colorChars))
        return

    if len(model) > stdvalues.modelChars:
        Error.error_window("Model must be less than or equal to " + str(stdvalues.modelChars))
        return

    # no error, this will be impletmented as a drop down

    # plate number duplication
    if plateCheck(platenum) == 1:
        Error.error_window("Duplicate License Plate Number")
        return

    # checks if any fields are empty
    if fname == "" or lname == "" or address == "" or platenum == "" or make == "" or color == "" or model == "" or priority == "" or zipcode == "" or state == "":
        Error.error_window("All fields must be completed.")
        return
    # End of field check#################################################

    # runs query against database
    addDriver = ("INSERT INTO drivers"
                 "(fname, lname,address,zipcod,state,platenum,carmake,color,model,priority)"
                 "VALUES (%s, %s,%s,%s,%s, %s,%s,%s,%s,%s)")
    # execute query
    dataDriver = (fname, lname, address, zipcode, state, platenum, make, color, model, priority)
    cursor.execute(addDriver, dataDriver)

    conn.commit()
    # cursor.close()


# reads text entry boxes
def read_textbox(tbox):
    return tbox.get()


# deletes a driver
def deleteDriver(plate):
    rows = ("DELETE FROM drivers WHERE platenum = %s")
    cursor.execute(rows, plate)
    conn.commit()


# checks for duplicate plates upon  data entry into the DB
def plateCheck(stringIn):
    cursor.execute("SELECT * FROM drivers")
    rows = cursor.fetchall()

    for row in rows:

        if stringIn == row[5]:
            return 1


# EDIT DRIVER IS IN PROGRESS
def editDriverRequest(plate):
    print("Hello")


# searches the user table in the database for the user login that has connected.
# this fucntion is used to determine user permissions ADMIN or NON-ADMIN
def findUser(loginName):
    try:
        cursor.execute("SELECT * FROM users WHERE (loginname = %s)", (loginName,))
        rows = cursor.fetchall()
        return rows
    except:
        Error.error_window("Not a valid user.")
        sys.exit()


# returns the user info from dbUser.py object >>thisUser
def getUserInfo():
    return thisUser.getUserInfo()


def logOut():
    conn.close()


# database connection and login screen########################
def conn():
    # uses the inputs from the user to log in
    try:
        # connection to AWS database
        new_conn = pymysql.connect(host='copproject.cveza4dgo3d2.us-east-2.rds.amazonaws.com', port=3306, user=username,
                               passwd=password, db='poopproject')

        # connection to local db database
        # OFF###conn=pymysql.connect(host='127.0.0.1',port=3312,user=username,passwd=password,db='poopproject')
        return new_conn
    except:
        Error.error_window("Could not connect to database")
        sys.exit()


# gloval variables
global username
username = ""

global password
password = ""

login_scrn = Login()
login_scrn.create_window()

username = login_scrn.username
password = login_scrn.password

conn = conn()
cursor = conn.cursor();

# look up user to access their information for permissions
userInfo = findUser(username)
# creates the object in the dbUsers
thisUser = dbUsers.Users()
# set the users info, this is used to grant permissions
thisUser.setUser(userInfo)
