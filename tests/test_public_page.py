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
@allure.title('Validación de inicio de Sesion') 
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_login(setup):
    """
    Pruebas a SSIOC para inicio de sesion con un tiempo de espera de 5 minutos y posteriormente cerrar sesion.
    URL: http://10.35.16.24:8086/
    """
    try:
        driver = setup
        public_page = PublicPage(driver)
        time.sleep(15)
        elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Usuario")))
        file_path3 = public_page.highlight_and_capture_element(elemento) 
        validacion = "Se valida pagina inicio de sesión y sus elementos para iniciar sesion."
        Utils.attach_allure_results(validacion, file_path3) 
        allure.attach(driver.get_screenshot_as_png(), name="01 - Pagina de Login", attachment_type=allure.attachment_type.PNG)  
        driver.find_element(By.ID, "Usuario").send_keys("eric.ruiz")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.implicitly_wait(100)
        elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".timer")))
        file_path = public_page.highlight_and_capture_element(elemento)  
        validacion = "Se localizó el elemento de temporizador de tiempo de sesion."
        Utils.attach_allure_results(validacion, file_path)
        allure.attach(driver.get_screenshot_as_png(), name="02 - Pagina de inicio", attachment_type=allure.attachment_type.PNG)  
        driver.implicitly_wait(100)
        time.sleep(300)
        print("Se continua prueba despues 5 minutos y despues cerrar sesión")
        elemento = driver.find_element(By.XPATH, "//div[6]/span")
        file_path2 = public_page.highlight_and_capture_element(elemento) 
        validacion = "Se localizó el elemento para cerrar sesión."
        Utils.attach_allure_results(validacion, file_path2)
        driver.find_element(By.XPATH, "//div[6]/span").click()  
        allure.attach(driver.get_screenshot_as_png(), name="03 - Cierre de sesión", attachment_type=allure.attachment_type.PNG)  
        print("Se valida cierre de sesión correcto")          
            
    except NoSuchElementException:
        error_message = f"Elemento no encontrado: {elemento}"
        allure.attach(f"Error: {error_message}", name="NoSuchElementException", attachment_type=allure.attachment_type.TEXT)

        # Capture screenshot on error using driver.get_screenshot_as_png()
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        pytest.fail(error_message)

@allure.feature('Pruebas a SSIOC')
@allure.story('Validación de tiempo de inicio de Sesión') 
@allure.title('Validación de tiempo de inicio de Sesión') 
@allure.tag('prioridad:alta', 'tipo:funcional')
def test_login2(setup):
    """
    Pruebas a SSIOC para inicio de sesion con un tiempo de espera de 28 minutos y posteriormente validar el modal de continuar la sesion, 
    posteriormente indicar que se continue la sesion e inmediatamente realizar cerrar sesion.
    URL: http://10.35.16.24:8086/
    """
    try:
        driver = setup
        public_page = PublicPage(driver)
        time.sleep(15)
        elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "Usuario")))
        file_path3 = public_page.highlight_and_capture_element(elemento) 
        validacion = "Se valida pagina inicio de sesión y sus elementos para iniciar sesion."
        Utils.attach_allure_results(validacion, file_path3) 
        allure.attach(driver.get_screenshot_as_png(), name="01 - Pagina de Login", attachment_type=allure.attachment_type.PNG)  
        driver.find_element(By.ID, "Usuario").send_keys("eric.ruiz")
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        driver.implicitly_wait(100)
        elemento = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".timer")))
        file_path = public_page.highlight_and_capture_element(elemento)  
        validacion = "Se localizó el elemento de temporizador de tiempo de sesion."
        Utils.attach_allure_results(validacion, file_path)
        allure.attach(driver.get_screenshot_as_png(), name="02 - Pagina de inicio", attachment_type=allure.attachment_type.PNG)  
        modal = Utils.wait_for_28_minutes(driver)
        if modal:
            button1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/div/div/app-home/app-refresktokenmodal/app-basemodal/div/div/div/div[1]/button[1]")))
            file_path = public_page.highlight_and_capture_element(button1)  
            validacion = "Se localizó el botón del modal."
            Utils.attach_allure_results(validacion, file_path)
            button1.click()
        else:
            allure.attach(driver.get_screenshot_as_png(), name="Modal no encontrado", attachment_type=allure.attachment_type.PNG)
            pytest.fail("El modal no apareció durante el periodo de espera.")
        print("Se continua prueba despues 28 minutos y encontrar modal y despues cerrar sesión")
        elemento = driver.find_element(By.XPATH, "//div[6]/span")
        file_path2 = public_page.highlight_and_capture_element(elemento) 
        validacion = "Se localizó el elemento para cerrar sesión."
        Utils.attach_allure_results(validacion, file_path2)
        driver.find_element(By.XPATH, "//div[6]/span").click()  
        allure.attach(driver.get_screenshot_as_png(), name="03 - Cierre de sesión", attachment_type=allure.attachment_type.PNG)  
        print("Se valida cierre de sesión correcto")   
         
    except NoSuchElementException:
        error_message = f"Elemento no encontrado: {elemento}"
        allure.attach(f"Error: {error_message}", name="NoSuchElementException", attachment_type=allure.attachment_type.TEXT)

        # Capture screenshot on error using driver.get_screenshot_as_png()
        allure.attach(driver.get_screenshot_as_png(), name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
        pytest.fail(error_message)