"""
        class of test Services Auth
    """
import json
from django.test import RequestFactory, TransactionTestCase, Client
from auth.services.auth_services import sign_validation, account_get_info, connect_validation, get_history_article, replace_short_dash, get_page
from django.contrib.auth import logout, get_user_model
from purbeurre.models import Categories, Product
from auth import admin
from auth import apps
from auth import models

# Create your tests here.


class TestMyServicesAuth(TransactionTestCase):
    """class of test Services Auth

    Args:
        TransactionTestCase ([type]): TransactionTestCase and not
        TestCase because Every test needs "setUp method"
    """
    reset_sequences = True

    def setUp(self):
        """[summary]
        """
        # Every test needs a client.
        self.factory = RequestFactory()
        self.client = Client()
        self.create_product()

    def make_account(self):
        """this method can create an account for the test
        """
        info = {"inputUsername": "Test_accound2", "inputemail": "Test-accound@monmail.com2",
                "inputPassword1": "Test_psw2",
                "inputPassword2": "Test_psw2", "inputNom": "Test_Nom",
                "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])

    def test_sign_validation(self):
        """this method test the inscription
        """
        info = {"inputUsername": "Test_accound", "inputemail":
                "Test-accound@monmail.com", "inputPassword1": "Test_psw",
                "inputPassword2": "Test_psw",
                "inputNom": "Test_Nom", "inputprenom": "Test_prenom"}
        request = self.factory.post('/auth/sign_in.html', data=info)
        request.session = self.client.session
        result = sign_validation(request)
        result_dict = {"methode": "redirect", "value": "account"}
        self.assertEqual(result, result_dict)

    def test_account_get_info(self):
        """this method test the account information
        """
        user = get_user_model()
        request = self.factory.get('/auth/account.html')
        request.user = user.objects.create_user(
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
        """this method test the account connection
        """
        self.make_account()
        info = {"inputUsername": "Test_accound2", "inputPassword": "Test_psw2"}
        request = self.factory.post('/auth/sign_in.html', data=info)
        request.session = self.client.session
        # request.user = User.objects.get(username="Test_accound2")
        result_dict = {"methode": "redirect", "value": "account"}
        resulta = connect_validation(request)
        self.assertEqual(result_dict, resulta)

    def test_get_history_article(self):
        """this method can get the history article
        """
        user = get_user_model()
        self.make_account()
        info = {"inputUsername": "Test_accound2", "inputPassword": "Test_psw2"}
        request = self.factory.post('/auth/sign_in.html', data=info)
        request.session = self.client.session
        request.user = user.objects.get(username="Test_accound2")
        rst = get_history_article(request, 6)
        if "methode" in rst and "value" in rst and "paginate" in rst and "seek" in rst:
            self.assertEqual(True, True)
        else:
            self.assertEqual(False, True)

    def test_replace_indent(self):
        """this method test if all the short dash has been removed from the string 
        """
        product_show = Product.objects.get(id="1")

        product_show = replace_short_dash(product_show)

        self.assertEqual(product_show.categories.name,
                         "boissons a la canneberge")

    def create_product(self):
        """this method create a object product
        """
        categories = Categories.objects.create(name="boissons-a-la-canneberge",
                                               url="https://fr.openfoodfacts.org/categorie/boissons-a-la-canneberge.json",
                                               nb_of_products=int(54))

        categories.save()
        categories_fk = Categories.objects.get(name="boissons-a-la-canneberge")
        product_nutriments = {"fat_value": "0.5", "nova-group_100g": 4, "carbohydrates": "10.5", "saturated-fat_value": "0.1", "fat_serving": 1, "fat_100g": "0.5", "salt": 0, "sodium_value": 0, "fat": "0.5", "carbohydrates_serving": 21, "sugars_value": "10.5", "sodium_serving": 0, "salt_unit": "g", "fruits-vegetables-nuts_serving": 25, "salt_value": 0, "sodium": 0, "energy-kcal": 44, "energy-kcal_serving": 88, "fruits-vegetables-nuts_100g": 25, "saturated-fat_unit": "g", "nova-group_serving": 4, "sodium_unit": "g", "proteins_unit": "g", "energy_unit": "kcal", "salt_serving": 0, "fruits-vegetables-nuts-estimate-from-ingredients_100g": 25, "sodium_100g": 0, "sugars": "10.5", "energy_100g": 184, "proteins_value": "0.5", "nova-group": 4, "saturated-fat_serving": "0.2", "saturated-fat_100g": "0.1",
                              "sugars_serving": 21, "proteins_100g": "0.5", "energy": 184, "carbohydrates_value": "10.5", "nutrition-score-fr_100g": 14, "carbon-footprint-from-known-ingredients_100g": "7.5", "carbon-footprint-from-known-ingredients_serving": 15, "energy-kcal_100g": 44, "carbohydrates_100g": "10.5", "salt_100g": 0, "fruits-vegetables-nuts_value": 25, "carbohydrates_unit": "g", "saturated-fat": "0.1", "carbon-footprint-from-known-ingredients_product": 75, "proteins_serving": 1, "fruits-vegetables-nuts_label": "0", "fruits-vegetables-nuts_unit": "g", "energy-kcal_value": 44, "energy-kcal_unit": "kcal", "energy_serving": 368, "nutrition-score-fr": 14, "sugars_100g": "10.5", "fruits-vegetables-nuts": 25, "sugars_unit": "g", "proteins": "0.5", "fat_unit": "g", "energy_value": 44}
        product_bdd = Product.objects.create(name="Cranberry",
                                             countries="France",
                                             id_openfoodfacts="3596710355051",
                                             url="https://fr.openfoodfacts.org/produit/3596710355051/cranberry-auchan",
                                             image_url="https://static.openfoodfacts.org/images/products/359/671/035/5051/front_fr.45.400.jpg",
                                             store="Auchan",
                                             nutriscore_grade="e",
                                             categories=categories_fk,
                                             nutriments=json.dumps(product_nutriments))

        product_bdd.save()

    def test_get_page(self):
        """this method can get back a chosen page of the paginator
        """
        product_show = Product.objects.filter(
            id="1")
        recherche, paginate = get_page(1, product_show, 6)

        self.assertEqual(recherche[0].name, "Cranberry")
        self.assertEqual(paginate, False)
