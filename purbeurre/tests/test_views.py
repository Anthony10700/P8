"""
        class of test viewe purbeurre
    """
import time
from django.test import TestCase, Client
# Create your tests here.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from purbeurre.models import Product, Categories
# from pyvirtualdisplay import Display 
# display = Display(visible=0, size=(1024, 768)) 
# display.start() 

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True


class UrlPurbeurreTests(TestCase):
    """
    Class test of url of app

    Args:
        TestCase ([type]): [description]
    """
    @classmethod
    def setUpTestData(cls):
        """This method make a account for testing the url form sign_in
        """       
        browser = webdriver.Firefox(options=firefox_options)
        print("\nCreation d'un compte\n")
        info = {"inputUsername": "Frost101",
                "inputemail": "anthony.thillerot@laposte.nettt",
                "inputPassword1": "azerty",
                "inputPassword2": "azerty",
                "inputNom": "Test_Nom",
                "inputprenom": "Test_prenom"}

        browser.get('http://127.0.0.1:8000/auth/sign_in.html')
        grid = browser.find_element_by_id('inputemail')
        grid.send_keys(info["inputemail"])
        grid = browser.find_element_by_id('inputUsername')
        grid.send_keys(info["inputUsername"])
        grid = browser.find_element_by_id('inputPassword1')
        grid.send_keys(info["inputPassword1"])
        grid = browser.find_element_by_id('inputPassword2')
        grid.send_keys(info["inputPassword2"])
        grid = browser.find_element_by_id('inputNom')
        grid.send_keys(info["inputNom"])
        grid = browser.find_element_by_id('inputprenom')
        grid.send_keys(info["inputprenom"])

        browser.execute_script(
            "document.getElementById('gridCheck').checked = true;")
        time.sleep(1)
        browser.execute_script(
            "document.getElementsByClassName('btn btn-primary')[1].click();")

        browser.quit()

    def setUp(self):
        """This method similar at __init__ for each instance
        """
        # Every test needs a client.
        self.client = Client()

        self.browser = webdriver.Firefox(options=firefox_options)
        
    def test_index(self):
        """
        This method test the index url
        """
        response = self.client.get('/purbeurre/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Pur Beurre")
        time.sleep(2)
        self.browser.quit()

    def test_index_selenium(self):
        """
        test index with selenium
        """
        self.browser.get('http://127.0.0.1:8000/purbeurre/index.html')
        self.assertEqual(self.browser.title, "Pur Beurre")
        time.sleep(2)
        self.browser.quit()

    def test_seek_search_selenium(self):
        """test search product with selenium no auth
        """
        self.browser.get('http://127.0.0.1:8000/purbeurre/index.html')
        elem = self.browser.find_element_by_id('search-nav')
        elem.send_keys('boisson' + Keys.RETURN)
        time.sleep(2)
        self.assertEqual(self.browser.title, "Resultats de votre recherche")
        time.sleep(2)
        self.browser.quit()

    def connect(self):
        self.browser.get('http://127.0.0.1:8000/auth/sign_in.html')
        inputusername = self.browser.find_element_by_id('inputEmail_connect')
        inputusername.send_keys('anthony.thillerot@laposte.nettt')
        inputpassword = self.browser.find_element_by_id(
            'inputPassword_connect')
        inputpassword.send_keys('azerty')
        # grid = self.browser.find_element_by_id('gridCheck_connect')
        self.browser.execute_script(
            "document.getElementById('gridCheck_connect').checked = true;")
        # button = self.browser.find_element_by_id('button_valid_form')
        self.browser.execute_script(
            "document.getElementById('button_valid_form').click();")

    def test_connection_selenium(self):
        """test connection with selenium
        """
        self.connect()
        time.sleep(2)
        self.assertEqual(self.browser.title, "Bienvenue Frost101")
        time.sleep(2)
        self.browser.quit()

    def test_seek_search_connection_selenium(self):
        """test searh connection with selenium
        """
        self.connect()
        time.sleep(2)
        self.assertEqual(self.browser.title, "Bienvenue Frost101")

        self.browser.get('http://127.0.0.1:8000/purbeurre/index.html')
        elem = self.browser.find_element_by_id('search-nav')
        elem.send_keys('boisson' + Keys.RETURN)
        time.sleep(2)
        self.assertEqual(self.browser.title, "Resultats de votre recherche")
        element_art = self.browser.find_elements_by_xpath(
            "//div[@id='div_card_all']/div")
        self.assertEqual(len(element_art), 1)
        time.sleep(2)
        self.browser.quit()

    def test_show_product_selenium(self):
        """test show_product with selenium
        """
        self.connect()
        time.sleep(5)
        self.assertEqual(self.browser.title, "Bienvenue Frost101")
        self.browser.get(
            'http://127.0.0.1:8000/purbeurre/show_product.html/?id=1&search=boisson')  # noqa: E501
        elem = self.browser.find_element_by_class_name(
            'card_description').find_elements_by_tag_name("h5")[0]
        self.assertEqual(elem.text, "Repères nutritionnels pour 100g :")
        time.sleep(2)
        self.browser.quit()      
