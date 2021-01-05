from django.db import models
from django.conf import settings
# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    url = models.URLField(max_length=200, unique=True, null=False)
    nb_of_products = models.IntegerField(null=True)


class Product(models.Model):
    name = models.CharField(max_length=800, unique=False, null=False)
    countries = models.CharField(max_length=800, unique=False, null=True)
    id_openfoodfacts = models.CharField(
        max_length=800, unique=True, null=False)
    url = models.URLField(max_length=800, unique=True, null=False)
    image_url = models.URLField(max_length=800, unique=True, null=False)
    store = models.CharField(max_length=800, unique=False, null=True)
    nutriscore_grade = models.CharField(max_length=1, unique=False, null=False)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    nutriments = models.CharField(max_length=8000, unique=False, null=False)
    user_id = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="save_product", name="save_product")


# class Products_save(models.Model):

#     product_id = models.ManyToManyField(Product)
