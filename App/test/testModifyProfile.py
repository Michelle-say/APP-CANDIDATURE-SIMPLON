import unittest
from selenium import webdriver
from locators import BasePageLocators, LoginPageLocators, ProfilePageLocators, ModifyProfilePageLocators

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

    def test_modify_last_name(self):
        driver = self.driver
        #Get last name on profile page
        last_name = driver.find_element(*ProfilePageLocators.LAST_NAME).text
        #Navigation to modify profile page
        change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
        change_profile_button.click()
        
        last_name_text_box = driver.find_element(*ModifyProfilePageLocators.LAST_NAME_TEXT_BOX)
        last_name_text_box.clear()
        last_name_text_box.send_keys('last_name')
        validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
        validate_button.click()
        last_name_changed = driver.find_element(*ProfilePageLocators.LAST_NAME).text
        test = ('last_name' == last_name_changed)
        #Reintialization of the last name
        if test:
            #Here the unit test is successful
            #So we reinitialize the last name before quit test
            change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
            change_profile_button.click()
            last_name_text_box = driver.find_element(*ModifyProfilePageLocators.LAST_NAME_TEXT_BOX)
            last_name_text_box.clear()
            last_name_text_box.send_keys(last_name)
            validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
            validate_button.click()
            assert True
        else:
            assert False

    def test_modify_first_name(self):
        driver = self.driver
        #Get last name on profile page
        first_name = driver.find_element(*ProfilePageLocators.FIRST_NAME).text
        #Navigation to modify profile page
        change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
        change_profile_button.click()
            
        first_name_text_box = driver.find_element(*ModifyProfilePageLocators.FIRST_NAME_TEXT_BOX)
        first_name_text_box.clear()
        first_name_text_box.send_keys('first_name')
        validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
        validate_button.click()
        first_name_changed = driver.find_element(*ProfilePageLocators.FIRST_NAME).text
        test = ('first_name' == first_name_changed)
        #Reintialization of the first name
        if test:
            #Here the unit test is successful
            #So we reinitialize the first name before quit test
            change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
            change_profile_button.click()
            last_name_text_box = driver.find_element(*ModifyProfilePageLocators.FIRST_NAME_TEXT_BOX)
            last_name_text_box.clear()
            last_name_text_box.send_keys(first_name)
            validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
            validate_button.click()
            assert True
        else:
            assert False

    def test_modify_email(self):
        driver = self.driver
        #Get email on profile page
        email = driver.find_element(*ProfilePageLocators.EMAIL).text
        #Navigation to modify profile page
        change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
        change_profile_button.click()
            
        email_text_box = driver.find_element(*ModifyProfilePageLocators.EMAIL_TEXT_BOX)
        email_text_box.clear()
        email_text_box.send_keys('email@email.fr')
        validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
        validate_button.click()
        email_changed = driver.find_element(*ProfilePageLocators.EMAIL).text
        test = ('email@email.fr' == email_changed)
        #Reintialization of the email
        if test:
            #Here the unit test is successful
            #So we reinitialize the email before quit test
            change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
            change_profile_button.click()
            email_text_box = driver.find_element(*ModifyProfilePageLocators.EMAIL_TEXT_BOX)
            email_text_box.clear()
            email_text_box.send_keys(email)
            validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
            validate_button.click()
            assert True
        else:
            assert False

    def test_modify_cell_phone_number(self):
        driver = self.driver
        #Get email on profile page
        cell_phone_number = driver.find_element(*ProfilePageLocators.CELL_PHONE_NUMBER).text
        #Navigation to modify profile page
        change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
        change_profile_button.click()
            
        cell_phone_number_text_box = driver.find_element(*ModifyProfilePageLocators.CELL_PHONE_NUMBER_TEXT_BOX)
        cell_phone_number_text_box.clear()
        cell_phone_number_text_box.send_keys('0302040506')
        validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
        validate_button.click()
        cell_phone_number_changed = driver.find_element(*ProfilePageLocators.CELL_PHONE_NUMBER).text
        test = ('0302040506' == cell_phone_number_changed)
        #Reintialization of the cell phone number
        if test:
            #Here the unit test is successful
            #So we reinitialize the cell phone number before quit test
            change_profile_button = driver.find_element(*ProfilePageLocators.CHANGE_PROFILE_BUTTON)
            change_profile_button.click()
            cell_phone_number_text_box = driver.find_element(*ModifyProfilePageLocators.CELL_PHONE_NUMBER_TEXT_BOX)
            cell_phone_number_text_box.clear()
            cell_phone_number_text_box.send_keys(cell_phone_number)
            validate_button = driver.find_element(*ModifyProfilePageLocators.VALIDATE_BUTTON)
            validate_button.click()
            assert True
        else:
            assert False

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()