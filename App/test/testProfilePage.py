import unittest
from selenium import webdriver
from locators import ProfilePageLocators
from locators import BasePageLocators, LoginPageLocators, ProfilePageLocators

class CandiAppSearch(unittest.TestCase):

    def setUp(self):
        PATH = 'C:\SeleniumDrivers\chromedriver.exe'
        self.driver = webdriver.Chrome(PATH)
        driver = self.driver
        driver.get("https://candi-app1.herokuapp.com/login")
        driver.implicitly_wait(10)
        email_elt = driver.find_element(*LoginPageLocators.EMAIL_TEXT_BOX)
        password_elt = driver.find_element(*LoginPageLocators.PASSWORD_TEXT_BOX)
        login_elt = driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        email_elt.send_keys('sbelarbi@simplon.co')
        password_elt.send_keys('1234')
        login_elt.click()
        profile_button = driver.find_element(*BasePageLocators.PROFILE_PAGE)
        profile_button.click()
        # change_profile_button = driver.find_element_by_xpath("//a[@href='/modify_profile/']")
        # change_profile_button.click()

    def test_title_profile_page(self):
        driver = self.driver
        self.assertEqual("Profil", driver.title)

    def test_last_name(self):
        driver = self.driver
        last_name = driver.find_element(*ProfilePageLocators.LAST_NAME).text
        print(last_name)
        self.assertEqual("Belarbi", last_name)

    def test_first_name(self):
        driver = self.driver
        last_name = driver.find_element(*ProfilePageLocators.FIRST_NAME).text
        self.assertEqual("Safia", last_name)

    def test_email(self):
        driver = self.driver
        email = driver.find_element(*ProfilePageLocators.EMAIL).text
        self.assertEqual("sbelarbi@simplon.co", email)

    def test_cell_phone_number(self):
        driver = self.driver
        cell_phone_number = driver.find_element(*ProfilePageLocators.CELL_PHONE_NUMBER).text
        self.assertEqual("None", cell_phone_number)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()