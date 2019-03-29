import pymysql.cursors
from tkinter import *
from tkinter import ttk
import tkinter as tk
import dbUsers

# data bas info, it needs to match either your local mysql server
# ---command to CREATE TABLE poopproject.drivers(fname VARCHAR(20), lname VARCHAR(20), address VARCHAR(20),zipcod VARCHAR(5),state VARCHAR(2),
# platenum VARCHAR(12), carmake VARCHAR(20), color VARCHAR(20), model VARCHAR(20), priority VARCHAR(3));
# or the AWS server

# Database constants
# This must be set to the values in the data base fields to prevent errors
firstNameChars=20
lastNameChars=20
addressChars=20
carmakeChars=20
plateNumChars=7
colorChars=20
modelChars=20

def login(usernameTB,passwordTB):
    global username
    global password
    username=read_textbox(usernameTB)
    password=read_textbox(passwordTB)
    
# Searches by Zip or Plate Depeding on paramater from searchZipPlateInpScreen()
def searchZipPlate(string,textfield):
    zipOrPlate=read_textbox(textfield)
    
    # check for empty string. 
    if zipOrPlate=="":
        errorWindow("Please Enter a " + string)
        return ""
    # check if we are searching by zip
    if string =="zip":
        label="Zip Code"
        cursor.execute("SELECT * FROM drivers WHERE (zipcod = %s)",(zipOrPlate,))
        rows = cursor.fetchall()
     # checks if we are searching by plate number   
    if string =="plate":
        label="Plate Number"
        cursor.execute("SELECT * FROM drivers WHERE (platenum = %s)",(zipOrPlate,))
        rows = cursor.fetchall()
    # return rows which is passed to displaySearch
    
    return rows
    # displaySearch(rows)
    
# functionality to search and display all drivers in the data base by first and last name   
def searchDriverFirstLastName(fname,lname):

        firstName=read_textbox(fname)
        lastName=read_textbox(lname)
        
       
        if firstName == "" or lastName=="":
            errorWindow("Please Enter a first and last name. ")
            return ""
        
        try:
            cursor.execute("SELECT * FROM drivers WHERE (fname = %s and lname = %s)",(firstName,lastName,))
            rows = cursor.fetchall()
 
            # displaySearch(rows)
            return rows
        except Error as e:
            print(e)

def close_window():
    mainWindow.destroy()

# the logic to to read in all the text boxes from callAddDrivers() probably way to many paramaters
# REFACTOR in the future to group boxes into a object and pass object
def addDriver (firstNameTextBox, lastNameTextBox, streetAddressTextBox,
             zipCodeTextBox, stateTextBox, plateNumberTextBox,
             carMakeTextBox, colorTextBox, modelTextBox,
             priorityTextBox, addDriverWindow):

    # REads in each value from the text box and checks if the value is valid for the DB#################
    # and check if all fields fall within the valid Database character length TRY TO REFACTOR
    fname=read_textbox(firstNameTextBox).upper()
    if len(fname)>firstNameChars:
        errorWindow("First Name must be less than or equal to " + str(firstNameChars))
        return
    
    lname=read_textbox(lastNameTextBox).upper()
    if len(lname)>lastNameChars:
        errorWindow("Last Name must be less than or equal to " + str(lastNameChars))
        return
    
    address=read_textbox(streetAddressTextBox).upper()
    if len(address)>addressChars:
        errorWindow("Address must be less than or equal to " + str(addressChars))
        return
    
    zipcode=read_textbox(zipCodeTextBox).upper()
    # check length of zip
    if len(zipcode) != 5:
        errorWindow("Zip code should be 5 numbers")
        return
    
    state=read_textbox(stateTextBox).upper()
        # no error check, this will be implemented as a drop down
    
    platenum=read_textbox(plateNumberTextBox).upper()
    if len(platenum)!=plateNumChars:
        errorWindow("Plate number must be " + str(plateNumChars)+" characters.")
        return

    carmake=read_textbox(carMakeTextBox).upper()
    if len(carmake)>addressChars:
        errorWindow("Car Make must be less than or equal to " + str(carmakeChars))
        return
    
    color=read_textbox(colorTextBox).upper()
    if len(color)>colorChars:
        errorWindow("Color must be less than or equal to " + str(colorChars))
        return
    model=read_textbox(modelTextBox).upper()
    if len(model)>modelChars:
        errorWindow("Model must be less than or equal to " + str(modelChars))
        return
                    
    priority=read_textbox(priorityTextBox).upper()
    # no error, this will be impletmented as a drop down
   
    # plate number duplication
    if plateCheck(platenum)==1:
        errorWindow("Duplicate License Plate Number")
        return
    
    # checks if any fields are empty
    if fname =="" or lname =="" or address =="" or platenum =="" or carmake =="" or color =="" or model =="" or priority =="" or zipcode =="" or state =="":
        errorWindow("All fields must be completed.")
        return
    # End of field check#################################################
        
    # runs query against database
    addDriver=("INSERT INTO drivers"
                "(fname, lname,address,zipcod,state,platenum,carmake,color,model,priority)"
                "VALUES (%s, %s,%s,%s,%s, %s,%s,%s,%s,%s)")
    # execute query
    dataDriver = (fname, lname, address,zipcode,state,platenum,carmake,color,model,priority)
    cursor.execute(addDriver,dataDriver)

    conn.commit()
    # cursor.close()
    addDriverWindow.destroy()

