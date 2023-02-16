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


if __name__ == "__main__":
    url = "http://web.archive.org/web/20221127215609/https://sisu.mec.gov.br/#/selecionados"
    test = Module_SiSu()

    driver = test.init_driver()
    test.access_website(driver, url)

    time.sleep(15)
    test.close_driver(driver)

