from django.test import TestCase, RequestFactory
from auth.forms import CustomUserCreationForm
from auth.services.auth_services import sign_validation, account_get_info, connect_validation, get_history_article
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your tests here.


class TestMyServicesAuth(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.factory = RequestFactory()
        self.client = Client()

    def make_account(self):
        info = {"inputUsername": "Test_accound2", "inputemail": "Test-accound@monmail.com2", "inputPassword1": "Test_psw2",
                "inputPassword2": "Test_psw2", "inputNom": "Test_Nom", "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])

    def test_sign_validation(self):
        info = {"inputUsername": "Test_accound", "inputemail": "Test-accound@monmail.com", "inputPassword1": "Test_psw",
                "inputPassword2": "Test_psw", "inputNom": "Test_Nom", "inputprenom": "Test_prenom"}
        request = self.factory.post('/auth/sign_in.html', data=info)
        request.session = self.client.session
        result = sign_validation(request)
        result_dict = {"methode": "redirect", "value": "account"}
        self.assertEqual(result, result_dict)

    def test_account_get_info(self):
        request = self.factory.get('/auth/account.html')
        request.user = User.objects.create_user(
            username='jacob', email='jacob@test.fr', password='top_secret')
        account_get = account_get_info(request)
        request.session = self.client.session
        request_response_dict = {"title": "Bienvenue " + request.user.username,
                                 "account_info": {"Email": request.user.email,
                                                  "Speudo": request.user.username,
                                                  "Prénom": request.user.first_name,
                                                  "Nom": request.user.last_name}}
        self.assertEqual(account_get, request_response_dict)
        logout(request)
        account_get = account_get_info(request)
        request_response_dict = {}
        self.assertEqual(account_get, request_response_dict)

    def test_connect_validation(self):
        self.make_account()
        info = {"inputUsername": "Test_accound2", "inputPassword": "Test_psw2"}
        request = self.factory.post('/auth/sign_in.html', data=info)
        request.session = self.client.session
        # request.user = User.objects.get(username="Test_accound2")
        result_dict = {"methode": "redirect", "value": "account"}
        resulta = connect_validation(request)
        self.assertEqual(result_dict, resulta)

    def test_get_history_article(self):
        self.make_account()
        info = {"inputUsername": "Test_accound2", "inputPassword": "Test_psw2"}
        request = self.factory.post('/auth/sign_in.html', data=info)
        request.session = self.client.session
        request.user = User.objects.get(username="Test_accound2")
        resulta = get_history_article(request, 6)
        if "methode" in resulta and "value" in resulta and "paginate" in resulta and "seek" in resulta:
            self.assertEqual(True, True)
        else:
            self.assertEqual(False, True)