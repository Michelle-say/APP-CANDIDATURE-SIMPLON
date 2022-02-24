from ast import If
import unittest
from click import password_option
from selenium import webdriver
from locators import BasePageLocators, LoginPageLocators, ProfilePageLocators, ModifyPasswordPageLocators
import time

class CandiAppSearch(unittest.TestCase):

    def setUp(self):
        PATH = 'C:\SeleniumDrivers\chromedriver.exe'
        self.driver = webdriver.Chrome(PATH)
        driver = self.driver
        driver.get("https://candi-app1.herokuapp.com/login")
        driver.implicitly_wait(10)

        #Login and navigation to profile page
        email_elt = driver.find_element(*LoginPageLocators.EMAIL_TEXT_BOX)
        password_elt = driver.find_element(*LoginPageLocators.PASSWORD_TEXT_BOX)
        login_elt = driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        email_elt.send_keys('sbelarbi@simplon.co')
        password_elt.send_keys('1234')
        login_elt.click()
        profile_button = driver.find_element(*BasePageLocators.PROFILE_PAGE)
        profile_button.click()

    # def test_title_modify_profile_page(self):
    #     driver = self.driver        
    #     change_profile_button = driver.find_element_by_xpath("//a[@href='/modify_profile/']")
    #     change_profile_button.click()
    #     self.assertEqual("Modify your profile", driver.title)

    def test_modify_password(self):
        driver = self.driver
        #Get last name on profile page
        current_password = '1234'
        #Navigation to modify profile page
        change_password_button = driver.find_element(*ProfilePageLocators.CHANGE_PASSWORD_BUTTON)
        change_password_button.click()
        
        current_email = 'sbelarbi@simplon.co'
        email_text_box = driver.find_element(*ModifyPasswordPageLocators.EMAIL_TEXT_BOX)
        email_text_box.send_keys(current_email)
        current_password_text_box = driver.find_element(*ModifyPasswordPageLocators.CURRENT_PASSWORD_TEXT_BOX)
        current_password_text_box.send_keys(current_password)
        new_password_text_box = driver.find_element(*ModifyPasswordPageLocators.NEW_PASSWORD_TEXT_BOX)
        new_password_text_box.send_keys('4321')

        validate_button = driver.find_element(*ModifyPasswordPageLocators.VALIDATE_BUTTON)
        validate_button.click()

        #Logout
        logout_button = driver.find_element(*BasePageLocators.LOGOUT)
        logout_button.click()

        #login
        login_button = driver.find_element(*BasePageLocators.LOGIN)
        login_button.click()
        email_text_box = driver.find_element(*LoginPageLocators.EMAIL_TEXT_BOX)
        email_text_box.send_keys(current_email)
        password_text_box = driver.find_element(*LoginPageLocators.PASSWORD_TEXT_BOX)
        password_text_box.send_keys('4321')
        login_button = driver.find_element(*LoginPageLocators.LOGIN_BUTTON)
        login_button.click()

        test = driver.title == 'Board'

        #Reintialization of the password
        if test:
            #Here the unit test is successful
            #So we reinitialize the password before quit test
            profile_button = driver.find_element(*BasePageLocators.PROFILE_PAGE)
            profile_button.click()
            change_password_button = driver.find_element(*ProfilePageLocators.CHANGE_PASSWORD_BUTTON)
            change_password_button.click()
            email_text_box = driver.find_element(*ModifyPasswordPageLocators.EMAIL_TEXT_BOX)
            email_text_box.send_keys(current_email)
            current_password_text_box = driver.find_element(*ModifyPasswordPageLocators.CURRENT_PASSWORD_TEXT_BOX)
            current_password_text_box.send_keys('4321')
            new_password_text_box = driver.find_element(*ModifyPasswordPageLocators.NEW_PASSWORD_TEXT_BOX)
            new_password_text_box.send_keys(current_password)
            validate_button = driver.find_element(*ModifyPasswordPageLocators.VALIDATE_BUTTON)
            validate_button.click()
            assert True
        else:
            assert False

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()