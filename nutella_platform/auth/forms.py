from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class CustomUserCreationForm(forms.Form):
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
        User = get_user_model()
        email = self.cleaned_data['inputemail'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_speudo(self):
        User = get_user_model()
        Username = self.cleaned_data['inputUsername'].lower()
        r = User.objects.filter(username=Username)
        if r.count():
            raise ValidationError("Username already exists")
        return Username

    def clean_password2(self):

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
        User = get_user_model()
        user = User.objects.create_user(
            username=self.cleaned_data['inputUsername'],
            first_name=self.cleaned_data['inputprenom'],
            last_name=self.cleaned_data['inputNom'],
            email=self.cleaned_data['inputemail'],
            password=self.clean_password2()

        )
        return user
