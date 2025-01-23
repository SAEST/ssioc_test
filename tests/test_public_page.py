import pytest
import allure
from selenium.common.exceptions import NoSuchElementException
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
        driver.find_element(By.ID, "Usuario").send_keys("eric.ruiz")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        elemento = driver.find_element(By.CSS_SELECTOR, ".timer")
        file_path = public_page.highlight_and_capture_element(elemento)  
        #driver.find_element(By.CSS_SELECTOR, ".col-2:nth-child(5)").click()
        #elemento2 = driver.find_element(By.CSS_SELECTOR, ".timer")
        #driver.find_element(By.CSS_SELECTOR, ".col-2 > span").click()
        #file_path2 = public_page.highlight_and_capture_element(elemento2) 
        Utils.attach_allure_results(file_path)
        #Utils.attach_allure_results(file_path2)
            
    except NoSuchElementException:
        # Manejar la excepción si el elemento no se encuentra
        error_message = f"Elemento no encontrado:"
        allure.attach(f"Error: {error_message}", name="NoSuchElementException", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(error_message)