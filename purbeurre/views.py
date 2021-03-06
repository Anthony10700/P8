"""
    Views for purbeurre app, contain the views of results,
    show_product, unsave, legale and 404


    Returns:
        render: render of views
        redirect : redirect of views
    """
from django.shortcuts import render
from django.db import transaction
from django.shortcuts import redirect
from django.contrib import messages
from django.template.defaulttags import register
from django.core.exceptions import ObjectDoesNotExist
from purbeurre.services.purbeurre_services import save_product_result,\
    get_articles, show_specify_product,\
    get_page, remove_product, replace_indent, like_dislike_services
import json
from django.http import HttpResponse


@register.filter
def get_item(dictionary, key):
    """This method is a filter to your template

    Args:
        dictionary (dict): dictionary
        key (string): key of your dictionary

    Returns:
        string: value of your dictionary key
    """
    return dictionary.get(key)


def index(request):
    """this view concern the index of the main page

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {'title': "Pur Beurre"}
    return render(request, 'purbeurre/index.html', context=context)


@transaction.atomic
def resultats(request):
    """this view concern the result of the research

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

        elif request.method == 'GET' and "search" in request.GET:
            result_dict = get_articles(request, 6)
            if result_dict["methode"] == "redirect":
                messages.error(request, result_dict["message"])
                return redirect(result_dict["value"])
            elif result_dict["methode"] == "render":
                context = {
                    'title': "Resultats de votre recherche",
                    'articles_list': result_dict["seek"],
                    'aliment_search': request.GET["search"],
                    "paginate": result_dict["paginate"],
                    "str_dict_return_param": result_dict[
                        "str_dict_return_param"]}
                return render(request, result_dict["value"],  context=context)

    else:
        if request.method == 'GET' and "search" in request.GET:
            result_dict = get_articles(request, 6)
            if result_dict["methode"] == "redirect":
                messages.error(request, result_dict["message"])
                return redirect(result_dict["value"])
            elif result_dict["methode"] == "render":
                context = {'title': "Resultats de votre recherche",
                           'articles_list': result_dict["seek"],
                           'aliment_search': request.GET["search"],
                           "paginate": result_dict["paginate"],
                           "str_dict_return_param": result_dict[
                               "str_dict_return_param"]}
                return render(request, result_dict["value"],  context=context)
        else:
            context = {
                'title': "Vous n'êtes pas connecté.",
                'err_show': "Vous n'êtes pas connecté."}
            return render(request, 'auth/sign_in.html',  context=context)


def show_product(request):
    """this view concern the display of a product

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        if request.method == 'GET':
            result_dict = show_specify_product(request)

            if result_dict["methode"] == "render" and "context" in result_dict:
                return render(request, result_dict["value"],
                              context=result_dict["context"])
            elif result_dict["methode"] == "redirect"\
                    and "message" in result_dict:
                messages.error(request, result_dict["message"])
                context = {'title': "Product"}
                return render(request, 'purbeurre/resultats.html',
                              context=context)
        else:
            context = {'title': "Bienvenue"}
            return render(request, 'purbeurre/index.html',  context=context)

            # context = {'title': "Vous n'êtes pas connecté.",
            #            'err_show': "Vous n'êtes pas connecté."}
            # return render(request, 'auth/sign_in.html',  context=context)
    except ValueError:
        context = {'title': "Bienvenue"}
        return render(request, 'purbeurre/index.html',  context=context)


@transaction.atomic
def unsave(request):
    """this view can cancel an article previously saved

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

            except ObjectDoesNotExist:
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
    """this view concern the display of the legal mention

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    context = {'title': "Mentions légales"}
    return render(request, 'purbeurre/legal_notice.html',  context=context)


def page_not_found_view(request, exception=None):
    """Customizing error views 404

    Args:
        request ([type]): which is the URL that resulted in the error
        exception ([type]): which is a useful representation of the
        exception that triggered the view
        (e.g. containing any message passed to a specific Http404 instance).

    Returns:
        [type]: [description]
    """

    return render(request, '404.html')


def page_server_error(request, exception=None):
    """Customizing error views page_server_error

    Args:
        request ([type]): which is the URL that resulted in the error
        exception ([type]): which is a useful representation of the
        exception that triggered the view
        (e.g. containing any message passed to a specific Http404 instance).

    Returns:
        render: [description]
    """

    return render(request, '500.html')


def like_dislike(request):
    """View for add a like or dislike product

    Args:
        request ([type]): [description]
    """
    if request.user.is_authenticated:
        if request.method == "GET":
            context = like_dislike_services(request)
            if context["text"] == "like dislake save":
                context["text"] = "Produit ajouté au "
                return HttpResponse(
                    json.dumps(context),
                    content_type="application/json")
            elif context["text"] == "err":
                context["text"] = "Error in services"
                return HttpResponse(
                    json.dumps(context),
                    content_type="application/json")
        else:
            context = {'err': "Error no POST request"}
            return HttpResponse(
                json.dumps(context),
                content_type="application/json")
    else:
        context = {
            'err': "Vous n'êtes pas connecté.",
            "like": 0,
            "dislike": 0}
        return HttpResponse(
            json.dumps(context),
            content_type="application/json")
