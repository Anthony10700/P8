from django.db import models

# Create your models here.
# class Users_pur_beurre(models.Model):
#     inputUsername = models.CharField(max_length=200, unique=True , null=False)
#     inputemail = models.EmailField(max_length=200, unique=True , null=False)
#     inputPassword = models.CharField(max_length=256, unique=True , null=False)
#     inputNom = models.CharField(max_length=45, unique=False , null=True)
#     inputprenom = models.CharField(max_length=45, unique=False , null=True)
#     inputPhone = models.CharField(max_length=14, unique=True , null=True)
#     date_created_at = models.DateTimeField(null=False, auto_now_add=True)
#     is_admin = models.BooleanField(unique=False , null=True)
    
#     class Meta:
#         verbose_name = "Users_pur_beurre"

#     def __str__(self):
#         return self.inputUsername


# class Categories(models.Model):
#     name = models.CharField(max_length=200, unique=True , null=False)
#     url = models.URLField(max_length=200, unique=True , null=False)
#     nb_of_products = models.IntegerField(null=True)

# class Product(models.Model):
#     name = models.CharField(max_length=200, unique=False , null=False)
#     countries = models.CharField(max_length=200, unique=False , null=True)
#     id_openfoodfacts = models.CharField(max_length=200, unique=True , null=False)
#     url = models.URLField(max_length=200, unique=True , null=False)
#     image_url = models.URLField(max_length=200, unique=True , null=False)
#     store = models.CharField(max_length=200, unique=False , null=True)
#     nutriscore_grade = models.CharField(max_length=1, unique=False , null=False)
#     categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

# class Products_save(models.Model):
#     user_id = models.ManyToManyField(Users)
#     product_id = models.ManyToManyField(Product)
