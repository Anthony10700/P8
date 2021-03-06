"""this file contain the job code method of  all views

    Returns:
        [type]: [description]
    """
import json
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from purbeurre.models import Product


# Get an instance of a logger
logger = logging.getLogger(__name__)


def save_product_result(user, request):
    """This method save an article to a manytomany table with user

    Returns:
        dictionary: "methode": "", "value": "" and "messages":""
    """
    result_dict = {"methode": "", "value": ""}  # dictionnary return
    try:
        product_show = Product.objects.get(id=request.POST["id"])
        # select a product that matches to request id
        product_show.save_product.add(user)  # add user to selected products
        product_show.save()  # save selected products in data base
        result_dict["methode"] = "redirect"
        # set method redirect in key methode
        result_dict["value"] = request.path_info + \
            "?search=" + request.POST["search"]
        #  set value of path in key value
        result_dict["message"] = 'Votre article à bien été enregistré'
        #  set message for user in key message
        return result_dict  # returns dictionnary to views

    except ObjectDoesNotExist:
        result_dict["methode"] = "render"  # set method render in key
        # methode if try error
        result_dict["value"] = 'purbeurre/resultats.html'  # set value
        # of path in key value
        result_dict["message"] = "Erreur dans l'enregistrement \
            de votre produit"
        #  set message for user in key message
        return result_dict  # returns dictionnary to views


def get_result_in_list_nutriscore(request):
    """This methodes get nutriscore form resulte et make a list

    Args:
        request ([type]): [description]
    """
    list_of_nutri = []

    if "nutriscore_a" in request.GET:
        if request.GET["nutriscore_a"] == "on":
            list_of_nutri.append("a")

    if "nutriscore_b" in request.GET:
        if request.GET["nutriscore_b"] == "on":
            list_of_nutri.append("b")

    if "nutriscore_c" in request.GET:
        if request.GET["nutriscore_c"] == "on":
            list_of_nutri.append("c")

    if "nutriscore_d" in request.GET:
        if request.GET["nutriscore_d"] == "on":
            list_of_nutri.append("d")

    if "nutriscore_e" in request.GET:
        if request.GET["nutriscore_e"] == "on":
            list_of_nutri.append("e")
    return list_of_nutri


def get_articles(request, nb_of_articles_per_page):
    """
    This method get articles in bdd

    Args:
        request (request): request of views results
        nb_of_articles_per_page (int): number of articles per page

    Returns:
        dictionary: "methode": "", "value": "" , "paginate":"", "seek":""
                    OR
                    "methode": "", "value": "" ,"messages":""
    """
    try:
        result_dict = {"methode": "", "value": ""}

        str_dict_return_param = ""
        for key in dict(request.GET):
            if key != "page":
                str_dict_return_param += key + "=" + request.GET[key] + "&"
        str_dict_return_param = str_dict_return_param[:-1]
        result_final_of_produts = []
        recherche = Product.objects.filter(
            name__icontains=request.GET["search"])

        list_of_result_in_form = get_result_in_list_nutriscore(request)
        if len(list_of_result_in_form) >= 1:
            recherche = recherche.filter(
                nutriscore_grade__in=list_of_result_in_form)

        if "like_limit_1" in request.GET:
            if request.GET["like_limit_1"] == "on":
                for product_in in recherche:
                    if product_in.like_count >= product_in.dislike_count:
                        result_final_of_produts.append(product_in)

        if "like_limit_2" in request.GET:
            if request.GET["like_limit_2"] == "on":
                for product_in in recherche:
                    if product_in.like_count < product_in.dislike_count:
                        result_final_of_produts.append(product_in)

        if "like_limit_2" not in request.GET:
            if "like_limit_1" not in request.GET:
                result_final_of_produts = recherche

        logger.info('New search', exc_info=True, extra={'request': request, })

        if 'page' in request.GET:
            page = int(request.GET['page'])
            if page <= 0:
                page = 1
        else:
            page = 1
        seek, paginate = get_page(
            page,
            result_final_of_produts,
            nb_of_articles_per_page)

        result_dict["methode"] = "render"
        result_dict["value"] = "purbeurre/resultats.html"
        result_dict["paginate"] = paginate
        result_dict["seek"] = seek
        result_dict["str_dict_return_param"] = str_dict_return_param
        return result_dict

    except ObjectDoesNotExist:
        result_dict["methode"] = "redirect"
        result_dict["value"] = "resultat"
        result_dict["message"] = "Erreur dans la recherche de votre produit"
        return result_dict


