"""
url urlpatterns of purbeurre app
"""
from django.urls import path

from . import views

urlpatterns = [
    path('resultats.html', views.resultats, name="resultat"),
    path('show_product.html/', views.show_product, name="show_product"),
    path('unsave.html', views.unsave, name="unsave"),
    path('legal_notice.html', views.legale, name="legal_notice"),
    path('index.html', views.index, name="index")
]
