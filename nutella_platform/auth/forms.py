""" Class for custom user creation formulaire

    Raises:
        ValidationError: "Email already exists"
        ValidationError: "Username already exists"
        ValidationError: "Password don't match"

    Returns:
        form: formulaire
    """
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class CustomUserCreationForm(forms.Form):
    """[summary]

    Args:
        forms Form: super class Form

    Raises:
        ValidationError: "Email already exists"
        ValidationError: "Username already exists"
        ValidationError: "Password don't match"

    Returns:
        form: formulaire
    """
    inputUsername = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'inputUsername'}), min_length=2, max_length=150, required=True)
    inputemail = forms.EmailField(widget=forms.EmailInput(
        attrs={'id': 'inputemail'}), required=True)
    inputPassword1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'inputPassword1'}), min_length=4, max_length=150, required=True)
    inputPassword2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'id': 'inputPassword2'}), min_length=4, max_length=150, required=True)
    inputNom = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'inputNom'}), min_length=2, max_length=150)
    inputprenom = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'inputprenom'}), min_length=2, max_length=150)

    def clean_email(self):
        """
        This methode clean email in lower case and test if exists

        Raises:
            ValidationError: "Email already exists"

        Returns:
            str: email of formulaire in lower case
        """
        user = get_user_model()
        email = self.cleaned_data['inputemail'].lower()
        email_select = user.objects.filter(email=email)
        if email_select.count():
            raise ValidationError("Email already exists")
        return email

    def clean_speudo(self):
        """
        This methode clean speudo in lower case and test if exists
        Raises:
            ValidationError: [description]

        Returns:
            str : username
        """
        user = get_user_model()
        username = self.cleaned_data['inputUsername'].lower()
        username_select = user.objects.filter(username=username)
        if username_select.count():
            raise ValidationError("Username already exists")
        return username

    def clean_password2(self):
        """
        This methode clean a password and hash in pbkdf2_sha256

        Raises:
            ValidationError: "Password don't match"

        Returns:
            str: password2 hash pbkdf2_sha256
        """
        password1 = self.cleaned_data.get('inputPassword1')
        password2 = self.cleaned_data.get('inputPassword2')
        password1 = make_password(password=password1,
                                  salt="1",
                                  hasher='pbkdf2_sha256')
        password2 = make_password(password=password2,
                                  salt="1",
                                  hasher='pbkdf2_sha256')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self):
        """
        Save the form in db database

        Returns:
            User : object User created
        """
        user = get_user_model()
        username = user.objects.create_user(
            username=self.cleaned_data['inputUsername'],
            first_name=self.cleaned_data['inputprenom'],
            last_name=self.cleaned_data['inputNom'],
            email=self.cleaned_data['inputemail'],
            password=self.clean_password2()

        )
        return username
