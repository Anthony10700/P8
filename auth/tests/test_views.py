"""
        class of test viewe purbeurre
    """
import json
from django.test import TestCase, RequestFactory, TransactionTestCase, Client
from purbeurre.services.purbeurre_services import save_product_result, get_articles, show_specify_product, remove_product, replace_indent, get_page
from django.contrib.auth import get_user_model
from purbeurre.models import Categories, Product
# Create your tests here.
from purbeurre.templatetags.utils import get_item


class UrlAuthTests(TestCase):
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

    def test_sign_in(self):
        """
        This method test the sign_in url
        """
        response = self.client.get('/auth/sign_in.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Inscription")

        self.make_account()

        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/sign_in.html')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/account.html")

    def test_accound(self):
        """This methode test the account url
        """
        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], "Test-accound@monmail.com")

    def test_history(self):
        """This method test the history url
        """
        response = self.client.get('/auth/history.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['title'], "Vous n'êtes pas connecté.")

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/history.html')
        self.assertEqual(
            response.context['title'], "Historique de vos articles")

    def test_deconnection(self):
        """This method test the deconnection url
        """
        response = self.client.get('/auth/deconnection.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['title'], "Vous n'êtes pas connecté.")

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/deconnection.html')
        self.assertEqual(response.context['title'], "Déconnexion")

    def test_connect(self):
        """This method test the connection url
        """
        response = self.client.get('/auth/connection.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Inscription")

        self.make_account()

        info = {"inputUsername": "Test_accound", "inputPassword": "Test_psw"}
        response = self.client.post('/auth/connection.html', data=info)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/account.html")

        info = {"inputUsername": "Test_accound", "inputPassword": "Tsdqsdqs"}
        response = self.client.post('/auth/connection.html', data=info)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/sign_in.html")

    def make_account(self):
        """This method make a account for testing the url form sign_in
        """
        info = {"inputUsername": "Test_accound", "inputemail": "Test-accound@monmail.com",
                "inputPassword1": "Test_psw", "inputPassword2": "Test_psw", "inputNom": "Test_Nom",
                "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])
