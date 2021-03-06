"""this file is for including the job code

    Returns:
        [type]: [description]
    """
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model
from auth.forms import CustomUserCreationForm


def sign_validation(request):
    """This method test if a form is valide return to a dictionary

    Args:
       request (request): views request

    Returns:
        dictionary: "methode": "", "value": ""
    """
    result_dict = {"methode": "", "value": ""}
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.clean_password2()
        form.clean_email()
        form.clean_pseudo()
        user = form.save()
        login(request, user)
        result_dict["methode"] = "redirect"
        result_dict["value"] = "account"
        return result_dict
    else:
        result_dict["methode"] = "render"
        result_dict["value"] = "auth/sign_in.html"
        result_dict["form"] = form
        return result_dict


def connect_validation(request):
    """
    This method test if connection is valid

    Args:
        request (request): views request

    Returns:
        dictionary: "methode": "", "value": "" ,"messages":""
    """
    result_dict = {"methode": "", "value": ""}
    if 'inputPassword_connect' in request.POST \
            and 'inputEmail_connect' in request.POST:
        email = request.POST['inputEmail_connect']
        password = request.POST['inputPassword_connect']
        password = make_password(password=password,
                                 salt="1",
                                 hasher='pbkdf2_sha256')
        user_get = get_user_model()
        try:
            user_tmp = user_get.objects.get(email=email)
        except user_get.DoesNotExist:
            user_tmp = None
        if user_tmp is not None:
            user = authenticate(request,
                                username=user_tmp.username, password=password)
        else:
            user = None
        if user is not None:
            login(request, user)
            request.session.set_expiry(3600)
            request.session.clear_expired()
            result_dict["methode"] = "redirect"
            result_dict["value"] = "account"
            return result_dict
        else:
            result_dict["methode"] = "redirect"
            result_dict["value"] = "sign_in"
            result_dict["messages"] = "Mot de passe ou pseudo incorrect"
            return result_dict
    else:
        result_dict["methode"] = "render"
        result_dict["value"] = "auth/sign_in.html"
        return result_dict


def account_get_info(request):
    """This method create a context of user information  if he is connected

    Args:
        request (request): request of views auth account

    Returns:
        dict: context of render accound info
    """
    if request.user.is_authenticated:

        user = request.user
        context = {"title": "Bienvenue " + user.username,
                            "account_info": {"Email": user.email,
                                             "Speudo": user.username,
                                             "Prénom": user.first_name,
                                             "Nom": user.last_name}}
        return context
    return {}


def get_history_article(request, nb_of_articles_per_page):
    """
    this method is for getting  all  the article saved by the user

    Args:
        request (request): request of views auth history
        nb_of_articles_per_page (int): number of articles per page

    Returns:
        render: render of views, contains all articles saved, in articles_list
        paginate in context is for: True the button show in html page,
        False the button no visible
    """
    result_dict = {"methode": "", "value": ""}
    recherche = request.user.save_product.all()

    if 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    recherche = replace_short_dash(recherche)

    seek, paginate = get_page(page, recherche, nb_of_articles_per_page)

    result_dict["methode"] = "render"
    result_dict["value"] = "auth/history.html"
    result_dict["paginate"] = paginate
    result_dict["seek"] = seek
    return result_dict


def get_page(page, all_product, nb_of_articles_per_page):
    """This method make a paginator for all products

    Args:
        page (int): page of paginator
        all_product (Product): product
        nb_of_articles_per_page (int): number of articles per page

    Returns:
        tuple: nb_of_articles_per_page product and paginate.
        paginate in context is for: True the button show in html page,
        False the button no visible
    """
    paginator = Paginator(all_product, nb_of_articles_per_page)

    try:
        recherche = paginator.page(page)
    except PageNotAnInteger:
        recherche = paginator.page(1)
    except EmptyPage:
        recherche = paginator.page(paginator.num_pages)

    if paginator.num_pages > 1:
        paginate = True
    else:
        paginate = False

    return recherche, paginate


def replace_short_dash(all_product_result):
    """This method replace all short dash(-) by nothing  in the string

    Args:
        all_product_result (product list):  list of products

    Returns:
        [product list]: list of products
    """
    try:
        iter(all_product_result)
    except TypeError:
        all_product_result.categories.name = \
            all_product_result.categories.name.replace("-", " ")
        return all_product_result
    else:
        for arct in all_product_result:
            arct.categories.name = arct.categories.name.replace("-", " ")
        return all_product_result
