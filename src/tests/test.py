import socket
import unittest
import tkinter
import app
import pymysql

# conn
# search_zip_plate
# search_driver_fname_lname
# add_driver read_textbox
# delete_driver
# plate_check
# edit_driver_request
# scan_license_plate
# is_right_password
# get_user
# log_out
# check_input

# used to "disable" network access for error testing
def guard(*args, **kwargs):
    raise ConnectionError


init_socket = socket.socket


class TestDBCommands(unittest.TestCase):
    def setUp(self):
        self.test_data_access_user = app.dbCommands.DataAccess("TESTUSER", "TESTUSER")

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

    # search_zip_plate
    def testSearchZipPlateZipRight(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("zip", "12345")
        self.assertIsNotNone(data[0])

    def testSearchZipPlateZipWrong(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("zip", "00000")
        self.assertEqual(data, ())

    def testSearchZipPlateZipEmpty(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("zip", "")
        self.assertEqual(data, ())

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
        data = self.test_data_access_user.search_zip_plate("plate", "1234567")
        self.assertIsNotNone(data[0])

    def testSearchZipPlatePlateWrong(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("plate", "0000000")
        self.assertEqual(data, ())

    def testSearchZipPlatePlateEmpty(self):
        """
        Test that verifies search_zip_plate() will return data given a zip code
        :return:
        """
        data = self.test_data_access_user.search_zip_plate("plate", "")
        self.assertEqual(data, ())

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

    # search_driver_fname_lname
    def testSearchDriverFnameLnameRight(self):
        """
        Test that verifies search_driver_fname_lname() will return data given full name
        :return:
        """
        data = self.test_data_access_user.search_driver_fname_lname("Test", "Test")
        self.assertIsNotNone(data[0])

    def testSearchDriverFnameLnameFnameWrong(self):
        """
        Test that verifies search_driver_fname_lname() will not return data given wrong first name
        :return:
        """
        data = self.test_data_access_user.search_driver_fname_lname("Test1", "Test")
        self.assertEqual(data, ())

    def testSearchDriverFnameLnameLnameWrong(self):
        """
        Test that verifies search_driver_fname_lname() will not return data given wrong last name
        :return:
        """
        data = self.test_data_access_user.search_driver_fname_lname("Test", "Test1")
        self.assertEqual(data, ())

    def testSearchDriverFnameLnameAllWrong(self):
        """
        Test that verifies search_driver_fname_lname() will not return data given wrong full name
        :return:
        """
        data = self.test_data_access_user.search_driver_fname_lname("Test1", "Test1")
        self.assertEqual(data, ())

    def testSearchDriverFnameLnameFnameEmpty(self):
        """
        Test that verifies search_driver_fname_lname() will throw Assertion Error when first name is empty
        :return:
        """
        self.assertIsInstance(AssertionError,
                              self.test_data_access_user.search_driver_fname_lname("", "Test").__class__)

    def testSearchDriverFnameLnameLnameEmpty(self):
        """
        Test that verifies search_driver_fname_lname() will throw Assertion Error when last name is empty
        :return:
        """
        self.assertIsInstance(AssertionError,
                              self.test_data_access_user.search_driver_fname_lname("Test", "").__class__)

    def testSearchDriverFnameLnameAllEmpty(self):
        """
        Test that verifies search_driver_fname_lname() will throw Assertion Error when full name is empty
        :return:
        """
        self.assertIsInstance(AssertionError, self.test_data_access_user.search_driver_fname_lname("", "").__class__)

    # add_driver
    def testAddDriver(self):
        """
        Test that validates add_driver() successfully adds new driver given correct parameters
        :return:
        """
        # drop row if platenum is already in database
        drop = "DELETE FROM drivers WHERE platenum = '1234567'; "
        self.test_data_access_user.cursor.execute(drop)

        data_driver = ("TEST",
                       "TEST",
                       "123 Car Dr",
                       "12345",
                       "FL",
                       "1234567",
                       "TOYOTA",
                       "BLACK",
                       "CAMRY",
                       "YES")

        self.test_data_access_user.add_driver(data_driver[0],
                                              data_driver[1],
                                              data_driver[2],
                                              data_driver[3],
                                              data_driver[4],
                                              data_driver[5],
                                              data_driver[6],
                                              data_driver[7],
                                              data_driver[8],
                                              data_driver[9])

        get_driver = "SELECT * FROM drivers WHERE platenum = '1234567'; "
        self.test_data_access_user.cursor.execute(get_driver)

        results = self.test_data_access_user.cursor.fetchone()

        self.assertEqual(results[0], "TEST")
        self.assertEqual(results[1], "TEST")
        self.assertEqual(results[2], "123 Car Dr")
        self.assertEqual(results[3], "12345")
        self.assertEqual(results[4], "FL")
        self.assertEqual(results[5], "1234567")
        self.assertEqual(results[6], "TOYOTA")
        self.assertEqual(results[7], "BLACK")
        self.assertEqual(results[8], "CAMRY")
        self.assertEqual(results[9], "YES")


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
        self.test_user_user.data_access = None
        self.assertIsNone(self.test_user_user.data_access)

        data = self.test_user_user.find_user("TESTUSER")
        self.assertIsInstance(data, AttributeError)

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
        self.assertEqual(self.test_login.username, "")
        self.assertEqual(self.test_login.password, "")

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
    unittest.main()
