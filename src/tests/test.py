import socket
import tkinter
import unittest
import timeout_decorator
import PlateRecMain

import pymysql

import app

GLOBAL_TIMEOUT = 1

# scan_license_plate
# is_right_password
# get_user
# log_out
# check_input

# used to "disable" network access for error testing
def guard(*args, **kwargs):
    raise ConnectionError


init_socket = socket.socket


class TestDBInterface(unittest.TestCase):
    def setUp(self):
        username = "TESTUSER"
        password = "TESTUSER"
        self.db_interface = app.dbInterface.DbInterface(username, password, 1)

        username = "TESTADMIN"
        password = "TESTADMIN"
        self.db_interface_admin = app.dbInterface.DbInterface(username, password, 1)

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "00000",
                            "FL",
                            "1234567",
                            "FORD",
                            "BLUE",
                            "F150",
                            "NO")

    def tearDown(self):
        self.db_interface.data_access.log_out()
        self.db_interface_admin.data_access.log_out()

    def testGetUser(self):
        self.assertEqual(self.db_interface.get_user(), self.db_interface.data_access.get_user())
        self.assertEqual(self.db_interface_admin.get_user(), self.db_interface_admin.data_access.get_user())

    def testAddButton(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

        self.db_interface.add_drivers_screen()
        self.db_interface.invoke_add_btn(self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.db_interface.data_access.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 1)

        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

    def testEditSearchButton(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.db_interface.data_access.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.db_interface.data_access.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 1)

        self.db_interface.edit_driver_search()
        self.db_interface.invoke_edit_search_button(self.data_driver)

        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

    def testEditButton(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.db_interface.data_access.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.db_interface.data_access.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 1)

        self.db_interface.edit_driver_screen(self.data_driver[5], self.db_interface.data_access.cursor.fetchall())

        self.data_driver = ("TESTNEW",
                            "TEST",
                            "123 Car Dr",
                            "00000",
                            "FL",
                            "1234567",
                            "FORD",
                            "BLUE",
                            "F150",
                            "NO")

        self.db_interface.invoke_edit_button(self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND fname = %s ; "
        get_driver_data = (self.data_driver[5], self.data_driver[0])

        self.db_interface.data_access.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 1)

        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

    def testDeleteButton(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.db_interface.data_access.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.db_interface.data_access.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 1)

        self.db_interface.del_driver_screen()
        self.db_interface.invoke_delete_button(self.data_driver)

        self.db_interface.data_access.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 0)

        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

    def testSearchZipPlateInpButton(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.db_interface.data_access.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.db_interface.data_access.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 1)

        self.db_interface.search_zip_plate_inp_screen("plate")
        self.db_interface.invoke_search_zip_plate_button(self.data_driver)

        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

    def testSearchFnameLname(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.db_interface.data_access.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.db_interface.data_access.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.db_interface.data_access.cursor.rowcount, 1)

        self.db_interface.search_lname_inp_screen()
        self.db_interface.invoke_search_fname_lname(self.data_driver)

        self.db_interface.data_access.cursor.execute(drop, self.data_driver[5])

    @unittest.skip("")
    def testLogOutButton(self):
        app = PlateRecMain.App(1)
        appLogin = app.login

        self.app.db_interface.log_out_screen(app)
        self.assertIsNot(app.login, appLogin)


