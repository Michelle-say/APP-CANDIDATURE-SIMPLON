from selenium.webdriver.common.by import By

class BasePageLocators(object):
    """A class for base page locators."""

    LOGIN = (By.NAME, 'login')
    LOGOUT = (By.NAME, 'logout')
    PROFILE_PAGE = (By.XPATH, "//a[@href='/profile/']")

class LoginPageLocators(object):
    """A class for login page locators."""

    EMAIL_TEXT_BOX = (By.ID, 'email')
    PASSWORD_TEXT_BOX = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, "button")

class ProfilePageLocators(object):
    """A class for profile page locators."""

    LAST_NAME = (By.XPATH, '//div[2]/p')
    FIRST_NAME = (By.XPATH, '//div[4]/p')
    EMAIL = (By.XPATH, '//div[6]/p')
    CELL_PHONE_NUMBER = (By.XPATH, '//div[8]/p')
    CHANGE_PROFILE_BUTTON = (By.XPATH,"//a[@href='/modify_profile/']")
    CHANGE_PASSWORD_BUTTON = (By.XPATH,"//a[@href='/modify_password']")

class ModifyProfilePageLocators(object):
    """A class for modify profile page locators."""

    LAST_NAME_TEXT_BOX = (By.ID, 'last_name')
    FIRST_NAME_TEXT_BOX = (By.ID, 'first_name')
    EMAIL_TEXT_BOX = (By.ID, 'email_address')
    CELL_PHONE_NUMBER_TEXT_BOX = (By.ID, 'telephone_number')
    VALIDATE_BUTTON = (By.ID, 'button')

class ModifyPasswordPageLocators(object):
    """A class for modify password page locators."""

    EMAIL_TEXT_BOX = (By.ID, 'email')
    CURRENT_PASSWORD_TEXT_BOX = (By.ID, 'current_password')
    NEW_PASSWORD_TEXT_BOX = (By.ID, 'new_password')
    VALIDATE_BUTTON = (By.ID, 'button')