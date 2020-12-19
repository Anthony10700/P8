"""The script for import api open food facts data with data base """
# !/usr/bin/python3
# -*- coding: Utf-8 -*
import json
from purbeurre.models import Categories
from purbeurre.models import Product

import requests
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'import_porduct'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nb_of_page = 1

    def add_arguments(self, parser):
        parser.add_argument('nb_page', type=int,
                            help='Number of page for download')

    def handle(self, *args, **kwargs):
        self.nb_of_page = kwargs['nb_page']
        self.main()

    def main(self):
        """This function import api open food facts data and make new DATA BASE myslq and
        table """

        list_of_categories = []

        list_of_url_categories = [
            "https://fr.openfoodfacts.org/categorie/boissons-a-la-canneberge.json",
            "https://fr.openfoodfacts.org/categorie/boissons-a-l-orange.json",
            "https://fr.openfoodfacts.org/categorie/jus-de-fruits.json",
            "https://fr.openfoodfacts.org/categorie/nectars-de-fruits.json",
            "https://fr.openfoodfacts.org/categorie/sodas-aux-fruits.json",
            "https://fr.openfoodfacts.org/categorie/boissons-chaudes.json",
            "https://fr.openfoodfacts.org/categorie/boissons-au-cafe.json",
            "https://fr.openfoodfacts.org/categorie/tisanes-infusees.json",
            "https://fr.openfoodfacts.org/categorie/boissons-au-the.json",
            "https://fr.openfoodfacts.org/categorie/gateaux.json"
        ]

        for url in list_of_url_categories:
            payload = {}
            headers = {}
            data_all = {}

            response = requests.request(
                "GET", url, headers=headers, data=payload)

            test = json.loads(response.text.encode('utf8'))
            list_of_categories.append(test)

        for product_ in list_of_url_categories:
            #  import all product for all categories in the limit nb_of_page
            list_temp = []
            for i in range(1, self.nb_of_page + 1):
                print(product_.replace(".json", "") + "/" + str(i) + ".json")
                url_in = product_.replace(".json", "") + "/" + str(i) + ".json"
                response = requests.request(
                    "GET", url_in, headers=headers, data=payload)
                data = json.loads(response.text.encode('utf8'))
                data = data["products"]
                data_temp = []
                for d_var in data:
                    if str(d_var['categories_lc']) == "fr":
                        data_temp.append(d_var)
                list_temp.extend(data_temp)
            data_all.update({str(product_).split(
                "/")[4].replace(".json", ""): list_temp})

        # print(data_all)

        print("####################################")
        print("####################################")
        print("####################################")
        print("#### Suppression des categories ####")
        print("####################################")
        print("####################################")
        print("####################################")

        for categ in Categories.objects.all():

            print(str(categ.name) + " : supprimé")
            categ.delete()

        print("#################################")
        print("#################################")
        print("#################################")
        print("#### Création des categories ####")
        print("#################################")
        print("#################################")
        print("#################################")
        for var_i, item in enumerate(list_of_url_categories):
            #  insert in database all categories completed_name, URL and nb_of_products
            product_ = list_of_categories[var_i]
            url = item
            name_produc = str(item).split("/")[4].replace(".json", "")
            nb_prod = product_["count"]

            categories = Categories.objects.create(name=name_produc,
                                                   url=url,
                                                   nb_of_products=int(nb_prod))

            print(categories.name + " : crée")

            categories.save()

        print("############################")
        print("############################")
        print("############################")
        print("#### Ajout des produits ####")
        print("############################")
        print("############################")
        print("############################")

        list_of_key = ["product_name", "countries", "id", "url", "image_url",
                       "stores", "categories"]

        for categ in data_all:
            #  insert all product in database with the fk_key FOREIGN KEY (`categories_idcategories`)"
            #  REFERENCES `openfoodfacts`.`categories` (`idcategories`)"

            print(categ)
            categories_fk = Categories.objects.get(name=categ)
            for product in data_all[categ]:
                produit_value_ok = True

                if "nutriscore_grade" in product:
                    nutri_value = product["nutriscore_grade"]
                else:
                    nutri_value = "e"

                for value in range(0, 7):
                    if not list_of_key[value] in product:
                        product[list_of_key[value]] = ""

                for key in list_of_key:
                    if len(product[key]) > 800:
                        produit_value_ok = False

                if produit_value_ok:
                    try:
                        product_bdd = Product.objects.create(name=product["product_name"],
                                                             countries=product["countries"],
                                                             id_openfoodfacts=product["id"],
                                                             url=product["url"],
                                                             image_url=product["image_url"],
                                                             store=product["stores"],
                                                             nutriscore_grade=nutri_value,
                                                             categories=categories_fk)
                        product_bdd.save()

                    except IntegrityError:
                        self.stdout.write(
                            "########## la valeur d'une clé dupliquée rompt la contrainte unique ##########")

        self.stdout.write("########## FIN ##########")


if __name__ == "__main__":
    c = Command()
    print("e")
