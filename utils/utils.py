from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class Utils:
    @staticmethod
    def wait_for_element(driver, locator, timeout=10):
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

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