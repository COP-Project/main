from dbCommands import *
from StandardValues import Error
import sys


# User class. dbCommands creates an object that stores our currnet connected user
# This information is sent to PlateRecMain which determines permissions
class Users:
    def __init__(self, username, data_access):
        self.data_access = data_access

        try:
            name = self.find_user(username)

            self.passport = Passport(name[0][0], name[0][1], name[0][2], name[0][3])
        except AttributeError as ae:
            Error.error_window("Could not retrieve account information")
            sys.exit(-1)

    # returns the information, used by dbCommands and is called by PlateRecMain
    def get_user_info(self):
        return self.passport

    # searches the user table in the database for the user login that has connected.
    # this function is used to determine user permissions ADMIN or NON-ADMIN
    def find_user(self, login_name):
        try:
            self.data_access.cursor.execute("SELECT * FROM users WHERE (loginname = %s)", login_name)
            rows = self.data_access.cursor.fetchall()

            if self.data_access.cursor.rowcount <= 0:
                raise PermissionError()

            return rows

        except AttributeError as ae:
            Error.error_window("No database connection")
            return ae
        except PermissionError as pe:
            Error.error_window("Invalid username")
            return pe
        except OSError as os:
            Error.error_window("Problem with access to database")
            return os


class Passport:
    def __init__(self, fname, lname, login, access):
        self.firstName = fname
        self.lastName = lname
        self.loginName = login
        self.access = access

    def __getitem__(self, item):
        return str(item)
