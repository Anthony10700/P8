"""Test file for all class models
    """
import json
from django.test import TestCase
from purbeurre.models import Product, Categories


class ProductModelTest(TestCase):
    """Class test of modef Product

    Args:
        TestCase ([type]): [description]
    """
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods
        """

        categories = Categories.objects.create(
            name="boissons-a-la-canneberge",
            url="https://fr.openfoodfacts.org/categorie/\
                boissons-a-la-canneberge.json",
            nb_of_products=int(54))

        categories.save()
        product_nutriments = {
            "fat_value": "0.5", "nova-group_100g": 4, "carbohydrates": "10.5",
            "saturated-fat_value": "0.1", "fat_serving": 1, "fat_100g": "0.5",
            "salt": 0, "sodium_value": 0, "fat": "0.5",
            "carbohydrates_serving": 21, "sugars_value": "10.5",
            "sodium_serving": 0, "salt_unit": "g",
            "fruits-vegetables-nuts_serving": 25, "salt_value": 0,
            "sodium": 0, "energy-kcal": 44, "energy-kcal_serving": 88,
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

        categories_fk = Categories.objects.get(name="boissons-a-la-canneberge")
        product_bdd = Product.objects.create(
            name="Cranberry",
            countries="France",
            id_openfoodfacts="3596710355051",
            url="https://fr.openfoodfacts.org/produit/3596710355051/cranberry-auchan",  # noqa: E501
            image_url="https://static.openfoodfacts.org/images/products/359/671/035/5051/front_fr.45.400.jpg",  # noqa: E501
            store="Auchan",
            nutriscore_grade="e",
            categories=categories_fk,
            nutriments=json.dumps(product_nutriments))

        product_bdd.save()

    def setUp(self):
        self.product_nutriments = {
            "fat_value": "0.5", "nova-group_100g": 4, "carbohydrates": "10.5",
            "saturated-fat_value": "0.1", "fat_serving": 1, "fat_100g": "0.5",
            "salt": 0, "sodium_value": 0, "fat": "0.5",
            "carbohydrates_serving": 21, "sugars_value": "10.5",
            "sodium_serving": 0, "salt_unit": "g",
            "fruits-vegetables-nuts_serving": 25, "salt_value": 0,
            "sodium": 0, "energy-kcal": 44, "energy-kcal_serving": 88,
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

    def test_name(self):
        """test_name in product
        """
        product = Product.objects.get(id=1)
        field_label = product.name
        self.assertEqual(field_label, "Cranberry")

    def test_countries(self):
        """test_countries in product
        """
        product = Product.objects.get(id=1)
        field_label = product.countries
        self.assertEqual(field_label, "France")

    def test_id_openfoodfacts(self):
        """test_id_openfoodfacts in product
        """
        product = Product.objects.get(id=1)
        field_label = product.id_openfoodfacts
        self.assertEqual(field_label, "3596710355051")

    def test_url(self):
        """test_url in product
        """
        product = Product.objects.get(id=1)
        field_label = product.url
        self.assertEqual(
            field_label,
            "https://fr.openfoodfacts.org/produit/3596710355051/cranberry-auchan")  # noqa: E501

    def test_image_url(self):
        """test_image_url in product
        """
        product = Product.objects.get(id=1)
        field_label = product.image_url
        self.assertEqual(
            field_label,
            "https://static.openfoodfacts.org/images/products/359/671/035/5051/front_fr.45.400.jpg")  # noqa: E501

    def test_store(self):
        """test_store in product
        """
        product = Product.objects.get(id=1)
        field_label = product.store
        self.assertEqual(field_label, "Auchan")

    def test_nutriscore_grade(self):
        """test_nutriscore_grade in product
        """
        product = Product.objects.get(id=1)
        field_label = product.nutriscore_grade
        self.assertEqual(field_label, "e")

    def test_categories(self):
        """test_categories in product
        """
        product = Product.objects.get(id=1)
        field_label = product.categories.name
        self.assertEqual(field_label, "boissons-a-la-canneberge")

    def test_nutriments(self):
        """test_nutriments in product
        """
        product = Product.objects.get(id=1)
        field_label = product.nutriments
        self.assertEqual(field_label, json.dumps(self.product_nutriments))


class CategoriesModelTest(TestCase):
    """Class test of modef categories

    Args:
        TestCase ([type]): [description]
    """
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods
        """
        categories = Categories.objects.create(
            name="boissons",
            url="https://fr.openfoodfacts.org/categorie/boissons.json",
            nb_of_products=int(5))

        categories.save()

    def test_name(self):
        """test_name categories
        """
        categories = Categories.objects.get(name="boissons")
        field_label = categories.name
        self.assertEqual(field_label, "boissons")

    def test_url(self):
        """test_url categories
        """
        categories = Categories.objects.get(name="boissons")
        field_label = categories.url
        self.assertEqual(
            field_label,
            "https://fr.openfoodfacts.org/categorie/boissons.json")

    def test_nb_of_products(self):
        """test_nb_of_products categories
        """
        categories = Categories.objects.get(name="boissons")
        field_label = categories.nb_of_products
        self.assertEqual(field_label, 5)
