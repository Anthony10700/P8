"""Class of admin panel
"""
from django.contrib import admin
from purbeurre.models import Product, Categories

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """admin product panel

    Args:
        admin ([type]): [description]
    """
    search_fields  = ['name', 'id']
    list_filter = ['categories','save_product']

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """admin categories panel

    Args:
        admin ([type]): [description]
    """
    search_fields  = ['name', 'id']
    