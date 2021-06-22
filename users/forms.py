from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import MinimumLengthValidator, validate_password
from users.validators import NumberValidator, UppercaseValidator, LowercaseValidator, SymbolValidator
import re

UserModel = get_user_model()

class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password',)

class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password',)


class SignUpForm(forms.Form):
    username = forms.CharField(label="username", max_length=15)
    email = forms.EmailField(label="email_address")
    first_name = forms.CharField(label="First name", max_length=25, required=False)
    last_name = forms.CharField(label="Last name", max_length=25, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", max_length=100,)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", max_length=100)

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")


        if re.match('^[0-9]', username) or re.match('^\.', username):
            raise ValidationError("Username cannot start with a number or a period(.)")

        if re.findall('\s', username):
            raise ValidationError("spaces are not allowed in username.")

        if UserModel.objects.filter(username=username).exists():
            raise ValidationError("Username already registered.")

        if UserModel.objects.filter(email=email).exists():
            raise ValidationError("Email address already resgistered.")

        password = validate_password(password=self.cleaned_data.get("password"))
        if self.cleaned_data.get("password") != confirm_password:
            raise ValidationError("Confirm password must match the password.")


    def save(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        password = self.cleaned_data.get("password")

        return UserModel.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username or email")
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        queryset = UserModel.objects.filter(Q(username=username) | Q(email=username))
        if not queryset.exists():
            raise ValidationError("User with given username or email does not exist!")
        return username