class TestDBCommands(unittest.TestCase):
    def setUp(self):
        self.test_data_access_user = app.dbCommands.DataAccess("TESTUSER", "TESTUSER")

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "00000",
                            "FL",
                            "1234567",
                            "FORD",
                            "BLUE",
                            "F150",
                            "NO")

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234568",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234567")

    def tearDown(self):
        self.test_data_access_user.log_out()

    def testInitDBAccess(self):
        """
        Test that DataAccess() creates new data access instance with correct user
        :return:
        """
        self.assertIsNotNone(self.test_data_access_user)
        self.assertIsNotNone(self.test_data_access_user.conn)
        self.assertIsNotNone(self.test_data_access_user.cursor)
        self.assertIsNotNone(self.test_data_access_user.user)

    # conn
    def testConn(self):
        """
        Test that DataAccess.conn() creates connection to database and populates cursor correctly given authorization
        :return:
        """
        # Create new instance of data access to manipulate fields
        test_data_access = app.dbCommands.DataAccess("TESTUSER", "TESTUSER")
        data_conn = test_data_access.connect()

        results = data_conn.cursor().execute("SELECT count(*) FROM users;")
        self.assertIsNotNone(results, 0)

    def testConnError(self):
        """
        Test that DataAccess.conn() catches error if database connection fails
        :return:
        """
        self.assertIsInstance(app.dbCommands.DataAccess("TESTUSER", "TESTUSER"), pymysql.OperationalError)
    # conn end

    # search_zip_plate
    def testSearchZipPlateZipRight(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertGreater(self.test_data_access_user.cursor.rowcount, 0)

        data = self.test_data_access_user.search_zip_plate("zip", self.data_driver[3])
        self.assertIsNotNone(data)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchZipPlateZipWrong(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertGreater(self.test_data_access_user.cursor.rowcount, 0)

        data = self.test_data_access_user.search_zip_plate("zip", "00000")

        self.assertIsNotNone(data)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchZipPlateZipEmpty(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("zip", "")
        self.assertEqual(data, None)

    def testSearchZipPlateZipInvalid(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("zip", "123456")
        self.assertEqual(data, ())

    def testSearchZipPlatePlateRight(self):
        """
        Test that verifies search_zip_plate() will return data given a license plate
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertGreater(self.test_data_access_user.cursor.rowcount, 0)

        data = self.test_data_access_user.search_zip_plate("plate", self.data_driver[5])

        self.assertIsNotNone(data)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchZipPlatePlateWrong(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertGreater(self.test_data_access_user.cursor.rowcount, 0)

        data = self.test_data_access_user.search_zip_plate("plate", self.data_driver[5])

        self.assertIsNotNone(data)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchZipPlatePlateEmpty(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("plate", "")
        self.assertEqual(data, None)

    def testSearchZipPlatePlateInvalid(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("plate", "12345678")
        self.assertEqual(data, ())

    def testSearchZipPlateAssertionErrorEmptyString(self):
        """
        Test that verifies search_zip_plate() will raise an Assertion error if zip or plate is not specified
        :return:
        """
        self.assertIsInstance(AssertionError, self.test_data_access_user.search_zip_plate("", "1234567").__class__)

    def testSearchZipPlateAssertionErrorWrongString(self):
        """
        Test that verifies search_zip_plate() will raise an Assertion error if string is not zip or plate
        :return:
        """
        self.assertIsInstance(AssertionError, self.test_data_access_user.search_zip_plate("nope", "1234567").__class__)
    # search_zip_plate end

    # search_driver_fname_lname
    def testSearchDriverFnameLnameRight(self):
        """
        Test that verifies search_driver_fname_lname() will return data given full name
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        data = self.test_data_access_user.search_driver_fname_lname(self.data_driver[0], self.data_driver[1])
        self.assertIsNotNone(data)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchDriverFnameLnameFnameWrong(self):
        """
        Test that verifies search_driver_fname_lname() will not return data given wrong first name
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        data = self.test_data_access_user.search_driver_fname_lname("Wrong", self.data_driver[1])
        self.assertEqual(data, ())

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchDriverFnameLnameLnameWrong(self):
        """
        Test that verifies search_driver_fname_lname() will not return data given wrong last name
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        data = self.test_data_access_user.search_driver_fname_lname(self.data_driver[0], "Wrong")
        self.assertEqual(data, ())

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchDriverFnameLnameAllWrong(self):
        """
        Test that verifies search_driver_fname_lname() will not return data given wrong full name
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        data = self.test_data_access_user.search_driver_fname_lname("Wrong", "Wrong")
        self.assertEqual(data, ())

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchDriverFnameLnameFnameEmpty(self):
        """
        Test that verifies search_driver_fname_lname() will throw Assertion Error when first name is empty
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertIsInstance(AssertionError,
                              self.test_data_access_user.search_driver_fname_lname("", self.data_driver[0]).__class__)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchDriverFnameLnameLnameEmpty(self):
        """
        Test that verifies search_driver_fname_lname() will throw Assertion Error when last name is empty
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertIsInstance(AssertionError,
                              self.test_data_access_user.search_driver_fname_lname(self.data_driver[0], "").__class__)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testSearchDriverFnameLnameAllEmpty(self):
        """
        Test that verifies search_driver_fname_lname() will throw Assertion Error when full name is empty
        :return:
        """
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertIsInstance(AssertionError,
                              self.test_data_access_user.search_driver_fname_lname("", "").__class__)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])
    # search_driver_fname_lname end

    # add_driver
    def testAddDriverRight(self):
        """
        Test that validates add_driver() successfully adds new driver given correct parameters
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.test_data_access_user.add_driver(self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        results = self.test_data_access_user.cursor.fetchone()

        self.assertEqual(results[0], self.data_driver[0])
        self.assertEqual(results[1], self.data_driver[1])
        self.assertEqual(results[2], self.data_driver[2])
        self.assertEqual(results[3], self.data_driver[3])
        self.assertEqual(results[4], self.data_driver[4])
        self.assertEqual(results[5], self.data_driver[5])
        self.assertEqual(results[6], self.data_driver[6])
        self.assertEqual(results[7], self.data_driver[7])
        self.assertEqual(results[8], self.data_driver[8])
        self.assertEqual(results[9], self.data_driver[9])

        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])
        self.test_data_access_user.conn.commit()

    def testAddDriverEmptyFname(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverEmptyLname(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverEmptyAddress(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverEmptyZip(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverEmptyPlate(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverEmptyMake(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverEmptyColor(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverEmptyModel(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongFname(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TESTTTTTTTTTTTTTTTTTTT",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongLname(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TESTTTTTTTTTTTTTTTTTTT",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongAddress(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "TESTTTTTTTTTTTTTTTTTTT",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongZip(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "1234567",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongPlate(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "123456789",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongMake(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TESTTTTTTTTTTTTTTTTTTT",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongColor(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "TESTTTTTTTTTTTTTTTTTTT",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooLongModel(self):
        """
        Test that validates add_driver() doesn't add driver given TooLong input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "12345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "TESTTTTTTTTTTTTTTTTTTT",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverTooShortZip(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "1234",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverHasLettersZip(self):
        """
        Test that validates add_driver() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        self.data_driver = ("TEST",
                            "TEST",
                            "123 Car Dr",
                            "A2345",
                            "FL",
                            "1234567",
                            "TOYOTA",
                            "BLACK",
                            "CAMRY",
                            "YES")

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

    def testAddDriverDuplicatePlate(self):
        """
        Test that validates add_driver() does not add duplicate plate
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        error = self.test_data_access_user.add_driver(self.data_driver)

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s; "
        self.test_data_access_user.cursor.execute(get_driver, self.data_driver[5])

        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])
        self.test_data_access_user.conn.commit()
    # add_driver end

    # delete_driver
    def testDeleteDriverRight(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)
        self.test_data_access_user.delete_driver(self.data_driver[5])

        search = "SELECT 1 FROM drivers WHERE platenum = %s "

        self.test_data_access_user.cursor.execute(search, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testDeleteDriverEmptyPlate(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)
        self.test_data_access_user.delete_driver("")

        search = "SELECT 1 FROM drivers WHERE platenum = %s ;"

        self.test_data_access_user.cursor.execute(search, "")
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testDeleteDriverTooLongPlate(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, "12345678")

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.data_driver = (
            "TEST",
            "TEST",
            "TEST",
            "00000",
            "FL",
            "12345678",
            "TEST",
            "TEST",
            "TEST",
            "YES")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)
        self.test_data_access_user.delete_driver("12345678")

        search = "SELECT 1 FROM drivers WHERE platenum = %s "

        self.test_data_access_user.cursor.execute(search, self.data_driver[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()
    # delete_driver end

    # plate_check
    def testPlateCheckRight(self):
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)
        self.assertEqual(self.test_data_access_user.plate_check(self.data_driver[5]), 1)

    def testPlateCheckEmpty(self):
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertEqual(self.test_data_access_user.plate_check(""), 0)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

    def testPlateCheckTooLong(self):
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        self.assertEqual(self.test_data_access_user.plate_check("12345678"), 0)

        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])
    # plate_check end

    # edit_driver_request
    def testEditDriverRight(self):
        """
        Test that validates edit_driver_request() successfully adds new driver given correct parameters
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[10])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[10])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        results = self.test_data_access_user.cursor.fetchone()

        self.assertEqual(results[0], self.data_driver_edit[0])
        self.assertEqual(results[1], self.data_driver_edit[1])
        self.assertEqual(results[2], self.data_driver_edit[2])
        self.assertEqual(results[3], self.data_driver_edit[3])
        self.assertEqual(results[4], self.data_driver_edit[4])
        self.assertEqual(results[5], self.data_driver_edit[10])
        self.assertEqual(results[6], self.data_driver_edit[6])
        self.assertEqual(results[7], self.data_driver_edit[7])
        self.assertEqual(results[8], self.data_driver_edit[8])
        self.assertEqual(results[9], self.data_driver_edit[9])

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[10])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyFname(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND fname = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[0])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyLname(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND lname = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[1])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyAddress(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        
        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])
        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND address = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[2])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyZip(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND zipcod = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[3])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyPlate(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s"

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyMake(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND carmake = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[6])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyColor(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND color = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[7])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverEmptyModel(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND model = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[8])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()

    def testEditDriverTooLongFname(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TESTTTTTTTTTTTTTTTTTTT",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND zipcod = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[0])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooLongLname(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TESTTTTTTTTTTTTTTTTTTT",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND lname = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[1])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooLongAddress(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "TESTTTTTTTTTTTTTTTTTTT",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND color = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[2])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooLongZip(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "000000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND zipcod = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[3])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooLongPlate(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "12345678",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "12345678")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[10])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooLongMake(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "TESTTTTTTTTTTTTTTTTTTT",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND carmake = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[6])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooLongModel(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "TESTTTTTTTTTTTTTTTTTTT",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND model = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[8])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooLongColor(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "00000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "TESTTTTTTTTTTTTTTTTTTT",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND color = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[7])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverTooShortZip(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "0000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND zipcod = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[3])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

    def testEditDriverHasLettersZip(self):
        """
        Test that validates edit_driver_request() doesn't add driver given empty input
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = %s ; "
        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])

        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s ; "

        self.test_data_access_user.cursor.execute(get_driver, self.data_driver_edit[5])
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 1)

        self.data_driver_edit = ("TEST",
                                 "TEST",
                                 "123 Car Dr",
                                 "A0000",
                                 "FL",
                                 "1234567",
                                 "FORD",
                                 "BLUE",
                                 "F150",
                                 "NO",
                                 "1234568")

        error = self.test_data_access_user.edit_driver_request(self.data_driver_edit, self.data_driver_edit[5])

        self.assertEqual(error, -1)

        get_driver = "SELECT * FROM drivers WHERE platenum = %s AND zipcod = %s"
        get_driver_data = (self.data_driver_edit[5], self.data_driver_edit[0])

        self.test_data_access_user.cursor.execute(get_driver, get_driver_data)
        self.assertEqual(self.test_data_access_user.cursor.rowcount, 0)

        self.test_data_access_user.cursor.execute(drop, self.data_driver_edit[5])
        self.test_data_access_user.conn.commit()
    # edit_driver_request end

    # scan_license_plate

    # scan_license_plate end

    # is_right_password
    def testIsRightPasswordRight(self):
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)
        self.assertEqual(self.test_data_access_user.is_right_password("TESTUSER"), 1)

    def testIsRightPasswordEmpty(self):
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)
        self.assertEqual(self.test_data_access_user.is_right_password(""), 0)

    def testIsRightPasswordWrong(self):
        add_driver = ("INSERT INTO drivers "
                      " (fname, lname, address, zipcod, state, platenum, carmake, color, model, priority) "
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ")

        self.test_data_access_user.cursor.execute(add_driver, self.data_driver)
        self.assertEqual(self.test_data_access_user.is_right_password("Wrong"), 0)

    # is_right_password end

    # get_user
    def testGetUser(self):
        self.assertEqual(self.test_data_access_user.get_user(), self.test_data_access_user.user)
    # get_user end

    # check_input

    # check_input end


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.test_username_user = "TESTUSER"
        self.test_password_user = "TESTUSER"
        self.test_user_user = app.dbUsers.Users(self.test_username_user,
                                                app.dbCommands.DataAccess(self.test_username_user,
                                                                          self.test_password_user))

        self.test_username_admin = "TESTADMIN"
        self.test_password_admin = "TESTADMIN"
        self.test_user_admin = app.dbUsers.Users(self.test_username_admin,
                                                 app.dbCommands.DataAccess(self.test_username_admin,
                                                                           self.test_password_admin))

    def tearDown(self):
        self.test_user_user.data_access.log_out()
        self.test_user_admin.data_access.log_out()

    def testInitUserUser(self):
        """
        Test that Users() creates new user with correct permissions for USER level access
        :return:
        """
        self.assertIsNotNone(self.test_user_user)
        self.assertIsNotNone(self.test_user_user.data_access)
        self.assertIsNotNone(self.test_user_user.passport)

        self.assertEqual(self.test_user_user.passport.firstName, "TESTUSER")
        self.assertEqual(self.test_user_user.passport.lastName, "TESTUSER")
        self.assertEqual(self.test_user_user.passport.loginName, "TESTUSER")
        self.assertEqual(self.test_user_user.passport.access, "USER")

    def testInitUserAdmin(self):
        """
        Test that Users() creates new user with correct permissions for ADMIN level access
        :return:
        """
        self.assertIsNotNone(self.test_user_admin)
        self.assertIsNotNone(self.test_user_admin.data_access)
        self.assertIsNotNone(self.test_user_admin.passport)

        self.assertEqual(self.test_user_admin.passport.firstName, "TESTADMIN")
        self.assertEqual(self.test_user_admin.passport.lastName, "TESTADMIN")
        self.assertEqual(self.test_user_admin.passport.loginName, "TESTADMIN")
        self.assertEqual(self.test_user_admin.passport.access, "ADMIN")

    def testGetUserInfoUser(self):
        """
        Test that get_user_info() returns passport containing all information pertinent to the user instance for USER
        :return:
        """
        data = self.test_user_user.get_user_info()

        self.assertEqual(data.firstName, "TESTUSER")
        self.assertEqual(data.lastName, "TESTUSER")
        self.assertEqual(data.loginName, "TESTUSER")
        self.assertEqual(data.access, "USER")

    def testGetUserInfoAdmin(self):
        """
        Test that get_user_info() returns passport containing all information pertinent to the user instance for ADMIN
        :return:
        """
        data = self.test_user_admin.get_user_info()

        self.assertEqual(data.firstName, "TESTADMIN")
        self.assertEqual(data.lastName, "TESTADMIN")
        self.assertEqual(data.loginName, "TESTADMIN")
        self.assertEqual(data.access, "ADMIN")

    def testFindUserUser(self):
        """
        Test that find_user() can query database to return correct user information
        :return:
        """
        self.assertIsNotNone(self.test_user_user.data_access.cursor)

        data = self.test_user_user.find_user("TESTUSER")

        self.assertIsNotNone(data)

        self.assertEqual(data[0][0], "TESTUSER")
        self.assertEqual(data[0][1], "TESTUSER")
        self.assertEqual(data[0][2], "TESTUSER")
        self.assertEqual(data[0][3], "USER")

    def testFindUserAttribute(self):
        """
        Test that find_user() can query database to return correct admin information
        :return:
        """
        self.assertIsNotNone(self.test_user_admin.data_access)

        data = self.test_user_admin.find_user("TESTADMIN")

        self.assertIsNotNone(data)

        self.assertEqual(data[0][0], "TESTADMIN")
        self.assertEqual(data[0][1], "TESTADMIN")
        self.assertEqual(data[0][2], "TESTADMIN")
        self.assertEqual(data[0][3], "ADMIN")

    def testFindUserAttributeError(self):
        """
        Test that validates AttributeError is raised if database access is not initialized
        :return:
        """
        temp = self.test_user_user.data_access
        self.test_user_user.data_access = None
        self.assertIsNone(self.test_user_user.data_access)

        data = self.test_user_user.find_user("TESTUSER")
        self.assertIsInstance(data, AttributeError)

        self.test_user_user.data_access = temp

    def testFindUserPermissionError(self):
        """
        Test that validates Permission Error is raised if an invalid username is supplied
        :return:
        """
        data = self.test_user_user.find_user("wronguser")
        self.assertIsInstance(data, PermissionError)

    def testFindUserNetworkError(self):
        """
        Test that validates Network Error is raised if database connection is lost
        TODO : Need to research what condition makes this true consistently
        :return:
        """
        data = self.test_user_user.find_user("TESTUSER")
        self.assertIsInstance(data, OSError)


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.test_login = app.login.Login(1)

    def testInitLogin(self):
        """
        Test that Login() creates new Login class with empty class members username and password
        """
        self.assertEqual(self.test_login.username, "TESTUSER")
        self.assertEqual(self.test_login.password, "TESTUSER")

    def testLogin(self):
        """
        Test that login() will act correctly
        """
        test_user = "TESTADMIN"
        test_pass = "TESTADMIN"

        username_tb = tkinter.Entry()
        username_tb.insert(tkinter.END, test_user)

        password_tb = tkinter.Entry()
        password_tb.insert(tkinter.END, test_pass)

        self.test_login.login(username_tb, password_tb)

        self.assertEqual(self.test_login.username, test_user)
        self.assertEqual(self.test_login.password, test_pass)


if __name__ == '__main__':
    timeout_decorator.timeout(GLOBAL_TIMEOUT)(unittest.main)()
