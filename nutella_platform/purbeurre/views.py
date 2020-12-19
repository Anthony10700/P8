from django.shortcuts import render
from django.db import transaction
from purbeurre.forms import CustomUserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Product

# TODO: Voir la responsivité sur la hauteur du footer, et avec les form
# Create your views here.


def index(request):
    context = {'title': "Pur Beurre"}
    return render(request, 'purbeurre/index.html', context=context)


@transaction.atomic
def sign_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':

            form = CustomUserCreationForm(request.POST)

            if form.is_valid():
                try:
                    form.clean_password2()
                    form.clean_email()
                    form.clean_speudo()
                    user = form.save()
                    login(request, user)
                    # messages.success(request, 'Account created successfully')
                    return redirect('account')

                except ValidationError as err:
                    messages.error(request, err.message)
                    return redirect('sign_in')
            else:
                context = {'form': form}
                return render(request, 'purbeurre/sign_in.html', context=context)
        else:
            context = {'title': "Inscription"}
            return render(request, 'purbeurre/sign_in.html',  context=context)

    else:
        return redirect('account')


@transaction.atomic
def connect(request):
    if request.method == 'POST':
        if 'inputUsername' in request.POST and 'inputPassword' in request.POST:
            username = request.POST['inputUsername']
            password = request.POST['inputPassword']
            password = make_password(password=password,
                                     salt="1",
                                     hasher='pbkdf2_sha256')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(3600)
                request.session.clear_expired()
                return redirect('account')
            else:
                messages.error(request, "Mots de passe ou Speudo incorrect")
                return redirect('sign_in')

    else:
        context = {'title': "Inscription"}
        return render(request, 'purbeurre/sign_in.html',  context=context)


def account(request):
    if request.user.is_authenticated:
        user = request.user
        context = {"title": "Bienvenue " + user.username,
                            "account_info": {"Email": user.email,
                                             "Speudo": user.username,
                                             "Prénom": user.first_name,
                                             "Nom": user.last_name}}
        return render(request, 'purbeurre/account.html', context=context)
    else:
        context = {'title': "Utilisateur pas connecter"}
        return render(request, 'purbeurre/index.html',  context=context)


def logout_view(request):
    if request.user.is_authenticated:

        logout(request)
        context = {'title': "Déconnexion"}
        return render(request, 'purbeurre/index.html',  context=context)
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'purbeurre/sign_in.html',  context=context)


def history(request):
    if request.user.is_authenticated:
        recherche = request.user.save_product.all()

        for arct in recherche:
            arct.categories.name = arct.categories.name.replace(
                "-", " ")

        context = {'title': "Historique de vos articles",
                   'articles_list': recherche}
        return render(request, 'purbeurre/history.html',  context=context)

    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'purbeurre/sign_in.html',  context=context)


def resultats(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:

                product_show = Product.objects.get(id=request.POST["id"])

                userr = request.user

                product_show.save_product.add(userr)

                product_show.save()

                messages.success(
                    request, 'Votre article à bien été enregistré')
                print(request)
                return redirect(request.path_info + "?search=" + request.POST["search"])
            except:
                context = {'title': "Erreur"}
                return render(request, 'purbeurre/resultats.html',  context=context)
        else:

            try:

                print(request.GET["search"])
                recherche = Product.objects.filter(
                    name__icontains=request.GET["search"])[:8]

                for arct in recherche:
                    arct.categories.name = arct.categories.name.replace(
                        "-", " ")

                context = {'title': "resultats de votre recherche",
                           'articles_list': recherche, 'aliment_search': request.GET["search"]}
                return render(request, 'purbeurre/resultats.html',  context=context)
            except:
                context = {'title': "Erreur dans votre recherche"}
                return render(request, 'purbeurre/resultats.html',  context=context)
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'purbeurre/sign_in.html',  context=context)


def show_product(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            try:

                product_show = Product.objects.get(id=request.GET["id"])

                product_show.categories.name = product_show.categories.name.replace(
                    "-", " ")

                print(product_show)
                context = {'title': "resultats de votre recherche",
                           'articles_list': product_show, 'aliment_search': request.GET["search"]}
                return render(request, 'purbeurre/show_product.html',  context=context)

            except:
                context = {'title': "Erreur"}
                return render(request, 'purbeurre/resultats.html',  context=context)
        else:
            context = {'title': "Bienvenue"}
            return render(request, 'purbeurre/index.html',  context=context)
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'purbeurre/sign_in.html',  context=context)


def unsave(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:

                product_show = Product.objects.get(id=request.POST["id"])

                product_show.save_product.remove(request.user)

                recherche = request.user.save_product.all()

                for arct in recherche:
                    arct.categories.name = arct.categories.name.replace(
                        "-", " ")

                context = {'title': "Historique de vos articles",
                           'articles_list': recherche}
                return render(request, 'purbeurre/history.html',  context=context)

            except:
                recherche = request.user.save_product.all()

                for arct in recherche:
                    arct.categories.name = arct.categories.name.replace(
                        "-", " ")

                context = {'title': "Historique de vos articles",
                           'articles_list': recherche}
                return render(request, 'purbeurre/history.html',  context=context)
        else:
            recherche = request.user.save_product.all()

            for arct in recherche:
                arct.categories.name = arct.categories.name.replace(
                    "-", " ")

            context = {'title': "Historique de vos articles",
                       'articles_list': recherche}
            return render(request, 'purbeurre/history.html',  context=context)
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'purbeurre/sign_in.html',  context=context)
