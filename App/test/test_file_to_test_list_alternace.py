import pytest
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



PATH = "C://Users//Apprenant//Documents//chromedriver_win32//chromedriver.exe"

# Test if user is in alternance list
def test_user_in_alternance():
    driver_yes_alternance = webdriver.Chrome(PATH)
    driver_yes_alternance.get("http://127.0.0.1:5000/list_with_alternance")

    key_no_alternance = 'theophile'
    search =  driver_yes_alternance.find_element_by_class_name("form-control")
    search.send_keys(key_no_alternance)
    search.send_keys(Keys.RETURN)

    time.sleep(5)

    elem = driver_yes_alternance.find_elements_by_tag_name("td")

    assert len(elem) ==  5 # check if there is 5 elements
    assert str(elem[0].text).lower() ==  key_no_alternance # check if search item is correct

    driver_yes_alternance.quit()

# Test if user is in non alternance list 
def test_user_not_in_alternance():

    driver_no_alternance = webdriver.Chrome(PATH)
    driver_no_alternance.get("http://127.0.0.1:5000/list_without_alternance")

    key_no_alternance = 'chua'
    search =  driver_no_alternance.find_element_by_class_name("form-control")
    search.send_keys(key_no_alternance)
    search.send_keys(Keys.RETURN)

    time.sleep(5)
    elem = driver_no_alternance.find_elements_by_tag_name("td")

    assert len(elem) ==  4 # check if there is 4 elements
    assert str(elem[0].text).lower() ==  key_no_alternance # check if search item is correct

    driver_no_alternance.quit()

# test if return no result when search for invalid users in alternance list
def test_invalid_user_in_alternance():
    driver_yes_alternance = webdriver.Chrome(PATH)
    driver_yes_alternance.get("http://127.0.0.1:5000/list_with_alternance")

    key_invalid_user = 'iamnotaninvaliduser'
    search =  driver_yes_alternance.find_element_by_class_name("form-control")
    search.send_keys(key_invalid_user)
    search.send_keys(Keys.RETURN)
    time.sleep(5)

    elem = driver_yes_alternance.find_elements_by_tag_name("td")

    assert len(elem) ==  1 # check if there is 1 elements
    assert str(elem[0].text).lower() == 'aucun résultat'

    driver_yes_alternance.quit()


# test if return no result when search for invalid users in non alternance list
def test_invalid_user_in_no_alternance():

    driver_no_alternance = webdriver.Chrome(PATH)
    driver_no_alternance.get("http://127.0.0.1:5000/list_without_alternance")

    key_invalid_user = 'iamnotaninvaliduser'
    search =  driver_no_alternance.find_element_by_class_name("form-control")
    search.send_keys(key_invalid_user)
    search.send_keys(Keys.RETURN)
    time.sleep(5)

    elem = driver_no_alternance.find_elements_by_tag_name("td")

    assert len(elem) ==  1 # check if there is 1 elements
    assert str(elem[0].text).lower() == 'aucun résultat'

    driver_no_alternance.quit()


def check_if_user_only_in_one_list():

    key_user_alternance = 'charles'
    key_user_no_alternance = 'test'

    driver_no_alternance = webdriver.Chrome(PATH)
    driver_no_alternance.get("http://127.0.0.1:5000/list_without_alternance")

    search =  driver_no_alternance.find_element_by_class_name("form-control")
    search.send_keys(key_user_no_alternance)
    search.send_keys(Keys.RETURN)
    time.sleep(5)

    elem_no_alternance = driver_no_alternance.find_elements_by_tag_name("td")

    assert len(elem_no_alternance) == 4
    assert str(elem_no_alternance[0].text).lower() == key_user_no_alternance

    driver_yes_alternance = webdriver.Chrome(PATH)
    driver_yes_alternance.get("http://127.0.0.1:5000/list_with_alternance")

    search =  driver_yes_alternance.find_element_by_class_name("form-control")
    search.send_keys(key_user_no_alternance)
    search.send_keys(Keys.RETURN)
    time.sleep(5)

    elem_yes_alternance = driver_yes_alternance.find_elements_by_tag_name("td")

    assert len(elem_yes_alternance) ==  1 # check if there is 1 elements
    assert str(elem_yes_alternance[0].text).lower() == 'aucun résultat'

    search.send_keys(key_user_alternance)
    search.send_keys(Keys.RETURN)
    time.sleep(5)

    elem_no_alternance = driver_no_alternance.find_elements_by_tag_name("td")

    # elem_yes_alternance = driver_yes_alternance.find_elements_by_tag_name("td")

    assert len(elem_no_alternance) ==  1 # check if there is 1 elements
    assert str(elem_no_alternance[0].text).lower() == 'aucun résultat'


    search.send_keys(key_user_alternance)
    search.send_keys(Keys.RETURN)
    time.sleep(5)

    elem_yes_alternance = driver_yes_alternance.find_elements_by_tag_name("td")

    assert len(elem_yes_alternance) == 5
    assert str(elem_yes_alternance[0].text).lower() == key_user_alternance

    driver_no_alternance.quit()
    driver_yes_alternance.quit()
    
