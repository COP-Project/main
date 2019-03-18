import pymysql.cursors
from tkinter import *
from tkinter import ttk
import tkinter as tk
from dbCommands import *

#################search by zip or plate or display all high priority
def searchZipPlateInpScreen(string):

    #are we searching by zip or plate?
    if string =="zip":
        label="Zip Code"
        
    if string =="plate":
        label="Plate Number"
        
     #set plate zip window   
    searchZipPlatescreen = tk.Tk()
    searchZipPlatescreen.configure(background="white")
    searchZipPlatescreen.winfo_toplevel().title("Search Driver By" + label)
    searchZipPlatescreen.geometry("350x100")
    
    #variable text box AND LABEL
    
    addLabel(label,0,0,searchZipPlatescreen)
    zipPlateLblTextBox=Entry(searchZipPlatescreen)
    zipPlateLblTextBox.grid(row=0,column=1,padx=20)

    #button displaysSearch() from string returned by searchZipPlate()
    searchZipPlateBtn = Button(searchZipPlatescreen,bg="black",fg="white", text="Search",command= lambda:
                               [displaySearch(searchZipPlate(string,zipPlateLblTextBox))])
    
    searchZipPlateBtn.grid(row=0,column=3,padx=20)
########################searches by first and last name
def searchLastNameIntScreen():
    searchLMscreen = tk.Tk()
    searchLMscreen.configure(background="white")
    searchLMscreen.winfo_toplevel().title("Search Driver By Name")
    searchLMscreen.geometry("250x200")

    #text boxes and buttons
    #FIRST NAME LABEL AND BOX
    addLabel("First Name",0,0,searchLMscreen)
    schfNameTextBox=Entry(searchLMscreen)
    schfNameTextBox.grid(row=0,column=1,padx=20)
    #LAST NAME LABEL AND BOX
    addLabel("Last Name",1,0,searchLMscreen)
    schLNameTextBox=Entry(searchLMscreen)
    schLNameTextBox.grid(row=1,column=1,padx=20)

    searchNameDriverBtn = Button(searchLMscreen, text="Search",bg="black",fg="white",command= lambda:
                                 [displaySearch(searchDriverFirstLastName(schfNameTextBox,schLNameTextBox))])
    
    searchNameDriverBtn.grid(row=2,column=0,padx=20)

####sets up window for driver inputs calls addDrivers() 
def callAddDrivers():
      #creates window
    addDriverWindow = Toplevel()
    addDriverWindow.configure(background="white")
    addDriverWindow.geometry("400x400")
    addDriverWindow.winfo_toplevel().title("New Driver Entry")

    padding=20

    #text boxes and buttons
    #FIRST NAME LABEL AND BOX
    addLabel("First Name",0,0,addDriverWindow)
    #firstNameLabel.pack()
    #v=StringVar(addDriverWindow, value="tesssstt")
    firstNameTextBox=Entry(addDriverWindow)#textvariable=v
    firstNameTextBox.grid(row=0,column=1,padx=padding)
    #LAST NAME LABEL AND BOX
    addLabel("Last Name",1,0,addDriverWindow)
    lastNameTextBox=Entry(addDriverWindow)
    lastNameTextBox.grid(row=1,column=1,padx=padding)
    #Streetname/ address
    addLabel("Address",2,0,addDriverWindow)
    streetAddressTextBox=Entry(addDriverWindow)
    streetAddressTextBox.grid(row=2,column=1,padx=padding)
    #Zip Code
    
    addLabel("Zip Code",3,0,addDriverWindow)
    zipCodeTextBox=Entry(addDriverWindow)
    zipCodeTextBox.grid(row=3,column=1,padx=padding)
    #State
    
    addLabel("State",4,0,addDriverWindow)
    stateTextBox=Entry(addDriverWindow)
    stateTextBox.grid(row=4,column=1,padx=padding)
    #platenumber
    addLabel("Plate #",5,0,addDriverWindow)
    plateNumberTextBox=Entry(addDriverWindow,state=NORMAL)
    plateNumberTextBox.grid(row=5,column=1,padx=padding)
    
    
    #car make
    addLabel("Car Make",6,0,addDriverWindow)
    carMakeTextBox=Entry(addDriverWindow)
    carMakeTextBox.grid(row=6,column=1,padx=padding)
    #model
    addLabel("Model",7,0,addDriverWindow)
    modelTextBox=Entry(addDriverWindow)
    modelTextBox.grid(row=7,column=1,padx=padding)
    #Color
    addLabel("Color",8,0,addDriverWindow)
    colorTextBox=Entry(addDriverWindow)
    colorTextBox.grid(row=8,column=1,padx=padding)
    
    #priority
    addLabel("High Priority?",9,0,addDriverWindow)
    priorityTextBox=Entry(addDriverWindow)
    priorityTextBox.grid(row=9,column=1,padx=padding)

    #save button
    saveUserBtn = Button(addDriverWindow, bg="black",fg="white", text="Save")
    saveUserBtn.grid(row=11,column=0,pady=30,padx=30)
    #save button action, runs addUser and then calls closeHomeWindow to close the top lvl window
    #NOTE: Removed closeWindowHome() from button. This was causing the window to close even if a blank text box was passed.
    #Passing the addDRiverWindow in addUser() instead for a fix.<<<<REFACTOR
    
    saveUserBtn.config(command=lambda: addDriver(firstNameTextBox,lastNameTextBox,
                                                    streetAddressTextBox,zipCodeTextBox,stateTextBox,plateNumberTextBox,carMakeTextBox,
                                                   colorTextBox,modelTextBox,priorityTextBox,addDriverWindow))
    
