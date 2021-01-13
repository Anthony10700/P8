"""
url file
"""
from django.urls import path

from . import views

urlpatterns = [
    path('sign_in.html', views.sign_in, name="sign_in"),
    path('connection.html', views.connect, name="connection"),
    path('account.html', views.account,  name="account"),
    path('deconnection.html', views.logout_view, name="deconnection"),
    path('history.html', views.history, name="history")
]