def show_specify_product(request):
    """This method show a product , get id in request get id and send in context
    the product in articles_list

    Args:
        request (request): request of views results

    Returns:
        dictionary: "methode": "", "value": "" and "context":""
    """
    try:
        result_dict = {"methode": "", "value": ""}  # dictionnary return
        product_show = Product.objects.get(id=request.GET["id"])  # select a
        # product that matches to request id
        product_save = Product.objects.get(id=request.GET["id"])
        product_show = replace_indent(product_show)
        # replace all short dash in the product_show.name

        prod = json.loads(product_show.nutriments)
        # load the JSON string into the database

        if "search" in request.GET:
            search = request.GET["search"]
        else:
            search = ""
        # check search in the request get ,
        # because the field must be returned to the user
        like_value = product_save.like_count
        dislike_value = product_save.dislike_count

        result_dict["methode"] = "render"
        # set method render in key methode
        result_dict["value"] = 'purbeurre/show_product.html'
        # set page resultats in key value
        result_dict["context"] = {'title': "resultats de votre recherche",
                                  'articles_list': product_show,
                                  'aliment_search': search, "nutriments": prod,
                                  'like': like_value,
                                  'dislike': dislike_value}
        # set context in key context for the views

        return result_dict  # returns dictionnary to views
    except ObjectDoesNotExist:
        result_dict["methode"] = "redirect"
        # set method redirect in key methode
        result_dict["value"] = "resultat"
        # set value resultat in key value
        result_dict["message"] = "Erreur dans la recherche de votre produit"
        # set message for user in key message
        return result_dict  # returns dictionnary to views


def remove_product(request):
    """This method remove product with specify id

    Args:
        request (request): need "id" in request.POST
    """
    if "id" in request.POST:
        product_show = Product.objects.get(id=request.POST["id"])
        product_show.save_product.remove(request.user)


def get_page(page, all_product, nb_of_articles_per_page):
    """This method make a paginator of all products

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


def replace_indent(all_product_result):
    """This method replace all short dash in the string

    Args:
        all_product_result (product list):  list of product

    Returns:
        [product list]: list of product
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


def like_dislike_services(request):
    """methode for services like and dislike feature

    Args:
        request ([type]): [description]
    """
    value_tmp = ""
    if "like" in request.GET:
        value_tmp = request.GET["like"]
        product_select = Product.objects.get(id=value_tmp)
        try:
            product_select.disklike_products.get(id=request.user.id)
            product_select.disklike_products.remove(request.user)
        except ObjectDoesNotExist:
            pass
        product_select.like_products.add(request.user)
    elif "dislike" in request.GET:
        value_tmp = request.GET["dislike"]
        product_select = Product.objects.get(id=value_tmp)
        try:
            product_select.like_products.get(id=request.user.id)
            product_select.like_products.remove(request.user)
        except ObjectDoesNotExist:
            pass
        product_select.disklike_products.add(request.user)
    else:
        value_tmp = "err"
        return value_tmp

    like_value = len(product_select.like_products.all())
    dislike_value = len(product_select.disklike_products.all())
    context = {"text": "like dislake save",
               "like": like_value,
               "dislike": dislike_value}

    product_select.like_count = like_value
    product_select.dislike_count = dislike_value
    product_select.save()
    return context
