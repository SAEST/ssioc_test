from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.by import By
import time
import datetime as dt

class Utils:
    @staticmethod
    def wait_for_element(driver, locator, timeout=10):
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    
    def wait_for_28_minutes(driver):
        """Espera 30 minutos o hasta que aparezca el modal."""
        current_date_and_time = dt.datetime.now()
        print(f"La prueba inició a las {current_date_and_time}")
        start_time = time.time()
        end_time = start_time + 28 * 60  # 30 minutos en segundos
        while time.time() < end_time:
            try:
                modal = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/div/app-home/app-refresktokenmodal/app-basemodal"))
                )
                # Capturar pantalla del modal
                allure.attach(driver.get_screenshot_as_png(), name="Modal encontrado", attachment_type=allure.attachment_type.PNG)
                print(f"Modal encontrado a las {dt.datetime.now()}")
                return modal
            except:
                pass
            time.sleep(5)
            current_date_and_time = dt.datetime.now()
            print(f"Modal no ha sido encontrado {current_date_and_time}")
        return None
    
    def modal_sesion_existente(driver):

        try:
            modal = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/div/app-login/app-loginmodal/app-basemodal/div/div"))
            )
            # Capturar pantalla del modal
            allure.attach(driver.get_screenshot_as_png(), name="Modal encontrado", attachment_type=allure.attachment_type.PNG)
            print(f"Modal encontrado a las {dt.datetime.now()}")
            return modal
        except:
            pass
        time.sleep(5)
        return None

    def attach_allure_results(validacion, file_path):
        """
        Adjunta resultados al encontrar elementos en la página
        """
        with allure.step("Encontrando elementos en la página"):
            allure.attach(
                f" {validacion}",
                name="Resultado de la validación",
                attachment_type=allure.attachment_type.TEXT
            )
            with open(file_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Captura de pantalla del elemento",
                    attachment_type=allure.attachment_type.PNG
                )    