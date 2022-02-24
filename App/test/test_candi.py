from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pytest

class Test_apprenant():
    @pytest.fixture()
    def test_setup(self):
        global driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        driver.get("http://localhost:5000")
        yield
        driver.quit()
        print('Test completed')
        
    def test_login_echec(self, test_setup):
        try:
            WebDriverWait(driver,15).until(EC.presence_of_element_located((By.NAME, "login")))
            driver.find_element(By.NAME,"login").click()
            driver.find_element(By.NAME,"email").send_keys("gsoulat31@gmail.com")
            driver.find_element(By.NAME,"password").send_keys("123456")
            driver.find_element(By.NAME,"submit").click()
            alert = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "alert")))
            assert "Adresse email ou mot de passe invalide" in alert.text
        except:
            assert False
            
    def test_login_succes(self, test_setup):
        try:
            WebDriverWait(driver,15).until(EC.presence_of_element_located((By.NAME, "login")))
            driver.find_element(By.NAME,"login").click()
            driver.find_element(By.NAME,"email").send_keys("gsoulat31@gmail.com")
            driver.find_element(By.NAME,"password").send_keys("1234")
            driver.find_element(By.NAME,"submit").click()
            WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "alert")))
            title = driver.title
            assert title == "Board"
        except:
            assert False

    def test_add_candidacy(self, test_setup):
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, "login")))
            driver.find_element(By.NAME,"login").click()
            driver.find_element(By.NAME,"email").send_keys("gsoulat31@gmail.com")
            driver.find_element(By.NAME,"password").send_keys("1234")
            driver.find_element(By.NAME,"submit").click()
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "addcandidacy")))
            driver.find_element(By.ID,"addcandidacy").click()
            title = driver.title
            assert title == "Ajout candidature"
            driver.find_element(By.NAME,"entreprise").send_keys("PALLEX")
            driver.find_element(By.NAME,"ville_entreprise").send_keys("Saint florent sur cher")
            driver.find_element(By.NAME,"contact_full_name").send_keys("jose garcia")
            driver.find_element(By.NAME,"contact_email").send_keys("jose.garcia@pallex.fr")          
            driver.find_element(By.NAME,"contact_mobilephone").send_keys("0248010203")
            Select_status = Select(driver.find_element(By.NAME,"status"))
            Select_status.select_by_value("En cours")
            driver.find_element(By.NAME,"date").send_keys("27/10/2021")
            time.sleep(10)
            driver.find_element(By.NAME, "submit").click()
        except:
            assert False

    def test_modify_candidacy(self, test_setup):
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, "login")))
            driver.find_element(By.NAME,"login").click()
            driver.find_element(By.NAME,"email").send_keys("gsoulat31@gmail.com")
            driver.find_element(By.NAME,"password").send_keys("1234")
            driver.find_element(By.NAME,"submit").click()
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "addcandidacy")))
            title = driver.title
            assert title == "Board"
            time.sleep(5)
            driver.find_element(By.NAME,"edit_candidacy?id=45").click()
            driver.find_element(By.NAME,"entreprise").clear()
            driver.find_element(By.NAME,"entreprise").send_keys("SIMPLON")
            driver.find_element(By.NAME,"ville_entreprise").clear()
            driver.find_element(By.NAME,"ville_entreprise").send_keys("LILLE")
            driver.find_element(By.NAME,"contact_full_name").clear()
            driver.find_element(By.NAME,"contact_full_name").send_keys("Safia")
            driver.find_element(By.NAME,"contact_email").clear()
            driver.find_element(By.NAME,"contact_email").send_keys("safia@simplon.fr")          
            driver.find_element(By.NAME,"contact_mobilephone").clear()
            driver.find_element(By.NAME,"contact_mobilephone").send_keys("0606060606")
            Select_status = Select(driver.find_element(By.NAME,"status"))
            Select_status.select_by_value("Rejeté")
            driver.find_element(By.NAME,"comment").clear()
            driver.find_element(By.NAME,"comment").send_keys("NON je ne te veux pas en Alternance 1")
            driver.find_element(By.NAME,"date").clear()
            driver.find_element(By.NAME,"date").send_keys("10/01/2022")
            title = driver.title
            assert title == "Modifier candidature"
            driver.find_element(By.NAME, "submit").click()
            time.sleep(2)
            title = driver.title
            assert title == "Board"
        except:
            assert False
            
    def test_supprimer_candidacy(self, test_setup):
        try:
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.NAME, "login")))
            driver.find_element(By.NAME,"login").click()
            driver.find_element(By.NAME,"email").send_keys("gsoulat31@gmail.com")
            driver.find_element(By.NAME,"password").send_keys("1234")
            driver.find_element(By.NAME,"submit").click()
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "addcandidacy")))
            title = driver.title
            assert title == "Board"
            driver.find_element(By.NAME,"delete_candidacy?id=64").click()
            time.sleep(5)
            title = driver.title
            assert title == "Board"
        except:
            assert False