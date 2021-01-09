"""
        class of test viewe purbeurre
    """
import json
import time
from django.test import TestCase, RequestFactory, TransactionTestCase, Client
from purbeurre.services.purbeurre_services import save_product_result, get_articles, show_specify_product, remove_product, replace_indent, get_page
from django.contrib.auth import get_user_model
from purbeurre.models import Categories, Product
# Create your tests here.
from purbeurre.templatetags.utils import get_item
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# TODO quand connecter image profif changer le passage de la souris

class UrlPurbeurreTests(TestCase):
    """
    Class test of url of app

    Args:
        TestCase ([type]): [description]
    """
    def setUp(self):
        """This method similar at __init__ for each instance
        """
        # Every test needs a client.
        self.client = Client()
        self.browser = webdriver.Firefox()

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
        self.assertEqual( self.browser.title, "Pur Beurre")
        time.sleep(2)
        self.browser.quit()

    def test_seek_search_selenium(self):
        """test search product with selenium no auth
        """
        self.browser.get('http://127.0.0.1:8000/purbeurre/index.html')
        elem =  self.browser.find_element_by_id('search-nav')
        elem.send_keys('boisson' + Keys.RETURN)
        time.sleep(2)
        self.assertEqual( self.browser.title, "Resultats de votre recherche")
        time.sleep(2)
        self.browser.quit()

    def test_connection_selenium(self):
        """test connection with selenium
        """
        self.browser.get('http://127.0.0.1:8000/auth/sign_in.html')
        inputusername =  self.browser.find_element_by_id('inputUsername')
        inputusername.send_keys('Frost10')
        inputpassword =  self.browser.find_element_by_id('inputPassword')
        inputpassword.send_keys('azerty')
        grid =  self.browser.find_element_by_id('gridCheck')
        grid.click()
        button =  self.browser.find_element_by_id('button_valid_form')
        button.click()
        time.sleep(2)
        self.assertEqual( self.browser.title, "Bienvenue Frost10")
        time.sleep(2)
        self.browser.quit()

    def test_seek_search_connection_selenium(self):
        """test searh connection with selenium
        """
        self.browser.get('http://127.0.0.1:8000/auth/sign_in.html')
        inputusername =  self.browser.find_element_by_id('inputUsername')
        inputusername.send_keys('Frost10')
        inputpassword =  self.browser.find_element_by_id('inputPassword')
        inputpassword.send_keys('azerty')
        grid =  self.browser.find_element_by_id('gridCheck')
        grid.click()
        button =  self.browser.find_element_by_id('button_valid_form')
        button.click() 
        time.sleep(2)
        self.assertEqual( self.browser.title, "Bienvenue Frost10")

        self.browser.get('http://127.0.0.1:8000/purbeurre/index.html')
        elem =  self.browser.find_element_by_id('search-nav')
        elem.send_keys('boisson' + Keys.RETURN)
        time.sleep(2)
        self.assertEqual(self.browser.title, "Resultats de votre recherche")
        element_art = self.browser.find_elements_by_xpath("//div[@id='div_card_all']/div")
        self.assertEqual(len(element_art),6)
        time.sleep(2)
        self.browser.quit()


    def test_show_product_selenium(self):
        """test show_product with selenium
        """
        self.browser.get('http://127.0.0.1:8000/auth/sign_in.html')
        inputusername =  self.browser.find_element_by_id('inputUsername')
        inputusername.send_keys('Frost10')
        inputpassword =  self.browser.find_element_by_id('inputPassword')
        inputpassword.send_keys('azerty')
        grid =  self.browser.find_element_by_id('gridCheck')
        grid.click()
        button =  self.browser.find_element_by_id('button_valid_form')
        button.click()    
        time.sleep(2)
        self.assertEqual( self.browser.title, "Bienvenue Frost10")

        self.browser.get('http://127.0.0.1:8000/purbeurre/show_product.html/?id=8954&search=boisson')
        elem = self.browser.find_element_by_class_name('card_description').find_elements_by_tag_name("h5")[0]
        self.assertEqual(elem.text, "Repères nutritionnels pour 100g :")
        time.sleep(2)
        self.browser.quit()    
# TODO faire les autres test des url purbeurre app unsave , legal etc