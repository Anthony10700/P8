from django.test import TestCase

# Create your tests here.
from django.test import Client


class CreateUserTests(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_sign_in(self):
        response = self.client.get('/sign_in.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Inscription")

        self.make_account()

        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/sign_in.html')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account.html")

    def test_index(self):
        response = self.client.get('/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Pur Beurre")

    def test_accound(self):
        response = self.client.get('/account.html')
        self.assertEqual(response.status_code, 200)

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], "Test-accound@monmail.com")

    def test_history(self):
        response = self.client.get('/history.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['title'], "Vous n'êtes pas connecté.")

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/history.html')
        self.assertEqual(
            response.context['title'], "Historique de vos articles")

    def test_deconnection(self):
        response = self.client.get('/deconnection.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['title'], "Vous n'êtes pas connecté.")

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/deconnection.html')
        self.assertEqual(response.context['title'], "Déconnexion")

    def test_connect(self):

        response = self.client.get('/connection.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Inscription")

        self.make_account()

        info = {"inputUsername": "Test_accound", "inputPassword": "Test_psw"}
        response = self.client.post('/connection.html', data=info)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account.html")

        info = {"inputUsername": "Test_accound", "inputPassword": "Tsdqsdqs"}
        response = self.client.post('/connection.html', data=info)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/sign_in.html")

    def make_account(self):
        info = {"inputUsername": "Test_accound", "inputemail": "Test-accound@monmail.com", "inputPassword1": "Test_psw",
                "inputPassword2": "Test_psw", "inputNom": "Test_Nom", "inputprenom": "Test_prenom"}
        response = self.client.post('/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])
