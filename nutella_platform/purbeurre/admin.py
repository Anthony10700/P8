from django.contrib import admin
from purbeurre.models import Product, Categories

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields  = ['name', 'id']
    list_filter = ['categories','save_product']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    search_fields  = ['name', 'id']

