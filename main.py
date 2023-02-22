# import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from datetime import datetime, timedelta
# from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
# import selenium
# import json
import time
from selenium import webdriver


# import dotenv
# import os


class Module_SiSu:

    def __init__(self):
        self.driver = None
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--window-size=1920,1080")
        self.url = "http://web.archive.org/web/20221127215609/https://sisu.mec.gov.br/#/selecionados"

    @staticmethod
    def init_driver():
        """Inicia e retorna o Webdriver"""
        return webdriver.Chrome()

    def define_driver(self, driver):
        self.driver = driver

    def define_url(self, url=None):
        if url is None:
            return
        self.url = url

    @staticmethod
    def close_driver(driver):
        """
        Encerra o Webdriver.
        :param object driver: Webriver que será encerrado
        """
        driver.quit()

    def access_website(self):
        """
        Login no sistema.
        :param object driver: Selenium Webdriver
        :param str url: URL do portal de resultados do SiSu
        """
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)

    def find_boxes(self):
        """
        Localiza os campos do formulário de pesquisa.
        :return:
        """
        return self.driver.find_elements(By.TAG_NAME, "input")

    def find_options(self, box):
        """
        Encontra cada opção dentro da caixa de seleção.
        :param box:
        :return:
        """
        return self.driver.find_elements(By.CLASS_NAME, "ng-option")

    def do_search(self):
        """
        Encontra e clica na opção de pesquisar
        """
        # driver.find_element(By.XPATH, "/html/body/sisu-root/div/section/sisu-selecionados/div/section/div/div/div[2]/div[3]/a").click()
        self.driver.find_element(By.CLASS_NAME, "btn-botao").click()

    # TODO Inserir o caminho para download. XPATH ou CLASS_NAME
    def do_download(self):
        """
        Click na opção de download
        """
        # driver.find_element(By.XPATH, "???").click()
        self.driver.find_element(By.CLASS_NAME, "").click()

    def scroll_into_view(self, element):
        """
        Posiciona o elemento no meio da tela para que se possa interagir com ele sem dificuldades.
        :param element:
        :return:
        """
        size = element.size
        location = element.location

        viewport_width = self.driver.execute_script("return document.documentElement.clientWidth;")
        viewport_height = self.driver.execute_script("return document.documentElement.clientHeight;")

        x = location['x'] + size['width'] / 2 - viewport_width / 2
        y = location['y'] + size['height'] / 2 - viewport_height / 2

        self.driver.execute_script(f"window.scrollTo({x}, {y});")
        # ActionChains(driver).move_to_element(object).perform()

    def scroll_and_click(self, element):
        self.scroll_into_view(element)
        element.click()

    def main(self, driver, url=None):
        self.define_driver(driver)
        self.define_url(url)

        self.access_website()
        boxes = self.find_boxes()
        self.scroll_into_view(boxes[0])
        boxes[0].click()

        options_instituicao = self.find_options(boxes[0])

        # Click em cada instituição
        for instituicao in options_instituicao:
            # O texto precisa ser extraído antes, porque quando esse elemento sumir da tela, não será possível.
            text_instituicao = instituicao.text
            print(f"Procurando: {text_instituicao}")
            self.scroll_and_click(boxes[0])
            self.scroll_and_click(instituicao)

            self.scroll_and_click(boxes[1])
            options_local = self.find_options(boxes[1])

            # Click em cada local
            for local in options_local:
                text_local = local.text
                print(f"Procurando: {text_instituicao} - {text_local}")
                self.scroll_and_click(boxes[1])
                self.scroll_and_click(local)

                self.scroll_and_click(boxes[2])
                options_curso = self.find_options(boxes[2])

                # Click em cada curso - Caso não seja necessario preencher todos os campos, o código daqui pra frente
                # pode ser comentado. e o search e download descomentado
                # self.do_search(driver)
                # self.do_download(driver)
                for curso in options_curso:
                    text_curso = curso.text
                    print(f"Procurando: {text_instituicao} - {text_local} - {text_curso}")
                    self.scroll_and_click(boxes[2])
                    self.scroll_and_click(curso)

                    self.scroll_and_click(boxes[3])
                    options_grau_turno = self.find_options(boxes[3])

                    for grauTurno in options_grau_turno:
                        text_grauTurno = grauTurno.text
                        print(f"Procurando: {text_instituicao} - {text_local} - {text_curso} - {text_grauTurno}")
                        self.scroll_and_click(boxes[3])
                        self.scroll_and_click(grauTurno)

                        self.do_search()
                        print("Realizando Download")
                        # self.do_download()


if __name__ == "__main__":
    url = "http://web.archive.org/web/20221127215609/https://sisu.mec.gov.br/#/selecionados"
    test = Module_SiSu()

    driver = test.init_driver()
    test.main(driver)
    time.sleep(15)
    test.close_driver(driver)
