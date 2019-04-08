import pymysql.cursors
import sys
import dbUsers
from StandardValues import StandardValues, Error
from readPlate import read_a_plate
from openalpr import Alpr
from twilio.rest import Client


class DataAccess:
    # data bas info, it needs to match either your local mysql server
    # ---command to CREATE TABLE poopproject.drivers(fname VARCHAR(20),
    # lname VARCHAR(20), address VARCHAR(20),zipcod VARCHAR(5),state VARCHAR(2),
    # platenum VARCHAR(12), carmake VARCHAR(20), color VARCHAR(20), model VARCHAR(20), priority VARCHAR(3));
    # or the AWS server

    def __init__(self, username, password):
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

            return new_conn
        except pymysql.OperationalError as oe:
            Error.error_window("Could not connect to database")
            print(oe)
            return pymysql.OperationalError

    def search_driver(self, driver_data, priority_changed):
        cursor = self.conn.cursor()
        filter_str = ""

        # build filter AND clauses
        if driver_data[0] != "" and len(driver_data[0]) <= StandardValues.firstNameChars:
            filter_str = filter_str + " AND fname = '{}'".format(driver_data[0])

        if driver_data[1] != "" and len(driver_data[1]) <= StandardValues.lastNameChars:
            filter_str = filter_str + " AND lname = '{}'".format(driver_data[1])

        if driver_data[2] != "" and len(driver_data[2]) <= StandardValues.addressChars:
            filter_str = filter_str + " AND address = '{}'".format(driver_data[2])

        if driver_data[3] != "":
            filter_str = filter_str + " AND zipcod = '{}'".format(driver_data[3])

        if driver_data[4] != "" and driver_data[4] != "PLEASE SELECT":
            filter_str = filter_str + " AND state = '{}'".format(driver_data[4])

        if driver_data[5] != "" and len(driver_data[5]) <= StandardValues.plateNumChars:
            filter_str = filter_str + " AND platenum = '{}'".format(driver_data[5])

        if driver_data[6] != "" and len(driver_data[6]) <= StandardValues.carmakeChars:
            filter_str = filter_str + " AND carmake = '{}'".format(driver_data[6])

        if driver_data[7] != "" and len(driver_data[7]) <= StandardValues.colorChars:
            filter_str = filter_str + " AND color = '{}'".format(driver_data[7])

        if driver_data[8] != "" and len(driver_data[8]) <= StandardValues.modelChars:
            filter_str = filter_str + " AND model = '{}'".format(driver_data[8])

        if driver_data[9] != "" and priority_changed:
            value = 1 if driver_data[9] == True else 0
            filter_str = filter_str + " AND priority = {}".format(value)

        filter_driver = ("SELECT "
                         "fname, lname, address, zipcod, state, platenum, carmake, color, model, "
                         "(CASE WHEN priority = 0 THEN 0 ELSE 1 end) as priority "
                         " FROM drivers "
                         "WHERE 1 = 1 " + filter_str + " ;")

        cursor.execute(filter_driver)

        results = cursor.fetchall()

        cursor.close()
        return results

    # the logic to to read in all the text boxes from calladd_drivers() probably way to many paramaters
    # REFACTOR in the future to group boxes into a object and pass object
    def add_driver(self, driver_data):
        cursor = self.conn.cursor()
        error = check_input(driver_data)

        if error == -1:
            return -1

        # plate number duplication
        if self.plate_check(driver_data[5]) == 1:
            Error.error_window("Duplicate License Plate Number")
            return -1

        cursor = self.conn.cursor()

        # runs query against database
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")
        # execute query
        cursor.execute(add_driver, driver_data)

        self.conn.commit()
        cursor.close()

    # deletes a driver
    def delete_driver(self, plate):
        cursor = self.conn.cursor()
        rows = "DELETE FROM drivers WHERE platenum = %s"
        cursor.execute(rows, plate)
        self.conn.commit()
        cursor.close()

    # checks for duplicate plates upon  data entry into the DB
    def plate_check(self, string_in):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM drivers WHERE platenum = %s ", string_in)
        rowcount = cursor.rowcount
        cursor.close()

        return 1 if (rowcount == 1) else 0

    def edit_driver_request(self, data_driver, platenum_old):
        cursor = self.conn.cursor()
        error = check_input(data_driver)

        if error == -1:
            return -1

        edit_driver = ("UPDATE drivers "
                       "SET fname = %s, lname = %s, address = %s, zipcod = %s, state = %s, "
                       "platenum = %s, carmake = %s, color = %s, model = %s, priority = %s "
                       "WHERE platenum = %s ")

        edit_data_driver = (data_driver[0],
                            data_driver[1],
                            data_driver[2],
                            data_driver[3],
                            data_driver[4],
                            data_driver[5],
                            data_driver[6],
                            data_driver[7],
                            data_driver[8],
                            data_driver[9],
                            platenum_old)

        cursor.execute(edit_driver, edit_data_driver)

        self.conn.commit()
        cursor.close()

    def scan_license_plate(self, img, state):
        test_file = check_file_input(img)
        test_openalpr = check_openalpr()
        if test_file == -1 or test_openalpr == -1:
            return -1

        plates = read_a_plate(img, state.lower())
        for eachplate in plates:
            driver = self.get_driver_by_plate(eachplate)
            self.send_alert(driver) if driver is not None else []

    def get_driver_by_plate(self, plate):
        cursor = self.conn.cursor()
        if plate == "" or len(plate) > 7:
            return None

        get_driver = " SELECT * FROM drivers WHERE platenum = %s; "

        cursor.execute(get_driver, plate)
        driver = cursor.fetchone()

        if cursor.rowcount < 1:
            return None

        cursor.close()
        return driver

    def send_alert(self, driver):
        alert_body = ("CAR RECOGNIZED: " + driver[6].title() + " " + driver[8].title() + ", " + driver[7] +
                      "\nPLATE NUMBER: " + driver[5])

        if driver[9]:
            alert_body = "!!!!!\n" + alert_body + "\n!!!!!\n"

        client = Client(StandardValues.twilio_api_key, StandardValues.twilio_auth_token)
        client.messages.create(to="+13863375957",
                               from_="+13212339188",
                               body=alert_body)

    def is_right_password(self, password):
        cursor = self.conn.cursor()
        check_password = ("SELECT 1 "
                          "FROM users "
                          "WHERE passwords = AES_ENCRYPT(%s, %s) ")

        data_password = (password, StandardValues.aes_key)
        cursor.execute(check_password, data_password)

        rows = cursor.fetchall()

        if cursor.rowcount > 0 and rows[0][0] == 1:
            cursor.close()
            return 1

        cursor.close()
        return 0

    # returns the user info from dbUser.py object >>thisUser
    def get_user(self):
        return self.user

    def log_out(self):
        self.conn.close()


