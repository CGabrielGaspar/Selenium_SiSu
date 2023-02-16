import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import selenium
import json
import time
from selenium import webdriver
import dotenv
import os


class Module_SiSu:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--window-size=1920,1080")
        self.url = "http://web.archive.org/web/20221127215609/https://sisu.mec.gov.br/#/selecionados"

    @staticmethod
    def init_driver():
        """Inicia e retorna o Webdriver"""
        return webdriver.Edge()

    @staticmethod
    def close_driver(driver):
        """
        Encerra o Webdriver.
        :param object driver: Webriver que será encerrado
        """
        driver.quit()

    @staticmethod
    def access_website(driver, url):
        """
        Login no sistema.
        :param object driver: Selenium Webdriver
        :param str url: URL do portal de resultados do SiSu
        """
        driver.implicitly_wait(10)
        driver.get(url)

    @staticmethod
    def find_boxes(driver):
        '''
        Localiza os campos do formulário de pesquisa.
        :param driver:
        :return:
        '''
        return driver.find_elements(By.TAG_NAME, "input")

    @staticmethod
    def find_options(driver, box):
        '''
        Encontra cada opção dentro da caixa de seleção.
        :param driver:
        :param box:
        :return:
        '''
        return driver.find_elements(By.CLASS_NAME, "ng-option")

    @staticmethod
    def do_search(driver):
        '''
        Encontra e clica na opção de pesquisar
        :param driver:
        :return:
        '''
        # driver.find_element(By.XPATH, "/html/body/sisu-root/div/section/sisu-selecionados/div/section/div/div/div[2]/div[3]/a").click()
        driver.find_element(By.CLASS_NAME, "btn-botao").click()

    # TODO Inserir o caminho para download. XPATH ou CLASS_NAME
    @staticmethod
    def do_download(driver):
        '''
        Click na opção de download
        :param driver:
        :return:
        '''
        # driver.find_element(By.XPATH, "").click()
        driver.find_element(By.CLASS_NAME, "").click()

    def main(self, driver):
        self.access_website(driver, self.url)
        boxes = self.find_boxes(driver)
        boxes[0].click()

        options_instituicao = self.find_options(driver, boxes[0])

        # Click em cada instituição
        for instituicao in options_instituicao:
            print(f"Procurando: {instituicao.text}")
            boxes[0].click()
            instituicao.click()

            boxes[1].click()
            options_local = self.find_options(driver, boxes[1])

            # Click em cada local
            for local in options_local:
                print(f"Procurando: {instituicao.text} - {local.text}")
                boxes[1].click()
                local.click()

                boxes[2].click()
                options_curso = self.find_options(driver, boxes[2])

                # Click em cada curso - Caso não seja necessario preencher todos os campos, o código daqui pra frente
                # pode ser comentado. e o search e download descomentado
                # self.do_search(driver)
                # self.do_download(driver)
                for curso in options_curso:
                    print(f"Procurando: {instituicao.text} - {local.text} - {curso.text}")
                    boxes[2].click()
                    curso.click()

                    boxes[3].click()
                    options_grau_turno = self.find_options(driver, boxes[3])

                    for grauTurno in options_grau_turno:
                        print(f"Procurando: {instituicao.text} - {local.text} - {curso.text} - {grauTurno.text}")
                        boxes[3].click()
                        grauTurno.click()

                        self.do_search(driver)


if __name__ == "__main__":
    url = "http://web.archive.org/web/20221127215609/https://sisu.mec.gov.br/#/selecionados"
    test = Module_SiSu()

    driver = test.init_driver()
    test.main(driver)
    time.sleep(15)
    test.close_driver(driver)
