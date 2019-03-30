from dbCommands import *


# User class. dbCommands creates an object that stores our currnet connected user
# This information is sent to PlateRecMain which determines permissions
class Users:
    # sets the information stored in the users table in the database
    # dbCommands runs the search by login name, which will be unique
    # it then passes the information as a list(tuple)
    def setUser(self, name):
        global firstName
        global lastName
        global loginName
        global access
        firstName = name[0][0]
        lastName = name[0][1]
        loginName = name[0][2]
        access = name[0][3]

    # returns the information, used by dbCommands and is called by PlateRecMain
    def getUserInfo(self):
        user_list = [firstName, lastName, loginName, access]
        return user_list
