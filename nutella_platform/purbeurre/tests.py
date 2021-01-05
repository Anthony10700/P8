from django.test import TestCase, RequestFactory, TransactionTestCase
from purbeurre.services.purbeurre_services import save_product_result, get_articles, show_specify_product, remove_product
from django.contrib.auth.models import AnonymousUser, User
from purbeurre.models import Categories
from purbeurre.models import Product
# Create your tests here.
from django.test import Client


class CreateUserTests(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        

    def test_sign_in(self):
        response = self.client.get('/auth/sign_in.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Inscription")

        self.make_account()

        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/sign_in.html')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/auth/account.html")

    def test_index(self):
        response = self.client.get('/purbeurre/index.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], "Pur Beurre")

    def test_accound(self):
        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], "Test-accound@monmail.com")

    def test_history(self):
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
        response = self.client.get('/auth/deconnection.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['title'], "Vous n'êtes pas connecté.")

        self.make_account()
        self.client.login(username='Test_accound', password='Test_psw')
        response = self.client.get('/auth/deconnection.html')
        self.assertEqual(response.context['title'], "Déconnexion")

    def test_connect(self):

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
        info = {"inputUsername": "Test_accound", "inputemail": "Test-accound@monmail.com", "inputPassword1": "Test_psw",
                "inputPassword2": "Test_psw", "inputNom": "Test_Nom", "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])


class TestMyServicesPurbeurre(TransactionTestCase):
    reset_sequences = True
    def setUp(self):
        # Every test needs a client.
        self.factory = RequestFactory()
        self.client = Client()
        self.make_account()
        self.create_product()

    def make_account(self):
        info = {"inputUsername": "Test_accound2", "inputemail": "Test-accound@monmail.com2", "inputPassword1": "Test_psw2",
                "inputPassword2": "Test_psw2", "inputNom": "Test_Nom", "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])



    def create_product(self):
        
        categories = Categories.objects.create(name="boissons-a-la-canneberge",
                                                   url="https://fr.openfoodfacts.org/categorie/boissons-a-la-canneberge.json",
                                                   nb_of_products=int(54))

        categories.save()
        categories_fk = Categories.objects.get(name="boissons-a-la-canneberge")

        product_bdd = Product.objects.create(name="Cranberry",
                                             countries="France",
                                             id_openfoodfacts="3596710355051",
                                             url="https://fr.openfoodfacts.org/produit/3596710355051/cranberry-auchan",
                                             image_url="https://static.openfoodfacts.org/images/products/359/671/035/5051/front_fr.45.400.jpg",
                                             store="Auchan",
                                             nutriscore_grade="e",
                                             categories=categories_fk,
                                             nutriments="{""fat_value"": ""0.5"", ""nova-group_100g"": 4, ""carbohydrates"": ""10.5"", ""saturated-fat_value"": ""0.1"", ""fat_serving"": 1, ""fat_100g"": ""0.5"", ""salt"": 0, ""sodium_value"": 0, ""fat"": ""0.5"", ""carbohydrates_serving"": 21, ""sugars_value"": ""10.5"", ""sodium_serving"": 0, ""salt_unit"": ""g"", ""fruits-vegetables-nuts_serving"": 25, ""salt_value"": 0, ""sodium"": 0, ""energy-kcal"": 44, ""energy-kcal_serving"": 88, ""fruits-vegetables-nuts_100g"": 25, ""saturated-fat_unit"": ""g"", ""nova-group_serving"": 4, ""sodium_unit"": ""g"", ""proteins_unit"": ""g"", ""energy_unit"": ""kcal"", ""salt_serving"": 0, ""fruits-vegetables-nuts-estimate-from-ingredients_100g"": 25, ""sodium_100g"": 0, ""sugars"": ""10.5"", ""energy_100g"": 184, ""proteins_value"": ""0.5"", ""nova-group"": 4, ""saturated-fat_serving"": ""0.2"", ""saturated-fat_100g"": ""0.1"", ""sugars_serving"": 21, ""proteins_100g"": ""0.5"", ""energy"": 184, ""carbohydrates_value"": ""10.5"", ""nutrition-score-fr_100g"": 14, ""carbon-footprint-from-known-ingredients_100g"": ""7.5"", ""carbon-footprint-from-known-ingredients_serving"": 15, ""energy-kcal_100g"": 44, ""carbohydrates_100g"": ""10.5"", ""salt_100g"": 0, ""fruits-vegetables-nuts_value"": 25, ""carbohydrates_unit"": ""g"", ""saturated-fat"": ""0.1"", ""carbon-footprint-from-known-ingredients_product"": 75, ""proteins_serving"": 1, ""fruits-vegetables-nuts_label"": ""0"", ""fruits-vegetables-nuts_unit"": ""g"", ""energy-kcal_value"": 44, ""energy-kcal_unit"": ""kcal"", ""energy_serving"": 368, ""nutrition-score-fr"": 14, ""sugars_100g"": ""10.5"", ""fruits-vegetables-nuts"": 25, ""sugars_unit"": ""g"", ""proteins"": ""0.5"", ""fat_unit"": ""g"", ""energy_value"": 44}")

        product_bdd.save()





    def test_save_product_result(self):

        info = {"id": "1", "search": "boissons"}        
        request = self.factory.post('/purbeurre/resultats.html', data=info)
        request.session = self.client.session
        request.user = User.objects.get(username="Test_accound2")
        result = save_product_result(request.user, request)
        result_dict = {"methode": "redirect", "value": request.path_info +
                       "?search=" + request.POST["search"], "message": 'Votre article à bien été enregistré'}
        self.assertEqual(result, result_dict)

    def test_get_articles(self):
             
        info = {"search": "boissons"}
        request = self.factory.get('/purbeurre/resultats.html', data=info)
        request.session = self.client.session
        request.user = User.objects.get(username="Test_accound2")
        resulta = get_articles(request, 6)        
        if "methode" in resulta and "value" in resulta and "paginate" in resulta and "seek" in resulta:
            self.assertEqual(True, True)
        else:
            self.assertEqual(False, True)