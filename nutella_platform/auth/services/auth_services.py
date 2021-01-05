"""[summary]

    Returns:
        [type]: [description]
    """
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from auth.forms import CustomUserCreationForm


def sign_validation(request):
    result_dict = {"methode": "", "value": ""}
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        form.clean_password2()
        form.clean_email()
        form.clean_speudo()
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
        [redirect]: [django.shortcuts] OR [render]: [django.shortcuts]        
    """
    result_dict = {"methode": "", "value": ""}
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
            result_dict["methode"] = "redirect"
            result_dict["value"] = "account"
            return result_dict
        else:
            result_dict["methode"] = "redirect"
            result_dict["value"] = "sign_in"
            result_dict["messages"] = "Mots de passe ou Speudo incorrect"
            return result_dict
    else:
        result_dict["methode"] = "render"
        result_dict["value"] = "auth/sign_in.html"
        return result_dict


def account_get_info(request):
    """This methodes create a context of info user if connected

    Args:
        request (request): request of views auth account

    Returns:
        [dict]: [context of render accound info]
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
    this methodes is for get all article saved

    Args:
        request (request): request of views auth history
        nb_of_articles_per_page (int): number of articles per page

    Returns:
        render: render of views, contains all articles saved, in articles_list
        paginate in context is for: True the button show in html page, False the button no visible
    """
    result_dict = {"methode": "", "value": ""}
    recherche = request.user.save_product.all()

    if 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1

    recherche = replace_indent(recherche)

    seek, paginate = get_page(page, recherche, nb_of_articles_per_page)

    result_dict["methode"] = "render"
    result_dict["value"] = "auth/history.html"
    result_dict["paginate"] = paginate
    result_dict["seek"] = seek
    return result_dict


def get_page(page, all_product, nb_of_articles_per_page):
    """This methodes make paginator of all product

    Args:
        page (int): page of paginator
        all_product (Product): product 
        nb_of_articles_per_page (int): number of articles per page

    Returns:
        tuple: nb_of_articles_per_page product and paginate.
        paginate in context is for: True the button show in html page, False the button no visible
    """
    paginator = Paginator([all_product], nb_of_articles_per_page)

    try:
        recherche = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recherche = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recherche = paginator.page(paginator.num_pages)

    if paginator.num_pages > 1:
        paginate = True
    else:
        paginate = False

    return recherche, paginate


def replace_indent(all_product_result):
    """This methode replace all indent in you string

    Args:
        all_product_result (product list):  list of product

    Returns:
        [product list]: list of product
    """
    try:
        for arct in all_product_result:
            arct.categories.name = arct.categories.name.replace("-", " ")
        return all_product_result
    except:
        all_product_result.categories.name = all_product_result.categories.name.replace(
            "-", " ")
        return all_product_result
