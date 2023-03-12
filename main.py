from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time


class Module_SiSu:

    def __init__(self):
        self.driver = None
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--window-size=1920,1080")
        self.url = "https://sisu.mec.gov.br/#/selecionados"

    @staticmethod
    def init_driver():
        """Inicia e retorna o Webdriver"""
        return webdriver.Edge()
        # return webdriver.Chrome()

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
        # button = driver.find_element(By.XPATH, "/html/body/sisu-root/div/section/sisu-selecionados/div/section/div/div/div[2]/div[3]/a")
        button = self.driver.find_element(By.CLASS_NAME, "btn-botao")
        self.scroll_and_click(button)

    def do_download(self):
        """
        Click na opção de download
        """
        # button = driver.find_element(By.XPATH,
        #                              "/html/body/sisu-root/div/section/sisu-selecionados/div/section/div/div/div[3]/div[1]/div[4]/a")
        button = self.driver.find_element(By.CLASS_NAME, "baixar-arquivo")
        self.scroll_and_click(button)

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

    def scroll_and_click(self, element):
        try:
            self.wait_loading()
            self.scroll_into_view(element)
            element.click()
        except ElementNotInteractableException:
            self.scroll_and_click(element)
            return

    def wait_loading(self):
        """
        Verifica se a pagina está carregando
        :return:
        """
        try:
            if self.driver.find_element(By.CLASS_NAME, "loading").is_displayed():
                print("Loading page...")
                time.sleep(1)
                self.wait_loading()
            else:
                return
        except NoSuchElementException:
            return

    @staticmethod
    def moveto_next_option(box, first=True):
        """
        TODO: Testar melhor opção
        Usa arrowskeys para escolher a proxima opção, porque a opção talvez não apareça para ser clicada do outro jeito.
        :param first: Determina se é a primeira opção da lista dropdown. Importante para não pular o primeiro item.
        :param box:
        :return:
        """
        if first:
            box.send_keys(Keys.ENTER)
        else:
            box.send_keys(Keys.ARROW_DOWN)
            box.send_keys(Keys.ENTER)

    def extract_texts(self, list_items):
        r_list = []
        for item in list_items:
            r_list.append(item.text)
        return r_list

    def main(self, driver, url=None, downloads_all=False):
        '''

        :param driver: Driver
        :param url: URL do SiSu
        :param downloads_all: O sistema tem um "bug" que
        :return:
        '''
        self.define_driver(driver)
        self.define_url(url)

        self.access_website()
        boxes = self.find_boxes()
        self.scroll_and_click(boxes[0])

        options_instituicao = self.find_options(boxes[0])

        # Click em cada instituição
        first_instituicao = True
        print(len(options_instituicao))
        for instituicao in options_instituicao:
            self.scroll_and_click(boxes[0])
            self.moveto_next_option(boxes[0], first_instituicao)
            self.scroll_and_click(boxes[1])

            options_local = self.find_options(boxes[1])

            first_instituicao = False
            first_local = True
            # Click em cada local
            for local in options_local:
                self.scroll_and_click(boxes[1])
                self.moveto_next_option(boxes[1], first_local)
                self.scroll_and_click(boxes[2])

                options_curso = self.find_options(boxes[2])

                if downloads_all and not first_local:  # Se funciona do antigo jeito que, só cada univ. baixa todos os dados, pula os loops de baixar varias vezes a
                    break

                first_local = False
                first_curso = True
                # Click em cada curso
                for curso in options_curso:
                    self.scroll_and_click(boxes[2])
                    self.moveto_next_option(boxes[2], first_curso)
                    self.scroll_and_click(boxes[3])

                    options_grau_turno = self.find_options(boxes[3])

                    if downloads_all and not first_curso:  # Se funciona do antigo jeito que, só cada univ. baixa todos os dados, pula os loops de baixar varias vezes a
                        break

                    first_curso = False
                    first_grau_turno = True
                    for grau_turno in options_grau_turno:
                        self.scroll_and_click(boxes[3])
                        self.moveto_next_option(boxes[3], first_grau_turno)

                        self.do_search()
                        self.wait_loading()
                        self.do_download()

                        if downloads_all and not first_grau_turno:  # Se funciona do antigo jeito que, só cada univ. baixa todos os dados, pula os loops de baixar varias vezes a
                            break

                        first_grau_turno = False


if __name__ == "__main__":
    url = "https://sisu.mec.gov.br/#/selecionados"
    test = Module_SiSu()

    driver = test.init_driver()
    test.main(driver, downloads_all=True)
    time.sleep(15)
    test.close_driver(driver)