# reads text entry boxes  
def read_textbox(tbox):
    return tbox.get()

# deletes a driver
def deleteDriver(plate):
    
    plateNum=read_textbox(plate)
    rows=("DELETE FROM drivers WHERE platenum = %s")
    cursor.execute(rows,(plateNum),)
    conn.commit()

# checks for duplicate plates upon  data entry into the DB
def plateCheck(stringIn):

    cursor.execute("SELECT * FROM drivers")
    rows = cursor.fetchall()

    for row in rows:
                
                if stringIn==row[5]:
                    return 1

# error window and prints it in a pop up window
def errorWindow(stringIn):
    errorWindow = Toplevel()
    errorWindow.geometry("500x200")
    errorWindow.winfo_toplevel().title("Error!!")
    errorLabel=Label(errorWindow, text="Error "+ stringIn)
    errorLabel.pack()
    okBtn = ttk.Button(errorWindow, text="OK",command= errorWindow.destroy)
    okBtn.pack()


# EDIT DRIVER IS IN PROGRESS
def editDriverRequest(plate):
    print("Hello")


# searches the user table in the database for the user login that has connected.
# this fucntion is used to determine user permissions ADMIN or NON-ADMIN
def findUser(loginName):
             
        try:
            cursor.execute("SELECT * FROM users WHERE (loginname = %s)",(loginName,))
            rows = cursor.fetchall()
            return rows
        except:
            errorWindow("Not a valid user.")
            sys.exit()

# returns the user info from dbUser.py object >>thisUser
def getUserInfo():
    return thisUser.getUserInfo()

def logOut():
    conn.close()
# database connection and login screen########################


# gloval variables
global username
username=""

global password
password=""

# set login screen
root = tk.Tk()
root.withdraw() # won't need this
loginScrn = Toplevel()
loginScrn.configure(background="white")
loginScrn.geometry("550x100")
loginScrn.winfo_toplevel().title("User Login")

# seet username and pw text boxes and labels
usernameLabel=Label(loginScrn,bg="white", text="User Name")
usernameLabel.grid(row=1,column=0)
usernameTextBox=Entry(loginScrn)
usernameTextBox.grid(row=1,column=1,padx=20)

pwLabel=Label(loginScrn,bg="white", text="Password")
pwLabel.grid(row=2,column=0)
pwTextBox=Entry(loginScrn)
pwTextBox.grid(row=2,column=1,padx=20)

var=tk.IntVar()  # variable use to pause until the submitbutton is pressed
submitBtn = Button(loginScrn,bg="black",fg="white", text="Submit",command= lambda:  [var.set(1),login(usernameTextBox,pwTextBox),loginScrn.destroy()])

submitBtn.grid(row=1,column=3,padx=15)
submitBtn.wait_variable(var)#wait

# uses the inputs from the user to log in
try:
    # connection to AWS database
    conn=pymysql.connect(host='copproject.cveza4dgo3d2.us-east-2.rds.amazonaws.com',port=3306,user=username,passwd=password,db='poopproject')
   
    # connection to local db database
    # OFF###conn=pymysql.connect(host='127.0.0.1',port=3312,user=username,passwd=password,db='poopproject')
    cursor = conn.cursor()
except:
    errorWindow("Could Not connect to Database")
    sys.exit()

# look up user to access their information for permissions
userInfo=findUser(username)
# creates the object in the dbUsers
thisUser=dbUsers.Users()
# set the users info, this is used to grant permissions
thisUser.setUser(userInfo)





