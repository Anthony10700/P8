"""[summary]

    Returns:
        [type]: [description]
    """
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from auth.services.auth_services import connect_validation, account_get_info, get_history_article, sign_validation

# Create your views here.


def sign_in(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """

    if not request.user.is_authenticated:
        if request.method == 'POST':
            try:
                result_dict = sign_validation(request)
                if result_dict["methode"] == "redirect":
                    return redirect(result_dict["value"])
                elif result_dict["methode"] == "render":
                    context = {'form': result_dict["form"]}
                    return render(request, result_dict["value"], context=context)
            except ValidationError as err:
                messages.error(request, err.message)
                return redirect('sign_in')

        else:
            context = {'title': "Inscription"}
            return render(request, 'auth/sign_in.html',  context=context)
    else:
        return redirect('account')


def connect(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        result_dict = connect_validation(request)
        if result_dict["methode"] == "redirect":
            if result_dict["value"] == "account":
                return redirect(result_dict["value"])
            elif result_dict["value"] == "sign_in":
                messages.error(request, result_dict["messages"])
                return redirect(result_dict["value"])
        if result_dict["methode"] == "render":
            context = {'title': "Inscription"}
            return render(request, result_dict["value"],  context=context)
    else:
        context = {'title': "Inscription"}
        return render(request, 'auth/sign_in.html',  context=context)


def account(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        context = account_get_info(request)
        return render(request, 'auth/account.html', context=context)
    else:
        context = {'title': "Utilisateur pas connecter"}
        return render(request, 'purbeurre/index.html',  context=context)


def logout_view(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        logout(request)
        context = {'title': "Déconnexion"}
        return render(request, 'purbeurre/index.html',  context=context)
    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'auth/sign_in.html',  context=context)


def history(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.user.is_authenticated:
        result_dict = get_history_article(request, 6)
        if result_dict["methode"] == "render":
            context = {'title': "Historique de vos articles", 'articles_list': result_dict["seek"],
                       "paginate": result_dict["paginate"], 'aliment_search': ""}
            return render(request, result_dict["value"],  context=context)

    else:
        context = {'title': "Vous n'êtes pas connecté.",
                   'err_show': "Vous n'êtes pas connecté."}
        return render(request, 'auth/sign_in.html',  context=context)