#pop up screen to delete a driver
def delDriverScreen():

    #creates window 
    delDriverScrn = Toplevel()
    delDriverScrn.configure(background="white")
    delDriverScrn.geometry("550x100")
    delDriverScrn.winfo_toplevel().title("Delete Driver")

    #label and text box
    submitLabel=Label(delDriverScrn,bg="white", text="Please Enter the Driver's plate number you wish to delete.")
    submitLabel.grid(row=1,column=0)
    submitTextBox=Entry(delDriverScrn)
    submitTextBox.grid(row=1,column=1,padx=20)

    #delete button
    delSubmitBtn = Button(delDriverScrn,bg="black",fg="white", text="Submit")
    delSubmitBtn.grid(row=1,column=3,padx=15)

    #delete button functionality
    delSubmitBtn.config(command=lambda: [deleteDriver(submitTextBox),delDriverScrn.destroy()])    

#function to add a label to a window
def addLabel(stringIn,rowIn,colIn,window):
    plateNumberLabel=Label(window, bg="white", text=stringIn)
    plateNumberLabel.grid(row=rowIn,column=colIn)

#displays the search results in a new window            
def displaySearch(rows):
    n=2
    y=0
    if rows == "":
        return
    #set up window
    displayZipPlatescreen = tk.Tk()
    displayZipPlatescreen.configure(background="white")
    displayZipPlatescreen.winfo_toplevel().title("Search Results")
    displayZipPlatescreen.geometry("700x400")

    #loop to print the header to the window
    header=("First Name","Last Name","Street","Zip Code","State","Plate","Make","Color","Model","Priority")
    for top in header:
        headerRow=Label(displayZipPlatescreen, text=header[y],bg="white")
        headerRow.grid(row=0, column=y,padx=3)
        y=y+1

    #loop to print the data pulled from the database
    for row in rows:
                i=0
                #newString= row[0] +'\t'+ row[1] +'\t'+ row[2]+'\t'+ row[3] + '\t' + row[4] + '\t' + row[5] + '\t' + row[6] + '\t' + row[7]+ '\t' + row[8] + '\t' + row[9]
                for line in row:
                    searchRow=Label(displayZipPlatescreen, text=row[i],bg="white")
                    searchRow.grid(row=n, column=i,padx=3)
                    i=i+1
                searchRow.grid(row=n, column=i)
                n=n+1


   #addes the delete button to the bottom of the search window
    deleteBtn = Button(displayZipPlatescreen,bg="black",fg="white", text="Delete Driver",command= lambda:  [delDriverScreen()])
    editBtn = Button(displayZipPlatescreen,bg="black",fg="white", text="Edit Driver",command= lambda:[print("implement")])#implement
    deleteBtn.grid(row=n+3,column=3)
    editBtn.grid(row=n+4,column=3)
