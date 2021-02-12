"""
url urlpatterns of purbeurre app
"""
from django.urls import path

from . import views


# def trigger_error(request):
#     """Methode fgfor sentry test

#     Args:
#         request ([type]): [description]
#     """
#     division_by_zero = 1 / 0


urlpatterns = [
    path('resultats.html', views.resultats, name="resultat"),
    path('show_product.html/', views.show_product, name="show_product"),
    path('unsave.html', views.unsave, name="unsave"),
    path('legal_notice.html', views.legale, name="legal_notice"),
    path('index.html', views.index, name="index"),
    # path('sentry-debug/', trigger_error),
    path('like_dislike/', views.like_dislike, name="like_dislike")
]
