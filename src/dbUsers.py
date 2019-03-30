from dbCommands import *


# User class. dbCommands creates an object that stores our currnet connected user
# This information is sent to PlateRecMain which determines permissions
class Users:
    def __init__(self, name, data_access):
        self.passport = Passport(name[0][0], name[0][1], name[0][2], name[0][3])
        self.data_access = data_access

    # returns the information, used by dbCommands and is called by PlateRecMain
    def getUserInfo(self):
        return self.passport


class Passport:
    def __init__(self, fname, lname, login, access):
        self.firstName = fname
        self.lastName = lname
        self.loginName = login
        self.access = access

    def __getitem__(self, item):
        return str(item)
