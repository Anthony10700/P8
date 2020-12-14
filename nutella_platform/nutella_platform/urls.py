"""nutella_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from purbeurre import views
app_name = "purbeurre"

urlpatterns = [
    path('',views.index),
    path('index.html',views.index),
    path('purbeurre/', include('purbeurre.urls')),
    path('admin/', admin.site.urls),
    path('sign_in.html', views.sign_in, name="sign_in"),
    path('connection.html', views.connect),
    path('account.html', views.account,  name="account"),
    path('deconnection.html', views.logout_view),
    path('history.html', views.history)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns