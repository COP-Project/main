from dbCommands import *
from StandardValues import Error
import sys


# User class. dbCommands creates an object that stores our currnet connected user
# This information is sent to PlateRecMain which determines permissions
class Users:
    def __init__(self, username, data_access):
        self.data_access = data_access

        name = self.findUser(username)
        self.passport = Passport(name[0][0], name[0][1], name[0][2], name[0][3])

    # returns the information, used by dbCommands and is called by PlateRecMain
    def getUserInfo(self):
        return self.passport

    # searches the user table in the database for the user login that has self.connected.
    # this fucntion is used to determine user permissions ADMIN or NON-ADMIN
    def findUser(self, login_name):
        try:
            self.data_access.cursor.execute("SELECT * FROM users WHERE (loginname = %s)", login_name)
            rows = self.data_access.cursor.fetchall()

            if self.data_access.cursor.rowcount <= 0:
                raise Exception()

            return rows
        except:
            Error.error_window("Invalid username")
            sys.exit()


class Passport:
    def __init__(self, fname, lname, login, access):
        self.firstName = fname
        self.lastName = lname
        self.loginName = login
        self.access = access

    def __getitem__(self, item):
        return str(item)
