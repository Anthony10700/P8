from django.shortcuts import render
from django.db import transaction
from purbeurre.forms import CustomUserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.
def index(request):
    context = {'title' : "Pur Beurre"}
    return render(request, 'purbeurre/index.html', context=context)


@transaction.atomic
def sign_in(request):            
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            try:
                form.clean_password2()
                form.clean_email()
                form.clean_speudo()
                form.save()
                messages.success(request, 'Account created successfully')
                return redirect('sign_in')

            except ValidationError as err:
                messages.error(request, err.message)
                return redirect('sign_in')
        else:
            context = {'form': form}           
            return render(request, 'purbeurre/sign_in.html', context)

    else:
        context = {'title' : "Inscription"}
        return render(request, 'purbeurre/sign_in.html',  context=context)

@transaction.atomic
def connect(request):
    if request.method == 'POST':
        if 'inputUsername' in request.POST and 'inputPassword' in request.POST:
            username = request.POST['inputUsername']
            password = request.POST['inputPassword']
            password =  make_password(password=password,
                                        salt="1",
                                        hasher='pbkdf2_sha256')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)                
                context = {"title" : "account"}
                return render(request, 'purbeurre/account.html', context)
            else:
                messages.error(request, "Mots de passe ou Speudo incorrect")
                return redirect('sign_in')

    else:
        context = {'title' : "Inscription"}
        return render(request, 'purbeurre/sign_in.html',  context=context)

def account(request):
    if request.user.is_authenticated:

        
        context = {'title' : "Bienvenue"}
        return render(request, 'purbeurre/account.html',  context=context)
    else:
        context = {'title' : "Utilisateur pas connecter"}
        return render(request, 'purbeurre/index.html',  context=context)

def logout_view(request):
    if request.user.is_authenticated:

        logout(request)
        context = {'title' : "Deconnection"}
        return render(request, 'purbeurre/index.html',  context=context)
    else:
        context = {'title' : "Utilisateur pas connecter"}
        return render(request, 'purbeurre/index.html',  context=context)