"""
        class of test Services purbeurre
    """
import json
from django.test import RequestFactory, TransactionTestCase, Client
from django.contrib.auth import get_user_model
from purbeurre.models import Categories, Product
from purbeurre.services.purbeurre_services import save_product_result,\
    get_articles, show_specify_product,\
    remove_product, replace_indent, get_page
# Create your tests here.
from purbeurre.templatetags.utils import get_item


class TestMyServicesPurbeurre(TransactionTestCase):
    """This class is for the service worker of app purbeurre

    Args:
        TransactionTestCase ([type]): TransactionTestCase because
        Every test needs setUp method.
    """
    reset_sequences = True

    def setUp(self):
        """This method similar at __init__ for each instance
        """
        # Every test needs a client.
        self.factory = RequestFactory()
        self.client = Client()
        self.make_account()
        self.create_product()

    def make_account(self):
        """This method make a account for testing the url form sign_in
        """
        info = {"inputUsername": "Test_accound2",
                "inputemail": "Test-accound@monmail.com2",
                "inputPassword1": "Test_psw2",
                "inputPassword2": "Test_psw2",
                "inputNom": "Test_Nom",
                "inputprenom": "Test_prenom"}
        response = self.client.post('/auth/sign_in.html', data=info)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/auth/account.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['account_info']["Email"], info["inputemail"])

    def create_product(self):
        """This method create a product for testing
        """
        categories = Categories.objects.create(
            name="boissons-a-la-canneberge",
            url="https://fr.openfoodfacts.org/categorie/\
                boissons-a-la-canneberge.json",
            nb_of_products=int(54))

        categories.save()
        categories_fk = Categories.objects.get(name="boissons-a-la-canneberge")
        product_nutriments = {
            "fat_value": "0.5", "nova-group_100g": 4,
            "carbohydrates": "10.5", "saturated-fat_value": "0.1",
            "fat_serving": 1, "fat_100g": "0.5", "salt": 0, "sodium_value": 0,
            "fat": "0.5", "carbohydrates_serving": 21, "sugars_value": "10.5",
            "sodium_serving": 0, "salt_unit": "g",
            "fruits-vegetables-nuts_serving": 25, "salt_value": 0, "sodium": 0,
            "energy-kcal": 44, "energy-kcal_serving": 88,
            "fruits-vegetables-nuts_100g": 25, "saturated-fat_unit": "g",
            "nova-group_serving": 4, "sodium_unit": "g", "proteins_unit": "g",
            "energy_unit": "kcal", "salt_serving": 0,
            "fruits-vegetables-nuts-estimate-from-ingredients_100g": 25,
            "sodium_100g": 0, "sugars": "10.5", "energy_100g": 184,
            "proteins_value": "0.5", "nova-group": 4,
            "saturated-fat_serving": "0.2", "saturated-fat_100g": "0.1",
            "sugars_serving": 21, "proteins_100g": "0.5", "energy": 184,
            "carbohydrates_value": "10.5", "nutrition-score-fr_100g": 14,
            "carbon-footprint-from-known-ingredients_100g": "7.5",
            "carbon-footprint-from-known-ingredients_serving": 15,
            "energy-kcal_100g": 44, "carbohydrates_100g": "10.5",
            "salt_100g": 0, "fruits-vegetables-nuts_value": 25,
            "carbohydrates_unit": "g", "saturated-fat": "0.1",
            "carbon-footprint-from-known-ingredients_product": 75,
            "proteins_serving": 1, "fruits-vegetables-nuts_label": "0",
            "fruits-vegetables-nuts_unit": "g", "energy-kcal_value": 44,
            "energy-kcal_unit": "kcal", "energy_serving": 368,
            "nutrition-score-fr": 14, "sugars_100g": "10.5",
            "fruits-vegetables-nuts": 25, "sugars_unit": "g",
            "proteins": "0.5", "fat_unit": "g", "energy_value": 44}

        product_bdd = Product.objects.create(
            name="Cranberry",
            countries="France",
            id_openfoodfacts="3596710355051",
            url="https://fr.openfoodfacts.org/produit/\
                3596710355051/cranberry-auchan",
            image_url="https://static.openfoodfacts.org/\
                images/products/359/671/035/5051/front_fr.45.400.jpg",
            store="Auchan",
            nutriscore_grade="e",
            categories=categories_fk,
            nutriments=json.dumps(product_nutriments))

        product_bdd.save()

    def test_save_product_result(self):
        """This method test save_product_result
        """
        user = get_user_model()
        info = {"id": "1", "search": "boissons"}
        request = self.factory.post('/purbeurre/resultats.html', data=info)
        request.session = self.client.session
        request.user = user.objects.get(username="Test_accound2")
        result = save_product_result(request.user, request)
        result_dict = {"methode": "redirect", "value": request.path_info +
                       "?search=" + request.POST["search"],
                       "message": 'Votre article à bien été enregistré'}
        self.assertEqual(result, result_dict)

    def test_get_articles(self):
        """This method test get_article
        """
        user = get_user_model()
        info = {"search": "boissons"}
        request = self.factory.get('/purbeurre/resultats.html', data=info)
        request.session = self.client.session
        request.user = user.objects.get(username="Test_accound2")
        rst = get_articles(request, 6)
        if "methode" in rst and "value" in rst \
                and "paginate" in rst and "seek" in rst:
            self.assertEqual(True, True)
        else:
            self.assertEqual(False, True)

    def test_show_specify_product(self):
        """This method test show_specify_product
        """
        user = get_user_model()
        info = {"id": "1"}
        request = self.factory.get('show_product.html/', data=info)
        request.session = self.client.session
        request.user = user.objects.get(username="Test_accound2")
        product_show = Product.objects.get(id=request.GET["id"])
        result = show_specify_product(request)
        prod = json.loads(product_show.nutriments)
        search = ""
        result_dict = {
            "methode": "render", "value": 'purbeurre/show_product.html',
            "context": {'title': "resultats de votre recherche",
                        'articles_list': product_show,
                        'aliment_search': search,
                        "nutriments": prod}}
        self.assertEqual(result, result_dict)

    def test_remove_product(self):
        """This method test remove_product
        """
        user = get_user_model()
        self.test_save_product_result()
        info = {"id": "1"}
        request = self.factory.post('unsave.html', data=info)
        request.session = self.client.session
        request.user = user.objects.get(username="Test_accound2")
        product_show = request.user.save_product.all()
        self.assertEqual(len(product_show), 1)
        remove_product(request)
        product_show = request.user.save_product.all()
        self.assertEqual(len(product_show), 0)

    def test_get_item(self):
        """This method test get_item
        """
        dict_in = {"id": "test"}
        self.assertEqual(get_item(dict_in, "id"), "test")

    def test_replace_indent(self):
        """This method test replace_short dash
        """
        product_show = Product.objects.get(id="1")

        product_show = replace_indent(product_show)

        self.assertEqual(product_show.categories.name,
                         "boissons a la canneberge")

    def test_get_page(self):
        """This method test get_page
        """
        product_show = Product.objects.filter(
            id="1")
        recherche, paginate = get_page(1, product_show, 6)

        self.assertEqual(recherche[0].name, "Cranberry")
        self.assertEqual(paginate, False)
