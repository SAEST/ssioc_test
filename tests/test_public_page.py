import pytest
import allure
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.public_page import PublicPage
from utils.utils import Utils

@allure.feature('Pruebas a SSIOC')
@allure.story('Validación de inicio de Sesion') 
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_login(setup):
    """
    Pruebas a SSIOC
    http://10.35.16.10:8086
    """
    try:
        driver = setup
        public_page = PublicPage(driver)
        time.sleep(15)
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Usuario")))
        file_path3 = public_page.highlight_and_capture_element(element)  
        driver.find_element(By.ID, "Usuario").send_keys("eric.ruiz")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.implicitly_wait(100)
        elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".timer")))
        file_path = public_page.highlight_and_capture_element(elemento)  
        driver.implicitly_wait(100)
        time.sleep(300)
        elemento2 = driver.find_element(By.XPATH, "//div[6]/span")
        file_path2 = public_page.highlight_and_capture_element(elemento2) 
        driver.find_element(By.XPATH, "//div[6]/span").click()        
        Utils.attach_allure_results(file_path3)
        Utils.attach_allure_results(file_path)
        Utils.attach_allure_results(file_path2)
            
    except NoSuchElementException:
        error_message = f"Elemento no encontrado:"
        allure.attach(f"Error: {error_message}", name="NoSuchElementException", attachment_type=allure.attachment_type.TEXT)

        # Capture screenshot on error using driver.get_screenshot_as_png()
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        pytest.fail(error_message)