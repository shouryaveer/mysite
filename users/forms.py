from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth import get_user_model
from users.models import User
UserModel = get_user_model()

class CustomUserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_pic', 'birth_date', 'location', 'bio',)

class CustomUserChangeForm(BaseUserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_pic', 'birth_date', 'location', 'bio',)