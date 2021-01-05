from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Product
import json
from django.template.defaulttags import register
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from purbeurre.services.purbeurre_services import save_product_result, get_articles, show_specify_product, get_page, remove_product, replace_indent


@register.filter
def get_item(dictionary, key):
    """This methode is a filtre to your gabari

    Args:
        dictionary (dict): dictionary
        key (string): key of your dictionary

    Returns:
        string: value of you dictionary key
    """
    return dictionary.get(key)

# TODO: Voir la responsivité sur la hauteur du footer, et avec les form


def index(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {'title': "Pur Beurre"}
    return render(request, 'purbeurre/index.html', context=context)


@transaction.atomic
def resultats(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:

        if request.method == 'POST':
            result_dict = save_product_result(request.user, request)
            if result_dict["methode"] == "redirect":
                messages.success(request, result_dict["message"])
                return redirect(result_dict["value"])
            elif result_dict["methode"] == "render":
                messages.error(request, result_dict["message"])
                context = {'title': "Products"}
                return render(request, result_dict["value"],  context=context)

        elif request.method == 'GET':
            result_dict = get_articles(request, 6)
            if result_dict["methode"] == "redirect":
                messages.error(request, result_dict["message"])
                return redirect(result_dict["value"])
            elif result_dict["methode"] == "render":
                context = {'title': "Resultats de votre recherche",
                           'articles_list': result_dict["seek"], 'aliment_search': request.GET["search"],
                           "paginate": result_dict["paginate"]}
                return render(request, result_dict["value"],  context=context)

    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'auth/sign_in.html',  context=context)


def show_product(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        if request.method == 'GET':
            result_dict = show_specify_product(request)
            if result_dict["methode"] == "render" and "context" in result_dict:
                return render(request, result_dict["value"],  context=result_dict["context"])
            elif result_dict["methode"] == "render" and "message" in result_dict:
                messages.error(request, result_dict["message"])
                context = {'title': "Product"}
                return render(request, 'purbeurre/resultats.html',  context=context)
        else:
            context = {'title': "Bienvenue"}
            return render(request, 'purbeurre/index.html',  context=context)
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'auth/sign_in.html',  context=context)


@transaction.atomic
def unsave(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                remove_product(request)

                all_product_result = request.user.save_product.all()

                all_product_result = replace_indent(all_product_result)

                seek, paginate = get_page(1, all_product_result, 6)

                context = {'title': "Historique de vos articles",
                           'articles_list': seek,
                           "paginate": paginate}
                return render(request, 'auth/history.html',  context=context)

            except:
                all_product_result = request.user.save_product.all()

                all_product_result = replace_indent(all_product_result)

                context = {'title': "Historique de vos articles",
                           'articles_list': all_product_result}
                return render(request, 'auth/history.html',  context=context)
        else:

            if 'page' in request.GET:
                page = request.GET.get('page')
            else:
                page = 1

            all_product_result = request.user.save_product.all()

            seek, paginate = get_page(page, all_product_result, 6)

            all_product_result = replace_indent(all_product_result)

            context = {'title': "Historique de vos articles",
                       'articles_list': all_product_result,
                       "paginate": paginate}
            return render(request, 'auth/history.html',  context=context)
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'auth/sign_in.html',  context=context)


def legale(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {'title': "Mentions légales"}
    return render(request, 'purbeurre/legal_notice.html',  context=context)


def page_not_found_view(request, expetion):
    return render(request, '404.html')