def check_file_input(img):
    try:
        check_opened_file = open(img, 'r')
        check_opened_file.close()
    except IOError:
        Error.error_window("File not found")
        return -1
    return 0


def check_openalpr():
    try:
        assert read_a_plate('../img/mt.jpg', 'mt')[0] == 'BJR216'
        assert read_a_plate('../img/ca.jpeg', 'ca')[0] == '7VDV740'
    except AssertionError as ae:
        Error.error_window("OpenALPR failure")
        return -1
    return 0


def check_input(data_driver):
    try:
        assert len(data_driver[0]) <= StandardValues.firstNameChars and data_driver[
            0] != "", "First Name must be less than or equal to " + str(StandardValues.firstNameChars)
        assert len(data_driver[1]) <= StandardValues.lastNameChars and data_driver[
            1] != "", "Last Name must be less than or equal to " + str(StandardValues.lastNameChars)
        assert len(data_driver[2]) <= StandardValues.addressChars and data_driver[
            2] != "", "Address must be less than or equal to " + str(StandardValues.addressChars)
        assert len(data_driver[3]) == 5 and data_driver[3] != "" and str(
            data_driver[3]).isdigit(), "Zip code should be 5 numbers"
        assert len(data_driver[5]) <= StandardValues.plateNumChars and data_driver[
            5] != "", "Plate number must be " + str(StandardValues.plateNumChars) + " characters."
        assert len(data_driver[6]) <= StandardValues.carmakeChars and data_driver[
            6] != "", "Car Make must be less than or equal to " + str(StandardValues.carmakeChars)
        assert len(data_driver[7]) <= StandardValues.modelChars and data_driver[
            7] != "", "Model must be less than or equal to " + str(StandardValues.modelChars)
        assert len(data_driver[8]) <= StandardValues.colorChars and data_driver[
            8] != "", "Color must be less than or equal to " + str(StandardValues.colorChars)
    except AssertionError as ae:
        Error.error_window(ae.__str__())
        return -1
    except ValueError as ve:
        Error.error_window(ve.__str__())
        return -1

    return 0
